DPmNullFlags = {
    'empty': 'NULL_EMPTY', # Single/Set Question - No data supplied required for calculating score
    'incomplete': 'NULL_INCOMPLETE' # Minor set of questions - Incomplete data supplied required calculating for score
}
DPmScaleRegister = dict()
DPmScaleColumnRegister = dict()

class DPmScales(): #Dissertation Psychometrics Scales
    # def __init__(self):
    #     self.scales = DPmScaleRegister

    def getlist(self):
        l = list()

        for k in DPmScaleRegister:
            l.append(k)

        return l

    def getscales(self):
        return DPmScaleRegister

    def getscalecolumns(self,scale_name):
        return DPmScaleColumnRegister[scale_name]

    def registerscale(self,scale_object):
        DPmScaleRegister[scale_object.name] = scale_object
        DPmScaleColumnRegister[scale_object.name] = list()
        self.scale = DPmScaleRegister
        print('[DPmScales] Registered scale:',scale_object.name)

    def registerscalecolumn(self,scale_name,col):
        if col not in DPmScaleColumnRegister[scale_name]:
            DPmScaleColumnRegister[scale_name].append(col)
        elif col in DPmScaleColumnRegister[scale_name]:
            print('[DPmScales] This column('+col+')already exists in the scale:',scale_name)

    def createtables(self,name):
        DPmScaleRegister[name].createtables()