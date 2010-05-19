#!/usr/bin/env python

from mcastcservice import McastServiceServer
import re,sys,socket,threading
from misc import Server,Request

class OnlineCalcServer(McastServiceServer,threading.Thread):
    """ serverDict: dicionario com elementos Server """
    def __init__(self, severId, mcastPort, mcastAddr, serverDict):

        threading.Thread.__init__(self)
        McastServiceServer.__init__(self,mcastPort,mcastAddr)
        self.__serverDict = serverDict
        self.__server = serverId
        self.__requestList = []

        # Sinaliza quando a thread tera que ser fechada
        self.__quit = False

    def run(self):
        """ Este metodo recebe as mensagens e endereca para o metodo
        correto """

        # Expressoes regulares de possiveis mensagens
        reID = "(?P<id>[0-9]+)"
        reREQCONF = "(?P<request>.*)"
        reALIVE = re.compile("^%s:ALIVE$" % reID)
        reCONFIRM = re.compile("%s:CONFIRM:%s$" % (reID,reREQCONF))
        reREQUEST = re.compile("^(?P<request>[0-9()\+\-\/\*]*)$")

        while not self.__quit:
            ((port,host),data) = getRequest()
            if reALIVE.match(data):
                data = reALIVE.search(data)
                self.hearBeatReceived(int(data.group("id")))
            elif reCONFIRM.match(data):
                data = reCONFIRM.search(data)
                serverID = data.group("id")
                request = data.group("request")
                self.requestSentby(serverId,request)
            elif reREQUEST.match(data):
                data = reREQUEST.search(data)
                request = Request(data.group("request"))
                self.addRequest(request)

    def addRequest(self, request):
        """ Adiciona uma nova requisicao a lista e a trata """

        # TODO: tratar request
        self.requestList.append(request)

    def removeRequest(self, request):
        """ Remove request da lista """
        if request in self.__requestList:
            self.__requestList.remove(request)

    def requestSentby(self, serverID, request):
    """ Confirmacao de que o servidor serverID respondeu a requisicao
    request, que deve ser removida da lista """
        self.removeRequest(request)

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
