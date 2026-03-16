"""
routers/locais.py
Endpoints públicos de locais:
  GET /locais          — lista todos os locais
  GET /locais/{id}     — detalhe de um local
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.local import LocalResponse
from app.services.local_service import listar_locais, buscar_local

router = APIRouter(prefix="/locais", tags=["Locais"])


@router.get(
    "",
    response_model=list[LocalResponse],
    summary="Listar todos os locais",
)
def get_locais(db: Session = Depends(get_db)):
    """
    Retorna todos os locais cadastrados com seus recursos de acessibilidade.
    Resposta compatível com o locais.json do frontend Vue.
    """
    locais = listar_locais(db)
    return [LocalResponse.from_orm_local(l) for l in locais]


@router.get(
    "/{local_id}",
    response_model=LocalResponse,
    summary="Detalhe de um local",
)
def get_local(local_id: int, db: Session = Depends(get_db)):
    """Retorna os dados de um local específico pelo ID."""
    local = buscar_local(db, local_id)
    return LocalResponse.from_orm_local(local)