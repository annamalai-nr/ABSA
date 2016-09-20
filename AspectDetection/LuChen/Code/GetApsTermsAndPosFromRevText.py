import os, json, sys
from pprint import pprint
from nltk.corpus import stopwords

FName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_GPS.json'
with open (FName) as FH:
    RevDict = json.load(FH)
PasredRev = [V['parsed_review'].split(',') for K, V in RevDict.iteritems()]
CandidateAspTermsPos = set()

POSTagsToLookFor = ['NN', 'NNP', 'JJ']
for PR in PasredRev:
    try:
        for Term in PR:
            AspTerm, POS = Term.split('/')
            if POS in POSTagsToLookFor:
                CandidateAspTermsPos.add ((AspTerm.strip().lower(), POS))
            elif POS.startswith ('VB'):
                CandidateAspTermsPos.add ((AspTerm.strip().lower(), POS))
            else:
                continue
    except:
        pass

CandidateAspTerms = set([Term for Term, Pos in CandidateAspTermsPos])
StopWords = set (stopwords.words('english'))
CandidateAspTerms = CandidateAspTerms - StopWords
# CandidateAspTerms.sort()
# pprint (CandidateAspTerms)
CandidateAspTermsPos = [(Term, Pos) for Term, Pos in CandidateAspTermsPos if Term in CandidateAspTerms]
CandidateAspTermsPos = list(CandidateAspTermsPos)
CandidateAspTermsPos.sort()
pprint(CandidateAspTermsPos)
OpFName = FName.replace('.json','_AspTermsAndPos.txt')
with open (OpFName,'w') as FH:
    for Tup in CandidateAspTermsPos:
        print >>FH, Tup
