from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_usuario_atual
from app.database import get_db
from app.models.mensagem import MensagemModel
from app.models.recebe import RecebeModel

router = APIRouter(
    prefix="/api/v1/notifications",
    tags=["Notificações"],
)

@router.get("/badges")
def consultar_badges(
    usuario_atual: str = Depends(get_usuario_atual),
    db: Session = Depends(get_db),
):
    badges = (
        db.query(MensagemModel.usuario, db.func.count(MensagemModel.id_mensagem))
        .join(RecebeModel, MensagemModel.id_mensagem == RecebeModel.id_mensagem)
        .filter(RecebeModel.usuario == usuario_atual)
        .filter(RecebeModel.lida == 0)
        .group_by(MensagemModel.usuario)
        .all()
    )
    
    return {remetente: quantidade for remetente, quantidade in badges}