import sqlite3
import json
import csv
import re


def prettyprint(d):
    print(json.dumps(d,indent=4))

import registerscales
import registerparticipants
from scales.ipip50 import * # Help @ https://stackoverflow.com/questions/15222913/python-imports-from-subfolders and https://stackoverflow.com/questions/29283139/python-from-import
from scales.auaifluency import *
from scales.hmts import *
from scales.cse import *
from scales.caq import *
from scales.custom import *

# I can make the following 3 paragraphs of code into another module so that parsing CSV is not unique to qualitrics
csvfn = "diss_survey_22 October 2022_19.48.csv" # sample data file
csvfh = open(csvfn,encoding='utf-8')

reader = csv.DictReader(csvfh)
headers = dict()
responses = list()

rownum=2 # rownum 1 are the column headers
for row in reader:
    if rownum == 2:
        headers = row
    elif rownum > 3:
        responses.append(row)
    
    rownum+=1

dpmscales = registerscales.DPmScales()

def parseandcompute(model_pid=None,WriteSQL=False):
    for response in responses:
        # Get model responses
        responseid = response['ResponseID']
        print('Model PID:',responseid)

        if responseid != model_pid: continue
        
        for colname,v in response.items():
            custom = [
                'country',
                'age',
                'occupation',
                'sex',
                'gender',
                'EndDate', # submission date (not demographic but important to collect)
                'consent_no_retention',
                'consent_retention'
            ]
            if colname in custom:
                dpmscales.registerscalecolumn(Custom().name,colname)
            elif re.search('^cse_[0-9]$',colname):
                #1/5
                dpmscales.registerscalecolumn(CSE().name,colname)
            elif re.search('^hmts_q[0-9]_m[0-9]$',colname):
                #2/5
                dpmscales.registerscalecolumn(HMTS().name,colname)
            elif re.search('^ipip_fifty_[0-9]+$',colname):
                #3/5
                dpmscales.registerscalecolumn(IPIP50().name,colname)
            elif colname.startswith('au') or colname.startswith('ai'):
                #4/5
                auregex = re.search('^au_[a-zA-Z]+',colname)
                airegex = re.search('^ai_[a-zA-Z]+',colname)

                if (auregex and auregex.group() == colname) or (airegex and airegex.group() == colname):
                    dpmscales.registerscalecolumn(AUAIFluency().name,colname)
            elif colname.startswith('caq') and 'timing' not in colname:
                #5/5
                dpmscales.registerscalecolumn(CAQ().name,colname)

        break

    for response in responses:
        responseid = response['ResponseID']
        if responseid == model_pid: continue # This is because most likely this is manually entered purely for the sake of answering all of the questions

        print('[DPmParse] Processing participant w/ the ID:',responseid)

        profile = registerparticipants.ParticipantProfile(responseid)
        profile.savescaledata(CSE().calculate(response))
        profile.savescaledata(HMTS().calculate(response))
        profile.savescaledata(IPIP50().calculate(response))
        profile.savescaledata(AUAIFluency().calculate(response))
        profile.savescaledata(CAQ().calculate(response))
        profile.savescaledata(Custom().calculate(response))

    if WriteSQL:
        conn = sqlite3.connect('databases/db.sqlite')
        cur = conn.cursor()

        for scale in dpmscales.getscales().values():
            if scale.name == 'caq': continue
            
            print('[DPmParse] Creating tables for the scale:',scale.name)

            scale.createtables(conn)
            # for scale in registerscales.DPmScaleRegister:
            #     if scale == 'caq': continue
                
            #     profile.exporttodb(conn,scale)
        conn.close()


# Model ID required to fill the templates to check for null entries.
parseandcompute('R_30r5r9UEUG8l8ln')

# registerparticipants.DPmProfiles().writecsv('ALL_SCALES','qualitytest',['R_3Dv8kYxq5wn1JaF'])
# registerparticipants.DPmProfiles().writecsv('ALL_SCALES','qualitytest')
registerparticipants.DPmProfiles().writecsv('ALL_SCALES','output')
# registerparticipants.DPmProfiles().writecsv('hmts',csvfn.replace('.csv',''))
# registerparticipants.DPmProfiles().writecsv(['auaifluency','cse','hmts','ipip50'])
# registerparticipants.DPmProfiles().writecsv('ALL_SCALES')


# profile = registerparticipants.DPmProfiles().getprofile('R_30r5r9UEUG8l8ln')
# print(profile.getscaledata('cse'))
# profile.exporttodb(conn,'cse')
# profile.exporttodb(conn,'auaifluency')




