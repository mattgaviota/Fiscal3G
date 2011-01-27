#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from decoradores import Verbose
import optparse

class Server(object):
    def __init__(self, device_path, model, connection="serial"):
        """
        Crea la estructura de directorios
        Crea el fichero de configuración de gnokii para el dispositivo pasado
        Inicia el proceso de smsd
            Puebla y vigila la cola interna
            Notifica errores al metaserver
        """
        self._imei = None

    def get_ime(self):
        return

#        if self._imei is None:
#            obtengo(IMEI
#        return self._imei

    def close(self):
        """
        Espera al servidor que finalice sus tareas
        Mata al servidor
        Limpia el entorno
        """
        return


def get_options():
    # Instance the parser and define the usage message
    optparser = optparse.OptionParser(usage="""
    %prog [-vq] [-t timeout] [host[:port]]...
    """, version="%prog .1")

    # Define the options and the actions of each one
    optparser.add_option("-v", "--verbose", action="count", dest="verbose",
        help="Increment verbosity")
    optparser.add_option("-q", "--quiet", action="count", dest="quiet",
        help="Decrement verbosity")

    # Define the default options
    optparser.set_defaults(verbose=0, quiet=0)

    # Process the options
    return optparser.parse_args()


def main(options, args):
    debug(options, args)

    return 0


if __name__ == "__main__":
    # == Reading the options of the execution ==
    options, args = get_options()

    error = Verbose(options.verbose - options.quiet + 2, "E: ")
    warning = Verbose(options.verbose - options.quiet + 1, "W: ")
    info = Verbose(options.verbose - options.quiet + 0)
    moreinfo = Verbose(options.verbose - options.quiet -1)
    debug = Verbose(options.verbose - options.quiet - 2, "D: ")

    debug("""Options: '%s', args: '%s'""" % (options, args))

    exit(main(options, args))
