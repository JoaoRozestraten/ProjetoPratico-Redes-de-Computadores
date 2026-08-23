import socket
import threading

from InputThread import InputThread
from OutputThread import OutputThread

SERVER_IP = "127.0.0.1"
SERVER_PORT = 65432


def main():
    print("Monitor do Sistema 1.0 (Client-side)")
    print("Feito por Daniel Picconi, João Rozestraten e Rodrigo Seiji\n")

    # Variável de controle
    # Usamos uma lista para que as threads
    # possam alterar o valor compartilhado
    running = [True]

    # Evento de recebimento de resposta
    response_event = threading.Event()

    # Criação do socket TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conexão com o servidor
    try:
        client.connect((SERVER_IP, SERVER_PORT))

    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor. Verifique o IP e a porta.")

        client.close()
        return

    # Criação das threads

    thread_send = InputThread(client, running, response_event)

    thread_recv = OutputThread(client, running, response_event)

    # Inicia as duas threads
    thread_recv.start()
    thread_send.start()

    # Espera a thread de envio terminar
    thread_send.join()

    # Cliente vai ser encerrado
    running[0] = False

    # Libera qualquer thread que esteja esperando
    response_event.set()

    # Finaliza o socket
    try:
        client.shutdown(socket.SHUT_RDWR)

    except OSError:
        pass

    finally:
        client.close()

    # Espera a thread de recebimento terminar
    thread_recv.join()

    print("Cliente encerrado.")


# Execução
if __name__ == "__main__":
    main()

