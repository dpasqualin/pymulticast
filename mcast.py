#!/usr/bin/env python

import socket,time,threading,os,signal

def waitrequest(*args):
    """ Executa funcao "handle" para cada mensagem recebida.
        Funcao executada em uma thread separada """

    obj, handle = args[0], args[1]
    obj.setThreadPID(os.getpid())
    while not obj.shouldQuit():
        try:
            handle(obj.read())
        except socket.error:
            pass
        time.sleep(0.01)

class McastParams(object):
    """ Esta classe armazena e retorna alguns parametros e funcoes comuns ao
    cliente e servidor multicast. O objetivo principal eh evitar redundancia
    de codigo """
    def __init__(self,port,addr,sbound="0.0.0.0",sport=None, ttl=1):

        self.__port = port
        self.__addr = addr
        self.__serverbound = sbound
        self.__serverport = sport or port-1
        self.__ttl = ttl

        self.__quit = False

    def quit(self):
        """ Mata threads, se existirem """
        if self.getThread():
            os.kill(self.getThreadPID(),signal.SIGKILL)
            self.closeSocket()

    def shouldQuit(self):
        return self.__quit

    def closeSocket(self):
        self.getSocket().close()

    def getSocket(self):
        return self.__socket

    def getTTL(self):
        return self.__ttl

    def getPort(self):
        return self.__port

    def getAddr(self):
        return self.__addr

    def getServerBound(self):
        return self.__serverbound

    def getServerPort(self):
        return self.__serverport

    def setThreadPID(self,pid):
        self.__threadPID = pid

    def getThreadPID(self):
        return self.__threadPID

    def read(self):
        return self.getSocket().recvfrom(1024)

    def send(self, msg):
        pass

#########################################################################
##### Multicast Server ##################################################
class McastServer(McastParams):
    """ Abre uma conexao multicast.
            port: Porta multicast
            addr: Endereco de multicast
            sbound: Endereco do servidor
            sport: Porta do servidor
            ttl: TTL
    """
    def __init__(self,port,addr,sbound="0.0.0.0",sport=None,
                 ttl=1, handle=None):
        McastParams.__init__(self,port,addr,sbound,sport,ttl)
        self.__socket = self.__connect()

        # Cria thread para receber mensagens
        if handle:
            self.__t = threading.Thread(target=waitrequest,
                                        args=(self,handle))
            self.__t.start()

    def __connect(self):
        """ Abre conexao  """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                             socket.IPPROTO_UDP)
        #The sender is bound on (serverbound:serverport)
        sock.bind((self.getServerBound(),self.getServerPort()))

        # Tell the kernel that we want to multicast and that the data is
        # sent to everyone (255 is the level of multicasting)
        ttl = self.getTTL()
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL,ttl)

        return sock

    def send(self, msg):
        """ Envia mensagem msg ao multicast """
        mcastaddr,mcastport = self.getAddr(), self.getPort()
        self.getSocket().sendto(msg, (mcastaddr,mcastport));

    def getSocket(self):
        return self.__socket

    def getThread(self):
        return self.__t

################################################################
################################################################

class McastClient(McastParams):
    """ Abre uma conexao multicast.
            port: Porta multicast
            addr: Endereco de multicast
            sbound: Endereco do servidor
            sport: Porta do servidor
            ttl: TTL
    """

    def __init__(self,port,addr,sbound="0.0.0.0",sport=None,
                 ttl=1,handle=None):
        McastParams.__init__(self,port,addr,sbound,sport,ttl)
        self.__socket = self.__connect()

        # Cria thread para receber mensagens
        if handle:
            self.__t = threading.Thread(target=waitrequest,
                                        args=(self,handle))
            self.__t.start()

    def __connect(self):

        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                             socket.IPPROTO_UDP)
        # Allow multiple sockets to use the same PORT number
        ttl = self.getTTL()
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,ttl)

        # Bind to the port that we know will read multicast data
        sbound,sport = self.getServerBound(),self.getPort()
        sock.bind((sbound,sport))

        # Tell the kernel that we are a multicast socket
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        # Tell the kernel that we want to add ourselves to a multicast group
        # The address for the multicast group is the third param
        mcastaddr = self.getAddr()
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                        socket.inet_aton(self.getAddr())+
                        socket.inet_aton(self.getServerBound()))

        sock.setblocking(0)

        return sock

    def getSocket(self):
        return self.__socket

    def getThread(self):
        return self.__t


###########################################################################
### Se executado diretamente via shell
if __name__ == "__main__":

    import sys

    ANY = "0.0.0.0"
    SENDERPORT=1501
    MCAST_ADDR = "224.168.2.9"
    MCAST_PORT = 1600
    TTL=1 # Nao sera repassado a nenhum router

    # Guarda a variavel usada para criar o multicast. Ser util para
    # fecha-lo quando um CTRL+C for detectado
    mcast = None

    def clienthandle(msg):
        data,addr = msg
        print "We got data!"
        print "FROM: ", addr
        print "DATA: ", data

    def runclient():
        """ Executa em modo client """
        global mcast
        mcast = McastClient(MCAST_PORT,MCAST_ADDR,
                                   handle=clienthandle)

    def runserver():
        """ Executa em modo servidor """
        global mcast
        mcast = McastServer(MCAST_PORT,MCAST_ADDR)

        while 1:
            #send the data "hello, world" to the multicast addr: port
            mcast.send("Hello World")
            time.sleep(5)

    # Configuracao das funcoes
    prog = { "client": runclient, "server" : runserver }

    if len(sys.argv) == 2 and sys.argv[1] in prog:
        try:
            print "Abrindo",sys.argv[1]
            prog[sys.argv[1]]()
            raw_input("ctrl+c para sair...")
        except:
            print "Saindo"
            mcast.quit()
            sys.exit(0)
    else:
        print "%s: server/client" % sys.argv[0]
        sys.exit(0)
