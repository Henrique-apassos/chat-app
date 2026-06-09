from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class RecebeModel(Base):
    """
    Representa a tabela 'recebe' no banco de dados.
    """

    __tablename__ = "recebe"

    usuario: Mapped[str] = mapped_column("USUARIO", String, ForeignKey("pessoa.USUARIO"), primary_key=True)
    id_mensagem: Mapped[int] = mapped_column("ID_MENSAGEM", Integer, ForeignKey("mensagem.ID_MENSAGEM"), primary_key=True)
    lida: Mapped[int | None] = mapped_column("LIDA", Integer, default=0)
