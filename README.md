# ProjetoPratico-Redes-de-Computadores
Projeto Pratico 1 - Redes de Computadores

Monitor do sistema
O monitor do sistema deverá implementar um cliente que possa monitorar a performance do sistema operacional
remoto (do servidor) remotamente: utilização de CPU e memória.
O usuário, através do cliente da aplicação, iniciará a conexão ao servidor, e receberá, de imediato, uma mensagem
no seguinte formato “<HORARIO>: CONECTADO!!” e um Menu com os monitores disponíveis e sintaxe de uso (no
diagrama, MSG1).
Duas threads então serão criadas, tanto no server quanto no cliente, para manipulação da conexão através do
handle que identifica a conexão.
No cliente, a thread 1 receberá via teclado o comando do usuário, por exemplo, “CPU-5<ENTER>”, e enviará este
texto ao server pela conexão. O server receberá esta mensagem pela conexão na thread 1 do diagrama, que é
responsável por um loop de leitura do socket, dará início a uma thread que executará o monitor solicitado com a
periodicidade solicitada, e retornará o output periodicamente através de uma thread similar à 2 do diagrama, em
loop infinito até que o usuário mande este monitor ser interrompido (o que terminará a thread do monitor, seja
enviando uma mensagem ou através de uma flag em memória compartilhada – use a criatividade). O usuário poderá
ainda solicitar outros monitores, que seguirão o mesmo processo com criação de threads secundárias para cada um,
como descrito no exemplo acima.
O cliente, em sua thread 2 em loop infinito recebe dados da conexão e imprime na tela.
Comandos a serem implementados (e interpretados pelo server) devem ser, no mínimo:
- CPU
- memoria
- Quit (termina thread de monitoração remota)
- Exit (termina todas as threads e sai).
