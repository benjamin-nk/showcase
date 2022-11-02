# scale: International Personality Item Pool
# scale source: Goldberg, L. R., Johnson, J. A., Eber, H. W., Hogan, R., Ashton, M. C., Cloninger, C. R., & Gough, H. C. (2006). The International Personality Item Pool and the future of public-domain personality measures. Journal of Research in Personality, 40, 84-96. 

import re
import registerscales
import registerparticipants

class IPIP50:
    def __init__(self):
        self.name = 'ipip50'
        self.score = {
            'openness': 0,
            'conscientiousness': 0,
            'extraversion': 0,
            'agreeableness': 0,
            'emotional_stability': 0
        }
        self.questionprefix = 'ipip_fifty_'
        self.ocean = {
            'extraversion' : { #1 -- see administering ipip
                '1': 'positive',
                '11' : 'positive',
                '21' : 'positive',
                '31' : 'positive',
                '41' : 'positive',
                '6' : 'negative',
                '16' : 'negative',
                '26' : 'negative',
                '36' : 'negative',
                '46' : 'negative',
            },
            'agreeableness' : { #2
                '2': 'negative',
                '12' : 'negative',
                '22' : 'negative',
                '32' : 'negative',
                '7' : 'positive',
                '17' : 'positive',
                '27' : 'positive',
                '37' : 'positive',
                '42' : 'positive',
                '47' : 'positive',
            },
            'conscientiousness' : { #3
                '3': 'positive',
                '13' : 'positive',
                '23' : 'positive',
                '33' : 'positive',
                '43' : 'positive',
                '48' : 'positive',
                '8' : 'negative',
                '18' : 'negative',
                '28' : 'negative',
                '38' : 'negative',
            },
            'emotional_stability' : { #4
                '4': 'negative',
                '9' : 'positive',
                '19' : 'positive',
                '14' : 'negative',
                '24' : 'negative',
                '29' : 'negative',
                '34' : 'negative',
                '39' : 'negative',
                '44' : 'negative',
                '49' : 'negative',
            },
            'openness' : { #5
                '5': 'positive',
                '10' : 'negative',
                '15' : 'positive',
                '20' : 'negative',
                '25' : 'positive',
                '30' : 'negative',
                '35' : 'positive',
                '40' : 'positive',
                '45' : 'positive',
                '50' : 'positive',
            }
        }
        self.positivekeys = {
            'very inaccurate': 1,
            'moderately inaccurate': 2,
            'neither inaccurate nor accurate': 3,
            'neither accurate nor inaccurate': 3,
            'moderately accurate': 4,
            'very accurate': 5
        }
        self.negativekeys = {
            'very inaccurate': 5,
            'moderately inaccurate': 4,
            'neither inaccurate nor accurate': 3,
            'neither accurate nor inaccurate': 3,
            'moderately accurate': 2,
            'very accurate': 1
        }

        self.dimensionranges = dict()

        for dimension,dic in self.ocean.items():
            self.dimensionranges[dimension] = {}

            for qnum,sign in dic.items():
                # i need to map the question to its value and sign
                # then for all the negative questions, total them
                # then for all the positive questions, total them
                try:
                    self.dimensionranges[dimension][sign]['count'] += 1
                except:
                    self.dimensionranges[dimension][sign] = {'count' : 1,}
        
        for dimension in self.dimensionranges:
            for sign in self.dimensionranges[dimension]:
                i=1
                while i <= self.dimensionranges[dimension][sign]['count']:
                    try:
                        self.dimensionranges[dimension][sign]['total'] += 5 * (sign == 'negative' and -1 or 1)
                    except:
                        self.dimensionranges[dimension][sign]['total'] = 5 * (sign == 'negative' and -1 or 1)
                    i += 1
                
            self.dimensionranges[dimension]['median'] = (self.dimensionranges[dimension]['negative']['total'] + self.dimensionranges[dimension]['positive']['total']) / 2

    # def addcolumn(self,colname):
    #     if colname not in registerscales.DPmScales().getscalecolumns(self.name):
    #         registerscales.DPmScales().registerscalecolumn(self.name,colname)

    def calculate(self,responsedict):
        # Ensures all questions for a dimension are answered otherwise dimension will be null
        templatecolumns = registerscales.DPmScales().getscalecolumns(self.name)
        columns = responsedict.items()
        count = {
            'extraversion': len(self.ocean['extraversion']),
            'emotional_stability': len(self.ocean['emotional_stability']),
            'conscientiousness': len(self.ocean['conscientiousness']),
            'openness': len(self.ocean['openness']),
            'agreeableness': len(self.ocean['agreeableness'])
        }
        check = {
            'extraversion': 0,
            'emotional_stability': 0,
            'conscientiousness': 0,
            'openness': 0,
            'agreeableness': 0
        }
        for colname in templatecolumns:
            for colname2,value in columns:
                if colname == colname2:
                    oceankey = re.search('^ipip_fifty_([0-9]+)',colname).groups()[0]
                    # check which dimension the key belongs in:
                    for dimension,d in self.ocean.items():
                        if oceankey in d:
                            if value != '': 
                                check[dimension] += 1

        # i need to set each dimension to null
        for dimension,chk in check.items():
            # compare response's answered question key count to normal question key count
            if chk != count[dimension]:
                self.score[dimension] = chk == 0 and registerscales.DPmNullFlags['empty'] or registerscales.DPmNullFlags['incomplete']
        
        # Calcuation:
        for colname in templatecolumns:
            for colname2,value in columns:
                if colname != colname2: continue
                if value == '' or value.isspace() : continue
                # Add calculation here:
                oceankey = re.search('^ipip_fifty_([0-9]+)',colname).groups()[0]

                # Total up scores for each dimension
                for dimension,dic in self.ocean.items():
                    # Skip if null
                    if self.score[dimension] in registerscales.DPmNullFlags.values(): continue 

                    if oceankey in dic:
                        if dic[oceankey] == 'positive':    
                            self.score[dimension] += self.positivekeys[value.lower()]
                        elif dic[oceankey] == 'negative': 
                            self.score[dimension] += self.negativekeys[value.lower()]
        return self        

    def report(self):
        print('IPIP Report:')
        for dimension,score in self.score.items():
            rangestr = 'Min: ' + str(self.dimensionranges[dimension]['negative']['total']) + ', Max: ' + str(self.dimensionranges[dimension]['positive']['total']) + ', Mdn: ' + str(self.dimensionranges[dimension]['median'])
            print(' '+dimension,':',score,'['+rangestr+']')

    def exportdata(self):
        return self.score

    def setprofile(self,pid):
        self.score = registerparticipants.DPmProfiles().getprofile(pid).getscaledata(self.name)

    def createtables(self,conn):
        conn.cursor().executescript('''
            DROP TABLE IF EXISTS IPIP50;

            CREATE TABLE IPIP50 (
                pid  TEXT NOT NULL PRIMARY KEY UNIQUE,
                score_openness INTEGER,
                score_conscientiousness INTEGER,
                score_extraversion INTEGER,
                score_agreeableness INTEGER,
                score_emotional_stability INTEGER
             );''')

    def exporttodb(self,conn,pid):
        self.setprofile(pid)

        conn.cursor().execute('''INSERT OR REPLACE INTO 
            IPIP50 (pid, score_openness, score_conscientiousness, score_extraversion, score_agreeableness, score_emotional_stability) 
            VALUES (?, ?, ?, ?, ?, ?)''',
         (pid, self.score['openness'],self.score['conscientiousness'],self.score['extraversion'],self.score['agreeableness'],self.score['emotional_stability']))
        conn.commit()

    def preparecsv(self,pid,IncludeHeader=True):
        self.setprofile(pid)

        headers = ['pid','ipip50_openness','ipip50_conscientiousness','ipip50_extraversion','ipip50_agreeableness','ipip50_emotional_stability']
        rows = [
            [pid,self.score['openness'],self.score['conscientiousness'],self.score['extraversion'],self.score['agreeableness'],self.score['emotional_stability']]
        ]

        return headers,rows

registerscales.DPmScales().registerscale(IPIP50())
