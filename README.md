# Monitor do Sistema 1.0

Projeto Prático 1 — Redes de Computadores

Feito por **Daniel Picconi**, **João Rozestraten** e **Rodrigo Seiji**.

## O que é

Um monitor remoto de performance de sistema operacional, feito com sockets TCP e threads em Python. O cliente se conecta a um servidor e pede, por comando, para monitorar métricas do sistema onde o servidor está rodando (CPU, memória, disco, rede, bateria etc.), recebendo o resultado periodicamente, em tempo real.

## Requisitos

- Python 3.9 ou superior
- Biblioteca `psutil` (veja `requirements.txt`)

```bash
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Como rodar

**1. Inicie o servidor:**

```bash
cd src/server
python3 main.py
```

**2. Em outro terminal, inicie o cliente:**

```bash
cd src/client
python3 main.py
```

O cliente conecta em `127.0.0.1:65432` por padrão (ajustável em `HOST`/`PORT` no `server/main.py` e `SERVER_IP`/`SERVER_PORT` no `client/main.py`).


## Comandos

Sintaxe: `<COMANDO>-<intervalo_em_segundos>`. Use `0` como intervalo pra rodar o comando uma única vez, sem ficar monitorando.

| Comando | O que faz |
|---|---|
| `CPU` | uso da CPU |
| `TEMP` | temperatura da CPU (se disponível no sistema) |
| `MEMORIA` | uso de memória |
| `DISCO` | uso de disco |
| `UPTIME` | tempo ligado |
| `REDE` | download/upload |
| `BATERIA` | nível de bateria |
| `NUCLEOS` | uso de CPU por núcleo |
| `IODISCO` | leitura/escrita de disco |

Comandos de controle (sem intervalo):

| Comando | O que faz |
|---|---|
| `HELP` | mostra o menu de comandos novamente |
| `QUIT-ALL` | para todos os monitores ativos |
| `QUIT-<COMANDO>` | para um monitor específico (ex: `QUIT-CPU`) |
| `EXIT` | encerra a conexão do cliente atual |
| `SHUTDOWN` | encerra o servidor inteiro |

Vários monitores diferentes podem rodar ao mesmo tempo (ex: `CPU-5` e `MEMORIA-2` simultâneos).

## Arquitetura

## Estrutura do projeto

```
src/
├── client/
│   ├── main.py
│   ├── SenderThread.py
│   └── ReceiverThread.py
└── server/
    ├── main.py
    ├── ReceiverThread.py
    ├── SenderThread.py
    ├── Monitor.py
    └── CommandsAndTools.py
```
