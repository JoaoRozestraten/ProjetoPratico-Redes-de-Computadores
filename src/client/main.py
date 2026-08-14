import socket
import threading
from InputThread import InputThread
from OutputThread import OutputThread

HOST = "127.0.0.1"
PORT = 65432

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

    print(f"Received {data!r}")

    thread_1 = InputThread(s)
    thread_2 = OutputThread(s)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()
