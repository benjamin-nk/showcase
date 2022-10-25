# scale: Alternative Uses and Instances (AUAI) tasks
# scale source:
# fluency is the number of original items
# originality is determined by manual review; in comparison to other entries or by the user themselves, rank-ordered.

import re
import csv
import registerparticipants
import registerscales

#AUAI is best done by hand. Unless i use it as a prelimary measure which i then go over...
class AUAIFluency:
    def __init__(self):
        self.name = 'auaifluency'
        self.score = {
            'uses': {},
            'instances': {},
            'totals': {
                'uses': {'score':0},
                'instances': {'score':0},
                'overall': {'score':0}
            }
        }

    def calculate(self,responsedict):
        templatecolumns = registerscales.DPmScales().getscalecolumns(self.name)
        columns = responsedict.items()
        # I need to fill this automatically with column names
        # Because uses and instances can have any task name ~ 'knife' and 'noise'
        count = {
            'uses': {},
            'instances': {}
        }
        check = {
            'uses': {},
            'instances': {}
        }
        for colname in templatecolumns:
            if colname.startswith('au'):
                key = 'uses'
                task = colname.replace('au_',"")
            elif colname.startswith('ai'):
                key = 'instances'
                task = colname.replace('ai_',"")

            if task not in count[key]: 
                count[key][task] = 0 
                check[key][task] = 0 
            count[key][task] += 1

        for colname in templatecolumns:
            for colname2,value in columns:
                if colname == colname2:
                    if value == '' or value.isspace(): continue

                    if colname.startswith('au'):
                        key = 'uses'
                        task = colname.replace('au_',"")
                    elif colname.startswith('ai'):
                        key = 'instances'
                        task = colname.replace('ai_',"")

                    check[key][task] += 1

        for tasktype,d in count.items():
            for task,taskcount in d.items():
                # Check if the repsonse has asnwered all uses and instances tasks
                # 2.1 If not then set score for the task (uses/instances) to 'null'
                # 2.2 Set score for tasktype overall to null
                # [NOPE] Still score totals[overall] but we can exclude these cases in analysis
                # For simplicity sake, missing data makes task score null for overall]
                if taskcount != check[tasktype][task]:
                    # *1. Here we have to create the task dictionaries in the format they will be computed later in this function
                    if task not in self.score[tasktype]:
                        self.score[tasktype][task] = {
                            'score': registerscales.DPmNullFlags['empty'],
                            'submission': ''
                        }
                    
                    # ** If i want to, i should include a check for if the some of the tasktype tasks have been complete or not for the correct flat
                    # ** Seeing as i am only using 1 of each task, its not important. 
                    # * All tasks of the type (uses/instances) have not been answered so the score is incomplete
                    self.score['totals'][tasktype] = {
                        'score': registerscales.DPmNullFlags['incomplete']
                    }
        
        # 3. If both total for uses and instances are null then the overall will be null
        if self.score['totals']['uses']['score'] in registerscales.DPmNullFlags.values() and self.score['totals']['instances']['score'] in registerscales.DPmNullFlags.values():
            scoretotals = set((self.score['totals']['uses']['score'],self.score['totals']['instances']['score']))
            # 3.1 if both the totals for uses/instances are empty then make overall empty
            if all(x == registerscales.DPmNullFlags['empty'] for x  in scoretotals):
                self.score['totals']['overall']['score'] = registerscales.DPmNullFlags['empty']
            # 3.2 otherwise its just incomplete
            else:
                self.score['totals']['overall']['score'] = registerscales.DPmNullFlags['incomplete']
                
        # Calcuation:
        for colname in templatecolumns:
            for colname2,value in columns:
                if colname != colname2: continue
                if value == '' or value.isspace(): continue
                # Add calculation here:
                # print('Original string:',str)
                self.original = value
                tasksubmission = value.rstrip()
                key = None

                if colname.startswith('au'):
                    key = 'uses'
                    task = colname.replace('au_',"")
                elif colname.startswith('ai'):
                    key = 'instances'
                    task = colname.replace('ai_',"")

                # Parse for fluency
                lst = list()
                tasksubmission = re.sub(',+',',',tasksubmission)
                tasksubmission = re.sub('%.+',',',tasksubmission)
                if len(tasksubmission) > 0:
                    # Break up items
                    if ',' in tasksubmission:
                        lst = tasksubmission.split(',')
                    else:
                        lst.append(tasksubmission)

                templst = list(lst)
                for item in templst:
                    # Check for repetitions and remove them
                    if lst.count(item) > 1: 
                        lst.remove(item)
                    elif item.isspace() or item == '' or item == ',':
                    # Remove empty cases 
                        lst.remove(item)

                # Enter score into dictionary to retain scores for multiple tasks
                self.score[key][task] = {
                    'score': len(lst),
                    'submission': value
                    }
        # Calculate Totals:
        for tasktype,d in self.score.items():
            if tasktype == 'totals': continue
            
            # *2. (This is later in the function that was refered to earlier)
            for task,d2 in d.items():
                score = d2['score']
                if score in registerscales.DPmNullFlags.values(): continue

                self.score['totals'][tasktype]['score'] += score
        
        for tasktype,d in self.score.items():
            if tasktype == 'totals': continue

            for task,d2 in d.items():
                score = d2['score']
                if score in registerscales.DPmNullFlags.values(): continue

                self.score['totals']['overall']['score'] += score  
        return self         
    
    def report(self):
        print('AUAI Report:')
        for k,d in self.score.items():
            print(' Task Type:', k)
            
            for k2,d2 in d.items():
                print('     Task:', k2)
                print('     Score:', d2['score'])
                # print('Score', d2.score)

    def exportdata(self):
        return self.score

    def setprofile(self,pid):
        self.score = registerparticipants.DPmProfiles().getprofile(pid).getscaledata(self.name)

    def createtables(self,conn):
        conn.cursor().executescript('''
            DROP TABLE IF EXISTS AUAI_Fluency_Total;
            DROP TABLE IF EXISTS AUAI_Fluency_Uses;
            DROP TABLE IF EXISTS AUAI_Fluency_Instances;

            CREATE TABLE AUAI_Fluency_Total (
                pid  TEXT NOT NULL PRIMARY KEY UNIQUE,
                uses  INTEGER,
                instances  INTEGER,
                overall  INTEGER
             );
            CREATE TABLE AUAI_Fluency_Uses (
                pid  TEXT NOT NULL PRIMARY KEY UNIQUE,
                task  TEXT,
                score INTEGER,
                submission TEXT 
             );
            CREATE TABLE AUAI_Fluency_Instances (
                pid  TEXT NOT NULL PRIMARY KEY UNIQUE,
                task  TEXT,
                score INTEGER, 
                submission TEXT 
             );''')

    def exporttodb(self,conn,pid):
        self.setprofile(pid)
        
        for tasktype,d in self.score.items():
            for task,d2 in d.items():
                if tasktype == 'uses':
                    conn.cursor().execute('''INSERT OR REPLACE INTO AUAI_Fluency_Uses (pid, task, score, submission) VALUES (?, ?, ?, ?)''', (pid, task, d2['score'], d2['submission']))
                elif tasktype == 'instances':
                    conn.cursor().execute('''INSERT OR REPLACE INTO AUAI_Fluency_Instances (pid, task, score, submission) VALUES (?, ?, ?, ?)''', (pid, task, d2['score'], d2['submission']))

        conn.cursor().execute('''INSERT OR REPLACE INTO AUAI_Fluency_Total (pid, uses, instances, overall) VALUES (?, ?, ?, ?)''', (pid, self.score['totals']['uses']['score'], self.score['totals']['instances']['score'], self.score['totals']['overall']['score'],))

        conn.commit()

    def preparecsv(self,pid,IncludeHeader=True):
        self.setprofile(pid)
        
        headers = ['pid']
        rows = [
            [pid]
        ]
        for tasktype,d in self.score.items():
            for task,d2 in d.items():
                headers.append('auai_fluency_'+tasktype+'_'+task)
                rows[0].append(d2['score'])

        return headers,rows
        
registerscales.DPmScales().registerscale(AUAIFluency())
# [] Double-checked calculations