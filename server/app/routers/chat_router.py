from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.ws_manager import gerenciador  

router = APIRouter(
    tags=["Chat Realtime"]
)

@router.websocket("/ws")
async def endpoint_websocket(websocket: WebSocket):
    await gerenciador.conectar(websocket)
    try:
        while True:
            mensagem = await websocket.receive_text()
            await gerenciador.enviar_mensagem(mensagem, remetente=websocket)
            
    except WebSocketDisconnect:
        gerenciador.desconectar(websocket)