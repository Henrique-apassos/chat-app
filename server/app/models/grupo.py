from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class GrupoModel(Base):
    __tablename__ = "grupo"

    id_grupo: Mapped[int] = mapped_column("ID_GRUPO", Integer, primary_key=True, autoincrement=True)
    nome_grupo: Mapped[str] = mapped_column("NOME_GRUPO", String)
    data_criacao: Mapped[str] = mapped_column("DATA_CRIACAO", String)
    descricao: Mapped[str | None] = mapped_column("DESCRICAO", String)