import threading


class InputThread(threading.Thread):
    def __init__(self, socket) -> None:
        super().__init__()
        self.s = socket

    def run(self) -> None:
        while True:
            try:
                user_message = input()
                if user_message.lower() == "quit":
                    print("Closing input thread...")
                    break
                self.s.sendall(user_message.encode("utf-8"))

            except Exception as e:
                print(f"Connection lost or error sending data: {e}")
                break
