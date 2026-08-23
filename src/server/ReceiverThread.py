# DANIEL: Com a nova atualização beta do macOS, o pip3 está quebrado, inviabilizando a instalação
# direta do psutil. Tive que instalar uma versão anterior do Python, instalar a
# biblioteca (psutil) e utilizar o import de annotations para conseguir usar
# implementações mais modernas (futuras). Não precisam comentar a linha 6, ela não causa nenhum
# efeito colateral para versões mais recentes (estou usando a 3.9.6).
from __future__ import annotations

import threading
from queue import Queue

from CommandsAndTools import CommandsAndTools
from Monitor import Monitor


class ReceiverThread(threading.Thread):
    def __init__(
        self,
        conn,
        addr,
        message_q: Queue,
        exit_flag: threading.Event,
        shutdown_flag: threading.Event,
    ) -> None:
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.message_q = message_q
        self.exit_flag = exit_flag
        self.shutdown_flag = shutdown_flag
        self.tools = CommandsAndTools()
        self.monitors: dict[str, tuple[Monitor, threading.Event]] = {}

    def _log(self, mensagem: str) -> None:
        print(f"{self.tools.horario()}, {self.addr[0]}: {mensagem}")

    def parse_command(self, data: bytes) -> tuple[str | None, str | None]:
        decoded_str = data.decode("utf-8").strip()
        if not decoded_str:
            return None, None

        if "-" not in decoded_str:
            return decoded_str.lower(), None

        parts = decoded_str.split("-")
        if len(parts) != 2:
            self._log(f"Formato de comando inválido: {decoded_str}")
            return None, None

        return parts[0].strip().lower(), parts[1].strip().lower()

    def _parar_monitor(self, nome: str) -> bool:
        alvo = self.monitors.pop(nome, None)
        if alvo is None:
            return False
        monitor, quit_flag = alvo
        quit_flag.set()
        monitor.join()
        return True

    def _parar_todos_monitores(self) -> None:
        for nome in list(self.monitors):
            self._parar_monitor(nome)

    def run(self) -> None:
        print(f"{self.tools.horario()}: Conectado com {self.addr}")
        self.message_q.put(self.tools.boas_vindas())

        while not self.exit_flag.is_set():
            data = self.conn.recv(1024)
            if not data:
                print(f"{self.tools.horario()}: Desconectou {self.addr}")
                self._parar_todos_monitores()
                self.exit_flag.set()
                break

            nome, arg = self.parse_command(data)
            if not nome:
                continue

            if nome == "help":
                self._log("Help solicitado")
                self.message_q.put(self.tools.ajuda())
                continue

            if nome == "quit":
                if arg == "all":
                    self._log("Parendo todos os monitor")
                    self._parar_todos_monitores()
                elif arg and self._parar_monitor(arg):
                    self._log(f"Parendo o monitor {arg}")
                else:
                    self._log(f"Nenhum monitor '{arg}' ativo")
                    self.message_q.put(f"Nenhum monitor '{arg}' ativo.\n".encode("utf-8"))
                continue

            if nome == "exit":
                self._log("Exit solicitado")
                self._parar_todos_monitores()
                print(f"{self.tools.horario()}: Desconectou {self.addr}")
                self.exit_flag.set()
                break

            if nome == "shutdown":
                self._log("Shutdown solicitado")
                self._parar_todos_monitores()
                self.message_q.put(b"Servidor encerrando servidor...\n")
                print(f"{self.tools.horario()}: Desconectou {self.addr}")
                self.shutdown_flag.set()
                self.exit_flag.set()
                break

            func = self.tools.obter(nome)
            if not func or arg is None:
                self._log(f"{nome} é inválido")
                self.message_q.put(f"Comando invalido: {nome}\n".encode("utf-8"))
                continue

            try:
                periodo = float(arg)
            except ValueError:
                self._log(f"Formatação inválida de comando: {nome}-{arg}")
                self.message_q.put(f"Comando invalido: {nome}-{arg}\n".encode("utf-8"))
                continue

            if periodo == 0:
                try:
                    self.message_q.put(func())
                except Exception as e:
                    print(f"{e}")
                continue

            try:
                self._parar_monitor(nome)
                quit_flag = threading.Event()
                monitor = Monitor(nome, periodo, func, self.message_q, quit_flag)
                self.monitors[nome] = (monitor, quit_flag)
                monitor.start()
                self._log(f"Iniciando o monitor {nome} a cada {periodo}s")
            except Exception as e:
                print(f"{e}")
