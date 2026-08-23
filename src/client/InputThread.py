import threading


class InputThread(threading.Thread):

    def __init__(self, socket, running, response_event) -> None:
        super().__init__()

        self.s = socket
        self.running = running
        self.response_event = response_event

    def run(self) -> None:

        while self.running[0]:

            # Garante que o evento esteja desligado
            self.response_event.clear()

            try:
                comando = input("\nComando: ").strip()

            except EOFError:  # NÃO ENTRAR EM DEADLOCK
                self.running[0] = False

                # Libera a thread
                self.response_event.set()

                break

            # Verifica se o cliente ainda está executando
            if not self.running[0]:
                break

            # Ignora comandos vazios
            if not comando:
                continue

            # Envia o comando para o servidor
            try:
                self.s.sendall(comando.encode())

            except (BrokenPipeError, ConnectionResetError, OSError):
                print("Erro ao enviar comando.")

                self.running[0] = False
                self.response_event.set()

                break

            # EXIT

            if comando.upper() == "EXIT":

                print("Aguardando resposta do servidor...")

                # Espera o servidor confirmar o final
                self.response_event.wait()

                self.running[0] = False

                break

            # OUTROS COMANDOS

            print("Aguardando resposta do servidor...")

            # A thread fica bloqueada até a thread de
            # recebimento receber uma resposta
            self.response_event.wait()

        print("Thread de envio encerrada.")