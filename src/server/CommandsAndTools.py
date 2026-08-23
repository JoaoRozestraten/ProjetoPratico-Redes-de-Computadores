from __future__ import annotations

import time
from datetime import timedelta
from typing import Callable

import psutil


class CommandsAndTools:
    DESCRICOES = {
        "cpu": "uso da CPU",
        "temp": "temperatura da CPU",
        "memoria": "uso de memoria",
        "disco": "uso de disco",
        "uptime": "tempo ligado",
        "rede": "download/upload",
        "bateria": "nivel de bateria",
        "nucleos": "uso de CPU por nucleo",
        "iodisco": "leitura/escrita de disco",
    }

    def __init__(self) -> None:
        self.comandos: dict[str, Callable[[], bytes]] = {
            "cpu": self.cpu,
            "temp": self.temperatura,
            "memoria": self.memoria,
            "disco": self.disco,
            "uptime": self.uptime,
            "rede": self.rede,
            "bateria": self.bateria,
            "nucleos": self.nucleos,
            "iodisco": self.iodisco,
        }

    def obter(self, nome: str) -> Callable[[], bytes] | None:
        return self.comandos.get(nome)

    @staticmethod
    def horario() -> str:
        return time.strftime("%H:%M:%S")

    def _menu(self) -> list[str]:
        linhas = [
            "Monitores disponiveis nesse servidor",
            "(sintaxe: <COMANDO>-<intervalo_em_segundos>):",
        ]
        linhas += [
            f"  {nome.upper()}-<segundos>  - {self.DESCRICOES[nome]}" for nome in self.comandos
        ]
        linhas += [
            "",
            "Comandos de controle:",
            "  QUIT-ALL       - para todos os monitores ativos",
            "  QUIT-<COMANDO> - para um monitor especifico",
            "  EXIT           - encerra a conexao",
            "  SHUTDOWN       - encerra o servidor inteiro",
            "  HELP           - mostra este menu novamente",
        ]
        return linhas

    def boas_vindas(self) -> bytes:
        linhas = [f"{self.horario()}: CONECTADO!!", ""] + self._menu()
        return ("\n".join(linhas) + "\n").encode("utf-8")

    def ajuda(self) -> bytes:
        return ("\n".join(self._menu()) + "\n").encode("utf-8")

    @staticmethod
    def _formatar_bytes(valor: float) -> str:
        for unidade in ("B", "KB", "MB", "GB", "TB"):
            if valor < 1024:
                return f"{valor:.2f} {unidade}"
            valor /= 1024
        return f"{valor:.2f} PB"

    def cpu(self) -> bytes:
        uso = psutil.cpu_percent(interval=1)
        return f"CPU: {uso:.1f}%\n".encode("utf-8")

    def temperatura(self) -> bytes:
        sensores = getattr(psutil, "sensors_temperatures", None)
        if sensores is None:
            return b"Temperatura da CPU: nao disponivel neste sistema.\n"

        for leituras in sensores().values():
            if leituras:
                return f"Temperatura da CPU: {leituras[0].current:.1f}C\n".encode("utf-8")

        return b"Temperatura da CPU: nao disponivel neste sistema.\n"

    def memoria(self) -> bytes:
        mem = psutil.virtual_memory()
        return (
            f"Memoria: {self._formatar_bytes(mem.used)} / "
            f"{self._formatar_bytes(mem.total)} ({mem.percent:.1f}%)\n"
        ).encode("utf-8")

    def disco(self) -> bytes:
        uso = psutil.disk_usage("/")
        return (
            f"Disco: {self._formatar_bytes(uso.used)} / "
            f"{self._formatar_bytes(uso.total)} ({uso.percent:.1f}%)\n"
        ).encode("utf-8")

    def uptime(self) -> bytes:
        segundos = time.time() - psutil.boot_time()
        return f"Uptime: {timedelta(seconds=int(segundos))}\n".encode("utf-8")

    def rede(self) -> bytes:
        antes = psutil.net_io_counters()
        time.sleep(1)
        depois = psutil.net_io_counters()

        download = depois.bytes_recv - antes.bytes_recv
        upload = depois.bytes_sent - antes.bytes_sent

        return (
            f"Download: {self._formatar_bytes(download)}/s | "
            f"Upload: {self._formatar_bytes(upload)}/s\n"
        ).encode("utf-8")

    def bateria(self) -> bytes:
        bateria = psutil.sensors_battery()
        if bateria is None:
            return b"Bateria: nao disponivel neste sistema.\n"

        status = "carregando" if bateria.power_plugged else "descarregando"
        return f"Bateria: {bateria.percent:.1f}% ({status})\n".encode("utf-8")

    def nucleos(self) -> bytes:
        usos = psutil.cpu_percent(interval=1, percpu=True)
        linha = " | ".join(f"core{i}: {uso:.1f}%" for i, uso in enumerate(usos))
        return f"CPU por nucleo: {linha}\n".encode("utf-8")

    def iodisco(self) -> bytes:
        antes = psutil.disk_io_counters()
        time.sleep(1)
        depois = psutil.disk_io_counters()

        leitura = depois.read_bytes - antes.read_bytes
        escrita = depois.write_bytes - antes.write_bytes

        return (
            f"Disco I/O: Leitura {self._formatar_bytes(leitura)}/s | "
            f"Escrita {self._formatar_bytes(escrita)}/s\n"
        ).encode("utf-8")
