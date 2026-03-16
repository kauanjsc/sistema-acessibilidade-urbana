"""
routers/auth.py
Endpoints de autenticação:
  POST /auth/register  — cadastro de novo usuário
  POST /auth/login     — login e emissão de JWT
  GET  /auth/me        — dados do usuário autenticado
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
# Trazemos o LoginRequest de volta para a importação!
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, TokenResponse, LoginRequest
from app.services.usuario_service import criar_usuario, autenticar_usuario
from app.security import criar_access_token, get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo usuário",
)
def register(dados: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Cadastra um novo cidadão na plataforma.
    Retorna os dados públicos do usuário criado (sem senha).
    """
    usuario = criar_usuario(db, dados)
    return usuario


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login — obter token JWT",
)
# Alteramos o parâmetro para receber o schema LoginRequest (JSON)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica o usuário com e-mail e senha.
    Retorna um token JWT Bearer e os dados do usuário.
    """
    # Voltamos a usar dados.email e dados.senha
    usuario = autenticar_usuario(db, dados.email, dados.senha)
    token = criar_access_token(data={"sub": str(usuario.id)})
    return TokenResponse(access_token=token, usuario=usuario)


@router.get(
    "/me",
    response_model=UsuarioResponse,
    summary="Dados do usuário autenticado",
)
def me(usuario_atual: Usuario = Depends(get_current_user)):
    """
    Retorna os dados do usuário dono do token JWT enviado.
    Requer header: Authorization: Bearer <token>
    """
    return usuario_atual