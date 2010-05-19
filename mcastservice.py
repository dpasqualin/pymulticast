#!/usr/bin/env python

from mcast import McastClient,McastServer
from udp import UDPServer,UDPClient
import sys,os

ANY = "0.0.0.0"
SENDER_PORT = 1501
MCAST_ADDR = "224.168.2.9"
MCAST_PORT = 1600
UDP_PORT = 20000
TTL = 1 # Nao sera repassado a nenhum router
UDP_HOST="localhost"

class McastServiceServer(object):
    """ Esta classe eh responsavel por ler uma nova requisicao do
    servico multicast e posteriormente enviar uma resposta ao cliente  """
    def __init__(self, mcastPort, mcastAddr):

        # Recebe requisicoes do multicast
        self.__mcastSrv = McastServer(mcastPort,mcastAddr)

    def getRequest(self):
        """ Le uma nova requisicao do multicast """
        return self.getMcast().read()

    def sendReply(self,udpHost,udpPort,response):
        """ Envia response para client (udpHost,udpPort) """
        UDPClient(udpHost,udpPort).send(response)

    def getMcast(self):
        return self.__mcastSrv

class McastServiceClient(object):
    """ Essa classe envia uma requisicao para (mcastPort,mcastAddr)
    e aguarda resposta em (udpHost,udpPort) """
    def __init__(self, mcastPort, mcastAddr, udpPort, udpAddr):
        # Sera usado para enviar requisicoes ao servico multicast
        self.__mcastClt = McastClient(mcastPort,mcastAddr)

        # O Socket udp aguarda pela resposta dos servidores
        self.__udpSrv = UDPServer(udpHost,udpPort)

    def run(self, request):
        """ Envia requisicao "request" via multicast e aguarda resposta
        via udp. """
        self.__sendToMcast(request)
        return self.readFromUDP()

    def __sendToMcast(self,request):
        self.getMcast().send(request)

    def __readFromUDP():
        return self.getUDP().read()

    def getMcast(self):
        return self.__mcastClt

    def getUDP(self):
        return self.__udpSrv

