import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from src.config.settings import get_settings

settings = get_settings()

_db_url = settings.DATABASE_URL

_is_sqlite = _db_url.startswith("sqlite")

_connect_args = {"check_same_thread": False} if _is_sqlite else {}

engine = create_engine(
    _db_url,
    connect_args=_connect_args,
    pool_pre_ping=not _is_sqlite,
)


if _is_sqlite:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
