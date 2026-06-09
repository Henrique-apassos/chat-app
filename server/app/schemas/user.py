from pydantic import BaseModel, EmailStr, field_validator


class UserRegisterRequest(BaseModel):
    """
    Dados esperados no corpo da requisição de cadastro.
    Apenas os campos mínimos obrigatórios são exigidos.
    Campos opcionais de perfil (nome, sobrenome, etc.) são preenchidos depois.
    """
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

    @field_validator("usuario")
    @classmethod
    def usuario_minimo(cls, value: str) -> str:
        """Regra de negócio: nome de usuário deve ter no mínimo 3 caracteres."""
        if len(value.strip()) < 3:
            raise ValueError("Nome de usuário deve ter no mínimo 3 caracteres")
        return value.strip()


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

class UserProfileUpdateRequest(BaseModel):
    usuario: str

    novo_usuario: str | None = None
    nome: str | None = None
    sobrenome: str | None = None
    email: EmailStr | None = None
    telefone: str | None = None
    biografia: str | None = None
    caminho_foto: str | None = None

    @field_validator("biografia")
    @classmethod
    def biografia_maxima(cls, value: str | None):

        if value is None: 
            return value
        
        if len(value) > 300:
            raise ValueError("A biografia deve ter no máximo 300 caracteres")
        
        return value
    
class UserDeleteRequest(BaseModel):
    """
    Dados esperados para confirmação da exclusão da conta.

    A senha informada deve corresponder à senha
    cadastrada para o usuário que está sendo excluído.
    """

    senha: str