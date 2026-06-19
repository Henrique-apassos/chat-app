from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth_router, chat_router, conversas_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Chat App API",
    description="Backend do Chat App — Disciplina de Engenharia de Software",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(chat_router.router)
app.include_router(user_router.router)
app.include_router(conversas_router.router)

@app.get("/health", tags=["Status"])
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso"}