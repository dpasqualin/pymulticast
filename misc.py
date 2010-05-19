#!/usr/bin/env python

import re,sys,socket

class Server(object):
    """ Armazena informacoes sobre um servidor """
    def __init__(self,serverID,serverHostname,isAlive=False):
        self.__id = serverID
        self.__hostname = serverHostname
        self.__isAlive = isAlive
        self.__ip = socket.gethostbyname(serverHostname)

    def getIP(self):
        return self.__ip

    def getID(self):
        return self.__id

    def getHostname(self):
        return self.__hostname

    def isAlive(self):
        return self.__isAlive

    def setAlive(self):
        self.__isAlive = True

    def setNotAlive(self):
        self.isAlive = False

    def __cmp__(self, x):
        if self.getID() == x.getID():
            return 0
        else:
            return 1

class Request(object):
    """ Esta classe armazena informacoes sobre uma requisicao.
        request eh no formato -> IP:PORT:REQUEST """
    def __init__(self,request):
        self.__IP, self.__port, self.__request = request.split()

    def getIP(self):
        return self.__IP

    def getPort(self):
        return self.__port

    def getRequest(self):
        return self.__request

    def __str__(self):
        return "%s:%s:%s" %(self.getIP(),getPort(),self.getRequest())

    def __cmp__(self,x):
        i1,i2 = self.getIP(),x.getIP()
        p1,p2 = self.getPort(),x.getPort()
        r1,r2 = self.getRequest(),x.getRequest()
        if i1 == i2 and p1 == p2 and r1 == r2:
            return 0
        else:
            return 1
