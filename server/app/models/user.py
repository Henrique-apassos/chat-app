from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class UserModel(Base):
    """
    Representa a tabela 'pessoa' no banco de dados.

    Campos obrigatórios (preenchidos no cadastro):
        usuario, email, senha, telefone
    
    'nome' é preenchido automaticamente com o valor de 'usuario' no cadastro.

    Campos opcionais (preenchidos na edição de perfil — outro membro):
        sobrenome, biografia, caminho_foto

    ATENÇÃO: 'senha' armazena o HASH bcrypt, nunca a senha pura.
    """
    __tablename__ = "pessoa"

    usuario: Mapped[str] = mapped_column("USUARIO", String, primary_key=True)
    email: Mapped[str] = mapped_column("EMAIL", String, unique=True)
    senha: Mapped[str] = mapped_column("SENHA", String)
    telefone: Mapped[str] = mapped_column("TELEFONE", String, unique=True)
    nome: Mapped[str] = mapped_column("NOME", String)
    sobrenome: Mapped[str | None] = mapped_column("SOBRENOME", String, nullable=True, default=None)
    biografia: Mapped[str | None] = mapped_column("BIOGRAFIA", String, nullable=True, default=None)
    caminho_foto: Mapped[str | None] = mapped_column("CAMINHO_FOTO", String, nullable=True, default=None)