import os, sys,json
from pprint import pprint
import numpy as np
import nltk.data
from nltk.tokenize import word_tokenize
from time import time
from joblib import Parallel, delayed

def GetLowerTriangle (RowTerm, RowIndex, AspTerms, TokenizedAllSentsInCorpus):
    T0 = time()
    CoOccurRow = np.zeros(len(AspTerms),dtype=int)
    for ColIndex, ColTerm in enumerate(AspTerms):
        if ColIndex == RowIndex:
            # print 'col term: ', ColTerm
            break

        for SentIndex, TokedSent in enumerate(TokenizedAllSentsInCorpus):
            Tokens = TokedSent
            if RowTerm in Tokens and ColTerm in Tokens:
                # print '---'
                # print AllSentsInCorpus[SentIndex]
                # print RowTerm
                # print ColTerm
                CoOccurRow[ColIndex] += 1
                # print '---'
                # raw_input()
    print 'done row index: : {}, row term: {} in {} sec'.format(RowIndex, RowTerm, round (time()-T0,2))
    return CoOccurRow

AspTermsFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_AspTerms.txt'
AspTermsFName = sys.argv[1]
AspTerms = [l.strip() for l in open (AspTermsFName)]
RevFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV.json'
RevFName = sys.argv[2]
with open (RevFName) as FH:
    RevsDict = json.load(FH)
Revs = [V['review_text'] for K,V in RevsDict.iteritems()]
del RevsDict
N = len(Revs)
print 'loaded {} review aspect terms from all {}'.format(len(AspTerms), AspTermsFName)
print 'loaded {} review text from all corpus: {}'.format(N, RevFName)
raw_input('hit any kay to continue ...')
AllSentsInCorpus = []
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
for R in Revs:
    SentsInR = sent_detector.tokenize(R.strip())
    SentsInR = [S.lower() for S in SentsInR]
    AllSentsInCorpus.extend(SentsInR)

TokenizedAllSentsInCorpus = [set(word_tokenize(Sent)) for Sent in AllSentsInCorpus]
print 'tokenized all sentences'

CoOccurMat = []
for RowIndex, RowTerm in enumerate(AspTerms):
    CoOccurRow = GetLowerTriangle (RowTerm, RowIndex, AspTerms, TokenizedAllSentsInCorpus)
    CoOccurMat.append(CoOccurRow)

# CoOccurMat = Parallel(n_jobs=8)(delayed(GetLowerTriangle)(RowTerm, RowIndex, AspTerms, TokenizedAllSentsInCorpus) \
#                                 for RowIndex, RowTerm in enumerate(AspTerms))

CoOccurMat = np.array(CoOccurMat)
for I in xrange (N):
    CoOccurMat[I][I]=1

for RowIndex in xrange(N):
    for ColIndex in xrange(N):
        if ColIndex > RowIndex:
            CoOccurMat[RowIndex][ColIndex] = CoOccurMat[ColIndex][RowIndex]

print 'Co-occurance matrix for each asp term is obtained from {} and its shape: {}'.format(AspTermsFName, CoOccurMat.shape)
OpFName = AspTermsFName.replace('AspTermsAfterRemNonGooglew2v.txt','CoOccurMat.txt')
np.savetxt(fname=OpFName, X=CoOccurMat, fmt='%d')

