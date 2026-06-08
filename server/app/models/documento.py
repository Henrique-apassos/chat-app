from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class DocumentoModel(Base):
    """
    Representa a tabela 'documento' no banco de dados.
    
    Campos obrigatórios:
        caminho
        
    Campos opcionais/estrangeiros:
        tipo, tamanho, id_mensagem
    """
    __tablename__ = "documento"

    # Mapeando e alinhando com os nomes em MAIÚSCULO do seu banco de dados
    id_documento: Mapped[int] = mapped_column("ID_DOCUMENTO", Integer, primary_key=True, autoincrement=True)
    caminho: Mapped[str] = mapped_column("CAMINHO", String)
    tipo: Mapped[str | None] = mapped_column("TIPO", String)
    tamanho: Mapped[set | None] = mapped_column("TAMANHO", String)
    
    # Chaves estrangeiras (Foreign Keys) ligando com as outras tabelas
    id_mensagem: Mapped[int | None] = mapped_column("ID_MENSAGEM", String, ForeignKey("mensagem.ID_MENSAGEM"))