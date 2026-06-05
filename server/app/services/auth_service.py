import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.contacts_store import user_contacts
from app.repositories.user_repository import UserRepository
from app.schemas.user import TokenResponse, UserLoginRequest, UserRegisterRequest

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "chave-padrao-insegura-mude-no-env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def cadastrar(self, data: UserRegisterRequest) -> dict:
        """
        Fluxo de cadastro:
        1. Verifica se e-mail já existe → 409 se existir
        2. Verifica se usuario já existe → 409 se existir
        3. Gera o hash da senha (nunca salva a senha pura)
        4. Persiste a pessoa no banco
        5. Retorna mensagem de sucesso
        """
        if self.repo.find_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado",
            )

        if self.repo.find_by_usuario(data.usuario):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nome de usuário já cadastrado",
            )

        senha_hasheada = pwd_context.hash(data.senha)

        self.repo.create(
            usuario=data.usuario,
            email=data.email,
            telefone=data.telefone,
            senha=senha_hasheada,
        )

        return {"message": "Cadastro realizado com sucesso"}

    def login(self, data: UserLoginRequest) -> TokenResponse:
        pessoa = self.repo.find_by_email(data.email)

        credenciais_invalidas = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

        if not pessoa:
            raise credenciais_invalidas

        if not pwd_context.verify(data.senha, pessoa.senha):
            raise credenciais_invalidas

        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": pessoa.usuario,
            "email": pessoa.email,
            "exp": expire,
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        contatos = user_contacts.get(pessoa.email, [])

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            welcome_message=f"Bem-vindo, {pessoa.email}",
            contacts=contatos,
        )