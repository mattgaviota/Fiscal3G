#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from decoradores import Verbose, Retry, Auto_verbose, Async, debug, nothreadsafe
from pprint import pprint
from subprocess import Popen, PIPE, signal
import optparse
import os
import time

GNOKII = "/usr/bin/gnokii" #FIXME: Hardcoded
SMSD = "/usr/sbin/smsd" #FIXME: Hardcoded
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

        self._smsd = None
        self.parent = parent

        self.device_path = device_path
        device_name = self.device_path.lstrip("/dev/")
        self.config_section = "%s.%s" % (device_name, model)

        self.model = model
        self.connection = connection or "serial"
        self.config_file = "gnokii" + device_path.replace("/", ".")
        self.make_config_file()

        self.description = None
        debug(self.get_description())

        self.configure_dirs()

        self._keep_running = True
        self.monitor(self)
    

    def send_sms(self, dest_number, content):
        sms_path = os.path.join(self.outbox,
            "%s.%s" % (
                self.description["IMEI"],
                time.strftime("%Y-%m-%d %T")))
        with open(sms_path, "w") as file:
            file.write(content)
        return


    @Auto_verbose(1, 2)
    def start_smsd(self):
        self._keep_running = True
        return self._keep_running


    @Auto_verbose(1, 2)
    def stop_smsd(self):
        self._keep_running = False
    

    @Async
    @nothreadsafe
    def monitor(self):
        """
        WTF, smsd doesnt accept the --config option, we must improvise.
        A global config file has a section by /dev/*-model device. e.g.:

            [phone_ttyUSB0-AT-HW]
            model = AT-HW

        We run smsd with the -t "devicename-model".
        """
        #TODO: Report this ^^^ bug

        while True:
            if self._keep_running and not self.is_alive():
                environ = {}
                environ["PWD"] = self.pathbase

                pprint(environ)
                command = ["smsd", "--logfile", self.log_path,
                    "--phone", self.config_section, "-c", self.outbox_path, 
                    "-m", "file", "-u",
                    os.path.join(self.parent.pathbase, "bin/handler.sh")]
                debug(" ".join(command))

                stdout = open(os.path.join(self.pathbase, "stdout"), "a")
                stdout.write(" ".join(command) + "\n")
                stderr = open(os.path.join(self.pathbase, "stderr"), "w")
                self._smsd = Popen(command, stdout=stdout,
                    stderr=stderr, shell=True)

                self._smsd.wait()

            else:
                debug("Server:Monitor: %s, %s" %
                    (self._keep_running, self.is_alive()))

            time.sleep(5)


    def is_alive(self):
        if self._smsd:
            if self._smsd.returncode is None:
                return True
            else:
                return False


    def configure_dirs(self):
        self.pathbase = os.path.join(self.parent.pathbase,
            self.description["IMEI"])

        self.log_path = os.path.join(self.pathbase, "logfile")

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

    
    @Retry(10, pause=1)
    def gnokii(self, *args):
        proc = Popen([GNOKII, "--config", self.config_file] + list(args),
            0, GNOKII, stdout=PIPE, stderr=PIPE)
        error = proc.wait()

        if not error:
            return proc


    @Retry(20, pause=5)
    def get_description(self):
        if not self.description:
            proc = self.gnokii("--identify")
            self.description = {}
            for line in proc.stdout.readlines():
                key, value = line.split(":")
                self.description[key.strip()] = value.strip()

        if self.description["IMEI"].isdigit():
            return self.description
        else:
            debug("%s has no IMEI?" % self.device_path)
            return


    def close(self):
        """
        Espera a que el servidor finalice sus tareas
        Mata al servidor
        Limpia el entorno
        """

        self.wait()

        for pause in xrange(15):
            if self._smsd is None:
                debug("smsd was no active")
                return
            elif self._smsd.returncode:
                break
            else:
                time.sleep(1)

        self._smsd.kill()

        return self.is_alive()

    def wait(self):
        time.sleep(2)


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
