
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import get_settings
from datetime import datetime
from pathlib import Path

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates_path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stats = {
        "suppliers": 0,
        "tenders": 0,
        "bids": 0,
        "results": 0
    }
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "current_time": current_time, "stats": stats, "page": "home"}
    )


@app.get("/suppliers", response_class=HTMLResponse)
async def suppliers_page(request: Request):
    suppliers = []
    return templates.TemplateResponse(
        "suppliers.html",
        {"request": request, "suppliers": suppliers, "page": "suppliers"}
    )


@app.get("/tenders", response_class=HTMLResponse)
async def tenders_page(request: Request):
    tenders = []
    stats = {"draft": 0, "published": 0, "in_progress": 0, "completed": 0}
    return templates.TemplateResponse(
        "tenders.html",
        {"request": request, "tenders": tenders, "stats": stats, "page": "tenders"}
    )


@app.get("/reviews", response_class=HTMLResponse)
async def reviews_page(request: Request):
    reviews = []
    stats = {"pending": 0, "in_progress": 0, "completed": 0, "reviewers": 0}
    return templates.TemplateResponse(
        "reviews.html",
        {"request": request, "reviews": reviews, "stats": stats, "page": "reviews"}
    )


@app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request):
    results = []
    score_summary = []
    stats = {"total": 0, "pending": 0, "approved": 0, "published": 0}
    return templates.TemplateResponse(
        "results.html",
        {"request": request, "results": results, "score_summary": score_summary, "stats": stats, "page": "results"}
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api")
async def api_root():
    return {"message": "招标管理系统 API", "version": settings.VERSION}
