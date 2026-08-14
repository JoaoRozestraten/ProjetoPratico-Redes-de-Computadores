import threading
import socket


class ReceiverThread(threading.Thread):
    def __init__(self, conn, addr, shared_q) -> None:
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.shared_q = shared_q

    def run(self):
        with self.conn:
            print(f"Connected to {self.addr}")
            while True:
                self.data = self.conn.recv(1024)
                if not self.data:
                    print(f"Disconnected from {self.addr}")
                    break

                self.conn.sendall(self.data)
