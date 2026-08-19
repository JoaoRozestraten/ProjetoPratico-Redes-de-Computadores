import threading
from queue import Queue
from typing import Callable
from monitor.Monitor import Monitor
import time

_REGESTRY: dict[str, Callable] = {
    # "CPU": cpuConsumption,
    # "RAM": ramConsumption,
    # "QUIT":  # deletes all monitors
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

            if "-" in data:
                cmd, periodo = data.decode("utf-8").split("-").upper()
                periodo = int(periodo)
                func = _REGESTRY.get(cmd)
                if func:
                    try:
                        monitor = Monitor(f"{data}", periodo, time.time(), func)
                        self.monitor_q.put(monitor)
                    except Exception as e:
                        print(f"{e}")
                else:
                    print(f"Commando {data} é inválido")
            else:
                print(f"Commando {data} é inválido")
