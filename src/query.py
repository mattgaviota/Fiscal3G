#!/usr/bin/env python
#-*- coding: utf-8 -*-

from os import path
from parser import Parser
import MySQLdb
import shutil
import sys

REPORT_ARCHIVE = path.abspath("report_archive.mbox")

class Query():

    def __init__(self):
        self.sqlsentence = ('INSERT INTO %s(%s, %s, %s, %s, %s)'
                            'VALUES(%s, %s, %s, %s, %s)')
        
    def set_path(self, path):
        self.path = path

    def connect_to_db(self, serverdata):
        self.datab = MySQLdb.connect(serverdata[0], serverdata[1],
            serverdata[2], serverdata[3])
        self.cursor = self.datab.cursor()
        return True

    def insert_to_db(self, values):
        self.cursor.execute(self.sqlsentence % values)
        return True

    def get_data_from_config(self):
        parse = Parser()
        parse.generate_values()
        self.serverdata = parse.get_serverdata_for_connection()
        self.values = parse.get_values_for_query()
        return True

    def get_serverdata(self):
        return self.serverdata

    def get_values(self):
        return self.values

    def get_reports(self):
        return self.reports

    def format_data_to_insert(self):
        file = open(self.path, 'r')
        data = [line.strip() for line in file.readlines()]
        self.reports = []
        data = [line.strip() for line in data]

        horaenvio = data[0].split()[1].replace(':','')
        horarecepcion = data[1].split()[1].replace(':','')
        telefono = data[2][-10:]

        body = data[3]
        normalbody = "".join([char if char.isdigit() else ";"
            for char in body])
        campos = [campo for campo in normalbody.split(";")if campo]

        print("### " + ";".join(campos))
        
        if len(campos) > 1:
            planilla = campos[0]
            ordenes = campos[1:]
            for orden in ordenes:
                self.reports.append(self.values + (telefono, planilla, orden, horaenvio, horarecepcion))
            return True
        else:
            print("  xxx %s %s %s" % (horaenvio, telefono, data[3]))
    

def main():
    db = Query()
    db.get_data_from_config()
    
    try:
        db.connect_to_db(db.get_serverdata())
    except:
        print("    XX Está la base de datos online?")
        for arg in sys.argv[1:]:
            shutil.move(arg, "to_db/%s" % arg.split("/")[-1])
    else:
        for arg in sys.argv[1:]:
            db.set_path(arg)
            db.format_data_to_insert()
            
            with open(REPORT_ARCHIVE, "a") as file:
                file.write("%s\n" % db.get_reports)
            
            for report in db.get_reports():
                db.insert_to_db(report)


if __name__ == '__main__':
    exit(main())
