import socket
import threading
from ReceiverThread import ReceiverThread
from SenderThread import SenderThread
from queue import Queue

HOST = "127.0.0.1"
PORT = 65432

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    with conn:
        q = Queue()  # fila compartilhada

        thread_1 = ReceiverThread(conn, addr, q)
        thread_2 = SenderThread(conn, addr, q)

        thread_1.start()
        thread_2.start()

        thread_1.join()
        thread_2.join()
