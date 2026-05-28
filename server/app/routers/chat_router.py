from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime

from app.database import SessionLocal
from app.models.mensagem import MensagemModel
from app.models.grupo import GrupoModel
from app.core.ws_manager import gerenciador 

router = APIRouter(
    tags=["Chat Realtime"]
)

@router.websocket("/ws/{nome_usuario}")
async def endpoint_websocket(websocket: WebSocket, nome_usuario: str):
    await gerenciador.conectar(websocket)
    try:
        while True:
            # Recebe o texto do Frontend
            texto_recebido = await websocket.receive_text()

            # Abre uma sessão com o banco de dados e salva as informações da mensagem
            with SessionLocal() as db:
                nova_mensagem = MensagemModel(
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    texto = texto_recebido,
                    status_envio = "ENVIADO",
                    usuario = nome_usuario,
                    id_grupo = None
                )

                db.add(nova_mensagem)
                db.commit()
            
            # Envia de fato a mensagem
            mensagem_formatada = f"[{nome_usuario}] {texto_recebido}"
            await gerenciador.enviar_mensagem(mensagem_formatada, remetente=websocket)
            
    except WebSocketDisconnect:
        gerenciador.desconectar(websocket)