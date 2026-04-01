
# 🗺️ MapInsight – Google Maps Review Scraper & Analyzer

**MapInsight** is a powerful web-based tool that lets you scrape, filter, and analyze reviews from any Google Maps location. It uses FastAPI for the backend, Selenium for automated scraping, and a modern glassmorphism UI to make everything look premium and intuitive.

> Built with 💡 by [Saksham Pathak](https://github.com/parthmax2), M.Sc. AI & ML @ IIIT Lucknow

---

## 🚀 Features

- 🔗 Input any **Google Maps Place URL**
- 📅 Filter reviews by custom **start and end date**
- 📊 View **top 10 reviews** with rating, username, and date
- 📦 Export filtered reviews as **Excel (.xlsx)** file
- 🗺️ Live **Map Embed** preview
- 💻 Full-stack web app with **FastAPI + Tailwind + JS**
- 🌈 Beautiful glassmorphism design with responsive layout

---

## 📸 Demo

> 🔗 Live on Render: **Coming Soon...**

![MapInsight Screenshot](https://storage.googleapis.com/a1aa/image/cb421f76-8571-4b4c-60f9-b85b6ded9e57.jpg)

---

## ⚙️ Tech Stack

| Layer      | Tech                          |
|------------|-------------------------------|
| Backend    | Python, FastAPI, Selenium     |
| Frontend   | HTML, Tailwind CSS, JavaScript|
| Parsing    | BeautifulSoup, Pandas         |
| Export     | OpenPyXL (.xlsx)              |
| Hosting    | Render.com                    |

---

## 🧪 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/parthmax2/MapInsight.git
cd MapInsight
````

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app locally

```bash
uvicorn backend.main:app --reload
```

Now visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🧾 API Endpoints

| Method | Endpoint                | Description                                                                       |
| ------ | ----------------------- | --------------------------------------------------------------------------------- |
| GET    | `/`                     | Loads frontend (`index.html`)                                                     |
| POST   | `/scrape`               | Accepts JSON payload with `url`, `num_reviews`, optional `start_date`, `end_date` |
| GET    | `/download/{file_name}` | Downloads Excel file                                                              |
| GET    | `/health`               | Health check endpoint                                                             |

---

## 🗂️ Project Structure

```
MapInsight/
├── backend/
│   ├── main.py         # FastAPI backend logic
│   └── scraper.py      # Selenium review scraper
├── frontend/
│   └── index.html      # Glassmorphism web UI
├── output/             # Excel files saved here
├── requirements.txt
└── README.md
```

## 🙋‍♂️ Author

**Saksham Pathak**
🎓 M.Sc. Artificial Intelligence & Machine Learning
🏫 Indian Institute of Information Technology, Lucknow
🌐 [GitHub](https://github.com/parthmax2) | [Hugging Face](https://huggingface.co/parthmax)

---

## 📄 License

This project is licensed under the **MIT License**.

---

## ⭐️ Show your support

If you like this project, consider giving it a ⭐️ on [GitHub](https://github.com/parthmax2/MapInsight)
It helps others discover it and motivates continued development!


