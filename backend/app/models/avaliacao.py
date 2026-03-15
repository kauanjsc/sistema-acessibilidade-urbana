"""
models/avaliacao.py
Model SQLAlchemy para a tabela 'avaliacoes'.
"""

from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Text, Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id:        Mapped[int]  = mapped_column(primary_key=True, index=True)
    user_id:   Mapped[int]  = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    local_id:  Mapped[int]  = mapped_column(ForeignKey("locais.id",   ondelete="CASCADE"), nullable=False, index=True)
    acessivel: Mapped[bool] = mapped_column(Boolean, nullable=False)
    comentario: Mapped[str] = mapped_column(Text, nullable=False)
    data:      Mapped[datetime] = mapped_column(
                                    DateTime(timezone=True),
                                    default=lambda: datetime.now(timezone.utc),
                                    nullable=False,
                                  )

    # Relacionamentos
    usuario: Mapped["Usuario"] = relationship(back_populates="avaliacoes")  # noqa: F821
    local:   Mapped["Local"]   = relationship(back_populates="avaliacoes")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Avaliacao id={self.id} local_id={self.local_id} acessivel={self.acessivel}>"