import os,sys,json,string,nltk
from gensim.models import word2vec
import numpy as np
import networkx as nx
from time import time
from pprint import pprint
from GetSentenceVectors import GetSentenceTensor, GetScaledSentenceTensor
import math
from copy import deepcopy

def LoadGoogleNewsW2VModel (ModelFName):
    T0 = time()
    print 'loading {} w2v model ...'.format(ModelFName)
    W2VModel = word2vec.Word2Vec.load_word2vec_format(ModelFName, binary=True)
    print 'loaded w2v model in {} sec.'.format(round(time()-T0,2))
    return W2VModel

def TokenizeWOStem(Sent):
    Sent = Sent.lower()
    SentChars = "".join([ch for ch in Sent if ch not in string.punctuation])
    Tokens = nltk.word_tokenize(SentChars)
    return Tokens

def GetMaxSentLen (TokenizedSentences):
    return max([len(T) for T in TokenizedSentences])

def GetSentenceToNxGraphDict (Sentences, CoreNLPParsedSents):
    SentenceToNxGraphDict = {}
    for S in Sentences:
        if S in SentenceToNxGraphDict.keys(): continue
        SentProcessed = False
        for SentCoreNLPInfoList in CoreNLPParsedSents:
            if SentProcessed: break
            if not SentCoreNLPInfoList: continue
            for SentCoreNLPDict in SentCoreNLPInfoList['sentences']:
                CoreNLPSent = SentCoreNLPDict['text']
                if CoreNLPSent == S:
                    G = nx.Graph();G.add_edges_from(SentCoreNLPDict['NxGraphEdges'])
                    SentenceToNxGraphDict[S] = deepcopy(G)
                    SentProcessed = True
                    break
    return SentenceToNxGraphDict

def GetHtAndUniqWordLabeledTokedSent (TokedSent):
    ReLabeledTokedSent = []
    for Index, W in enumerate(TokedSent):
        PrevWords = TokedSent[:Index]
        CountOfWSoFar = PrevWords.count(W)
        ReLabeledTokedSent.append('1_'+W+'_'+str(CountOfWSoFar+1))
    return ReLabeledTokedSent

def GetDistIJAndProbIJ (TokedSent, WOrg, TreeHt, G):
    DistIJs = {}
    ProbIJs = {}
    for IndexI, WordI in enumerate(TokedSent):
        for WordJ in TokedSent:
            if WordI == WordJ:
                DistIJs[(WordI, WordJ)] = 0
                ProbIJs[(WordI, WordJ)] = 1 + WOrg[IndexI]
            else:
                try:
                    ShortesPath = nx.shortest_path(G, WordI, WordJ)
                    DistIJs[(WordI, WordJ)] = len(ShortesPath) - 2
                except:
                    # print 'one of the words {} or {} is NOT present in parse tree' \
                    #       ', hence using maximum height of the tree as distance'.format(WordI, WordJ)
                    DistIJs[(WordI, WordJ)] = TreeHt  # make maximum height
                Frac = float(DistIJs[(WordI, WordJ)] * DistIJs[(WordI, WordJ)]) / (2 * TreeHt)
                ProbIJs[(WordI, WordJ)] = WOrg[IndexI] * math.exp(-Frac)
    return DistIJs, ProbIJs

def GetHtAndUniqWordLabeledAspTerm (ATerms, TokedSent):
    ATermsWithHtAnduniqCount = []
    for AT in ATerms:
        for W in TokedSent:
            if AT in W:
                ATermsWithHtAnduniqCount.append(W)
    return ATermsWithHtAnduniqCount

def GetWeightsAccToAspTerms (TokedSent, ATerms, ParseTreeNxGraph):
    ATerms = TokenizeWOStem(ATerms)
    G = ParseTreeNxGraph
    TreeHt = int(G.neighbors('ROOT')[0].split('_')[0])
    TokedSent = GetHtAndUniqWordLabeledTokedSent (TokedSent)
    ATerms = GetHtAndUniqWordLabeledAspTerm (ATerms, TokedSent)
    UniformPVal = 1.0/len(ATerms)
    WOrg = [UniformPVal if W in ATerms else 0 for W in TokedSent]
    DistIJs, ProbIJs = GetDistIJAndProbIJ(TokedSent, WOrg, TreeHt, G)
    WMod = [sum([ProbIJs[(WordI, WordJ)] for WordI, WordJ in ProbIJs.keys() if W == WordJ]) for W in TokedSent]
    del DistIJs, ProbIJs
    # pprint (WOrg)
    # pprint ([round(elem, 2) for elem in WMod])
    WModMean = float(np.array (WMod).mean())
    WMod = [X/WModMean for X in WMod]
    # pprint ([round(elem, 2) for elem in WMod])
    MinVal = min (WMod); MaxVal = max (WMod); ToMin = 0.7; ToMax = 1.3;ToDiff = ToMax - ToMin
    WModNormalized = [(((ToDiff)*(X-MinVal))/(MaxVal-MinVal))+ToMin for X in WMod]
    # pprint ([round(elem, 2) for elem in WModNormalized])
    return WModNormalized


def Main():
    NSamples = -1

    #1 load sentences, aspect terms and sentiment labels
    SentsAspectsLabelsFName = '../../../2014/Data/RestAspTermABSA.csv'
    Sentences = [''.join(l.strip().split(';')[:-2]).lower() for l in open(SentsAspectsLabelsFName).xreadlines()][:NSamples]
    AspectTerms = [''.join(l.strip().split(';')[-2]) for l in open(SentsAspectsLabelsFName).xreadlines()][:NSamples]
    Labels = [''.join(l.strip().split(';')[-1]) for l in open(SentsAspectsLabelsFName).xreadlines()][:NSamples]
    print 'loaded {} sentences, {} aspects and {} labels'.format(len(Sentences), len(AspectTerms), len(Labels))

    CoreNLPParsedFName = '../../Data/CoreNLPParsed.ParseTreeConvertedAsNxGraph.json'
    with open(CoreNLPParsedFName) as FH:
        CoreNLPParsedSents = json.load(FH)
    print 'loaded {} sentences that are pased by core nlp'.format(len(CoreNLPParsedSents))

    SentenceToNxGraphDict = GetSentenceToNxGraphDict (Sentences, CoreNLPParsedSents)
    del CoreNLPParsedSents
    print 'out of total {} sentences, loaded nx graph edges for {} sentences'.format(len(set(Sentences)),
                                                                                     len(SentenceToNxGraphDict))
    #2 tokenize each sentence
    TokenizedSentences = [TokenizeWOStem(S) for S in Sentences]
    print 'tokenized sentences'
    SentMaxLen = GetMaxSentLen (TokenizedSentences)
    print 'max sentence lenght found across all sentences (size of sentence tensor): ', SentMaxLen

    # 3 w2v model load
    GoogleNewsW2VModelFName = '../../../Embeddings/GoolgeNews/GoogleNews-vectors-negative300.bin'
    W2VModel = LoadGoogleNewsW2VModel(GoogleNewsW2VModelFName)
    W2VDims = 300

    # UnscaledSentenceTensors = GetAllSentenceTensors(TokenizedSentences, SentMaxLen, W2VModel, W2VDims)
    # print 'obtained {} sentence 2D tensors'.format(len(UnscaledSentenceTensors))

    UnScaledX = []
    ScaledX = []
    Y = []
    for SentIndex, TokedSent in enumerate(TokenizedSentences):
        T0 = time()
        ATerms = AspectTerms[SentIndex]
        Sent = Sentences[SentIndex]
        try:
            ParseTreeNxGraph = SentenceToNxGraphDict[Sent]
            ATermWts = GetWeightsAccToAspTerms (TokedSent, ATerms, ParseTreeNxGraph)
        except:
            ATermWts = [1.0 for W in TokedSent]

        UnScaledSentenceTensor = GetSentenceTensor (TokedSent, SentMaxLen, W2VDims, W2VModel, Avg= False)
        ScaledSentenceTensor = GetScaledSentenceTensor (UnScaledSentenceTensor, ATermWts)

        #for save
        OrgDims = UnScaledSentenceTensor.shape[0]*UnScaledSentenceTensor.shape[1]
        UnScaledSentenceTensor = UnScaledSentenceTensor.reshape(1,OrgDims)
        ScaledSentenceTensor = ScaledSentenceTensor.reshape(1,OrgDims)
        UnScaledX.append(UnScaledSentenceTensor)
        ScaledX.append(ScaledSentenceTensor)
        Y.append(Labels[SentIndex])

        print 'proced sent: {} in {} sec.'.format(SentIndex, time()-T0)

    UnScaledX = np.array (UnScaledX)
    ScaledX = np.array(ScaledX)
    CurShape = UnScaledX.shape
    UnScaledX = UnScaledX.reshape(CurShape[0],CurShape[-1])
    ScaledX = ScaledX.reshape(CurShape[0],CurShape[-1])

    np.savetxt (fname='UnscaledX.txt',X = UnScaledX)
    np.savetxt (fname='ScaledX.txt',X = ScaledX)
    with open('Y.txt', 'w') as FH:
        for y in Y:
            print>> FH, y

if __name__ == '__main__':
    Main()
