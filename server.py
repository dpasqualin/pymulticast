#!/usr/bin/env python

import socket
import time

ANY = "0.0.0.0"
SENDERPORT=1501
MCAST_ADDR = "224.168.2.9"
MCAST_PORT = 1600
TTL=1 # Nao sera repassado a nenhum router

class McastServer:
    """ Abre uma conexao multicast.
            port: Porta multicast
            addr: Endereco de multicast
            sbound: Endereco do servidor
            sport: Porta do servidor
            ttl: TTL
    """

    def __init__(self,port,addr,sbound="0.0.0.0",sport=None, ttl=1):
        self.__port = port
        self.__addr = addr
        self.__serverbound = sbound
        self.__serverport = sport or port-1
        self.__ttl = ttl
        self.__socket = self.__connect()

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
        self.getSocket().sendto(reply, (mcastaddr,mcastport));

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

if __name__ == "__main__":
    mcast_server = McastServer(MCAST_PORT,MCAST_ADDR)

    while 1:
        #send the data "hello, world" to the multicast addr: port
        mcast_server.send("Hello World")
        time.sleep(5)
