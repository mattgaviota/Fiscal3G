#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
from ConfigParser import SafeConfigParser
 
CONFIGFILE = os.path.expanduser('~/fiscal3g/.fiscalrc')


def appendtofile(filename, line):
    with open(filename, "a") as file:
        file.write(line + '\r\n')
    return True

def writetolog(entry):
    return appendtofile(LOGFILE, entry)

def writetoinbox(*args):
    return appendtofile(INBOX, "\t".join(args))

def main():
    config = SafeConfigParser()
    config.read(CONFIGFILE)
    
    numero, dia, fecha = sys.argv[1:]
    mensaje = '\r\n'.join(sys.stdin.readlines())
    entrada = ' '.join(('Arribo de mensaje : ',numero, dia, fecha, mensaje))
    writetolog(entrada)
    writetoinbox(numero, dia, fecha, mensaje)
    return

if __name__ == '__main__':
    exit(main())

