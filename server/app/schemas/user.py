from pydantic import BaseModel, EmailStr, field_validator


class UserRegisterRequest(BaseModel):
    """Dados esperados no corpo da requisição de cadastro."""
    usuario: str
    email: EmailStr
    telefone: str
    senha: str

    @field_validator("senha")
    @classmethod
    def senha_minima(cls, value: str) -> str:
        """Regra de negócio: senha deve ter no mínimo 6 caracteres."""
        if len(value) < 6:
            raise ValueError("A senha deve ter no mínimo 6 caracteres")
        return value


class UserLoginRequest(BaseModel):
    """Dados esperados no corpo da requisição de login."""
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    """Estrutura da resposta após login bem-sucedido."""
    access_token: str
    token_type: str
    expires_in: int
    welcome_message: str = ""
    contacts: list = []