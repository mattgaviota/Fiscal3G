#!/usr/bin/python

from dbus.mainloop.glib import DBusGMainLoop
import dbus
import gobject
from decoradores import Verbose
from debug import debug


class Monitor(object):
    def __init__(self):
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
        for modem in self.get_all_gsm():
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
        for udi, path in self.modems.items():
            print path


#    @Verbose(2)
    def add_device(self, udi):
        if self.is_gsm(udi):
            self.modems[udi] = self.get_path(udi)
            self.show_modems()
        return


#    @Verbose(2)
    def remove_device(self, udi):
        if self.is_serial(udi):
            if udi in self.modems:
                del(self.modems[udi])
                self.show_modems()
        return
       

    def is_serial(self, udi):
        return "_serial_" in udi


    def get_all_gsm(self):
        return self.hal_manager.FindDeviceByCapability("modem")


    def is_gsm(self, udi):
        if self.is_serial(udi):
            device = self.get_device(udi)
            capabilities = device.GetPropertyString('info.capabilities')

            if "modem" in capabilities:
                if any(("GSM" in commands for commands in
                    device.GetPropertyString('modem.command_sets'))):
                    return True
                else:
                    print([commands for commands in
                    device.GetPropertyString('modem.command_sets')])


def main():
    monitor = Monitor()
    try:
        monitor.loop.run()
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    exit(main())
