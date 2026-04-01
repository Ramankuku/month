from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, HttpUrl
import os
import uuid
from datetime import datetime

import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from scraper import GoogleScraper
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScrapeRequest(BaseModel):
    url: HttpUrl
    num_reviews: int = 50

def run_scraper(url: str, num_reviews: int):
    scraper = GoogleScraper()
    scraper.scrape_reviews(url, num_reviews)

@app.post("/scrape-now")
async def scrape_now(req: ScrapeRequest, background_tasks: BackgroundTasks):
    try:
        scraper = GoogleScraper(headless=True)
        result = scraper.scrape_reviews(str(req.url), req.num_reviews)

        file_name = os.path.basename(result["excel_path"])

        return {
            "success": True,
            "place_name": result["place_name"],
            "excel_filename": file_name,
            "download_link": f"/download/{file_name}",
            "json_path": result["json_path"],
            "total_collected": result["total_collected"],
            "top_reviews": result["top_reviews"][:5],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "trace": traceback.format_exc()})
import traceback

@app.get("/download/{file_name}")
def download(file_name: str):
    file_path = os.path.join(OUTPUT_DIR, file_name)

    if os.path.exists(file_path):
        return FileResponse(file_path, filename=file_name)

    return JSONResponse(status_code=404, content={"error": "File not found"})