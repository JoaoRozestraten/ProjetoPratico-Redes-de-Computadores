def thread_receber(client, state):
    running = state["running"]
    response_event = state["response_event"]

    while running[0]:

        try:
            data = client.recv(4096)#TAMANHO MAX 

            # Servidor fechou a conexão
            if not data:
                print("\nServidor desconectou.")
                running[0] = False
                response_event.set()
                break

            mensagem = data.decode()

            print("\n-----------------------------")
            print(mensagem)
            print("-----------------------------")

            # Libera a thread de envio
            # para fazer uma nova requisição
            response_event.set()

            # Verifica se o servidor está encerrando
            if "encerrando servidor" in mensagem.lower():
                running[0] = False
                break

        except (
            ConnectionResetError,
            ConnectionAbortedError,
            OSError
        ):
            running[0] = False
            response_event.set()
            break

    print("Thread de recebimento encerrada.")