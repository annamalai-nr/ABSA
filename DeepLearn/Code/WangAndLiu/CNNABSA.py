import os,sys,json,string,nltk
from gensim.models import word2vec
import numpy as np
import networkx as nx
from time import time
from pprint import pprint

groucho_grammar = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP | 'I' | NUM N
VP -> V NP | VP PP
Det -> 'an' | 'my'
N -> 'elephant' | 'pajamas' | 'elephants'
V -> 'shot'
P -> 'in'
NUM -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10'
""")
parser = nltk.ChartParser(groucho_grammar)

def GetParseTree (Tokens):
    for tree in parser.parse(Tokens):
        print(tree)

def TokenizeWOStem(Sent):
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

def GetWAvgSentenceVector (SentArray, Weights = None):
    if not Weights: return np.mean (SentArray)

    WVectors = []
    for Index, W in enumerate(Weights):
        WVec = W * SentArray[Index,:]
        WVectors.append(WVec)
    WVectors = np.array (WVectors)
    WAvgVector = np.mean (WVectors)
    return WAvgVector

def LoadGoogleNewsW2VModel (ModelFName):
    T0 = time()
    print 'loading {} w2v model ...'.format(ModelFName)
    W2VModel = word2vec.Word2Vec.load_word2vec_format(ModelFName, binary=True)
    print 'loaded w2v model in {} sec.'.format(round(time()-T0,2))
    return W2VModel

def Main():
    NSamples = 100
    W2VDims = 300
    SentMaxLen = 0
    W2VModel = None

    SentsAspectsLabelsFName = '../../2014/Data/RestAspCatABSA.csv'
    GoogleNewsW2VModelFName = '../../Embeddings/GoolgeNews/GoogleNews-vectors-negative300.bin'
    Sentences = [''.join(l.strip().split(';')[:-2]).lower() for l in open(SentsAspectsLabelsFName).xreadlines()][:NSamples]
    Aspects = [''.join(l.strip().split(';')[-2]) for l in open(SentsAspectsLabelsFName).xreadlines()][:NSamples]
    Labels = [''.join(l.strip().split(';')[-1]) for l in open(SentsAspectsLabelsFName).xreadlines()][:NSamples]

    print 'loaded {} sentences, {} aspects and {} labels'.format(len(Sentences), len(Aspects), len(Labels))

    W2VModel = LoadGoogleNewsW2VModel(GoogleNewsW2VModelFName)
    TokenizedSentences = [TokenizeWOStem(S) for S in Sentences]
    SentMaxLen = max([len(T) for T in TokenizedSentences])
    print 'longest sentence has {} tokens, this is the size of i/p to CNN'.format(SentMaxLen)
    SentenceTensors = [GetSentenceTensor(TokenizedSentences[Index], SentMaxLen, W2VDims, W2VModel)
                       for Index, S in enumerate(Sentences)]


if __name__ == '__main__':
    Main()