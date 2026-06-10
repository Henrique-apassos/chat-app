from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from datetime import datetime
import json
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from pydantic import BaseModel

from app import database
from app.models.mensagem import MensagemModel
from app.models.recebe import RecebeModel
from app.models.grupo import GrupoModel
from app.core.ws_manager import gerenciador 

router = APIRouter(
    tags=["Chat Realtime"]
)


# O MOTOR DO WEBSOCKET
@router.websocket("/ws/{nome_usuario}")
async def endpoint_websocket(websocket: WebSocket, nome_usuario: str):
    await gerenciador.conectar(websocket)
    try:
        while True:
            texto_recebido = await websocket.receive_text()

            if not texto_recebido.strip():
                continue

            # Desempacota o JSON do React
            destinatario_str = None
            texto_limpo = texto_recebido
            try:
                pacote = json.loads(texto_recebido)
                if isinstance(pacote, dict):
                    destinatario_str = pacote.get("para")
                    texto_limpo = pacote.get("texto", texto_recebido)
            except json.JSONDecodeError:
                pass 

            with database.SessionLocal() as db:
                # Salva na tabela 'mensagem' (Grava quem enviou)
                nova_mensagem = MensagemModel(
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    texto=texto_limpo,
                    status_envio="ENVIADO",
                    usuario=nome_usuario, # Remetente
                    id_grupo=None
                )
                db.add(nova_mensagem)
                db.commit()
                db.refresh(nova_mensagem) # Atualiza para pegar o ID gerado automaticamente
                
                # Lemos e guardamos o ID enquanto a conexão com o banco ainda está aberta!
                id_gerado = nova_mensagem.id_mensagem

                # Salva na tabela 'recebe' (Grava quem recebeu vinculando ao ID da mensagem)
                if destinatario_str:
                    novo_recebimento = RecebeModel(
                        usuario=destinatario_str, # Destinatário
                        id_mensagem=id_gerado,    # Usamos a variável segura aqui
                        lida=0
                    )
                    db.add(novo_recebimento)
                    db.commit()
            
            # Fora do 'with', a sessão fechou. Mas a nossa variável 'id_gerado' está a salvo!
            mensagem_formatada = json.dumps({
                "id_mensagem": id_gerado, 
                "remetente": nome_usuario, 
                "texto": texto_limpo
            })
            
            # 1. Envia a mensagem para o destinatário através do gestor
            await gerenciador.enviar_mensagem(mensagem_formatada, remetente=websocket)
            
            # 2. Devolve a confirmação para o próprio emissor ver a mensagem com o ID correto na sua interface
            await websocket.send_text(mensagem_formatada)
            
    except WebSocketDisconnect:
        gerenciador.desconectar(websocket)


# ROTA DE HISTÓRICO PARA O REACT 

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/mensagens/{remetente}/{destinatario}")
def obter_historico_mensagens(remetente: str, destinatario: str, db: Session = Depends(get_db)):
    """
    Busca o histórico fazendo um JOIN entre a tabela 'mensagem' e a 'recebe'
    """
    historico = db.query(MensagemModel).join(
        RecebeModel, MensagemModel.id_mensagem == RecebeModel.id_mensagem
    ).filter(
        or_(
            # Cenário 1: Remetente enviou, Destinatário recebeu
            and_(MensagemModel.usuario == remetente, RecebeModel.usuario == destinatario),
            # Cenário 2: Destinatário enviou, Remetente recebeu
            and_(MensagemModel.usuario == destinatario, RecebeModel.usuario == remetente)
        )
    ).order_by(MensagemModel.id_mensagem.asc()).all()

    # Formata a resposta para o frontend
    lista_mensagens = []
    for msg in historico:
        lista_mensagens.append({
            "id_mensagem": msg.id_mensagem,
            "remetente": msg.usuario,
            "texto": msg.texto
        })

    return lista_mensagens

# ROTA EDIÇÃO DE MENSAGEM  
class EditarMensagemRequest(BaseModel):
    usuario: str
    novo_texto: str

@router.put("/mensagens/{id_mensagem}")
def editar_mensagem(
    id_mensagem: int,
    dados: EditarMensagemRequest,
    db: Session = Depends(get_db)
):
    mensagem = db.query(MensagemModel).filter(
        MensagemModel.id_mensagem == id_mensagem
    ).first()

    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")

    if mensagem.usuario != dados.usuario:
        raise HTTPException(status_code=403, detail="Usuário não autorizado a editar esta mensagem")

    mensagem.texto = dados.novo_texto
    db.commit()
    db.refresh(mensagem)

    return {
        "mensagem": "Mensagem editada com sucesso",
        "id_mensagem": mensagem.id_mensagem,
        "texto": mensagem.texto,
        "editada": True
    }


# ROTA EXCLUSÃO DE MENSAGEM
class ExcluirMensagemRequest(BaseModel):
    usuario: str

@router.delete("/mensagens/{id_mensagem}")
def excluir_mensagem(
    id_mensagem: int,
    dados: ExcluirMensagemRequest,
    db: Session = Depends(get_db)
):
    mensagem = db.query(MensagemModel).filter(
        MensagemModel.id_mensagem == id_mensagem
    ).first()

    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")

    if mensagem.usuario != dados.usuario:
        raise HTTPException(status_code=403, detail="Usuário não autorizado a excluir esta mensagem")

    recebimentos = db.query(RecebeModel).filter(
        RecebeModel.id_mensagem == id_mensagem
    ).all()

    for recebimento in recebimentos:
        db.delete(recebimento)

    db.delete(mensagem)
    db.commit()

    return {
        "mensagem": "Mensagem excluída com sucesso",
        "id_mensagem": id_mensagem
    }