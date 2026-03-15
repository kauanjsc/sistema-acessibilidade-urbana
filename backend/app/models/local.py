"""
models/local.py
Model SQLAlchemy para a tabela 'locais'.
Espelha exatamente os campos presentes em src/data/locais.json do frontend.
"""

from sqlalchemy import String, Text, Float, Boolean, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Local(Base):
    __tablename__ = "locais"

    id:       Mapped[int]   = mapped_column(primary_key=True, index=True)
    nome:     Mapped[str]   = mapped_column(String(200), nullable=False)
    tipo:     Mapped[str]   = mapped_column(String(50),  nullable=False)  # ex: "shopping", "hospital"
    tipo_label: Mapped[str] = mapped_column(String(100), nullable=False)  # ex: "Shopping Center"
    endereco: Mapped[str]   = mapped_column(String(300), nullable=False)
    bairro:   Mapped[str]   = mapped_column(String(100), nullable=False)
    lat:      Mapped[float] = mapped_column(Float, nullable=False)
    lng:      Mapped[float] = mapped_column(Float, nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Recursos de acessibilidade (espelha o objeto 'acessibilidade' do JSON)
    rampa:              Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    banheiro_adaptado:  Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    vaga_pcd:           Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    elevador:           Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    entrada_acessivel:  Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    calcada_acessivel:  Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relacionamento reverso (1 local → N avaliações)
    avaliacoes: Mapped[list["Avaliacao"]] = relationship(  # noqa: F821
        back_populates="local", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Local id={self.id} nome={self.nome!r}>"