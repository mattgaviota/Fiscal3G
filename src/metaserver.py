#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from decoradores import Verbose
from devicemonitor import Monitor
from server import Server
import optparse

DEBUG = 2

class Metaserver(object):
    def __init__(self, pathbase="."):
        """
        Crea la estructura de directorios del metaservidor
        Inicia el monitor de dispositivos
            Maneja los eventos de conexion/desconexion
                Pide a farm que instancie y eliminea servidores
            Desencadena eventos
        """
        self.servers = {}
        self.pathbase = pathbase

        self.device_monitor = Monitor(self.configure_device,
            self.remove_device)
        self.device_monitor.loop.run()

    def configure_device(self, device_path, protocol, model=None):
        info("Metaserver:configured:%s, %s, %s" % (device_path, protocol,
            model))
        server = Server(self, device_path, protocol, model)
        self.servers[device_path] = server
        return

    def remove_device(self, device_path):
        info("Metaserver:removed:%s" % device_path)
        server = self.servers[device_path]
        server.close()
        del(self.servers[device_path])
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
    metaserver = Metaserver()

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

else:

    error = Verbose(2 - DEBUG, "E: ")
    warning = Verbose(1 - DEBUG, "W: ")
    info = Verbose(0 - DEBUG)
    moreinfo = Verbose(1 - DEBUG)
    debug = Verbose(2 - DEBUG, "D: ")
