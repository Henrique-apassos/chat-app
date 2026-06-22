from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.security import get_usuario_atual
from app.database import get_db
from app.models.mensagem import MensagemModel
from app.models.recebe import RecebeModel

router = APIRouter(
    prefix="/api/v1/notifications",
    tags=["Notificacoes"],
)

@router.get("/badges")
def consultar_badges(
    usuario_atual: str = Depends(get_usuario_atual),
    db: Session = Depends(get_db),
):
    """
    Consulta badges de mensagens nao lidas agrupadas por remetente.
    Retorna um dicionario {remetente: quantidade}.
    """
    try:
        badges = (
            db.query(MensagemModel.usuario, func.count(MensagemModel.id_mensagem))
            .join(RecebeModel, MensagemModel.id_mensagem == RecebeModel.id_mensagem)
            .filter(RecebeModel.usuario == usuario_atual)
            .filter(
                (RecebeModel.lida == 0) | (RecebeModel.lida.is_(None))
            )
            .group_by(MensagemModel.usuario)
            .all()
        )
        
        return {remetente: quantidade for remetente, quantidade in badges}
    
    except Exception as e:
        print(f"Erro ao consultar badges: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao consultar notificacoes"
        )