#!/usr/bin/python

from dbus.mainloop.glib import DBusGMainLoop
import dbus
import gobject
from decoradores import Verbose
from debug import debug
import optparse


class Monitor(object):
    def __init__(self, callback=None):
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
        self.system.add_signal_receiver(self.remove_device, 'DeviceRemoved',
            'org.freedesktop.Hal.Manager', 'org.freedesktop.Hal',
            '/org/freedesktop/Hal/Manager')


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
        print("<validados>")
        for udi, path_cset in self.modems.items():
            print("= %s, %s" % path_cset)
        print("</validados>")


    def add_device(self, udi):
        cset = self.get_cset(udi)
        if cset:
            self.modems[udi] = self.get_path(udi), cset
            print("+ %s, %s" % (self.modems[udi], cset))
            self.show_modems()
        return


    def remove_device(self, udi):
        if self.is_serial(udi):
            if udi in self.modems:
                print("- %s, %s" % self.modems[udi])
                del(self.modems[udi])
                self.show_modems()
        return
       

    def is_serial(self, udi):
        return "_serial_" in udi


    def get_all_modems(self):
        return self.hal_manager.FindDeviceByCapability("modem")


    def get_cset(self, udi):
        if self.is_serial(udi):
            device = self.get_device(udi)
            capabilities = device.GetPropertyString('info.capabilities')

            debug("Device connected, capabilities: %s" % capabilities)

            if "modem" in capabilities:
                debug("Modem at %s" % device)
                commands_sets = [c_set for c_set in
                    device.GetPropertyString('modem.command_sets')]
                for c_set in commands_sets:
                    if "GSM" in c_set:
                        return c_set
                    elif "V.250" in c_set:
                        return c_set
                else:
                    for c_set in commands_sets:
                        debug(c_set)


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
    monitor = Monitor()
    try:
        monitor.loop.run()
    except KeyboardInterrupt:
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
