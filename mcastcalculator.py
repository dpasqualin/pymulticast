#!/usr/bin/env python

from mcast import McastClient
from udp import UDPServer
import sys,os

ANY = "0.0.0.0"
SENDER_PORT = 1501
MCAST_ADDR = "224.168.2.9"
MCAST_PORT = 1600
UDP_PORT = 20000
TTL = 1 # Nao sera repassado a nenhum router
UDP_HOST="localhost"


class McastCalculatorClient(object):
    def __init__(self, mcastPort, mcastAddr, udpHost, udpPort):
        # Sera usado para enviar requisicoes ao servico multicast
        self.__mcastClt = McastClient(MCAST_PORT,MCAST_ADDR)

        # O Socket udp aguarda pela resposta dos servidores
        self.__udpClt = UDPServer(UDP_HOST,UDP_PORT)

    def calculate(self, calc):
        self.__sendToMcast(calc)
        return self.readFromUDP()

    def __sendToMcast(self,calc):
        self.getMcast().send(calc)

    def __readFromUDP()
        return self.getUDP().read()

    def getMcast(self):
        return self.__mcastClt

    def getUDP(self):
        return self.__udpClt

