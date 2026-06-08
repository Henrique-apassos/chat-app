from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/chatapp.db")

if DATABASE_URL.startswith("sqlite"):
    os.makedirs("database", exist_ok=True)

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