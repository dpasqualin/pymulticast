#!/usr/bin/env python

from mcastservice import McastServiceServer
import re,sys,socket,threading
from misc import Server,Request,Timeout,Log
from misc import LOGERROR,LOGWARNING,LOGCONTROL,LOGMESSAGE,LOGDEBUG

# O HeartBeat do servidor sera enviado de acordo com este intervalo
TOUT_HEARTBEAT = 1.0
# Se um servidor qualquer nao enviar um HeartBeat nesse intervalo de tempo
# ele deve ser marcado como "morto"
TOUT_DEAD = 5*TOUT_HEARTBEAT

class OnlineCalcServer(McastServiceServer,threading.Thread):
    def __init__(self, serverId, mcastPort, mcastAddr, serverFile):

        threading.Thread.__init__(self)
        McastServiceServer.__init__(self,mcastPort,mcastAddr)
        self.__serverDict = self.readServerFile(serverFile)
        self.__server = int(serverId)
        self.__requestList = []
        self.__timeoutList = []
        self.__log = Log()
        self.writeLog(LOGCONTROL,"Iniciando...")

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

        # Criando timeout para o heartbeat
        tout = Timeout(self.sendHeartBeat,TOUT_HEARTBEAT)
        tout.start()
        self.addTimeout(tout)

        while not self.__quit:
            (data,(ip,port)) = self.getRequest()
            if reALIVE.match(data):
                data = reALIVE.search(data)
                sid = int(data.group("id"))
                self.heartBeatReceived(sid)
            elif reCONFIRM.match(data):
                data = reCONFIRM.search(data)
                serverID = data.group("id")
                request = data.group("request")
                self.requestSentby(serverId,request)
            elif reREQUEST.match(data):
                data = reREQUEST.search(data)
                data = "%s:%s:%s" %(ip,str(port),data.group("request"))
                request = Request(data)
                self.addRequest(request)

    def readServerFile(self,serverFile):
        """ Le um arquivo contendo os servidores que serao utilizados e
        retorna um dicionario {id:Server} """

        serverList = {}
        for line in open(serverFile):
            # Se a linha nao eh um comentario nem vazia
            if not re.match("^(#|$)",line):
                sid,shostname,sport = line.split()
                serverList[int(sid)] = Server(sid,shostname,sport)

        return serverList

    def writeLog(self,verbose,msg):
        msg = "Server-%d %s"%( self.getServer().getID(),msg )
        self.__log.log(verbose,msg)

    def addTimeout(self,obj):
        self.__timeoutList.append(obj)

    def addRequest(self, request):
        """ Adiciona uma nova requisicao a lista e a trata """

        self.writeLog(LOGMESSAGE,"Request:%s"%request)
        # TODO: tratar request
        self.requestList.append(request)

    def removeRequest(self, request):
        """ Remove request da lista """
        if request in self.__requestList:
            self.writeLog(LOGMESSAGE,"Request processado:%s"%request)
            self.__requestList.remove(request)

    def requestSentby(self, serverID, request):
        """ Confirmacao de que o servidor serverID respondeu a requisicao
        request, que deve ser removida da lista """
        self.removeRequest(request)

    def heartBeatReceived(self,serverID):
        """ Marca servidor serverID como vivo """
        self.writeLog(LOGCONTROL,"HeartBeatReceived:%d"%serverID)
        self.getServerDict()[int(serverID)].setAlive()

    def missingHeartBeat(self,serverID):
        """ Marca servidor serverID como morto """
        self.writeLog(LOGCONTROL,"MissingHeartBeat:%d"%serverID)
        self.getServerDict()[int(serverID)].setNotAlive()

    def sendHeartBeat(self):
        """ Envia mensagem ao multicast informando que esta vivo """
        self.writeLog(LOGCONTROL,"HeartBeatSent")
        self.getMcast().send("%d:ALIVE"%self.getServer().getID())

    def whoAnswers(self):
        """ Retorna o menor servidor ativo """
        for idx in self.getServerDict().keys().sort():
            if self.getServerDict()[idx].isAlive():
                return self.getServerDict()[idx].getID()

    def sendReply(self,request):
        """ Computa request e (se sou o servidor com menor ID vivo)
        envia resposta para o cliente, ao mesmo tempo
        que comunica os outros servidores do grupo multicast que a
        requisicao request foi respondida. """
        if self.whoAnswers() == self.getServer():
            reply = eval(request.getRequest())
            self.writeLog(LOGCONTROL,"Respondendo %s = %s"%(request,reply))
            host,port = request.getHost(),request.getPort()
            McastServiceServer.sendReply(self,host,port,reply)
            self.sendReplyConfirm(request)

    def sendReplyConfirm(self,request):
        """ Envia por multicast confirmacao de resposta da requisicao
        "request", que eh do tipo "Request" """
        serverID = self.getServer().getID()
        self.getMcast().send("%d:CONFIRM:%s"%(serverID,request))

    def getServer(self):
        return self.getServerDict()[self.__server]

    def getServerDict(self):
        return self.__serverDict

    def getTimeoutList(self):
        return self.__timeoutList

    def quit(self):
        self.__quit = True
        self.writeLog(LOGCONTROL,"Saindo")
        for tout in self.getTimeoutList():
            tout.quit()
        self.writeLog(LOGDEBUG,"Morto")
