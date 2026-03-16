"""
services/local_service.py
Regras de negócio para locais.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.local import Local


def listar_locais(db: Session) -> list[Local]:
    """Retorna todos os locais ordenados por nome."""
    return db.query(Local).order_by(Local.nome).all()


def buscar_local(db: Session, local_id: int) -> Local:
    """
    Retorna um local pelo ID.
    Lança HTTP 404 se não encontrado.
    """
    local = db.get(Local, local_id)
    if local is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Local com id={local_id} não encontrado.",
        )
    return local