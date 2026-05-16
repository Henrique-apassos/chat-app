from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI

# Classe que gerencia as conexões
class GerenciadorDeConexao:
    def __init__(self):
        self.conexoes_ativas: list[WebSocket] = []

    async def conectar(self, websocket: WebSocket):
        await websocket.accept()
        self.conexoes_ativas.append(websocket)
        print("[*] Nova Conexão estabelecida!")

    def deconectar(self, websocket: WebSocket):
        self.conexoes_ativas.remove(websocket)
        print("[*] Conexão encerrada.")
    
    async def enviar_mensagem(self, mensagem: str, remetente: WebSocket ):
        for conexao in self.conexoes_ativas:
            if conexao != remetente:
                await conexao.send_text(mensagem)

gereciador = GerenciadorDeConexao()

# Porta de entrada para conexão dos clients
@app.websocket("/ws")
async def endpoint_websocket(websocket: WebSocket):
    await gereciador.conectar(websocket)
    try:
        while True:
            mensagem = await websocket.receive_text()

            await gereciador.enviar_mensagem(mensagem, remetente=websocket)
    except:
        # Quando o cliente fecha a aba do navegador
        gereciador.deconectar(websocket)