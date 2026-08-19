from queue import Queue
import threading
from server.monitor.Monitor import Monitor
import time


class SenderThread(threading.Thread):
    def __init__(self, conn, monitor_q: Queue[Monitor]) -> None:
        super().__init__()
        self.conn = conn
        self.monitor_q = monitor_q

    def run(self):
        while True:
            curr = self.monitor_q.get()
            tempo = time.time()

            if curr.state == "PRONTO":
                message = curr.callback()
                curr.next_time = tempo + curr.period
                self.conn.send(message)
                curr.state = "ESPERA"
            if curr.state == "ESPERA":
                if curr.next_time <= tempo:
                    curr.state = "PRONTO"
            if curr.state != "QUIT":
                self.monitor_q.put(curr)
