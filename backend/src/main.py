
import os
import shutil
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import get_settings
from src.services.tender_parser import tender_parser
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

upload_dir = Path(__file__).parent.parent / "uploads"
upload_dir.mkdir(exist_ok=True)


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


@app.post("/api/tenders/upload")
async def upload_tender_file(file: UploadFile = File(...)):
    allowed_extensions = {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".txt"}
    ext = Path(file.filename).suffix.lower() if file.filename else ""
    if ext not in allowed_extensions:
        return JSONResponse(
            status_code=400,
            content={"error": f"不支持的文件类型: {ext}，支持: {', '.join(allowed_extensions)}"}
        )

    file_content = await file.read()
    if len(file_content) > 50 * 1024 * 1024:
        return JSONResponse(status_code=400, content={"error": "文件大小不能超过50MB"})

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = upload_dir / safe_filename
    with open(file_path, "wb") as f:
        f.write(file_content)

    text = tender_parser.extract_text(file_content, file.filename)
    info = tender_parser.parse_tender_info(text)
    info["filename"] = file.filename
    info["saved_path"] = str(file_path)

    return JSONResponse(content={"success": True, "data": info})


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api")
async def api_root():
    return {"message": "招标管理系统 API", "version": settings.VERSION}
