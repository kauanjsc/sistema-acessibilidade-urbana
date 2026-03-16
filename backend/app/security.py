"""
security.py
Funções de segurança: hash de senha (bcrypt), criação e
validação de tokens JWT, dependência get_current_user.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db

settings = get_settings()

# ── Bcrypt ────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_senha(senha: str) -> str:
    """Gera o hash bcrypt de uma senha em texto claro."""
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Compara uma senha em texto claro com seu hash."""
    return pwd_context.verify(senha, senha_hash)


# ── JWT ───────────────────────────────────────────────────────
# Trocamos para HTTPBearer para colar o token puro no Swagger
security = HTTPBearer()


def criar_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT assinado com HS256.
    O payload recebe 'sub' (subject = user_id) e 'exp' (expiração).
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decodificar_token(token: str) -> dict:
    """Decodifica e valida o token JWT. Lança JWTError em caso de falha."""
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


# ── Dependência: usuário autenticado ─────────────────────────
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Dependência FastAPI injetada em endpoints protegidos.
    Valida o JWT e retorna o objeto Usuario do banco.
    Lança HTTP 401 em qualquer falha de autenticação.
    """
    # Importação local para evitar circular import
    from app.models.usuario import Usuario

    # Extrai o token de dentro do objeto HTTPAuthorizationCredentials
    token = credentials.credentials

    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decodificar_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credenciais_invalidas
    except JWTError:
        raise credenciais_invalidas

    usuario = db.get(Usuario, int(user_id))
    if usuario is None:
        raise credenciais_invalidas

    return usuario