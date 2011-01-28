#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from decoradores import Verbose
from subprocess import Popen, PIPE
import os
import optparse

GNOKII = "/usr/bin/gnokii" #FIXME: Hardcoded
SMSD = "/usr/bin/smsd" #FIXME: Hardcoded
DEBUG = 2

class Server(object):
    def __init__(self, parent, device_path, model, connection):
        """
        Crea la estructura de directorios
        Crea el fichero de configuración de gnokii para el dispositivo pasado
        Inicia el proceso de smsd
            Pueblo y vigilo la cola interna
            Notifico errores al metaserver
        """

        self.parent = parent

        self.device_path = device_path
        self.model = model
        self.connection = connection or "serial"
        self.config_file = "gnokii" + device_path.replace("/", ".")
        self.make_config_file()

        self.description = None
        debug(self.get_description())

        self.configure_dirs()
    

    def configure_dirs(self):
        self.pathbase = os.path.join(self.parent.pathbase,
            self.description["IMEI"])

        if not os.path.isdir(self.pathbase):
            os.mkdir(self.pathbase)

        if (os.path.commonprefix((self.config_file, self.pathbase)) !=
            self.pathbase):
            new_config_file = os.path.join(self.pathbase, self.config_file)
            os.rename(self.config_file, new_config_file)
            self.config_file = new_config_file

        self.inbox_path = os.path.join(self.pathbase, "inbox")
        if not os.path.isdir(self.inbox_path):
            os.mkdir(self.inbox_path)

        self.outbox_path = os.path.join(self.pathbase, "outbox")
        if not os.path.isdir(self.outbox_path):
            os.mkdir(self.outbox_path)


    def make_config_file(self):
        with open(self.config_file, "w") as file:
            file.write("[global]\n")
            file.write("connection = %s\n" % self.connection)
            file.write("model = %s\n" % self.model)
            file.write("port = %s\n" % self.device_path)


    def get_description(self):
        if not self.description:
            proc = Popen([GNOKII, "--config", self.config_file, "--identify"],
                0, GNOKII, stdout=PIPE, stderr=PIPE)
            self.description = {}
            for line in proc.stdout.readlines():
                key, value = line.split(":")
                self.description[key.strip()] = value.strip()

        return self.description


    def close(self):
        """
        Espera a que el servidor finalice sus tareas
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

else:

    error = Verbose(2 - DEBUG, "E: ")
    warning = Verbose(1 - DEBUG, "W: ")
    info = Verbose(0 - DEBUG)
    moreinfo = Verbose(1 - DEBUG)
    debug = Verbose(2 - DEBUG, "D: ")
