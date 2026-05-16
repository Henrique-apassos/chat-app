import socket
import threading

# Lista para guardar as conexões ativas (Computador A e B)
clientes_conectados = []

def lidar_com_cliente(conexao, endereco):
    print(f"[*] Nova conexão de: {endereco}")
    clientes_conectados.append(conexao)
    
    while True:
        try:
            # Aguarda a mensagem do cliente
            mensagem = conexao.recv(1024)
            if not mensagem:
                break # Cliente desconectou
            
            # Quando recebe uma mensagem, repassa para os outros clientes
            for cliente in clientes_conectados:
                if cliente != conexao: # Não envia de volta para quem mandou
                    cliente.sendall(mensagem)
                    
        except:
            break
            
    # Se sair do loop, a conexão caiu ou foi encerrada
    print(f"[*] Conexão encerrada com {endereco}")
    clientes_conectados.remove(conexao)
    conexao.close()

def iniciar_servidor():
    # Cria o socket TCP/IP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define o host e a porta (0.0.0.0 permite conexões de qualquer IP na rede)
    host = '0.0.0.0' 
    porta = 5000
    
    # Vincula o socket ao endereço e porta
    servidor.bind((host, porta))
    
    # Fica ouvindo por conexões (limite de duas conexões)
    servidor.listen(2)
    print(f"[*] Servidor escutando na porta {porta}...")

    while True:
        conexao, endereco = servidor.accept()
        # Cria uma linha de execução (thread) separada para cada computador
        thread = threading.Thread(target=lidar_com_cliente, args=(conexao, endereco))
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()