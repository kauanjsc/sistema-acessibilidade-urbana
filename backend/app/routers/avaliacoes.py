"""
routers/avaliacoes.py
Endpoints de contribuições cidadãs:
  POST /avaliacoes                    — enviar avaliação (🔒 autenticado)
  GET  /avaliacoes/local/{local_id}   — listar avaliações de um local
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.avaliacao import AvaliacaoCreate, AvaliacaoResponse, AvaliacoesLocalResponse
from app.services.avaliacao_service import criar_avaliacao, listar_avaliacoes_local
from app.security import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])


@router.post(
    "",
    response_model=AvaliacaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enviar avaliação de acessibilidade (🔒 requer login)",
)
def post_avaliacao(
    dados: AvaliacaoCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user),  # 🔒 JWT obrigatório
):
    """
    Registra uma nova avaliação de acessibilidade.
    Requer header: Authorization: Bearer <token>

    O usuário autenticado é automaticamente associado à avaliação.
    """
    avaliacao = criar_avaliacao(db, dados, user_id=usuario_atual.id)
    return AvaliacaoResponse.from_orm(avaliacao)


@router.get(
    "/local/{local_id}",
    response_model=AvaliacoesLocalResponse,
    summary="Listar avaliações de um local",
)
def get_avaliacoes_local(local_id: int, db: Session = Depends(get_db)):
    """
    Retorna todas as avaliações de um local específico,
    junto com as estatísticas agregadas (total, % positivo, etc.).
    Resposta compatível com o ListaComentarios.vue do frontend.
    """
    avaliacoes, stats = listar_avaliacoes_local(db, local_id)
    return AvaliacoesLocalResponse(
        estatisticas=stats,
        avaliacoes=[AvaliacaoResponse.from_orm(a) for a in avaliacoes],
    )