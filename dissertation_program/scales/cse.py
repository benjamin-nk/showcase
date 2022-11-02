# scale: Creative Self-Efficacy (CSE)
# scale source: Beghetto, R. A. (2006). Creative self-efficacy: Correlates in middle and secondary students. Creativity research journal, 18(4), 447-457.

import registerparticipants
import registerscales
import csv
import os

class CSE:
    def __init__(self):
        self.name = 'cse'    
        self.score = 0
        self.min = 3
        self.max = 15
        self.values = {
            "strongly disagree": 1,
            "somewhat disagree": 2,
            "neither agree nor disagree": 3,
            "somewhat agree": 4,
            "strongly agree": 5
        }

    def calculate(self,responsedict):
        templatecolumns = registerscales.DPmScales().getscalecolumns(self.name)
        columns = responsedict.items()

        count = len(templatecolumns)
        check = 0
        for colname in templatecolumns:
            for colname2,value in columns:
                if colname == colname2:
                    if value != '': 
                        check += 1

        if check != count:
            self.score = check == 0 and registerscales.DPmNullFlags['empty'] or registerscales.DPmNullFlags['incomplete']

            return self

        # Calcuation:
        for colname in templatecolumns:
            for colname2,value in columns:
                if colname != colname2: continue

                if value == '' or value.isspace(): continue

                self.score += self.values[value.lower()]

        return self

    def report(self):
        print('CSE:',self.score,'/',self.max)

    def exportdata(self):
        return self.score

    def setprofile(self,pid):
        self.score = registerparticipants.DPmProfiles().getprofile(pid).getscaledata(self.name)

    def createtables(self,conn):
        conn.cursor().executescript('''
            DROP TABLE IF EXISTS CSE;

            CREATE TABLE CSE (
                pid  TEXT NOT NULL PRIMARY KEY UNIQUE,
                score INTEGER 
             );''')

    def exporttodb(self,conn,pid):
        self.setprofile(pid)

        conn.cursor().execute('''INSERT OR REPLACE INTO CSE (pid, score) VALUES (?, ?)''', (pid, self.score))
        conn.commit()

    def preparecsv(self,pid,IncludeHeader=True):
        self.setprofile(pid)

        headers = ['pid','cse']
        rows = [
            [pid,self.score]
        ]

        return headers,rows


registerscales.DPmScales().registerscale(CSE())
