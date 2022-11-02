# scale: Creative Achievement Questionnare
# scale source: Carson, S. H., Peterson, J. B., & Higgins, D. M. (2005). Reliability, validity, and factor structure of the creative achievement questionnaire. Creativity research journal, 17(1), 37-50.

import re
import registerscales
import registerparticipants

class CAQ:
    def __init__(self):
        self.name = 'caq'
        self.profiles = dict()
        self.score = dict()
        self.score['global'] = 0
        self.score['visual_arts'] = 0
        self.score['music'] = 0
        self.score['dance'] = 0
        self.score['architectural_design'] = 0
        self.score['creative_writing'] = 0
        self.score['humor'] = 0
        self.score['inventions'] = 0
        self.score['scientific_discovery'] = 0
        self.score['theater_and_film'] = 0
        self.score['culinary_arts'] = 0
        self.domains = {
            'one' : {
                'desc' : 'Above-average KSAO',
                'score' : 0
            },
            'a' : {
                'desc' : 'Visual Arts',
                'score' : 0
            },
            'b' : {
                'desc' : 'Music',
                'score' : 0
            },
            'c' : {
                'desc' : 'Dance',
                'score' : 0
            },
            'd' : {
                'desc' : 'Architectural Design',
                'score' : 0
            },
            'e' : {
                'desc' : 'Creative Writing',
                'score' : 0
            },
            'f' : {
                'desc' : 'Humor',
                'score' : 0
            },
            'g' : {
                'desc' : 'Inventions',
                'score' : 0
            },
            'h' : {
                'desc' : 'Scientific Discovery',
                'score' : 0
            },
            'i' : {
                'desc' : 'Theater and Film',
                'score' : 0
            },
            'j' : {
                'desc' : 'Culinary Arts',
                'score' : 0
            },
            'k' : {
                'desc' : 'Other Creative Achievements',
                'score' : 0
            },
            'three' : {
                'desc' : 'Questions that apply...',
                'score' : 0
            },
        }

    def calculate(self,responsedict):
        templatecolumns = registerscales.DPmScales().getscalecolumns(self.name)
        columns = responsedict.items()
        count = {}
        check = {}
        for key in self.domains:
            # skip one, two three k
            if key in ['one','two','three','k']: continue

            count[key] = 1
            check[key] = 0
            
        for colname in templatecolumns:
            for colname2,value in columns:
                if colname == colname2:
                    if value == '' or value.isspace(): continue
                    # Skip multiplication factor questions
                    # No i need to set this to equal one if no input is given
                    if 'times' in colname: continue
                    # continue skipping one, two, three, and k
                    key = colname.replace('caq_','')
                    if key not in check: continue

                    check[key] += 1

        # Check each domain has been answered, if not = domain['score'] = null
        for key,kcheck in count.items():
            if kcheck != check[key]:
                domain = (self.domains[key]['desc']).lower().replace(' ','_')
                self.score[domain] = registerscales.DPmNullFlags['empty']

        # Calculation:
        for colname in templatecolumns:
            for colname2,value in columns:
                if colname != colname2: continue
                # however if whitespace is given for a question that is asteriks then what? multiply by one. No need?
                if value == '' or value.isspace(): continue

                key = colname.replace('caq_','')
                
                if not (re.search('^caq+_{1}[a-z]{1}$',colname) or colname == 'caq_one' or colname == 'caq_three'): continue

                key = colname.replace('caq_','')
                answernum = re.search('([0-9]).',value)
                answernum = answernum is not None and answernum.groups()[0]

                domain = (self.domains[key]['desc']).lower().replace(' ','_')
                # print('1',key,domain,answernum,value)
                # skip over non of the 10domains for scoring and null domains
                if domain not in self.score or self.score[domain] == registerscales.DPmNullFlags['empty'] : continue

                if key == 'one':
                    # Not included in scoring...
                    continue
                    # self.domains[key]['score'] = len(answer.split(','))
                    # # Search for e.g., '(painting, sculpture)' because it adds another split
                    # if re.search('\(.+,.+\)',answer):
                    #     self.domains[key]['score'] -= 1
                elif key == 'k':
                    # May need to be manually reviewed to add to CAQ domains
                    # Arguably miss out this to maintain psychometric integrity that could be confounded by subjective rating
                    # print('Score other listed creative achievements...:',key)
                    continue
                elif key == 'three':
                    # print('Score sentences that apply...:',key)
                    continue
                else:
                    # This is Step 1 # of the scoring instructions
                    if not value.startswith('*'): 
                        self.score[domain] = int(answernum)
                    # This is Step 2 # of the scoring instructions ('if an item is marked by an asterisk, multiply the number of times the item has been achieved by the number of the qustion to determine poitns for that item.')
                    else: 
                        scalecolumns = registerscales.DPmScales().getscalecolumns(self.name)

                        if responsedict[colname+'_times'] != '':
                            times = responsedict[colname+'_times']
                        else:
                            times = responsedict[colname+'_times_ii']

                        if times == '': times = 1 # Do this incase the participant did not submit a value, so missing value is treated as 1
                        # I could have set a default value of 1 in qualtrics but i don't want to anchor the participant's thinking
                        # print(key,domain,answernum,times)

                        self.score[domain] = int(answernum) * int(times)

        # 1. If i want to make it so that any skipped domains means global score will be INCOMPLETE i can do that here instead of the loop below
        for score in self.score.values():
            if score == registerscales.DPmNullFlags['empty']: continue
            # 2. This loop means that skipped domains will just be treated as 0
            self.score['global'] += score
        
        # If all values of CAQ are null then global must be null. Having it 0 would mess up an analysis.
        # set is 2 because global is included as domain that hasn't been set to null yet
        if registerscales.DPmNullFlags['empty'] in set(self.score.values()) and len(set(self.score.values())) == 2 and self.score['global'] == 0:
            self.score['global'] = registerscales.DPmNullFlags['empty']

        return self

    def report(self,key=None,omitzero=True):
        if key is None:
            print('CAQ Report:')
            print(' Global CAQ Score:',self.score['global'])
            for k,score in self.score:
                print('     Question/Domain:', k)
                print('     Score:', score)
    
    def exportdata(self):
        return self.score

    def setprofile(self,pid):
        self.score = registerparticipants.DPmProfiles().getprofile(pid).getscaledata(self.name)

    # def createtables(self,conn):
    #     conn.cursor().executescript('''
    #         DROP TABLE IF EXISTS CAQ;

    #         CREATE TABLE CAQ (
    #             pid  TEXT NOT NULL PRIMARY KEY UNIQUE,
    #             score INTEGER 
    #          );''')

    # def exporttodb(self,conn,pid):
    #     self.setprofile()

    #     conn.cursor().execute('''INSERT OR REPLACE INTO 
    #     CAQ (pid, score) 
    #     VALUES (?, ?)''', 
    #     (pid, self.score))
    #     conn.commit()

    def preparecsv(self,pid,IncludeHeader=True):
        self.setprofile(pid)

        headers = [
            'pid',
            'caq_visual_arts',
            'caq_music',
            'caq_dance',
            'caq_architectural_design',
            'caq_creative_writing',
            'caq_humor',
            'caq_inventions',
            'caq_scientific_discovery',
            'caq_theater_and_film',
            'caq_culinary_arts',
            'caq_global'
            ]
        rows = [
            [
                pid,
                self.score['visual_arts'],
                self.score['music'],
                self.score['dance'],
                self.score['architectural_design'],
                self.score['creative_writing'],
                self.score['humor'],
                self.score['inventions'],
                self.score['scientific_discovery'],
                self.score['theater_and_film'],
                self.score['culinary_arts'],
                self.score['global']
                ]
        ]

        return headers,rows

registerscales.DPmScales().registerscale(CAQ())

