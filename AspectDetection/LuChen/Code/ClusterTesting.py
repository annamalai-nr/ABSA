import os,sys, json
from ast import literal_eval
from collections import OrderedDict
from copy import deepcopy
from pprint import pprint
import numpy as np
from ClusterHelper import GetClustDist, GetNounAvailStatus, GetClosestMergableCluster, GetSentCoOccurSignificance

def GetDFAndPosForAspTerms (AspTerms, AspTermsDFName, AspTermsPosFName,
                            SentCoOccruFName, DocCoOccurFName,
                            SimGFName, SimTFName, SimGTFName,
                            WG, WT, WGT):
    with open (AspTermsDFName) as FH:
        AspTermsDFDict = json.load(FH)
    print 'loaded asp terms DF for {} asp terms from {}'.format (len (AspTerms), os.path.basename(AspTermsDFName))
    if len (AspTermsDFDict.keys()) != len(AspTerms):
        print 'the number of aspect terms in the DF dict (loaded from:{}) is different from the number of asp terms'.\
            format(AspTermsDFName)
        print '# of asp terms', len(AspTerms)
        print '# of asp terms from DF dict file', len(AspTermsDFDict.keys())
        print 'exiting...'
        sys.exit(-1)
        
    AspTermsPosTuple = [literal_eval(l.strip()) for l in open (AspTermsPosFName).xreadlines()]
    print 'loaded {} asp terms POS tags from {}'.format(len(AspTermsPosTuple), os.path.basename(AspTermsPosFName))

    AspTermsPosDict = {}
    for Term, PosTag in AspTermsPosTuple:
        AspTermsPosDict.setdefault(Term,[]).append(PosTag)
    del AspTermsPosTuple

    # if len(AspTermsPosDict.keys()) != len(AspTerms):
    #     print 'the number of aspect terms in the POS dict (loaded based on {}) is different from the number of asp terms'. \
    #         format(AspTermsPosFName)
    #     print '# of asp terms', len(AspTerms)
    #     print '# of asp terms from pos tags file', len (AspTermsPosDict.keys())
    #     print 'exiting...'
    #     sys.exit(-1)

    AspTermsInfoDict = {}
    for TermIndex, Term in enumerate(AspTerms):
        AspTermsInfoDict[Term] = {}
        AspTermsInfoDict[Term]['TermIndex'] = TermIndex
        AspTermsInfoDict[Term]['DF'] = AspTermsDFDict[Term]
        AspTermsInfoDict[Term]['POS'] = set(AspTermsPosDict[Term])

    print 'added term index, DF and POS info to the aspect term dict'

    SimG = np.loadtxt(SimGFName)
    SimT = np.loadtxt(SimTFName)
    # SimGT = np.loadtxt(SimGTFName)
    SimGT = np.maximum(SimG, SimT)
    print 'loaded simg, simt and simgt matrices of shape', SimG.shape, SimT.shape, SimGT.shape
    print 'min and max values of each matrices', ((SimG.min(), SimG.max()), (SimT.min(), SimT.max()), (SimGT.min(), SimGT.max()))
    Sim = WG*SimG + WT*SimT + WGT*SimGT
    print 'computed sim matrix from simg, simt and simgt of shape', Sim.shape
    print 'sim matrix min and max vlaues', Sim.min(), Sim.max()

    SentCoOccur = np.loadtxt (SentCoOccruFName)
    DocSentDashCoOccur = np.loadtxt (DocCoOccurFName)
    print 'loaded sentence and document sentence-dash level co-occurance matrices of shape: {} and {}'.format(SentCoOccur.shape,
                                                                                                              DocSentDashCoOccur.shape)


    for Index, Term in enumerate(AspTerms):
        # AspTermsInfoDict[Term]['G'] = SimG[Index,:]
        # AspTermsInfoDict[Term]['T'] = SimT[Index,:]
        # AspTermsInfoDict[Term]['GT'] = SimGT[Index,:]
        AspTermsInfoDict[Term]['Sim'] = Sim[Index,:]
        AspTermsInfoDict[Term]['SentCoOccurance'] = SentCoOccur[Index,:]
        AspTermsInfoDict[Term]['DocSentDashCoOccurance'] = DocSentDashCoOccur[Index,:]

    print 'added sim, sentence-level and document sent-dash level co-occurance info to the aspect term dict'

    print 'prepared asp term info dict with {} keys (i.e., asp terms)'.format(len(AspTermsInfoDict.keys()))
    # Tmp = {}
    # for K, V in AspTermsInfoDict.iteritems():
    #     Tmp[K] = V
    #     Tmp[K]['POS'] = list(V['POS'])
    #     Tmp[K]['Sim'] = V['Sim'].tolist()
    #     Tmp[K]['SentCoOccurance'] = V['SentCoOccurance'].tolist()
    #
    # with open ('Tmp.json','w') as FH:
    #     json.dump(Tmp,FH,indent=4)

    return AspTermsInfoDict

def GetSeedTerms (AspTermsDFPosDict, NumSeeds):
    TupleList = [(DFPosDict['DF'], Term) for Term, DFPosDict in AspTermsDFPosDict.iteritems()]
    TupleList.sort();TupleList.reverse()
    MostFreqSeedTerms = [Tup[1] for Tup in TupleList[:NumSeeds]]
    return MostFreqSeedTerms


def Mergable(Clusters, AspTermsInfoDict, Delta):
    Tup = []
    for RInd, RowClust in enumerate(Clusters):
        for CInd, ColClust in enumerate(Clusters):
            # if RInd > CInd: #jus process lower triangle
            if RInd == CInd:
                continue
            IsNounAvail = GetNounAvailStatus(RowClust, ColClust, AspTermsInfoDict)
            if not IsNounAvail: #constraint 1 fails
                Tup.append((100,(RowClust, ColClust)))
                continue

            IsSentCoOccurSignificant = GetSentCoOccurSignificance (RowClust, ColClust, AspTermsInfoDict)
            if not IsSentCoOccurSignificant:
                Tup.append((200, (RowClust, ColClust)))
                continue

            ClustDist = GetClustDist (RowClust, ColClust, AspTermsInfoDict)
            Tup.append((ClustDist, (RowClust, ColClust)))
            if ClustDist > Delta: #constraint 2 fails
                continue

            return True
    Tup.sort()
    pprint (Tup[:50])
    raw_input()
    return False



def MergeSeedClusters (SeedClusters, AspTermsInfoDict, Delta):
    Clusters = deepcopy(SeedClusters)
    while (Mergable(Clusters, AspTermsInfoDict, Delta)):
        print 'mergable clusters found'
        ClosestClustTuple, ClosestDist = GetClosestMergableCluster (Clusters, AspTermsInfoDict)
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
AspTermsDFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_AspTermsDFs.json'
AspTermsPosFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_AspTermsAndPos.txt'
SimGFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/SimMats/reviews_TV_SimG.txt'
SimTFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/SimMats/reviews_TV_SimT.txt'
SimGTFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/SimMats/reviews_TV_SimGT.txt'
SentCoOccurFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/SimMats/reviews_TV_SentCoOccurMat.txt'
DocCoOccurFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/SimMats/reviews_TV_DocSentDashCoOccurMat.txt'
# Params = {'s':500, 'k':50, 'delta':0.8, 'wg':0.2,'wt':0.2,'wgt':0.6}
Params = {'s':500, 'k':50, 'delta':0.9, 'wg':0.2,'wt':0.1,'wgt':0.7}

AspTerms = [l.strip() for l in open (AspTermsFName)]
print 'loaded {} asp terms from file: {}'.format(len(AspTerms), os.path.basename(AspTermsFName))

AspTermsInfoDict = GetDFAndPosForAspTerms (AspTerms=AspTerms, AspTermsDFName=AspTermsDFName, AspTermsPosFName=AspTermsPosFName,
                                           SentCoOccruFName=SentCoOccurFName, DocCoOccurFName=DocCoOccurFName,
                                           SimGFName=SimGFName, SimTFName=SimTFName, SimGTFName=SimGTFName,
                                           WG=Params['wg'], WT=Params['wt'], WGT=Params['wgt'])



c1 = set(['great', 'good', 'like', 'get', 'see', 'going', 'know', 'want', 'think', 'nice'])
c2 = set(['sure', 'something'])

pprint (GetSentCoOccurSignificance (c1, c2, AspTermsInfoDict))
pprint (GetClustDist(c1,c2,AspTermsInfoDict))
raw_input()


SeedTerms = GetSeedTerms (AspTermsInfoDict, Params['s'])
print 'identified {} seed term based on DF of the terms'.format(len(SeedTerms))






Clusters = [set() for I in xrange(Params['s'])]
for I in xrange (Params['s']): Clusters[I].add(SeedTerms[I])

print 'made {} seed clusters with the {} seed terms'.format(len(Clusters), len(SeedTerms))

Clusters = MergeSeedClusters (Clusters, AspTermsInfoDict, Params['delta'])

print 'after merging seed clusters'
pprint (Clusters)
