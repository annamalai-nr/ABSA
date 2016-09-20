import os, sys,json
from pprint import pprint
import numpy as np
import nltk.data
from nltk.tokenize import word_tokenize

AspTermsFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_AspTerms.txt'
AspTerms = [l.strip() for l in open (AspTermsFName)]
RevFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV.json'
with open (RevFName) as FH:
    RevsDict = json.load(FH)
Revs = [V['review_text'] for K,V in RevsDict.iteritems()]
del RevsDict
N = len(Revs)
print 'loaded {} review text from all corpus: {}'.format(N, AspTermsFName)
AllSentsInCorpus = []
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
for R in Revs:
    SentsInR = sent_detector.tokenize(R.strip())
    SentsInR = [S.lower() for S in SentsInR]
    AllSentsInCorpus.extend(SentsInR)

TokenizedAllSentsInCorpus = [set(word_tokenize(Sent)) for Sent in AllSentsInCorpus]
print 'tokenized all sentences'

CoOccurMat = []
for RIndex, RowTerm in enumerate(AspTerms):
    print 'processing ', RowTerm
    CoOccurRow = np.zeros (len(AspTerms))
    for Index, ColTerm in enumerate(AspTerms):
        if Index == RIndex: continue
        # print 'col term: ', ColTerm
        for SentIndex, TokedSent in enumerate(TokenizedAllSentsInCorpus):
            Tokens = TokedSent
            if RowTerm in Tokens and  ColTerm in Tokens:
                # print '---'
                # print AllSentsInCorpus[SentIndex]
                # print RowTerm
                # print ColTerm
                CoOccurRow[Index] += 1
                # print '---'
                # raw_input()
    CoOccurMat.append(CoOccurRow)

CoOccurMat = np.array(CoOccurMat)
print 'Co-occurance matrix for each asp term is obtained from {} and its shape: {}'.format(AspTermsFName, CoOccurMat.shape)
OpFName = AspTermsFName.replace('AspTerms.txt','CoOccurMat.txt')
np.savetxt(fname=OpFName, X=CoOccurMat)

