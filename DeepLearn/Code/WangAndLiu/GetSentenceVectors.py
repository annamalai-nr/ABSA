import os,sys,json,string,nltk
import numpy as np
from time import time
from pprint import pprint


def GetSentenceTensor (Tokens, SentMaxLen, W2VDims, W2VModel, Avg= False):
    PadSize = SentMaxLen
    Vects = np.zeros ((PadSize,W2VDims))
    for Index, T in enumerate(Tokens):
        try:
            Vec = W2VModel[T].reshape (1,W2VDims)
            Vects[Index] = np.array (Vec) #copy row to Vects
        except:
            print 'unable to find the google news vec for word: ', T
            continue
    Vects = np.array (Vects)
    if not Avg:
        return Vects
    else:
        AvgVect = np.mean(Vects)
        return AvgVect



def GetAllSentenceTensors(TokenizedSentences, SentMaxLen, W2VModel, W2VDims=300):
    print (len (TokenizedSentences))
    print SentMaxLen
    print W2VModel
    print W2VDims
    raw_input()
    print 'longest sentence has {} tokens, this is the size of i/p to CNN'.format(SentMaxLen)
    SentenceTensors = [GetSentenceTensor(TS, SentMaxLen, W2VDims, W2VModel)
                       for Index, TS in enumerate(TokenizedSentences)]
    return SentenceTensors

def Main ():
    # SentsAspectsLabelsFName = '../../../2014/Data/RestAspCatABSA.csv'
    # Sentences = [''.join(l.strip().split(';')[:-2]).lower() for l in open(SentsAspectsLabelsFName).xreadlines()][:5]
    # SentenceTensors = GetAllSentenceTensors(Sentences)
    # print 'obtained {} sentence 2D tensors'.format(len(SentenceTensors))
    print 'add test code here'

if __name__ == '__main__':
    Main()
