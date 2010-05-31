#!/usr/bin/env python

from socket import *

UDP_CLIENT_TIMEOUT=10.0

class UDPParams(object):

    def __init__(self,host,port):
        self.__socket = socket(AF_INET,SOCK_DGRAM)
        self.__host = host
        self.__port = int(port)
        self.__addr = (self.getHost(),self.getPort())

    def send(self, msg):
        self.getSocket().sendto(str(msg),self.getAddr())

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

    def __init__(self,host,port,timeout=UDP_CLIENT_TIMEOUT):
        UDPParams.__init__(self,host,port)
        self.getSocket().settimeout(timeout)
        self.__connect()

    def __connect(self):
        self.getSocket().bind(self.getAddr())

class UDPClient(UDPParams):
    pass
