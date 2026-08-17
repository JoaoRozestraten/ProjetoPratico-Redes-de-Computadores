import threading


class OutputThread(threading.Thread):

    def __init__(self, socket, running, response_event):
        super().__init__()

        self.s = socket
        self.running = running
        self.response_event = response_event

    def run(self) -> None:

        while self.running[0]:

            try:
                data = self.s.recv(4096)  # TAMANHO MAX

                # Servidor fechou a conexão
                if not data:
                    print("\nServidor desconectou.")

                    self.running[0] = False
                    self.response_event.set()

                    break

                mensagem = data.decode()

                print("\n-----------------------------")
                print(mensagem)
                print("-----------------------------")

                # Libera a thread de envio
                # para fazer uma nova requisição
                self.response_event.set()

                # Verifica se o servidor está encerrando
                if "encerrando servidor" in mensagem.lower():
                    self.running[0] = False

                    break

            except (
                ConnectionResetError,
                ConnectionAbortedError,
                OSError
            ):
                self.running[0] = False
                self.response_event.set()

                break

        print("Thread de recebimento encerrada.")