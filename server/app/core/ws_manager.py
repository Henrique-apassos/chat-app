from fastapi import WebSocket

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

# Criamos uma instância única (Singleton) para ser usada em toda a aplicação
gerenciador = GerenciadorDeConexao()