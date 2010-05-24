#!/usr/bin/env python

from mcastservice import McastServiceClient
import sys,re,socket

class OnlineCalcClient(McastServiceClient):
    def run(self,port,request):
        exp = "^[0-9\.()\+\-\/\*]*$"
        if re.match(exp,request):
            request = "%s:%s"%(port,request)
            return McastServiceClient.run(self,request)[0]
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
            if calc:
                print onlinecalc.run(udpPort,calc)
        except (EOFError,KeyboardInterrupt):
            print ""
            break

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main(len(sys.argv),sys.argv))
    except:
        raise
