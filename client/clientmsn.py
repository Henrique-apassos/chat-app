import socket
import time

def iniciar_receptor():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_servidor = '127.0.0.1' # Mude para o IP do servidor se estiver em outra máquina
    porta = 5000
    
    try:
        cliente.connect((host_servidor, porta))
        print("[*] Computador B conectado! Aguardando mensagens...")
        
        # Fica em loop ouvindo o que o servidor repassar
        while True:
            dados = cliente.recv(1024)
            if not dados:
                break
            
            mensagem = dados.decode('utf-8')
            print(f"-> Computador B recebeu: {mensagem}")
            
    except ConnectionRefusedError:
        print("[!] Não foi possível encontrar o servidor.")
    finally:
        cliente.close()

def iniciar_emissor():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_servidor = '127.0.0.1' # Mude para o IP do servidor se estiver em outra máquina
    porta = 5000
    
    try:
        cliente.connect((host_servidor, porta))
        print("[*] Computador A conectado ao servidor!")
        
        mensagem = "Olá"
        print(f"[*] Enviando mensagem: '{mensagem}'")
        
        # Envia a mensagem codificada em bytes
        cliente.sendall(mensagem.encode('utf-8'))
        
        # Uma pequena pausa para garantir que os pacotes de rede foram enviados
        time.sleep(1) 
        
    except ConnectionRefusedError:
        print("[!] Não foi possível encontrar o servidor.")
    finally:
        print("[*] Encerrando Computador A.")
        cliente.close()

if __name__ == "__main__":
    opcao = int(input("receber(1) ou enviar(2)? "))

    if opcao == 1:
        iniciar_receptor()
    elif opcao == 2:
        iniciar_emissor()
    else:
        print("Desligando...")