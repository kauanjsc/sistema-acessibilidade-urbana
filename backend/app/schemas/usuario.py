"""
schemas/usuario.py
Schemas Pydantic para usuários: registro, login, resposta pública.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict


# ── Request schemas ───────────────────────────────────────────

class UsuarioCreate(BaseModel):
    """Payload para POST /auth/register."""
    nome:  str
    email: EmailStr
    senha: str

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Nome não pode ser vazio.")
        return v.strip()

    @field_validator("senha")
    @classmethod
    def senha_minima(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Senha deve ter ao menos 6 caracteres.")
        return v


class LoginRequest(BaseModel):
    """Payload para POST /auth/login."""
    email: EmailStr
    senha: str


# ── Response schemas ──────────────────────────────────────────

class UsuarioResponse(BaseModel):
    """Dados públicos do usuário — nunca expõe a senha."""
    model_config = ConfigDict(from_attributes=True)

    id:           int
    nome:         str
    email:        str
    perfil:       str
    data_criacao: datetime


class TokenResponse(BaseModel):
    """Resposta do login bem-sucedido."""
    access_token: str
    token_type:   str = "bearer"
    usuario:      UsuarioResponse