import os, json
from pprint import pprint
import numpy as np, re
GTFName = '/home/annamalai/Desktop/ABSA/2014/Data/Restaurants_Test_Data_phaseB.xml.term-polarity.json'
AnkitResFName = '/home/annamalai/Desktop/ABSA/2014/Data/AnkitCodeRestaurantAspTermDict_SemEvalTest.json'

with open (GTFName) as FH:
    GTDict = json.load(FH)
with open (AnkitResFName) as FH:
    AnkitResDict = json.load(FH)

Tmp = {}
for K,V in AnkitResDict.iteritems():
    NewK = re.sub('[\W_]', '', K)
    Tmp[NewK]=V
AnkitResDict = Tmp

AspsComparisonPerSent = {}
for Key in GTDict.keys():
    Sent = GTDict[Key]['Sentence']
    GTAspects = [Asp.lower() for Asp in GTDict[Key]['TermAndPolarity']['Term']]
    AnkitDictKey = re.sub('[\W_]', '', Sent).lower()
    if AnkitDictKey not in AnkitResDict.keys():
        print 'Ankit\'s code didnt process sent: ', Sent
        continue
    AnkitResAspects = [Asp.lower().strip() for Asp in AnkitResDict[AnkitDictKey]]
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

with open ('AnkitCodeRestaurantAspTermDict_SemEvalTest_AnkitVsGT.json','w') as FH:
    json.dump(obj=AspsComparisonPerSent, fp=FH,indent=4)
