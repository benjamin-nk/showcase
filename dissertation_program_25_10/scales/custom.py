# scale: 
# scale source:

import registerparticipants
import registerscales
import csv
import os

class Custom:
    def __init__(self):
        self.name = 'custom'    
        self.score = dict()

    def calculate(self,responsedict):
        templatecolumns = registerscales.DPmScales().getscalecolumns(self.name)
        columns = responsedict.items()
        # count = len(templatecolumns)
        # check = 0
        # for colname in templatecolumns:
        #     for colname2,value in columns:
        #         if colname == colname2:
        #             if value == '' or value.isspace(): continue 
                    
        #             check += 1

        # if check != count: 
        #     self.score = 'null'

        #     return self

        for colname in templatecolumns:
            for colname2,value in columns:
                if colname != colname2: continue
                # Fill empty entry with 'null' - i can do it this way because these are independent questions rather than sets
                if value == '' or value.isspace(): 
                    self.score[colname] = registerscales.DPmNullFlags['empty']
                else:
                    self.score[colname] = value

        return self

    def report(self):
        pass

    def exportdata(self):
        return self.score

    def setprofile(self,pid):
        self.score = registerparticipants.DPmProfiles().getprofile(pid).getscaledata(self.name)

    def createtables(self,conn):
        pass
        # conn.cursor().executescript('''
        #     DROP TABLE IF EXISTS CSE;

        #     CREATE TABLE CSE (
        #         pid  TEXT NOT NULL PRIMARY KEY UNIQUE,
        #         score INTEGER 
        #      );''')

    def exporttodb(self,conn,pid):
        self.setprofile(pid)
        pass

        # conn.cursor().execute('''INSERT OR REPLACE INTO CSE (pid, score) VALUES (?, ?)''', (pid, self.score))
        # conn.commit()

    def preparecsv(self,pid,IncludeHeader=True):
        self.setprofile(pid)
        pass

        headers = [x for x in self.score]
        headers.insert(0,'pid')
        rows = [
            [x for x in self.score.values()]
        ]
        rows[0].insert(0,pid)

        return headers,rows


registerscales.DPmScales().registerscale(Custom())
