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
    """
    Serviço de autenticação — contém toda a lógica de negócio
    de cadastro e login. Segue o princípio da Responsabilidade Única (SRP).
    """

    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    # ── Métodos privados (Single Responsibility) ───────────────────────────

    def _hash_senha(self, senha: str) -> str:
        """Gera o hash bcrypt de uma senha pura."""
        return pwd_context.hash(senha)

    def _verificar_senha(self, senha_pura: str, senha_hash: str) -> bool:
        """Verifica se a senha pura corresponde ao hash armazenado."""
        return pwd_context.verify(senha_pura, senha_hash)

    def _gerar_token(self, usuario: str, email: str) -> str:
        """
        Gera um token JWT assinado com expiração configurável.
        Responsabilidade isolada — facilita testes e futuras trocas de algoritmo.
        """
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": usuario,
            "email": email,
            "exp": expire,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def _lancar_credenciais_invalidas(self) -> None:
        """
        Lança exceção 401 com mensagem genérica.
        Mensagem intencional — não revela se foi e-mail ou senha que errou.
        """
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    # ── Métodos públicos ───────────────────────────────────────────────────

    def cadastrar(self, data: UserRegisterRequest) -> dict:
        """
        Fluxo de cadastro:
        1. Verifica duplicidade de e-mail → 409 se existir
        2. Verifica duplicidade de usuario → 409 se existir
        3. Verifica duplicidade de telefone → 409 se existir
        4. Gera hash da senha (nunca salva a senha pura)
        5. Persiste no banco
        6. Retorna mensagem de sucesso
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

        if self.repo.find_by_telefone(data.telefone):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Telefone já cadastrado",
            )

        self.repo.create(
            usuario=data.usuario,
            email=data.email,
            telefone=data.telefone,
            senha=self._hash_senha(data.senha),
        )

        return {"message": "Cadastro realizado com sucesso"}

    def login(self, data: UserLoginRequest) -> TokenResponse:
        """
        Fluxo de login:
        1. Busca pessoa pelo e-mail
        2. Verifica senha contra hash
        3. Gera token JWT com expiração
        4. Retorna token + contatos + mensagem de boas-vindas
        """
        pessoa = self.repo.find_by_email(data.email)

        if not pessoa:
            self._lancar_credenciais_invalidas()

        if not self._verificar_senha(data.senha, pessoa.senha):
            self._lancar_credenciais_invalidas()

        return TokenResponse(
            access_token=self._gerar_token(pessoa.usuario, pessoa.email),
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            welcome_message=f"Bem-vindo, {pessoa.email}",
            contacts=user_contacts.get(pessoa.email, []),
        )