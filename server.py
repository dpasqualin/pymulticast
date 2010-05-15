#!/usr/bin/env python

import socket
import time

ANY = "0.0.0.0"
SENDERPORT=1501
MCAST_ADDR = "224.168.2.9"
MCAST_PORT = 1600
TTL=1 # Nao sera repassado a nenhum router

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#The sender is bound on (0.0.0.0:1501)
sock.bind((ANY,SENDERPORT))
#Tell the kernel that we want to multicast and that the data is sent
#to everyone (255 is the level of multicasting)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
while 1:
    time.sleep(10)
    #send the data "hello, world" to the multicast addr: port
    #Any subscribers to the multicast address will receive this data
    sock.sendto("Hello World", (MCAST_ADDR,MCAST_PORT) );
