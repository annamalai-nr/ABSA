import os, sys, ast, json
# from joblib import Parallel, delayed
from pprint import pprint
from collections import OrderedDict
from time import time

def ProcessSingleFile (FName):
    T0 = time()
    AuthorName = os.path.basename(FName).split('_')[0]
    ListOfDicts = [ast.literal_eval(l.strip()) for l in open (FName).xreadlines() if l.strip()]
    CombinedDict = OrderedDict()
    for Dict in ListOfDicts:
        CombinedDict[Dict['Sentence']] = {'timestamp':Dict['time'], 'aspects':Dict['Aspects'], 'author':AuthorName}

    print 'processed {} within {} sec'.format(FName,round(time()-T0))
    return CombinedDict



def PruneDictToRemoveLongSents (D, SentLenThreshold=2000, NumAspectThreshold=20):
    ReducedD = OrderedDict()
    for Sent, SentInfo in D.iteritems():
        if Sent.startswith('message-id :'): continue #removed this sent
        if len(SentInfo['aspects']) > NumAspectThreshold: continue #removed this sent
        if len(Sent) < SentLenThreshold:
            ReducedD[Sent] = SentInfo

    return ReducedD

def SaveDict (D, OpFName):
    with open(OpFName, 'w') as FH:
        json.dump(D, FH, indent=4)


########################################################################################################################
# main function
########################################################################################################################
TgtDir = '../Data/AnkitSentenceTuples_AsOf6Oct1243'
Files = [os.path.join (TgtDir, F) for F in os.listdir(TgtDir)]
print 'obtained {} files from {} folder for processing'.format (len(Files), TgtDir)

CombinedDict = OrderedDict()
for FName in Files:
    SinglePersonDict = ProcessSingleFile(FName)
    CombinedDict.update(SinglePersonDict)

PrunedDict = PruneDictToRemoveLongSents(CombinedDict)
SaveDict(CombinedDict, OpFName = 'Sentence3Tuple.json')
SaveDict(PrunedDict, OpFName = 'ReducedSentence3Tuple.json')

print 'found a total of {} sentences in the original sentence info dict'.format(len(CombinedDict.keys()))
print 'found a total of {} sentences in the pruned sentence info dict'.format(len(PrunedDict.keys()))


