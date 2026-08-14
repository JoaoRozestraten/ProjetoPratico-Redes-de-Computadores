import threading
import socket


class SenderThread(threading.Thread):
    def __init__(self, conn, addr) -> None:
        super().__init__()
        self.conn = conn

    def run(self):
        pass
