import threading
from queue import Queue
from typing import Callable
from monitor.Monitor import Monitor


def cpuTeste():
    return b"CPU teste\n"


_REGESTRY: dict[str, Callable] = {
    "CPU": cpuTeste,
    # "RAM": ramConsumption,
}


class ReceiverThread(threading.Thread):
    def __init__(
        self, conn, addr, message_q: Queue, exit_flag: threading.Event
    ) -> None:
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.message_q = message_q
        self.exit_flag = exit_flag
        self.monitors: list[Monitor] = []
        self.quit_flag = threading.Event()

    def parse_command(self, data: bytes) -> tuple[str | None, float | None]:
        decoded_str = data.decode("utf-8").strip()
        if not decoded_str:
            return None, None

        if "-" in decoded_str:
            parts = decoded_str.split("-")
            if len(parts) == 2:
                cmd = parts[0].strip().upper()
                period = float(parts[1].strip())
                return cmd, period
            else:
                print(f"Invalid command format: {decoded_str}")
                return None, None
        else:
            cmd = decoded_str.upper()
            return cmd, None

    def run(self):
        print(f"Connected to {self.addr}")
        while not self.exit_flag.is_set():
            data = self.conn.recv(1024)
            if not data:
                print(f"Disconnected from {self.addr}")
                break

            cmd, periodo = self.parse_command(data)

            if cmd:
                if cmd == "QUIT":
                    print("stoping all monitors")
                    self.quit_flag.set()
                    for monitor in self.monitors:
                        monitor.join()

                    self.quit_flag.clear()
                    self.monitors.clear()

                    continue

                if cmd == "EXIT":
                    self.quit_flag.set()
                    for monitor in self.monitors:
                        monitor.join()
                    self.exit_flag.set()
                    break

                func = _REGESTRY.get(cmd)
                if func and periodo is not None:
                    try:
                        monitor = Monitor(
                            cmd, periodo, func, self.message_q, self.quit_flag
                        )
                        self.monitors.append(monitor)
                        monitor.start()
                        print(f"Started monitoring {cmd} every {periodo}s")
                    except Exception as e:
                        print(f"{e}")
                else:
                    print(f"{cmd} é inválido")
