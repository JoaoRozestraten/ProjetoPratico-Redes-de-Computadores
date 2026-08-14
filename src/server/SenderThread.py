import threading
import socket
from queue import Queue


class SenderThread(threading.Thread):
    def __init__(self, conn, addr, q) -> None:
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.q = q

    def run(self):
        while True:
            data = self.q.get()
            if data is None:
                break

            self.conn.send(data)
