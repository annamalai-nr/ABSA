import os,sys,json,string,nltk
from gensim.models import word2vec
import numpy as np
import networkx as nx
from time import time
from pprint import pprint

def TokenizeWOStem(Sent):
    Sent = Sent.lower()
    SentChars = "".join([ch for ch in Sent if ch not in string.punctuation])
    Tokens = nltk.word_tokenize(SentChars)
    return Tokens

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
    AvgVect = np.mean (Vects)
    if not Avg:
        return Vects
    else:
        return AvgVect

def LoadGoogleNewsW2VModel (ModelFName):
    T0 = time()
    print 'loading {} w2v model ...'.format(ModelFName)
    W2VModel = word2vec.Word2Vec.load_word2vec_format(ModelFName, binary=True)
    print 'loaded w2v model in {} sec.'.format(round(time()-T0,2))
    return W2VModel

def GetAllSentenceTensors(Sentences):
    W2VDims = 300
    SentMaxLen = 0
    GoogleNewsW2VModelFName = '../../../Embeddings/GoolgeNews/GoogleNews-vectors-negative300.bin'
    W2VModel = LoadGoogleNewsW2VModel(GoogleNewsW2VModelFName)

    TokenizedSentences = [TokenizeWOStem(S) for S in Sentences]

    SentMaxLen = max([len(T) for T in TokenizedSentences])
    print 'longest sentence has {} tokens, this is the size of i/p to CNN'.format(SentMaxLen)
    SentenceTensors = [GetSentenceTensor(TokenizedSentences[Index], SentMaxLen, W2VDims, W2VModel)
                       for Index, S in enumerate(Sentences)]
    return SentenceTensors

def Main ():
    SentsAspectsLabelsFName = '../../../2014/Data/RestAspCatABSA.csv'
    Sentences = [''.join(l.strip().split(';')[:-2]).lower() for l in open(SentsAspectsLabelsFName).xreadlines()][:5]
    SentenceTensors = GetAllSentenceTensors(Sentences)
    print 'obtained {} sentence 2D tensors'.format(len(SentenceTensors))

if __name__ == '__main__':
    Main()
