"""
main.py
Ponto de entrada da API — Teresina Acessível Backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, locais, avaliacoes

# Importa models para que o SQLAlchemy os registre antes de criar tabelas
import app.models  # noqa: F401

settings = get_settings()

# ── Cria tabelas no banco (em produção use Alembic) ───────────
Base.metadata.create_all(bind=engine)

# ── Aplicação ─────────────────────────────────────────────────
app = FastAPI(
    title="Teresina Acessível — API",
    description="""
Backend REST para a plataforma colaborativa de mapeamento de acessibilidade urbana.

## Autenticação
Endpoints protegidos exigem token JWT no header:
```
Authorization: Bearer <token>
```
Obtenha o token via **POST /auth/login**.   

## Frontend
Desenvolvido em **Vue 3 + Vite + Leaflet**.
    """,
    version="1.0.0",
    contact={
        "name": "Kauan Santos — TCC UESPI",
        "email": "kauanjscardoso@gmail.com",
    },
    license_info={"name": "MIT"},
)

# ── CORS ───────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(locais.router)
app.include_router(avaliacoes.router)


# ── Health check ──────────────────────────────────────────────
@app.get("/", tags=["Health"], summary="Health check")
def root():
    return {
        "status": "online",
        "app": "Teresina Acessível API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"], summary="Status detalhado")
def health():
    return {"status": "ok", "environment": settings.environment}