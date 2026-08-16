def thread_enviar(client, state):
    running = state["running"]
    response_event = state["response_event"]

    while running[0]:

        # Garante que o evento esteja desligado
        response_event.clear()

        try:
            comando = input("\nComando: ").strip()

        except EOFError:  # NÃO ENTRAR EM DEADLOCK
            running[0] = False
            response_event.set()  # Libera a thread
            break

        # Verifica se o cliente ainda está executando
        if not running[0]:
            break

        # Ignora comandos vazios
        if not comando:
            continue

        # Envia o comando para o servidor
        try:
            client.sendall(comando.encode())

        except (BrokenPipeError, ConnectionResetError, OSError):
            print("Erro ao enviar comando.")
            running[0] = False
            response_event.set()
            break

        # EXIT
        if comando.upper() == "EXIT":
            print("Aguardando resposta do servidor...")

            # Espera o servidor confirmar o final
            response_event.wait()

            running[0] = False
            break

        # OUTROS COMANDOS

        print("Aguardando resposta do servidor...")

        # A thread fica bloqueada até a thread de
        # recebimento receber uma resposta
        response_event.wait()

    print("Thread de envio encerrada.")