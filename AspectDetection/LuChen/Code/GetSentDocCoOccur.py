import os, json
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from time import time


def Tokenize(Revs, AspectTerms):
    AspectTermsSet = set(AspectTerms)
    AllSentsInCorpus = []
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    for R in Revs:
        R = R.lower()
        SentsInR = sent_detector.tokenize(R.strip()) #list
        RevWordsInSents = [set(word_tokenize(Sent)) for Sent in SentsInR] #list of sets
        RevAspTermsInSents = [AspectTermsSet.intersection(WordsInSent) for WordsInSent in RevWordsInSents] #list of sets
        AllSentsInCorpus.append(RevAspTermsInSents) #list of list of sets
    print 'tokenized and filtered non-aspect terms in every sentence of {} reviews'.format(len(AllSentsInCorpus))

    if len(Revs)  != len (AllSentsInCorpus):
        print 'something wrong in sentence/word/aspect term parsing'
        exit(-1)
    return AllSentsInCorpus

def PopulateSentCoOccurMat (SentCoOccurMat, TokenizedRevs, AspTerms):
    T0 = time()
    for RevAsList in TokenizedRevs:
        for SentAsSet in RevAsList:
            if len(SentAsSet) > 1:
                for Word1 in SentAsSet:
                    for Word2 in SentAsSet:
                        if Word1 == Word2:
                            continue
                        else:
                            Word1AspTermIndex = AspTerms.index(Word1)
                            Word2AspTermIndex = AspTerms.index(Word2)
                            SentCoOccurMat [Word1AspTermIndex,Word2AspTermIndex] += 1
                            # SentCoOccurMat [Word2AspTermIndex,Word1AspTermIndex] += 1
    print 'computed sentence level co occur mat of shape: {} in {} sec'.format(SentCoOccurMat.shape,
                                                                               round(time()-T0))
    return SentCoOccurMat

def PopulateDocSentDashCoOccurMat (DocSentDashCoOccurMat, TokenizedRevs, AspTerms):
    T0 = time()
    for RevIndex, RevAsList in enumerate(TokenizedRevs):
        T00 = time()
        #RevAsList is a list of sets
        for Sent1Index, Sent1AsSet in enumerate(RevAsList):
            for Sent2Index, Sent2AsSet in enumerate(RevAsList):
                if Sent1Index == Sent2Index:
                    continue
                else:
                    for Word1 in Sent1AsSet:
                        for Word2 in Sent2AsSet:
                            if Word1 == Word2:
                                continue
                            else:
                                Word1AspTermIndex = AspTerms.index(Word1)
                                Word2AspTermIndex = AspTerms.index(Word2)
                                DocSentDashCoOccurMat[Word1AspTermIndex,Word2AspTermIndex] += 1
        print 'processed rev # {} in {} sec'.format(RevIndex, round(time()-T00))
    print 'computed doc sent\' cooccur mat of shape: {} in {} sec'.format(DocSentDashCoOccurMat.shape,
                                                                               round(time() - T0))
    return DocSentDashCoOccurMat





########################################################################################################################
#main
########################################################################################################################
AspTermsFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_GPS_AspTermsAfterRemNonGooglew2v.txt'
RevFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_GPS.json'

AspTerms = [l.strip() for l in open (AspTermsFName)]#[:10]
print 'loaded {} aspect terms from {}'.format(len(AspTerms), os.path.basename(AspTermsFName))

SentCoOccurMat = np.zeros (shape=(len(AspTerms),len(AspTerms)), dtype=int)
DocSentDashCoOccurMat = np.zeros (shape=(len(AspTerms),len(AspTerms)),dtype=int)
print 'inited sentence and doc co occur mat to zeros. Their shapes: ', SentCoOccurMat.shape, DocSentDashCoOccurMat.shape

with open (RevFName) as FH:
    RevsDict = json.load(FH)
Revs = [V['review_text'] for K,V in RevsDict.iteritems()]
del RevsDict
N = len(Revs)
print 'loaded {} review texts from {}'.format(N, RevFName)

TokenizedRevs = Tokenize(Revs, AspTerms)

# SentCoOccurMat = PopulateSentCoOccurMat (SentCoOccurMat, TokenizedRevs, AspTerms)
# OpFName = RevFName.replace('.json','_SentCoOccurMat.txt')
# np.savetxt (OpFName, SentCoOccurMat, fmt='%d')

DocSentDashCoOccurMat = PopulateDocSentDashCoOccurMat (DocSentDashCoOccurMat, TokenizedRevs, AspTerms)
OpFName = RevFName.replace('.json','_DocSentDashCoOccurMat.txt')
np.savetxt (OpFName, DocSentDashCoOccurMat, fmt='%d')
