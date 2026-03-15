"""
schemas/avaliacao.py
Schemas Pydantic para avaliações / contribuições cidadãs.
"""

from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict


# ── Request ───────────────────────────────────────────────────

class AvaliacaoCreate(BaseModel):
    """Payload para POST /avaliacoes."""
    local_id:   int
    acessivel:  bool
    comentario: str

    @field_validator("comentario")
    @classmethod
    def comentario_valido(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Comentário deve ter ao menos 10 caracteres.")
        if len(v) > 500:
            raise ValueError("Comentário deve ter no máximo 500 caracteres.")
        return v


# ── Response ──────────────────────────────────────────────────

class AutorSchema(BaseModel):
    """Dados públicos do autor de uma avaliação."""
    model_config = ConfigDict(from_attributes=True)
    id:   int
    nome: str


class AvaliacaoResponse(BaseModel):
    """
    Resposta de uma avaliação — estrutura compatível com o
    avaliacoesStore do frontend (mesmo formato de objeto).
    """
    model_config = ConfigDict(from_attributes=True)

    id:         int
    localId:    int      # camelCase para compatibilidade com o frontend
    acessivel:  bool
    comentario: str
    autor:      str      # nome do usuário
    usuarioId:  int      # id do usuário
    data:       datetime

    @classmethod
    def from_orm(cls, av) -> "AvaliacaoResponse":
        return cls(
            id=av.id,
            localId=av.local_id,
            acessivel=av.acessivel,
            comentario=av.comentario,
            autor=av.usuario.nome,
            usuarioId=av.user_id,
            data=av.data,
        )


class EstatisticasResponse(BaseModel):
    """Estatísticas agregadas de avaliações de um local."""
    total:               int
    acessiveis:          int
    naoAcessiveis:       int
    percentualAcessivel: int | None


class AvaliacoesLocalResponse(BaseModel):
    """Resposta de GET /avaliacoes/local/{local_id}."""
    estatisticas: EstatisticasResponse
    avaliacoes:   list[AvaliacaoResponse]