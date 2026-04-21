
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "招标管理系统"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/bidding_system"
    
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
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()

