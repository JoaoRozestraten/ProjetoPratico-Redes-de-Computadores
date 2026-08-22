import threading


class SenderThread(threading.Thread):
    def __init__(self, client, running: list, response_event: threading.Event) -> None:
        super().__init__()
        self.client = client
        self.running = running
        self.response_event = response_event

    def run(self) -> None:
        while self.running[0]:

            # Garante que o evento esteja desligado
            self.response_event.clear()

            try:
                comando = input("\nComando: ").strip()

            # Não entra em deadlock
            except EOFError:
                self.running[0] = False
                self.response_event.set()  # Libera a thread
                break

            # Verifica se o cliente ainda está executando
            if not self.running[0]:
                break

            # Ignora comandos vazios
            if not comando:
                continue

            # Envia o comando para o servidor
            try:
                self.client.sendall(comando.encode())

            except (BrokenPipeError, ConnectionResetError, OSError):
                print("Erro ao enviar comando.")
                self.running[0] = False
                self.response_event.set()
                break

            # Exit
            if comando.upper() == "EXIT":
                print("Aguardando resposta do servidor...")

                # Espera o servidor confirmar o final
                self.response_event.wait()

                self.running[0] = False
                break

            # Para os demais comandos
            print("Aguardando resposta do servidor...")

            # A thread fica bloqueada até a thread de
            # recebimento receber uma resposta
            self.response_event.wait()

        print("Thread de envio encerrada.")
