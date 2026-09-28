from __future__ import annotations

import threading
from queue import Queue

from CommandsAndTools import CommandsAndTools
from ReceiverThread import ReceiverThread
from SenderThread import SenderThread


class ClientHandler(threading.Thread):
    def __init__(
        self,
        conn,
        addr,
        clientes: list,
        lock: threading.Lock,
        limite: int,
        shutdown_flag: threading.Event,
    ) -> None:
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.clientes = clientes
        self.lock = lock
        self.limite = limite
        self.shutdown_flag = shutdown_flag
        self.message_q = Queue()
        self.exit_flag = threading.Event()

    def _registrar(self) -> str | None:
        # Checa e ocupa a vaga dentro do mesmo lock pra dois clientes nao pegarem a ultima vaga juntos
        with self.lock:
            if self.shutdown_flag.is_set():
                return "Servidor encerrando servidor...\n"
            if len(self.clientes) >= self.limite:
                return (
                    f"{CommandsAndTools.horario()}: LIMITE DE {self.limite} CLIENTES ATINGIDO, "
                    "tente novamente mais tarde.\n"
                )
            self.clientes.append(self)
            return None

    def _liberar(self) -> int:
        with self.lock:
            self.clientes.remove(self)
            return len(self.clientes)

    def encerrar(self) -> None:
        # Chamado pela linha principal no SHUTDOWN
        if not self.exit_flag.is_set():
            self.message_q.put(b"Servidor encerrando servidor...\n")
            self.exit_flag.set()

    def run(self) -> None:
        recusa = self._registrar()
        if recusa:
            print(f"{CommandsAndTools.horario()}: Recusado {self.addr}, limite de {self.limite} clientes")
            try:
                self.conn.sendall(recusa.encode("utf-8"))
            except OSError:
                pass
            self.conn.close()
            return

        print(f"{CommandsAndTools.horario()}: Vagas ocupadas {len(self.clientes)}/{self.limite}")

        thread_1 = ReceiverThread(self.conn, self.addr, self.message_q, self.exit_flag, self.shutdown_flag)
        thread_2 = SenderThread(self.conn, self.message_q, self.exit_flag)

        thread_1.start()
        thread_2.start()

        thread_1.join()
        thread_2.join()

        self.conn.close()

        ocupadas = self._liberar()
        print(f"{CommandsAndTools.horario()}: Vaga liberada, ocupadas {ocupadas}/{self.limite}")
