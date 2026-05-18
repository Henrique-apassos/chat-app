from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth_router

# Cria as tabelas no banco automaticamente ao iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Chat App API",
    description="Backend do Chat App — Disciplina de Engenharia de Software",
    version="1.0.0",
)

app.include_router(auth_router.router)


@app.get("/health", tags=["Status"])
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso"}