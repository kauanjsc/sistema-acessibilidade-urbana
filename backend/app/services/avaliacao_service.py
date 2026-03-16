"""
services/avaliacao_service.py
Regras de negócio para avaliações / contribuições cidadãs.
"""

from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.models.avaliacao import Avaliacao
from app.models.local import Local
from app.schemas.avaliacao import AvaliacaoCreate, EstatisticasResponse


def criar_avaliacao(
    db: Session,
    dados: AvaliacaoCreate,
    user_id: int,
) -> Avaliacao:
    """
    Persiste uma nova avaliação.
    Valida se o local existe antes de salvar.
    """
    local = db.get(Local, dados.local_id)
    if local is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Local com id={dados.local_id} não encontrado.",
        )

    avaliacao = Avaliacao(
        user_id=user_id,
        local_id=dados.local_id,
        acessivel=dados.acessivel,
        comentario=dados.comentario,
    )
    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)

    # Carrega relacionamento para montar a resposta corretamente
    db.refresh(avaliacao, ["usuario", "local"])
    return avaliacao


def listar_avaliacoes_local(
    db: Session,
    local_id: int,
) -> tuple[list[Avaliacao], EstatisticasResponse]:
    """
    Retorna avaliações de um local (mais recentes primeiro)
    junto com estatísticas agregadas.
    """
    # Valida existência do local
    local = db.get(Local, local_id)
    if local is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Local com id={local_id} não encontrado.",
        )

    avaliacoes = (
        db.query(Avaliacao)
        .options(joinedload(Avaliacao.usuario))
        .filter(Avaliacao.local_id == local_id)
        .order_by(Avaliacao.data.desc())
        .all()
    )

    total = len(avaliacoes)
    acessiveis = sum(1 for a in avaliacoes if a.acessivel)
    nao_acessiveis = total - acessiveis
    percentual = round((acessiveis / total) * 100) if total > 0 else None

    stats = EstatisticasResponse(
        total=total,
        acessiveis=acessiveis,
        naoAcessiveis=nao_acessiveis,
        percentualAcessivel=percentual,
    )

    return avaliacoes, stats