import socket
import threading
from queue import Queue
from ReceiverThread import ReceiverThread
from SenderThread import SenderThread


HOST = "127.0.0.1"
PORT = 65432


if __name__ == "__main__":
    print("Monitor do Sistema 1.0 (Server-side)")
    print("Feito por Daniel Picconi, João Rozestraten e Rodrigo Seiji\n")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server está escutando em ", HOST, "port", PORT)

    shutdown_flag = threading.Event()

    while True:
        conn, addr = s.accept()

        message_q = Queue()
        exit_flag = threading.Event()

        thread_1 = ReceiverThread(conn, addr, message_q, exit_flag, shutdown_flag)
        thread_2 = SenderThread(conn, message_q, exit_flag)

        thread_1.start()
        thread_2.start()

        thread_1.join()
        thread_2.join()

        conn.close()

        if shutdown_flag.is_set():
            print(f"Servidor encerrado por comando SHUTDOWN.")
            break

    s.close()
