import socket
import threading

from InputThread import InputThread
from OutputThread import OutputThread


SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000


def main():

    # Variável de controle
    # Usamos uma lista para que as threads
    # possam alterar o valor compartilhado
    running = [True]

    # Evento de recebimento de resposta
    response_event = threading.Event()

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

    thread_send = InputThread(
        client,
        running,
        response_event
    )

    thread_recv = OutputThread(
        client,
        running,
        response_event
    )

    # Inicia as duas threads
    thread_recv.start()
    thread_send.start()

    # Espera a thread de envio terminar
    thread_send.join()

    # Cliente vai ser encerrado
    running[0] = False

    # Libera qualquer thread que esteja esperando
    response_event.set()

    # FECHAMENTO DO SOCKET

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