"""
database.py
Configura a conexão com PostgreSQL via SQLAlchemy 2.x.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import get_settings

settings = get_settings()

# Engine síncrono — suficiente para FastAPI com endpoints síncronos/assíncronos simples
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,       # testa conexão antes de usar (evita "broken pipe")
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Classe base para todos os models SQLAlchemy."""
    pass


def get_db():
    """
    Dependency injection do FastAPI.
    Garante que a sessão seja fechada após cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()