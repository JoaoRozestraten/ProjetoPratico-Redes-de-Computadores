import threading


class OutputThread(threading.Thread):
    def __init__(self, socket):
        super().__init__()
        self.s = socket

    def run(self):
        while True:
            data = self.s.recv(1024)
            print(data.decode("utf-8"))
