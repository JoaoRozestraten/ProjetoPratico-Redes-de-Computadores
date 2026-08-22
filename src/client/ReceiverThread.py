import threading


class ReceiverThread(threading.Thread):
    def __init__(self, client, running: list, response_event: threading.Event) -> None:
        super().__init__()
        self.client = client
        self.running = running
        self.response_event = response_event

    def run(self) -> None:
        while self.running[0]:

            try:
                # Tamanho máximo
                data = self.client.recv(4096)

                # Servidor fechou a conexão
                if not data:
                    print("\nServidor desconectou.")
                    self.running[0] = False
                    self.response_event.set()
                    break

                mensagem = data.decode()

                print("\n" + mensagem)

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
