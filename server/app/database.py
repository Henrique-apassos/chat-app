from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chatapp.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

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