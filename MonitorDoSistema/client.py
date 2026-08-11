import socket
import threading


SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

# Variavel de controle (client-encerramento)
running = True

# Evento de recebimento de resposta
response_event = threading.Event()


# THREAD 1 - ENVIAR

def thread_enviar(client):
    global running

    while running:

        # Garante que o evento esteja desligado
        response_event.clear()

        try:
            comando = input("\nComando: ").strip()

        except EOFError: #NAO ENTRAR EM DEADLOCK
            running = False #sair do while
            response_event.set() #Liberação da thread
            break

        # Verifica se o cliente ainda está executando
        if not running:
            break

        # Ignora comandos vazios
        if not comando:
            continue

        # Envia o comando para o servidor
        try:
            client.sendall(comando.encode())

        #OBS: tratar 
        except (BrokenPipeError, ConnectionResetError, OSError):
            print("Erro ao enviar comando.")
            running = False
            response_event.set()
            break

        # EXIT

        if comando.upper() == "EXIT":
            print("Aguardando resposta do servidor...")

            # Espera o servidor confirmar o final
            response_event.wait()

            running = False
            break

        # OUTROS COMANDOS************************************


        print("Aguardando resposta do servidor...")

        # A thread fica bloqueada 
        # recebimento receba uma resposta para seguir
        response_event.wait()


# THREAD 2 - RECEBER

def thread_receber(client):
    global running

    while running:

        try:
            data = client.recv(4096)

            # Servidor fechou a conexão
            if not data:
                print("\nServidor desconectou.")
                running = False
                response_event.set()
                break

            mensagem = data.decode()

            print("\n-----------------------------")
            print(mensagem)
            print("-----------------------------")

            # Libera a thread de envio
            # para fazer uma nova requisição
            response_event.set()

            # Verifica se o servidor está encerrando
            if "encerrando servidor" in mensagem.lower():
                running = False
                break

        except (
            ConnectionResetError,
            ConnectionAbortedError,
            OSError
        ):
            running = False
            response_event.set()
            break

    print("Thread de recebimento encerrada.")

# MAIN

def main():
    global running

    # Criação do socket TCP
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # Conexão com o servidor
    try:
        client.connect(
            (SERVER_IP, SERVER_PORT)
        )

        print("Conectado ao servidor com sucesso!")

    except ConnectionRefusedError:
        print(
            "Não foi possível conectar ao servidor. "
            "Verifique o IP e a porta."
        )

        client.close()
        return

    # CRIAÇÃO DAS DUAS THREADS

    thread_send = threading.Thread(
        target=thread_enviar,
        args=(client,)
    )

    thread_recv = threading.Thread(
        target=thread_receber,
        args=(client,)
    )

    # Inicia as duas threads
    thread_recv.start()
    thread_send.start()

    # Espera a thread de envio terminar
    thread_send.join()

    # client vai ser encerrado
    running = False

    # Libera qualquer thread que esteja esperando
    response_event.set()

    # FECHAMENTO DO SOCKET!!!

    try:
        client.shutdown(socket.SHUT_RDWR)

    except OSError:
        pass

    finally:
        client.close()

    # Espera a thread de recebimento terminar
    thread_recv.join()

    print("Cliente encerrado.")

# EXECUÇÃO

if __name__ == "__main__":
    main()