#!/usr/bin/env python
#-*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser
import os


class Parser():

    def __init__(self):
        self.parser = SafeConfigParser()
        #self.parser.read(os.path.expanduser('~/Fiscal3G/config.ini'))
        self.parser.read('../config.ini')
        self.serverdata = []
        self.tablevalues = []
        self.table = []


    def generate_values(self):
        serverdatakeys = sorted(self.parser.options('DATABASE'))
        valuekeys = sorted(self.parser.options('ROWS'))

        for serverdata in serverdatakeys:
            self.serverdata.append(self.parser.get('DATABASE', serverdata))

        for values in valuekeys:
            self.tablevalues.append(self.parser.get('ROWS', values))

        self.table = [self.serverdata[-1]]

        self.serverdata = self.serverdata[:-1]
        return True


    def get_values_for_query(self):
        return tuple(self.table + self.tablevalues)


    def get_serverdata_for_connection(self):
        return tuple(self.serverdata)
