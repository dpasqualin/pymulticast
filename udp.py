#!/usr/bin/env python

from socket import *

class UDPParams(object):

    def __init__(self,host,port):
        self.__socket = socket(AF_INET,SOCK_DGRAM)
        self.__host = host
        self.__port = int(port)
        self.__addr = (self.getHost(),self.getPort())

    def send(self, msg):
        self.getSocket().sendto(msg,self.getAddr())

    def read(self):
        return self.getSocket().recvfrom(1024)

    def getSocket(self):
        return self.__socket

    def getPort(self):
        return self.__port

    def getHost(self):
        return self.__host

    def getAddr(self):
        return self.__addr

class UDPServer(UDPParams):

    def __init__(self,host,port):
        UDPParams.__init__(self,host,port)
        self.__connect()

    def __connect(self):
        print "sou server"
        self.getSocket().bind(self.getAddr())

class UDPClient(UDPParams):
    pass
