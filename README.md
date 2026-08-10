# Projeto-Pratico---Redes-de-Computadores
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
Chat Multiusuário
O chat multiusuário implementará uma sala de bate-papo onde vários usuários poderão se comunicar enviando
mensagens públicas a todos os usuários. Nesta primeira atividade, teremos somente um usuário, portanto, o que ele
enviar
O usuário, através do cliente da aplicação, iniciará a conexão ao servidor, e receberá, de imediato, uma mensagem
no seguinte formato “<HORARIO>: CONECTADO!!” (no diagrama, MSG1).
Duas threads então serão criadas, tanto no server quanto no cliente, para manipulação da conexão através do
handle que identifica a conexão.
Disciplina: Redes de Computadores
Curso: Eng.Computação
Atividade: Projeto Prático 1
O server, através da thread 2, enviará ao cliente, a cada minuto, a data e horário, independente do chat estar em idle
ou de usuários estarem falando pelo canal. O cliente, por sua vez, receberá esta informação através de sua thread 2,
e imprimirá na tela a informação.
O cliente, por sua thread 1, ficará esperando o usuário digitar comandos, que poderão ser:
MENSAGEM A SER ENVIADA
:nome <NOME> -> Usado para mudar o nome do usuário
:quit -> Usado para sair do aplicativo
A thread 1 enviará estes comandos ao servidor, que os receberá pela thread 1 em seu lado.
O servidor, em sua thread 1, receberá estes comandos e os armazenará em uma estrutura de dados em memória
compartilhada, e voltará a esperar novos dados vindo da rede.
A thread 2 do servidor, por sua vez, fará periodicamente a varredura da área de memória compartilhada e executará
a ação solicitada, seja ela definir o nome do usuário, enviar a mensagem a todos, ou desconectar um usuário.
Explicações:
1)caso o texto digitado iniciar com : (dois pontos), será interpretado como comando; caso não inicie com dois pontos,
será uma mensagem a ser enviada a todos os usuários.
2) caso o usuário não defina seu nome, será atribuído automaticamente “seu IP”:”porta do cliente”
3) Na tela dos usuários que recebem a mensagem, ela será formatada como:
NOME_DO_USUARIO (horário): MENSAGEM
4) Para o usuário que enviou a mensagem, ele receberá um eco sendo “Voce digitou: MENSAGEM”.
