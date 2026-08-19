import threading
from queue import Queue
from typing import Callable
from monitor.Monitor import Monitor
import time

_REGESTRY: dict[str, Callable] = {
    # "CPU": cpuConsumption,
    # "RAM": ramConsumption,
    # "EXIT":  # deletes a monitor
}


class ReceiverThread(threading.Thread):
    def __init__(self, conn, addr, monitor_q: Queue) -> None:
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.monitor_q = monitor_q

    def run(self):
        print(f"Connected to {self.addr}")
        while True:
            data = self.conn.recv(1024)
            if not data:
                print(f"Disconnected from {self.addr}")
                break
