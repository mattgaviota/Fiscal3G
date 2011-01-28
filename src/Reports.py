#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from Query import Query
from Parser import Parser

class Reports():
    
    def __init__(self):
        self.db = Query()
        self.parse = Parser()
        self.parse.generate_values()
        self.db.connect_to_db(self.parse.get_serverdata_for_connection())
    
    def impact_on_db(self, report):
        try:
            db.insert_to_db(self.parse.get_values_for_query() + report)
        except:
            print 'Cant insert to MySQL database'
        
        
