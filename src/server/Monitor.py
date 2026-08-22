from queue import Queue
import threading
from typing import Callable
import time


class Monitor(threading.Thread):
    def __init__(
        self,
        cmd: str,
        period: float,
        callback: Callable,
        message_q: Queue,
        quit_flag: threading.Event,
    ) -> None:
        super().__init__()
        self.cmd = cmd
        self.period = period
        self.callback = callback
        self.message_q = message_q
        self.quit_flag = quit_flag

    def run(self) -> None:
        while not self.quit_flag.is_set():
            self.message_q.put(self.callback())
            if self.quit_flag.wait(timeout=self.period):
                break
