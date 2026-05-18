from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import TokenResponse, UserLoginRequest, UserRegisterRequest
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def cadastrar(data: UserRegisterRequest, db: Session = Depends(get_db)):
    """
    Rota: POST /auth/register
    Corpo: { email, nome_de_usuario, telefone, senha }
    Sucesso: 201 + { message: "Cadastro realizado com sucesso" }
    """
    service = AuthService(db)
    return service.cadastrar(data)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(data: UserLoginRequest, db: Session = Depends(get_db)):
    """
    Rota: POST /auth/login
    Corpo: { email, senha }
    Sucesso: 200 + { access_token, token_type, expires_in, contacts }
    """
    service = AuthService(db)
    return service.login(data)