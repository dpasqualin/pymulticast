#!/usr/bin/env python

from mcastcalculator import McastCalculatorClient
import sys

class OnlineCalc(McastCalculatorClient):
    pass

def usage():
    print "./%s mcastPort mcastAddr udpPort udpAddr" % sys.argv[0]
    print "\tUm prompt informa que os calculos ja podem ser digitados."
    print "\tUm <enter> separa cada calculo."

if __name__ == "__main__":
    pass

