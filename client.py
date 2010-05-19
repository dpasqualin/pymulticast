#!/usr/bin/env python

from mcastservice import McastServiceClient
import sys,re

class OnlineCalcClient(McastServiceClient):
    def run(self,request):
        exp = "^[0-9()\+\-\/\*]*$"
        if re.match(exp,request):
            return McastServiceClient.run(self,request)
        else:
            return None

def usage():
    print "%s mcastPort mcastAddr udpPort udpAddr" % sys.argv[0]
    print "\tUm prompt informa que os calculos ja podem ser digitados."
    print "\tUm <enter> separa cada calculo."

def main(argc, argv):
    if argc != 5:
        usage()
        sys.exit(1)

    # Argumentos
    mcastPort,mcastAddr,udpPort,udpAddr = argv[1:]

    # Cria conexao com o multicast e abre udp para resposta
    onlinecalc = OnlineCalcClient(mcastPort,mcastAddr,udpPort,udpAddr)

    # Loop para leitura de comandos
    print "ctrl+c para sair."
    while True:
        try:
            calc = raw_input("> ")
            print onlinecalc.run(calc)
        except (EOFError,KeyboardInterrupt):
            print ""
            return 0

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main(len(sys.argv),sys.argv))
    except:
        raise
