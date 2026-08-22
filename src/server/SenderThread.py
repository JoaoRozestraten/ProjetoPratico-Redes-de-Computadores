from queue import Empty, Queue
import threading


class SenderThread(threading.Thread):
    def __init__(self, conn, message_q: Queue, exit_flag: threading.Event) -> None:
        super().__init__()
        self.conn = conn
        self.message_q = message_q
        self.exit_flag = exit_flag

    def run(self):
        while not self.exit_flag.is_set():
            try:
                message = self.message_q.get(timeout=0.5)
                self.conn.send(message)
            except Empty:
                continue
            except (ConnectionError, BrokenPipeError):
                self.exit_flag.set()
                break
