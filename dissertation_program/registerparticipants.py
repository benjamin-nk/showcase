import registerscales
import csv
import os

DPmParticipantRegister = dict() #Dissertation Psychometrics Participant Register

class ParticipantProfile():
    def __init__(self,pid=None):
        self.pid = pid
        if pid is not None and pid in DPmParticipantRegister:
            self.profile = DPmParticipantRegister[pid]
        else:
            self.profile = dict()

    def updateprofiles(self):
        DPmParticipantRegister[self.pid] = self.profile

    def setpid(self,pid):
        self.pid = pid

        self.updateprofiles()

    def getpid(self,pid):
        return self.pid

    def savescaledata(self,scale_object):
        self.profile[scale_object.name] = scale_object.exportdata()
        
        self.updateprofiles()

    def setscaledata(self,scale,data):
        self.profile[scale] = data
        
        self.updateprofiles()

    def getscaledata(self,scale=None):
        try:
            return self.profile[scale]
        except:
            if scale not in registerscales.DPmScaleRegister:
                print('Error: the scale ('+scale+') does not exist.')
            else:
                print('Error: the data for scale ('+scale+') does not exist for participant',self.pid)
            
            return {}

    def exporttodb(self,conn,scale):
        registerscales.DPmScales().getscales()[scale].exporttodb(conn,self.pid)

    def preparecsv(self,scale,IncludeHeader):
        return registerscales.DPmScales().getscales()[scale].preparecsv(self.pid,IncludeHeader)

class DPmProfiles(): #Dissertation Psychometrics Profiles
    def __init__(self):
        self.profiles = DPmParticipantRegister

    # Runs into manipulation of indivdiual profiles including exporting their data independentally
    def getprofile(self,pid):
        return ParticipantProfile(pid)

    def getprofiles(self):
        self.profiles = DPmParticipantRegister

        return self.profiles

    def writecsv(self,input_variable=None,prefix=None,responselist=None):
        self.getprofiles()

        csvheaders = list()
        csvrows = list()
        
        # os.mkdir('scales_profiles') 
        scales = list()       
        # if input_variable == 'ALL_SCALES' or type(input_variable) == type(list()):
        if input_variable == 'ALL_SCALES':
            scales = registerscales.DPmScales().getlist()
        elif type(input_variable) == type(list()):
            scales = input_variable
        elif input_variable in registerscales.DPmScales().getlist():
            scales = [input_variable]
        scales.sort()

        if len(scales) == 0: 
            print('WHY IS HTIS HAPPENIN?')
            pass
            
        fileid = ''
        scalecount = 1
        for scale in scales:
            AppendedHeaders = False
            AppendedRows = False
            # profile count
            pcount = 1
            for pid in self.profiles:
                profile = self.getprofile(pid)
                if responselist and profile.pid not in responselist: continue
                # Get the preparecsv data to append to the file
                csvdata = profile.preparecsv(scale,(pcount>1 and False))
                    
                # Set down first scale's headers and rows from first profile
                if pcount == 1 and scalecount == 1:
                    fileid = scale

                    # This is why when we prepare csv we put a list within a list, so that we can just append new rows per participant
                    # Here is where we begin our csv
                    # Following loops (profiles) must append their data
                    csvheaders, csvrows = csvdata
                else:
                    # Set down the following scales' headers and rows, also from the first profile
                    if pcount == 1 and scalecount > 1 and AppendedHeaders is False:
                        fileid = fileid+'_'+scale
                        
                        del csvdata[0][0] # remove pid header - not needed because first scale gave it
                        for header in csvdata[0]: #csvdata[0] is headers of the new profile
                            csvheaders.append(header)
                        
                        AppendedHeaders = True
                        
                        # if scalecount > 1:

                    
                    # i can comment this if i want ot check alignments
                    # alignments might get fucked up when there are missing entries
                    if scalecount > 1:
                        del csvdata[1][0][0] # remnove pid - not needed because the profiles will have given this with first entry
                    
                    for wrow in csvdata[1]:
                        if scalecount > 1:
                            #append row where pid = pid
                            pos = 0
                            for arow in csvrows:
                                # print(pid,'look',scale,wrow,arow)
                                if arow[0] == pid:
                                    # print('gotcha',pos,pid)
                                    for field in wrow:
                                        csvrows[pos].append(field)

                                    pcount +=1
                                    break

                                pos +=1

                            # I need to fill in missing values with NULL to keep from fucking up the csv
                        else:
                            csvrows.append(wrow) # returns the list within the list
                pcount += 1

            AppendedHeaders = False
            scalecount += 1

        # Count the entries
        csvheaders.insert(0,'i')
        pos=0
        for _ in csvrows:
            csvrows[pos].insert(0,pos+1)
            pos+=1

        fn = 'scales_profiles/'+(prefix and prefix+'_' or '')+fileid+'.csv'
        fh = open(fn,'w',newline='')
        csvwriter = csv.writer(fh)
        csvwriter.writerow(csvheaders)
        csvwriter.writerows(csvrows)
        fh.close()