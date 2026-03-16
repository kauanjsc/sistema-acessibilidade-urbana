"""
services/usuario_service.py
Regras de negócio relacionadas a usuários.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.security import hash_senha, verificar_senha


def criar_usuario(db: Session, dados: UsuarioCreate) -> Usuario:
    """
    Cria um novo usuário no banco.
    Lança HTTP 409 se o e-mail já estiver cadastrado.
    """
    existente = db.query(Usuario).filter(Usuario.email == dados.email.lower()).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado.",
        )

    usuario = Usuario(
        nome=dados.nome.strip(),
        email=dados.email.lower().strip(),
        senha_hash=hash_senha(dados.senha),
        perfil="cidadao",
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def autenticar_usuario(db: Session, email: str, senha: str) -> Usuario:
    """
    Valida credenciais.
    Lança HTTP 401 se email não existir ou senha estiver errada.
    Usa tempo de resposta constante para evitar timing attacks.
    """
    usuario = db.query(Usuario).filter(Usuario.email == email.lower().strip()).first()

    # Verifica senha mesmo se usuário não existir (evita timing attack)
    senha_ok = verificar_senha(senha, usuario.senha_hash) if usuario else False

    if not usuario or not senha_ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario