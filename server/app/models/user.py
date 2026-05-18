from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class UserModel(Base):
    """
    Representa a tabela 'pessoas' no banco de dados,
    mapeada diretamente a partir do modelo conceitual do drawio.
    ATENÇÃO: o campo 'senha' armazena o HASH da senha, nunca a senha pura.
    """
    __tablename__ = "pessoas"

    id_pessoa: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_de_usuario: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    senha: Mapped[str] = mapped_column(String, nullable=False)
    telefone: Mapped[str] = mapped_column(String, nullable=False)