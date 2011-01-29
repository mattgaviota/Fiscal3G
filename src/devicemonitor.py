#!/usr/bin/python

from dbus.mainloop.glib import DBusGMainLoop
from debug import debug
import shutil
from decoradores import Verbose
import csv
import dbus
import gobject
import optparse
import os
import time

DEBUG = 0

class Monitor(object):
    def __init__(self, on_added_device_device=None,
            on_removed_device_device=None):
        dummy_func = lambda *args:args
        self.on_added_device_device = on_added_device_device or dummy_func
        self.on_removed_device_device = on_removed_device_device or  dummy_func

        self.loop = DBusGMainLoop()
        self.system = dbus.SystemBus(mainloop=self.loop)

        hal_manager_proxy = self.system.get_object('org.freedesktop.Hal',
            '/org/freedesktop/Hal/Manager')
        self.hal_manager = dbus.Interface(hal_manager_proxy,
            'org.freedesktop.Hal.Manager')

        # Connects the wrappers
        self.system.add_signal_receiver(self.add_device, 'DeviceAdded',
            'org.freedesktop.Hal.Manager', 'org.freedesktop.Hal',
            '/org/freedesktop/Hal/Manager')

        self.system.add_signal_receiver(self.remove_device,
            'DeviceRemoved', 'org.freedesktop.Hal.Manager',
            'org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')

        reader = csv.reader(open("models.csv"))
        self.models = dict(reader)

        self.modems = {}
        for modem in self.get_all_modems():
            self.add_device(modem)

        self.loop = gobject.MainLoop()


    def get_device(self, udi):
        devproxy = self.system.get_object("org.freedesktop.Hal", udi)
        device = dbus.Interface(devproxy, 'org.freedesktop.Hal.Device')
        return device


    def get_path(self, udi):
        device = self.get_device(udi)
        path = device.GetPropertyString('linux.device_file')
        return path


    def show_modems(self):
        for udi, path_cset in self.modems.items():
            print("= %s, %s" % path_cset)


    def add_device(self, udi):
        cset = self.get_cset(udi)

        if cset:
#            time.sleep(4) #HACK: sleep until the modem wake up.
            model = self.models[cset]

            if cset:
                self.modems[udi] = self.get_path(udi), model
                debug("+ %s, %s" % self.modems[udi])
                return self.on_added_device_device(*self.modems[udi])
            else:
                return


    def remove_device(self, udi):

        if udi in self.modems:
            debug("- %s, %s" % self.modems[udi])
            path = self.modems[udi][0]
            del(self.modems[udi])
            return self.on_removed_device_device(path)


    def is_serial(self, udi):
        return "_serial_" in udi


    def get_all_modems(self):
        return self.hal_manager.FindDeviceByCapability("modem")


    def get_cset(self, udi):
        if self.is_serial(udi):
            device = self.get_device(udi)
            capabilities = device.GetPropertyString('info.capabilities')

            if "modem" in capabilities:
                commands_sets = [c_set for c_set in
                    device.GetPropertyString('modem.command_sets')]

                for c_set in commands_sets:
                    if "GSM" in c_set:
                        return "GSM"
                    elif "V.250" in c_set:
                        return c_set
                else:
                    for c_set in commands_sets:
                        debug(c_set)
                        return False
            else:
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

def get_conf_name(path):
    configs = "configs"
    assert os.path.isdir(configs)
    return "%s/gnokii%s.conf" % (configs, path.replace("/", "."))

def make_config_file(path, model, connection="serial"):
    moreinfo("Path: %s Model: %s Connection: %s" % (path, model, connection))
    with open(get_conf_name(path), "w") as file:
        file.writelines([
            "[global]\n",
            "initlength = default\n",
            "use_locking = no\n",
            "serial_baudrate = 19200\n",
            "serial_write_usleep = 1\n",
            "smsc_timeout = 30\n",
            "connection = %s\n" % connection,
            "model = %s\n" % model,
            "port = %s\n" % path,
            "[logging]"
            "debug = on\n"
            "rlpdebug = off\n"
            "xdebug = off\n"
        ])


def remove_config_file(path):
    moreinfo("Path:", path)
    try:
        os.remove(get_conf_name(path))
    except OSError:
        return


def main(options, args):
    shutil.rmtree("configs")
    os.mkdir("configs")
    monitor = Monitor(make_config_file, remove_config_file)
    try:
        monitor.loop.run()
    except KeyboardInterrupt:
        return 0
    shutil.rmtree("configs")


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
    warning = Verbose(1, "W: ")
    info = Verbose(0)
    moreinfo = Verbose(1)
    debug = Verbose(2, "D: ")
