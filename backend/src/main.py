
import os
import tempfile
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import get_settings
from src.services.tender_parser import tender_parser
from src.utils.database import create_tables
from src.api.routes import suppliers, tenders, bids, reviews, results, users
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

app.include_router(suppliers.router, prefix=settings.API_V1_STR)
app.include_router(tenders.router, prefix=settings.API_V1_STR)
app.include_router(bids.router, prefix=settings.API_V1_STR)
app.include_router(reviews.router, prefix=settings.API_V1_STR)
app.include_router(results.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)

_templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(_templates_dir))


@app.on_event("startup")
def on_startup():
    from src.models import supplier, tender, bid, review, user
    create_tables()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stats = {"suppliers": 0, "tenders": 0, "bids": 0, "results": 0}
    try:
        from src.utils.database import SessionLocal
        from src.models.supplier import Supplier
        from src.models.tender import Tender
        from src.models.bid import Bid
        db = SessionLocal()
        stats["suppliers"] = db.query(Supplier).count()
        stats["tenders"] = db.query(Tender).count()
        stats["bids"] = db.query(Bid).count()
        db.close()
    except Exception:
        pass
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "current_time": current_time, "stats": stats, "page": "home"}
    )


@app.get("/suppliers", response_class=HTMLResponse)
async def suppliers_page(request: Request):
    suppliers_list = []
    try:
        from src.utils.database import SessionLocal
        from src.models.supplier import Supplier
        db = SessionLocal()
        suppliers_list = db.query(Supplier).all()
        db.close()
    except Exception:
        pass
    return templates.TemplateResponse(
        "suppliers.html",
        {"request": request, "suppliers": suppliers_list, "page": "suppliers"}
    )


@app.get("/tenders", response_class=HTMLResponse)
async def tenders_page(request: Request):
    tenders_list = []
    stats = {"draft": 0, "published": 0, "in_progress": 0, "completed": 0}
    try:
        from src.utils.database import SessionLocal
        from src.models.tender import Tender
        db = SessionLocal()
        tenders_list = db.query(Tender).order_by(Tender.created_at.desc()).all()
        for t in tenders_list:
            if t.status in stats:
                stats[t.status] += 1
        db.close()
    except Exception:
        pass
    return templates.TemplateResponse(
        "tenders.html",
        {"request": request, "tenders": tenders_list, "stats": stats, "page": "tenders"}
    )


@app.get("/reviews", response_class=HTMLResponse)
async def reviews_page(request: Request):
    reviews_list = []
    stats = {"pending": 0, "in_progress": 0, "completed": 0, "reviewers": 0}
    try:
        from src.utils.database import SessionLocal
        from src.models.review import Reviewer
        db = SessionLocal()
        reviews_list = db.query(Reviewer).all()
        stats["reviewers"] = len(reviews_list)
        db.close()
    except Exception:
        pass
    return templates.TemplateResponse(
        "reviews.html",
        {"request": request, "reviews": reviews_list, "stats": stats, "page": "reviews"}
    )


@app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request):
    results_list = []
    score_summary = []
    stats = {"total": 0, "pending": 0, "approved": 0, "published": 0}
    return templates.TemplateResponse(
        "results.html",
        {"request": request, "results": results_list, "score_summary": score_summary, "stats": stats, "page": "results"}
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

    text = tender_parser.extract_text(file_content, file.filename)
    info = tender_parser.parse_tender_info(text)
    info["filename"] = file.filename

    blob_token = os.environ.get("BLOB_READ_WRITE_TOKEN", "")
    if blob_token:
        try:
            from vercel_blob import upload
            blob = upload(file_content, file.filename, token=blob_token)
            info["saved_url"] = blob["url"]
        except Exception:
            pass

    return JSONResponse(content={"success": True, "data": info})


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api")
async def api_root():
    return {"message": "招标管理系统 API", "version": settings.VERSION}
