from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import TokenResponse, UserLoginRequest, UserRegisterRequest
from app.services.auth_service import AuthService
from app.models.user import UserModel
import os

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def cadastrar(data: UserRegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.cadastrar(data)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(data: UserLoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(data)


@router.delete("/test/cleanup", status_code=status.HTTP_200_OK)
def cleanup(db: Session = Depends(get_db)):
    """Endpoint exclusivo para testes — limpa todos os usuários do banco."""
    if os.getenv("ENVIRONMENT") != "production":
        db.query(UserModel).delete()
        db.commit()
        return {"message": "Banco limpo com sucesso"}