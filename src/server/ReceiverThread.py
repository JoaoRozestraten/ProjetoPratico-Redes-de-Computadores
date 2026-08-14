import threading
import socket


class ReceiverThread(threading.Thread):
    def __init__(self, conn, addr, q) -> None:
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.q = q

    def run(self):
        print(f"Connected to {self.addr}")
        while True:
            data = self.conn.recv(1024)
            if not data:
                print("Disconnected")
                self.q.put(None)
                break

            print(data.decode("utf-8"))
            self.q.put(data)
