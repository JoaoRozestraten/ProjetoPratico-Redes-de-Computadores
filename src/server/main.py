from queue import Queue
import threading
import socket
from ReceiverThread import ReceiverThread
from SenderThread import SenderThread

HOST = "127.0.0.1"
PORT = 65430

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    message_q = Queue()
    exit_flag = threading.Event()

    thread_1 = ReceiverThread(conn, addr, message_q, exit_flag)
    thread_2 = SenderThread(conn, message_q, exit_flag)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()
