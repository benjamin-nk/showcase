# scale: Hagen's Matrices Test - Short form version
# scale source

import registerscales
import registerparticipants

class HMTS:
    def __init__(self):
        self.name = 'hmts'
        self.score = 0
        self.min = 0
        self.max = 6
        self.codes = {
            "hmts_q1_m1": 6,
            "hmts_q2_m2": 4,
            "hmts_q3_m3": 1,
            "hmts_q4_m5": 3,
            "hmts_q5_m7": 5,
            "hmts_q6_m9": 6,
        }

    # def addcolumn(self,colname):
    #     if colname not in registerscales.DPmScales().getscalecolumns(self.name):
    #         registerscales.DPmScales().registerscalecolumn(self.name,colname)

    def calculate(self,responsedict):
        templatecolumns = registerscales.DPmScales().getscalecolumns(self.name)
        columns = responsedict.items()
        count = len(templatecolumns)
        check = 0
        for colname in templatecolumns:
            for colname2,value in columns:
                if colname == colname2:
                    if value == '' or value.isspace(): continue 
                    
                    check += 1

        if check != count: self.score = check == 0 and registerscales.DPmNullFlags['empty'] or 0
        if self.score is registerscales.DPmNullFlags['empty']: return self
        
        # Calculation:
        for colname in templatecolumns:
            for colname2,value in columns:
                if colname != colname2: continue

                if value == '' or value.isspace(): continue

                if self.codes[colname] == int(value):
                    self.score += 1

        return self

    def report(self):
        print('HMT-S:',self.score,'/',self.max)

    def exportdata(self):
        return self.score

    def setprofile(self,pid):
        self.score = registerparticipants.DPmProfiles().getprofile(pid).getscaledata(self.name)

    def createtables(self,conn):
        conn.cursor().executescript('''
            DROP TABLE IF EXISTS HMTS;

            CREATE TABLE HMTS (
                pid  TEXT NOT NULL PRIMARY KEY UNIQUE,
                score INTEGER 
             );''')

    def exporttodb(self,conn,pid):
        self.setprofile(pid)

        conn.cursor().execute('''INSERT OR REPLACE INTO HMTS (pid, score) VALUES (?, ?)''', (pid, self.score))
        conn.commit()

    def preparecsv(self,pid,IncludeHeader=True):
        self.setprofile(pid)

        headers = ['pid','hmts']
        rows = [
            [pid,self.score]
        ]

        return headers,rows

registerscales.DPmScales().registerscale(HMTS())
