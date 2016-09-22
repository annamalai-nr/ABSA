import os,sys, json
from ast import literal_eval
from collections import OrderedDict
from copy import deepcopy
from pprint import pprint
import numpy as np
from ClusterHelper import GetClustDist, GetNounAvailStatus, GetClosestCluster

def GetDFAndPosForAspTerms (AspTerms, AspTermsFNameDFName, AspTermsPosFName, SentCoOccruFName,
                            SimGFName, SimTFName, SimGTFName,
                            WG, WT, WGT):
    with open (AspTermsFNameDFName) as FH:
        AspTermsFNameDFDict = json.load(FH)
        
    AspTermsPosTuple = [literal_eval(l.strip()) for l in open (AspTermsPosFName).xreadlines()]
    
    AspTermsPosDict = {}
    for Term, PosTag in AspTermsPosTuple:
        AspTermsPosDict.setdefault(Term,[]).append(PosTag)
    del AspTermsPosTuple
    AspTermsInfoDict = {}
    for TermIndex, Term in enumerate(AspTerms):
        AspTermsInfoDict[Term] = {}
        AspTermsInfoDict[Term]['TermIndex'] = TermIndex
        AspTermsInfoDict[Term]['DF'] = AspTermsFNameDFDict[Term]
        AspTermsInfoDict[Term]['POS'] = set(AspTermsPosDict[Term])


    SimG = np.loadtxt(SimGFName)
    SimT = np.loadtxt(SimTFName)
    # SimGT = np.loadtxt(SimGTFName)
    SimGT = np.maximum(SimG, SimT)
    Sim = WG*SimG + WT*SimT + WGT*SimGT

    # print Sim.max()
    # print Sim.min()
    # raw_input()
    SentCoOccr = np.loadtxt (SentCoOccruFName)

    for Index, Term in enumerate(AspTerms):
        # AspTermsInfoDict[Term]['G'] = SimG[Index,:]
        # AspTermsInfoDict[Term]['T'] = SimT[Index,:]
        # AspTermsInfoDict[Term]['GT'] = SimGT[Index,:]
        AspTermsInfoDict[Term]['Sim'] = Sim[Index,:]

        AspTermsInfoDict[Term]['SentCoOccurance'] = SentCoOccr[Index,:]

    return AspTermsInfoDict

def GetSeedTerms (AspTermsDFPosDict, NumSeeds):
    TupleList = [(DFPosDict['DF'], Term) for Term, DFPosDict in AspTermsDFPosDict.iteritems()]
    TupleList.sort()
    TupleList.reverse()
    MostFreqSeedTerms = [Tup[1] for Tup in TupleList[:NumSeeds]]
    return MostFreqSeedTerms


def Mergable(Clusters, AspTermsInfoDict, Delta):
    for RInd, RowClust in enumerate(Clusters):
        for CInd, ColClust in enumerate(Clusters):
            if RInd > CInd: #jus process lower triangle
                IsNounAvail = GetNounAvailStatus(RowClust, ColClust, AspTermsInfoDict)
                if not IsNounAvail:
                    continue

                ClustDist = GetClustDist (RowClust, ColClust, AspTermsInfoDict)
                if ClustDist > Delta:
                    continue

                #3rd const to code yet
                return True
    return False



def MergeSeedClusters (SeedClusters, AspTermsInfoDict, Delta):
    Clusters = deepcopy(SeedClusters)
    while (Mergable(Clusters, AspTermsInfoDict, Delta)):
        print 'mergable clusters found'
        ClosestClustTuple, ClosestDist = GetClosestCluster (Clusters, AspTermsInfoDict)
        print '*'*10
        print 'closest cluster pair: {} and their dist: {}'.format(ClosestClustTuple, ClosestDist)
        print '*' * 10
        # raw_input()
        Clusters.remove(ClosestClustTuple[0])
        Clusters.remove(ClosestClustTuple[1])
        NewClust = ClosestClustTuple[0].union(ClosestClustTuple[1])
        # print 'New cluster: ', NewClust
        Clusters.append(NewClust)
        # raw_input()

    return Clusters

AspTermsFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_AspTermsAfterRemNonGooglew2v.txt'
AspTermsFNameDFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_AspTermsDFs.json'
AspTermsPosFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_AspTermsAndPos.txt'
SimGFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/SimMats/reviews_TV_SimG.txt'
SimTFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/SimMats/reviews_TV_SimT.txt'
SimGTFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/SimMats/reviews_TV_SimGT.txt'
SentCoOccruFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/SimMats/reviews_TV_CoOccurMat.txt'
# Params = {'s':500, 'k':50, 'delta':0.8, 'wg':0.2,'wt':0.2,'wgt':0.6}
Params = {'s':500, 'k':50, 'delta':0.2, 'wg':0.1,'wt':0.3,'wgt':0.6}

AspTerms = [l.strip() for l in open (AspTermsFName)]

AspTermsInfoDict = GetDFAndPosForAspTerms (AspTerms, AspTermsFNameDFName, AspTermsPosFName,
                                           SimGFName, SimTFName, SimGTFName, SentCoOccruFName,
                                           Params['wg'], Params['wt'], Params['wgt'])
# pprint (AspTermsInfoDict)
# raw_input()

C1 = set(['going', 'nice', 'think', 'want', 'know'])
C2 = set(['good'])
GetClustDist(C1, C2, AspTermsInfoDict)


SeedTerms = GetSeedTerms (AspTermsInfoDict, Params['s'])
Clusters = [set() for I in xrange(Params['s'])]
for I in xrange (Params['s']):
    Clusters[I].add(SeedTerms[I])
pprint (Clusters)
Clusters = MergeSeedClusters (Clusters, AspTermsInfoDict, Params['delta'])
pprint (Clusters)
