import pandas as pd
import os
import json
import re
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

from webdriver_manager.chrome import ChromeDriverManager


class GoogleScraper:
    def __init__(self, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_argument("--disable-images")  # Faster

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def scrape_reviews(self, url, num_reviews=50):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
        import re
        from datetime import datetime, timedelta

        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # Load page
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='main']")))

        # Handle consent
        try:
            consent = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Accept') or contains(text(), 'Accept')]")))
            consent.click()
        except TimeoutException:
            pass

        # Click Reviews tab
        try:
            reviews_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label,'Reviews')]")))
            reviews_tab.click()
        except TimeoutException:
            pass

        # Wait for reviews
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-review-id]")))

        data = []
        last_review_count = 0
        max_scrolls = 50

        while len(data) < num_reviews and len(data) == last_review_count < max_scrolls:
            last_review_count = len(data)

            # Get all reviews
            reviews = driver.find_elements(By.CSS_SELECTOR, "div[data-review-id]")

            for review in reviews[len(data):]:
                try:
                    # Username
                    username_selectors = [".d4r55", "h3", ".TSUbDb"]
                    username = ""
                    for sel in username_selectors:
                        try:
                            username = review.find_element(By.CSS_SELECTOR, sel).text
                            if username:
                                break
                        except:
                            continue

                    # Rating
                    rating = 0
                    try:
                        aria = review.find_element(By.CSS_SELECTOR, "span[aria-label*='star']").get_attribute("aria-label")
                        rating = int(re.match(r'(\d)', aria).group(1))
                    except:
                        pass

                    # Review text
                    review_text_selectors = [".wiI7pd", ".MyEned", "div[role='heading'] + div"]
                    review_text = ""
                    for sel in review_text_selectors:
                        try:
                            review_text = review.find_element(By.CSS_SELECTOR, sel).text
                            if review_text and len(review_text) > 10:
                                break
                        except:
                            continue

                    # Date
                    date = ""
                    try:
                        date_elem = review.find_element(By.CSS_SELECTOR, ".rsqaWe, .q0vB6d")
                        date = date_elem.text
                    except:
                        pass

                    # Extra: photos
                    photos_count = len(review.find_elements(By.CSS_SELECTOR, ".iHwx0d img"))

                    # Extra: owner reply
                    owner_reply = review.find_element(By.CSS_SELECTOR, ".review-full-text, .owner-reply").text if review.find_elements(By.CSS_SELECTOR, ".review-full-text, .owner-reply") else ""

                    if username or review_text:
                        data.append({
                            "username": username,
                            "review": review_text,
                            "rating": rating,
                            "date": date,
                            "photos": photos_count,
                            "owner_reply": owner_reply
                        })
                except Exception:
                    continue

            # Scroll
            try:
                scrollable = driver.find_element(By.CSS_SELECTOR, "div[role='feed'], .m6QErb.DxyBCb")
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable)
                wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "div[data-review-id]")) > last_review_count)
            except:
                # Try load more button
                try:
                    load_more = driver.find_element(By.XPATH, "//button[contains(text(), 'More') or contains(@aria-label, 'reviews')]")
                    load_more.click()
                except:
                    break

        # Place name
        place_name = driver.title.split(" - Google")[0].replace("/", "").replace(" ", "_").strip()

        # Save
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        excel_path = f"{output_dir}/{place_name}.xlsx"
        json_path = f"{output_dir}/{place_name}.json"

        df = pd.DataFrame(data)
        df.to_excel(excel_path, index=False)
        df.to_json(json_path, orient="records", indent=2)

        return {
            "place_name": place_name,
            "excel_path": excel_path,
            "json_path": json_path,
            "top_reviews": data[:10],
            "all_reviews": data,
            "total_collected": len(data)
        }
