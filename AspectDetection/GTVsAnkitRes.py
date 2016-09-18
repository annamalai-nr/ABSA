import os, json
from pprint import pprint
import numpy as np
GTFName = '/home/annamalai/Desktop/ABSA/2014/Data/LaptopAspTermDict.json'
AnkitResFName = '/home/annamalai/Desktop/ABSA/2014/Data/AnkitCodeLaptopAspTermDict.json'

with open (GTFName) as FH:
    GTDict = json.load(FH)
with open (AnkitResFName) as FH:
    AnkitResDict = json.load(FH)

AspsComparisonPerSent = {}
for Sent in GTDict.keys():
    GTAspects = [Asp.lower() for Asp in GTDict[Sent]]
    AnkitResAspects = [Asp.lower() for Asp in AnkitResDict[Sent]]
    if len (AnkitResAspects) == 1 and 'sorry!!! no aspects' == AnkitResAspects[0]:
        AnkitResAspects = []

    if not GTAspects and not AnkitResAspects:
        P = 1
        R = 1
        F = 1
        TP = []
        FP = []
        FN = []
    else:
        TP = set (GTAspects).intersection(set(AnkitResAspects))
        FN = set(GTAspects) - set (TP)
        FP = set(AnkitResAspects) - set (TP)
        if not TP:
            P = 0
            R = 0
        else:
            P = float (len (TP)) / (len(TP)+len(FP))
            R = float(len(TP)) / (len(TP) + len(FN))
        if 0 == P and 0 == R:
            F = 0
        else:
            F = 2.0*(P*R)/(P+R)
        # AspsComparisonPerSent [Sent] = [P, R, F, GTAspects, AnkitResAspects, TP, FP, FN]
    AspsComparisonPerSent [Sent] = {'P':P, 'R':R, 'F':F, \
                                    'GTAspects':GTAspects, 'AnkitResAspects': AnkitResAspects, \
                                    'TP':list(TP), 'FP':len(FP), 'FN':len(FN)}

pprint (AspsComparisonPerSent)
AllP = np.array([Val['P'] for Key, Val in AspsComparisonPerSent.iteritems()])
AllR = np.array([Val['R'] for Key, Val in AspsComparisonPerSent.iteritems()])
AllF = np.array([Val['F'] for Key, Val in AspsComparisonPerSent.iteritems()])

print AllF.mean ()
print AllP.mean()
print AllR.mean()

with open ('LaptopAspsComparisonPerSentAnkitVsGT.json','w') as FH:
    json.dump(obj=AspsComparisonPerSent, fp=FH,indent=4)
