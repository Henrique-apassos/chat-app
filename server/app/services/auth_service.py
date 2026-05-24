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

# Contexto de criptografia — usa bcrypt, o padrão da indústria
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Contém toda a lógica de negócio de autenticação.
    Não acessa o banco diretamente — usa o Repository para isso.
    """

    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def cadastrar(self, data: UserRegisterRequest) -> dict:
        """
        Fluxo de cadastro:
        1. Verifica se e-mail já existe → 409 se existir
        2. Verifica se nome_usuario já existe → 409 se existir
        3. Gera o hash da senha (nunca salva a senha pura)
        4. Persiste a pessoa no banco
        5. Retorna mensagem de sucesso
        """
        if self.repo.find_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado",
            )

        if self.repo.find_by_nome_usuario(data.nome_usuario):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nome de usuário já cadastrado",
            )

        senha_hasheada = pwd_context.hash(data.senha)

        self.repo.create(
            nome_usuario=data.nome_usuario,
            email=data.email,
            telefone=data.telefone,
            senha=senha_hasheada,
        )

        return {"message": "Cadastro realizado com sucesso"}

    def login(self, data: UserLoginRequest) -> TokenResponse:
        """
        Fluxo de login:
        1. Busca pessoa pelo e-mail
        2. Verifica se a senha bate com o hash armazenado
        3. Se qualquer etapa falhar → 401 com mensagem GENÉRICA
           (nunca revelar qual campo está errado — segurança)
        4. Gera token JWT com tempo de expiração
        5. Retorna token, welcome_message e lista de contatos
        """
        pessoa = self.repo.find_by_email(data.email)

        # Mensagem genérica intencional — não revela se foi e-mail ou senha que errou
        credenciais_invalidas = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

        if not pessoa:
            raise credenciais_invalidas

        if not pwd_context.verify(data.senha, pessoa.senha):
            raise credenciais_invalidas

        # Gera o token JWT com expiração
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": pessoa.nome_usuario,
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