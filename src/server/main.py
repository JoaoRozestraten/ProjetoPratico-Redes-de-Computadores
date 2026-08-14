import socket
import threading
from ReceiverThread import ReceiverThread
from SenderThread import SenderThread

HOST = "127.0.0.1"
PORT = 65432

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    thread_1 = ReceiverThread(conn, addr)
    thread_2 = SenderThread(conn, addr)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()
