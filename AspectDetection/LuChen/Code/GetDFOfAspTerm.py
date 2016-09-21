import os, sys, json
import nltk
from nltk.tokenize import word_tokenize
from pprint import pprint
from collections import OrderedDict

AspTermsFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_GPS_AspTermsAfterRemNonGooglew2v.txt'
# AspTermsFName = sys.argv[1]
AspTerms = [l.strip() for l in open (AspTermsFName)]
print 'loaded {} aspect terms from {}'.format(len(AspTerms), AspTermsFName)

RevFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_GPS.json'
# RevFName = sys.argv[2]
with open (RevFName) as FH:
    RevsDict = json.load(FH)
Revs = [V['review_text'] for K,V in RevsDict.iteritems()]#[:100]
del RevsDict
print 'loaded {} reviews from {}'.format(len(Revs), RevFName)
# raw_input('hit any key to cont...')

AllRevSents = []
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
for R in Revs:
    SentsInR = sent_detector.tokenize(R.strip())
    SentTokens = [word_tokenize(S.lower()) for S in SentsInR]
    AllRevSents.append(SentTokens)

del Revs

AspTermDFs = OrderedDict()
for T in AspTerms:
    DF = 0
    for RevDocSentTokens in AllRevSents:
        Found = False
        for OneSentTokens in RevDocSentTokens:
            Tokens = set(OneSentTokens)
            if T in Tokens:
                Found = True
                break
        if Found:
            DF += 1
    print 'DF of {}: {}'.format(T, DF)
    AspTermDFs[T] = DF

# pprint (AspTermDFs)
# print len (AspTermDFs)
OpFName = AspTermsFName.replace('AspTermsAfterRemNonGooglew2v.txt','AspTermsDFs.json')
with open (OpFName,'w') as FH:
    json.dump(obj=AspTermDFs, fp=FH, indent=4)



