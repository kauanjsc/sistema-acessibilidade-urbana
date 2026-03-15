"""
models/usuario.py
Model SQLAlchemy para a tabela 'usuarios'.
"""

from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id:           Mapped[int]      = mapped_column(primary_key=True, index=True)
    nome:         Mapped[str]      = mapped_column(String(120), nullable=False)
    email:        Mapped[str]      = mapped_column(String(255), unique=True, index=True, nullable=False)
    senha_hash:   Mapped[str]      = mapped_column(String(255), nullable=False)
    perfil:       Mapped[str]      = mapped_column(
                                        SAEnum("cidadao", "admin", name="perfil_enum"),
                                        default="cidadao",
                                        nullable=False,
                                     )
    data_criacao: Mapped[datetime] = mapped_column(
                                        DateTime(timezone=True),
                                        default=lambda: datetime.now(timezone.utc),
                                        nullable=False,
                                     )

    # Relacionamento reverso (1 usuário → N avaliações)
    avaliacoes: Mapped[list["Avaliacao"]] = relationship(  # noqa: F821
        back_populates="usuario", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} email={self.email!r}>"