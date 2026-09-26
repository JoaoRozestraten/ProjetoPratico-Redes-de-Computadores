import socket
import sys
import threading
from ClientHandler import ClientHandler

HOST = "127.0.0.1"
PORT = 65432


if __name__ == "__main__":
    print("Monitor do Sistema 1.0 (Server-side)")
    print("Feito por Daniel Picconi, João Rozestraten e Rodrigo Seiji\n")

    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) < 1:
        print("Uso: python3 main.py <max_clientes>")
        sys.exit(1)
    limite = int(sys.argv[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    # Timeout pro accept() nao bloquear pra sempre e a linha principal conseguir ver o SHUTDOWN
    s.settimeout(1.0)
    print(f"Server está escutando em ", HOST, "port", PORT)
    print(f"Limite de clientes simultâneos: {limite}")

    # Memoria compartilhada: handlers dos clientes conectados
    clientes = []
    lock = threading.Lock()
    shutdown_flag = threading.Event()

    while not shutdown_flag.is_set():
        try:
            conn, addr = s.accept()
        except socket.timeout:
            continue

        ClientHandler(conn, addr, clientes, lock, limite, shutdown_flag).start()

    with lock:
        ativos = list(clientes)
        for handler in ativos:
            handler.encerrar()

    for handler in ativos:
        handler.join()

    s.close()
    print(f"Servidor encerrado por comando SHUTDOWN.")
