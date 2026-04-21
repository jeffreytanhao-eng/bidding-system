
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import get_settings
from src.api.routes import suppliers, tenders, bids, reviews, results

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


@app.get("/")
async def root():
    return {"message": "招标管理系统", "version": settings.VERSION}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

