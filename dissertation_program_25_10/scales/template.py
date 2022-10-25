# scale: 
# scale source:

import registerparticipants
import registerscales
import csv
import os

class __NULL__:
    def __init__(self):
        self.name = 'cse'    
        self.score = 0

    #Used only on first model participant
    # def addcolumn(self,colname):
    #     # This will define the fields globally the first time it is used
    #     # so that subsequent objects can use the list
    #     # Fool proof for adding same column
    #     if colname not in registerscales.DPmScales().getscalecolumns(self.name):
    #         registerscales.DPmScales().registerscalecolumn(self.name,colname)

    def calculate(self,responsedict):
        templatecolumns = registerscales.DPmScales().getscalecolumns(self.name)
        columns = responsedict.items()
        # Check that response column entries are not == ''
        # If all are == '' then set score to 'null'
        # This will affect SQL table schema
        count = len(templatecolumns)
        check = 0
        for colname in templatecolumns:
            for colname2,value in columns:
                if colname == colname2:
                    if value == '' or value.isspace(): continue

                    check += 1

        # With this, any missing data will be dealt with by excluding the scale measurement
        # Otherwise i would need to somehow add a caveat that only partial data was measured for the total score, which isn't good enough anyway
        if check != count: 
            self.score = 'null'

            return self
        
        # Calcuation:
        for colname in templatecolumns:
            for colname2,value in columns:
                if colname != colname2: continue

                if value == '' or value.isspace(): continue
                # Add calculation here:

        return self

    def calcuate(self,key,value):
        pass

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

        # headers = ['pid','cse']
        # rows = [
        #     [pid,self.score]
        # ]

        # return headers,rows

# registerscales.DPmScales().registerscale(__NULL__())
