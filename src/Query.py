#!/usr/bin/env python
#-*- coding: utf-8 -*-

import MySQLdb 

class Query():
    
    def __init__(self):
        self.sqlsentence = '''INSERT INTO %s(%s, %s, %s) VALUES (%s, %s, %s)'''
    
    def connect_to_db(self, host, user, passwd, database):
        self.datab = MySQLdb.connect(host, user, passwd, database)
        self.cursor = self.datab.cursor()
        
    def insert_to_db(self, values):
        self.cursor.execute(self.sqlsentence % values)
    
