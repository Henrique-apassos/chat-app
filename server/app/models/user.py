from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class UserModel(Base):
    """
    Representa a tabela 'pessoas' no banco de dados.

    Campos obrigatórios (preenchidos no cadastro):
        nome_usuario, email, senha, telefone

    Campos opcionais (preenchidos na edição de perfil — outro membro):
        nome, sobrenome, biografia, caminho_foto

    ATENÇÃO: 'senha' armazena o HASH bcrypt, nunca a senha pura.
    """
    __tablename__ = "pessoas"

    nome_usuario: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    senha: Mapped[str] = mapped_column(String, nullable=False)
    telefone: Mapped[str] = mapped_column(String, nullable=False)
    nome: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    sobrenome: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    biografia: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    caminho_foto: Mapped[str | None] = mapped_column(String, nullable=True, default=None)