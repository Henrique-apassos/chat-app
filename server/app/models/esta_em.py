from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class EstaModel(Base):
    """
    Representa a tabela 'esta_em' no banco de dados.
    """

    __tablename__ = "esta_em"

    usuario: Mapped[str] = mapped_column("USUARIO", String, ForeignKey("pessoa.USUARIO"), primary_key=True)
    id_grupo: Mapped[int] = mapped_column("ID_GRUPO", Integer, ForeignKey("mensagem.ID_GRUPO"), primary_key=True)
    papel: Mapped[str | None] = mapped_column("PAPEL", String, nullable=True)
    data_entrada: Mapped[str] = mapped_column("DATA_ENTRADA", String)