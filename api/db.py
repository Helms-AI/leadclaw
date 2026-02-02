"""
Database connection for Neon PostgreSQL
"""
import os
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL", "")

# Neon requires SSL
if DATABASE_URL and "sslmode" not in DATABASE_URL:
    DATABASE_URL = f"{DATABASE_URL}?sslmode=require"

engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None
SessionLocal = sessionmaker(bind=engine) if engine else None
Base = declarative_base()


@contextmanager
def get_db():
    """Context manager for database sessions"""
    if not SessionLocal:
        raise RuntimeError("DATABASE_URL not configured")
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    if engine:
        Base.metadata.create_all(bind=engine)


def health_check():
    """Check database connectivity"""
    if not engine:
        return {"status": "error", "message": "DATABASE_URL not configured"}
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Connected to Neon"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
