import threading


class OutputThread(threading.Thread):
    def __init__(self, socket):
        super().__init__()
        self.s = socket

    def run(self):
        pass
