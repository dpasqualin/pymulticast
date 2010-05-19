#!/usr/bin/env python

from mcastcservice import McastServiceServer
import re,sys,socket,Thread
from misc import Server,Request

class OnlineCalcServer(McastServiceServer):
    """ serverDict: dicionario com elementos Server """
    def __init__(self, severId, mcastPort, mcastAddr, serverDict):

        McastServiceServer.__init__(self,mcastPort,mcastAddr)
        self.__serverDict = serverDict
        self.__server = serverId
        self.__requestList = []

    def heartBeatReceived(self,serverID):
        """ Marca servidor serverID como vivo """
        self.getServerDict()[int(serverID)].setNotAlive()

    def missingHeartBeat(self,serverID):
        """ Marca servidor serverID como morto """
        self.getServerDict()[int(serverID)].setAlive()

    def sendHeartBeat(self):
        """ Envia mensagem ao multicast informando que esta vivo """
        self.getMcast().send("%d:ALIVE"%self.getServer().getID())

    def whoAnswers(self):
        """ Retorna o menor servidor ativo """
        for idx in self.getServerDict().keys().sort():
            if self.getServerDict()[idx].isAlive():
                return self.getServerDict()[idx]

    def sendReply(self,request):
        """ Computa request e (se sou o servidor com menor ID vivo)
        envia resposta para o cliente, ao mesmo tempo
        que comunica os outros servidores do grupo multicast que a
        requisicao request foi respondida. """
        if self.whoAnswers() == self.getMyServer():
            reply = eval(request.getRequest())
            host,port = request.getHost(),request.getPort()
            McastServiceServer.sendReply(self,host,port,reply)
            self.sendReplyConfirm(request)

    def sendReplyConfirm(self,request):
        """ Envia por multicast confirmacao de resposta da requisicao
        "request", que eh do tipo "Request" """
        self.getMcast().send("%d:CONFIRM:%s"%(self.getServer(),request))

    def getMyServer(self):
        return self.__server

    def getServerDict(self):
        return self.__serverDict
