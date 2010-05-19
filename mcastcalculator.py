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

class McastCalculatorServer(object):
    """ Esta classe eh responsavel por ler uma nova requisicao de calculo do
    servico multicast e posteriormente enviar uma resposta ao cliente  """
    def __init__(self, mcastPort, mcastAddr):

        # Recebe requisicoes do multicast
        self.__mcastSrv = McastServer(mcastPort,mcastAddr)

    def getRequest(self):
        """ Le uma nova requisicao do multicast """
        return self.getMcast().read()

    def sendResponse(self,udpHost,udpPort,response):
        """ Envia response para client (udpHost,udpPort) """
        UDPClient(udpHost,udpPort).send(response)

    def getMcast(self):
        return self.__mcastSrv

class McastCalculatorClient(object):
    """ Essa classe envia uma requisicao de calculo para
    (mcastPort,mcastAddr) e aguarda resposta em (udpHost,udpPort) """
    def __init__(self, mcastPort, mcastAddr, udpPort, udpAddr):
        # Sera usado para enviar requisicoes ao servico multicast
        self.__mcastClt = McastClient(mcastPort,mcastAddr)

        # O Socket udp aguarda pela resposta dos servidores
        self.__udpSrv = UDPServer(udpHost,udpPort)

    def calculate(self, calc):
        """ Envia equacao "calc" via multicast e aguarda resposta via udp.
            calc eh uma string que pode possuir os simbolos +-/*()
        """
        self.__sendToMcast(calc)
        return self.readFromUDP()

    def __sendToMcast(self,calc):
        self.getMcast().send(calc)

    def __readFromUDP()
        return self.getUDP().read()

    def getMcast(self):
        return self.__mcastClt

    def getUDP(self):
        return self.__udpSrv

