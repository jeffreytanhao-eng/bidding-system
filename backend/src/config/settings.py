import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "招标管理系统"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = ""

    REDIS_URL: str = "redis://localhost:6379/0"

    DINGTALK_APP_KEY: str = ""
    DINGTALK_APP_SECRET: str = ""

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "bidding"

    BLOB_READ_WRITE_TOKEN: str = ""

    class Config:
        env_file = ".env"


def _get_database_url() -> str:
    url = os.environ.get("DATABASE_URL", "")
    if url:
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url
    from pathlib import Path
    if os.environ.get("VERCEL"):
        _db_dir = Path("/tmp") / "bidding-data"
    else:
        _db_dir = Path(__file__).parent.parent.parent / "data"
    _db_dir.mkdir(parents=True, exist_ok=True)
    _db_path = (_db_dir / "bidding.db").as_posix()
    return f"sqlite:///{_db_path}"


@lru_cache()
def get_settings():
    os.environ.setdefault("DATABASE_URL", _get_database_url())
    return Settings()
