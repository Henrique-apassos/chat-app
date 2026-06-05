from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class MensagemModel(Base):
    """
    Representa a tabela 'mensagem' no banco de dados.
    
    Campos obrigatórios:
        timestamp, texto
        
    Campos opcionais/estrangeiros:
        status_envio, usuario (remetente), id_grupo (se for chat de grupo)
    """
    __tablename__ = "mensagem"

    # Mapeando e alinhando com os nomes em MAIÚSCULO do seu banco de dados
    id_mensagem: Mapped[int] = mapped_column("ID_MENSAGEM", Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[str] = mapped_column("TIMESTAMP", String)
    texto: Mapped[str] = mapped_column("TEXTO", String)
    status_envio: Mapped[str | None] = mapped_column("STATUS_ENVIO", String)
    
    # Chaves estrangeiras (Foreign Keys) ligando com as outras tabelas
    usuario: Mapped[str | None] = mapped_column("USUARIO", String, ForeignKey("pessoa.USUARIO"))
    id_grupo: Mapped[int | None] = mapped_column("ID_GRUPO", Integer, ForeignKey("grupo.ID_GRUPO"))