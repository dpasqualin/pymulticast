#!/usr/bin/env python

import re,sys,socket,threading
from time import sleep,asctime

CONFFILE = "mcast.conf"
LOGFILE = "mcast.log"

def readConf():
    """ Le arquivo de configuracao mcast.conf e retorna dicionario
        {opcao:valor} """

    res = {}
    for line in open(CONFFILE):
        if not re.match("^(#|$)",line):
            opt,value = [ i.strip() for i in line.split("=") ]
            res[opt] = value

    return res

class Log(object):
    """ Salva mensagens no arquivo de log LOGFILE, respeitando o verboso
    desejado escrito em CONFFILE """
    def __init__(self):
        self.__conf = readConf()
        self.__file = open(LOGFILE,"a")
        self.verbose = self.__conf["verbose"]

    def log(self, verbose, msg):
        """ Escreve mensagem de log no arquivo se verbose for <= ao verbose
        definido no arquivo de configuracao """
        if verbose <= self.verbose:
            timestamp = asctime()[4:].replace(":","")
            msg = "%s: %s\n" % (timestamp,msg)
            self.__write(msg)

    def __write(self,msg):
        self.__file.write(msg)
        self.__file.flush()

class Timeout(threading.Thread):
    """ Roda em uma thread separada o metodo timeoutFunction que deve
    existir dentro da classe passada como argumento em objMethod. O
    argumento timeout determina de quanto em quanto tempo essa funcao deve
    ser executada """
    def __init__(self, objMethod, timeout):
        threading.Thread.__init__(self)
        self.__objMethod = objMethod
        self.__timeout = timeout
        self.__quit = False

    def run(self):
        while not self.__quit:
            self.runMethod()
            sleep(self.getTimeout())

    def quit(self):
        self.__quit = True

    def getTimeout(self):
        return self.__timeout

    def runMethod(self):
        return self.__objMethod()

class Server(object):
    """ Armazena informacoes sobre um servidor """
    def __init__(self,serverID,serverHostname,serverPort,isAlive=False):
        self.__id = int(serverID)
        self.__hostname = serverHostname
        self.__isAlive = isAlive
        self.__port = int(serverPort)
        self.__ip = socket.gethostbyname(serverHostname)

    def getIP(self):
        return self.__ip

    def getID(self):
        return self.__id

    def getHostname(self):
        return self.__hostname

    def getPort(self):
        return self.__port

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
        self.__IP, self.__port, self.__request = request.split(":")

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

