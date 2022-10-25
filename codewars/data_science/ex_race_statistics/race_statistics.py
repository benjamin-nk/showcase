import datetime
import statistics

# https://www.codewars.com/kata/55b3425df71c1201a800009c

def stat(strg):
    #h|m|s
    strdata = strg.split(',')
    runnerdata = dict()

    num = 1
    for s in strdata:
        if num not in runnerdata: 
            runnerdata[num] = dict()

        ss = s.split('|')
        # 1. convert to seconds so we can calculate totals and then the overall calculate Range, Average, Median of the sample
        runnerdata[num]['h'] = int(ss[0]) * 60 * 60
        runnerdata[num]['m'] = int(ss[1]) * 60
        runnerdata[num]['s'] = int(ss[2])
        runnerdata[num]['total'] = runnerdata[num]['h']+runnerdata[num]['m']+runnerdata[num]['s']

        num +=1

    # 2. Calcuate statistics
    totals = list()
    samplesum = 0
    desc = {}
    for i,case in runnerdata.items():
        samplesum += case['total']
        totals.append(case['total'])
    # desc['stotal'] = str(datetime.timedelta(seconds = samplesum)).replace(':','|')
    desc['average'] = str(datetime.timedelta(seconds = int(samplesum / len(runnerdata)))).replace(':','|')
    totals.sort() # sort from highest to lowest in ascending order
    desc['median'] = str(datetime.timedelta(seconds = int(statistics.median(totals)))).replace(':','|')
    desc['range'] = str(datetime.timedelta(seconds = int(totals[len(totals)-1]-totals[0]))).replace(':','|')

    # 3. Format strings
    for stat,s in desc.items():
        l = s.split('|')
        
        pos = 0
        for s2 in l:
            if len(s2) == 1:
                s2 = '0'+s2 # add 0
                l[pos] = s2 # replace old substring with 0 suffixed
            pos +=1
        
        desc[stat] = ''.join([x+('|') for x in l])[:-1]

    output = "Range: {} Average: {} Median: {}".format(desc['range'],desc['average'],desc['median'])
    
    return output

# print(stat("01|15|59, 1|47|16, 01|17|20, 1|32|34, 2|17|17"))
    # Goal: "Range: 01|01|18 Average: 01|38|05 Median: 01|32|34")

