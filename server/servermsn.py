import socket

def iniciar_servidor():
    # Cria o socket TCP/IP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define o host e a porta (0.0.0.0 permite conexões de qualquer IP na rede)
    host = '0.0.0.0' 
    porta = 5000
    
    # Vincula o socket ao endereço e porta
    servidor.bind((host, porta))
    
    # Fica ouvindo por conexões (limite de 1 conexão na fila)
    servidor.listen(1)
    print(f"[*] Servidor escutando na porta {porta}...")
    
    # Aceita a conexão do cliente
    conexao, endereco = servidor.accept()
    print(f"[*] Conectado por {endereco}")
    
    with conexao:
        while True:
            # Recebe os dados (até 1024 bytes por vez)
            dados = conexao.recv(1024)
            if not dados:
                break
            
            mensagem = dados.decode('utf-8')
            print(f"Mensagem recebida: {mensagem}")
            
            # Envia uma confirmação de volta
            resposta = "Mensagem recebida com sucesso!"
            conexao.sendall(resposta.encode('utf-8'))

if __name__ == "__main__":
    iniciar_servidor()