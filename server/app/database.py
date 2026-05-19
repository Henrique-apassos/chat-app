from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Mudamos o valor padrão para apontar para dentro da pasta 'database'
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/chatapp.db")

# 2. Verifica se o banco configurado é o SQLite (para não dar erro se você usar Postgres no futuro)
if DATABASE_URL.startswith("sqlite"):
    # Cria a pasta 'database' na raiz do projeto
    os.makedirs("database", exist_ok=True)

# 3. Configuramos o connect_args APENAS para o SQLite (Postgres não aceita esse argumento)
args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """Classe base da qual todos os Models herdam."""
    pass

def get_db():
    """
    Fornece uma sessão de banco por requisição.
    O 'finally' garante que a sessão seja fechada mesmo se ocorrer erro.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()