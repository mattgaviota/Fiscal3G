#!/usr/bin/env python
#-*- coding: utf-8 -*-

import MySQLdb 

class Query():
    
    def __init__(self):
        self.sqlsentence = 'INSERT INTO %s(%s, %s, %s, %s, %s, %s)\
                            VALUES(%s, %s, %s, %s, %s, %s)'
        
    def connect_to_db(self, serverdata):
        self.datab = MySQLdb.connect(serverdata[0], serverdata[1], 
                                        serverdata[2], serverdata[3])
        self.cursor = self.datab.cursor()
        
    def insert_to_db(self, values):
        self.cursor.execute(self.sqlsentence % values)
