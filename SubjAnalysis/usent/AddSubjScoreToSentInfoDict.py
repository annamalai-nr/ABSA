import json,sys,os
from pprint import pprint
from sentiment import Sentiment
from time import time
from joblib import Parallel, delayed

def GetSubjScoreForSingleSent(SentIndex, Sentence):
    T0 = time()
    try:
        SentAnalyzer = Sentiment()
        ResDict = SentAnalyzer.analyze([Sentence])
        pprint(ResDict)
        SentSentimentPol = {S: {'sentiment':ResDict['sentiments'][I], 'score': ResDict['scores'][I]} for I,S in enumerate(ResDict['sentences'])}
        print 'processed sentence number {} in {} sec'.format(SentIndex, round(time() - T0))
        return SentSentimentPol
    except:
        print 'failed to process sentence number ', SentIndex
        return {}



SentDictFName = '../../CommonAspectFW/Data/ReducedSentence3Tuple.json'
with open (SentDictFName) as FH:
    SentDict = json.load (FH)

print 'loaded a dict with {} sentences'.format(len(SentDict))

# for SentIndex, Sent in enumerate(SentDict.iterkeys()):
#     SentDict[Sent]['subj_analysis_res'] = GetSubjScoreForSingleSent(SentAnalyzer, SentIndex,Sent)

SentenceAsKeys = SentDict.keys()[:100]
SentenceSubjResList = Parallel(n_jobs=8)(delayed(GetSubjScoreForSingleSent)(SentIndex, Sent) \
                                          for SentIndex, Sent in enumerate(SentenceAsKeys))
for Index, Sent in enumerate(SentenceAsKeys):
    SentDict[Sent]['subj_analysis_res'] = SentenceSubjResList[Index]

with open ('Tmp.json','w') as FH:
    json.dump (SentDict,FH, indent=4)