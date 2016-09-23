import numpy as np


def GetAvgDist (RowClust, ColClust, AspTermsInfoDict):
    Nr = []
    for RowClustTerm in RowClust:
        for ColClustTerm in ColClust:
            ColTermIndex = AspTermsInfoDict[ColClustTerm]['TermIndex']
            Sim = AspTermsInfoDict[RowClustTerm]['Sim'][ColTermIndex]
            Nr.append(1 - Sim)
    Nr = sum (Nr)
    Dr = len(RowClust) * len(ColClust)
    AvgDist = float (Nr)/Dr
    return AvgDist

def GetClusterRep (Clust, AspTermsInfoDict):
    Tup = [(AspTermsInfoDict[Elem]['DF'], Elem) for Elem in Clust]
    Tup.sort()
    Rep = Tup[-1][1]
    return Rep

def GetRepDist (RowClust, ColClust, AspTermsInfoDict):
    RowClustRep = GetClusterRep (RowClust, AspTermsInfoDict)
    ColClustRep = GetClusterRep (ColClust, AspTermsInfoDict)
    ColClustRepIndex = AspTermsInfoDict[ColClustRep]['TermIndex']
    SimBwReps = AspTermsInfoDict[RowClustRep]['Sim'][ColClustRepIndex]
    DistRep = 1 - SimBwReps
    return DistRep

def GetClustDist (RowClust, ColClust, AspTermsInfoDict):
    DistAvg = GetAvgDist (RowClust, ColClust, AspTermsInfoDict)
    if len (RowClust) == 1 and len(ColClust) == 1:
        return DistAvg
    DistRep = GetRepDist (RowClust, ColClust, AspTermsInfoDict)
    Dist = max (DistAvg, DistRep)
    return Dist

def GetNounAvailStatus (RowClust, ColClust, AspTermsInfoDict):
    for Elem in RowClust:
        if 'NN' in AspTermsInfoDict[Elem]['POS'] or 'NNP' in AspTermsInfoDict[Elem]['POS']:
            return True

    for Elem in ColClust:
        if 'NN' in AspTermsInfoDict[Elem]['POS'] or 'NNP' in AspTermsInfoDict[Elem]['POS']:
            return True

    return False


def GetClosestMergableCluster (Clusters, AspTermsInfoDict):
    DistsClustPairs = []
    for RClustIndex, RClust in enumerate(Clusters):
        for CClustIndex, CClust in enumerate(Clusters):
            # if RClustIndex > CClustIndex:
            if RClustIndex == CClustIndex:
                continue
            else:
                Dist = GetClustDist(RClust, CClust, AspTermsInfoDict)
                DistsClustPairs.append((Dist,(RClust,CClust)))
    DistsClustPairs.sort()
    for Dist, ClustPair in DistsClustPairs:
        IsNounAvail = GetNounAvailStatus(ClustPair[0], ClustPair[1], AspTermsInfoDict)
        if not IsNounAvail:  # constraint 1 fails
            continue

        IsSentCoOccurSignificant = GetSentCoOccurSignificance(ClustPair[0], ClustPair[1], AspTermsInfoDict)
        if not IsSentCoOccurSignificant:
            continue

        return ClustPair, Dist
    return (set(),set()), -1


def GetSentCoOccurSignificance (RowClust, ColClust, AspTermsInfoDict):
    SentCoOccurFreq = 0
    DocSentDashCoOccurFreq = 0
    for RowClustTerm in RowClust:
        for ColClustTerm in ColClust:
            if RowClustTerm == ColClustTerm:
                continue
            else:
                ColTermIndex = AspTermsInfoDict[ColClustTerm]['TermIndex']
                ThisPairSentCoCoccurFreq = AspTermsInfoDict[RowClustTerm]['SentCoOccurance'][ColTermIndex]
                ThisPairDocSentDashCoCoccurFreq = AspTermsInfoDict[RowClustTerm]['DocSentDashCoOccurance'][ColTermIndex]
                SentCoOccurFreq += ThisPairSentCoCoccurFreq
                DocSentDashCoOccurFreq += ThisPairDocSentDashCoCoccurFreq

    if SentCoOccurFreq > DocSentDashCoOccurFreq:
        return True
    else:
        return False


