#!/usr/bin/env python
#-*- coding: utf-8 -*-

import MySQLdb
from parser import Parser
import sys 

class Query():
    
    def __init__(self, args):
        self.sqlsentence = 'INSERT INTO %s(%s, %s, %s, %s, %s, %s)\
                            VALUES(%s, %s, %s, %s, %s, 0)'
        self.path = args[1]
        
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
        horaenvio = data[0].split()[1].replace(':','')
        horarecepcion = data[1].split()[1].replace(':','')    
        telefono = data[2][4:]
        campos = [campo for campo in "".join([char if char.isdigit() else ";"\
                        for char in data[3]]).split(";") if campo]
        planilla = campos[0]
        ordenes = campos[1:]
        for orden in ordenes:
            self.reports.append(self.values + (telefono, planilla, orden, horaenvio, horarecepcion))
        return True
        
def main():
    db = Query(sys.argv)
    db.get_data_from_config()
    db.format_data_to_insert()
    db.connect_to_db(db.get_serverdata())
    for report in db.get_reports():
        db.insert_to_db(report)
    
if __name__ == '__main__':
    exit(main())
