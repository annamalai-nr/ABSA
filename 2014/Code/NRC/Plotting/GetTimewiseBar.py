import os, json, sys
from collections import defaultdict, Counter
from pprint import pprint
import matplotlib.pyplot as plt
from random import randint
import numpy as np

def PlotCntBars(AuthCountMapping):
    fig = plt.figure(figsize=(6, 8))
    PosHt = [CountDict['positive'] for CountDict in AuthCountMapping.itervalues()]
    NegHt = [CountDict['negative'] for CountDict in AuthCountMapping.itervalues()]
    NuHt = [CountDict['neutral'] for CountDict in AuthCountMapping.itervalues()]
    Xticks = AuthCountMapping.keys()
    B0 = plt.bar(range(len(Xticks)), height=NuHt, color='gold')
    B1 = plt.bar(range(len(Xticks)), height=PosHt, bottom=NuHt, color='green')
    B2 = plt.bar(range(len(Xticks)), height=NegHt, bottom=[Nu + Po for Nu, Po in zip(NuHt, PosHt)], color='red')
    # plt.bar(range(len(Xticks)), height=NegHt,bottom=PosHt,color='red')
    plt.xticks([i + 0.5 for i in range(len(Xticks))], Xticks, size=20, rotation=90)
    plt.xlabel('Email Authors', size=20)
    plt.ylabel('# of sentences', size=20)
    plt.yticks(size=20)
    plt.legend((B0[0], B1[0], B2[0]), ('Neutral', 'Positive', 'Negative'),loc='best')
    plt.grid(True)
    plt.tight_layout(pad=1.5)
    plt.show()


def GetTimeCounts (FName, StartIndex=0, EndIndex=-1):
    Lines = [l.strip() for l in open (FName) if l.strip()][StartIndex:EndIndex]
    Polarities = [L.split('~')[-1].split(';') for L in Lines]
    Time = [L.split('~')[2].split(';')[0] for L in Lines]
    CleanPols = []
    for Pol in Polarities:
        Tmp = [P.replace('.','').replace(' ','').lower() for P in Pol]
        CleanPols.append(Tmp)

    D = defaultdict(list)
    for Index, T in enumerate(Time):
        D[T].extend (CleanPols[Index])

    D = {Auth:Counter(PolList) for Auth, PolList in D.iteritems()}
    pprint (D)
    raw_input()
    return D



#File names
SangSangFName = '../../Data/EnronStuff/SelectedAspSubjSent6K_SangSang.csv'
ShanFName = '../../Data/EnronStuff/SelectedAspSubjSent6K_Shan_Processed.csv'
AspTermToCapMapFName = '../../Data/EnronStuff/CommonAspTermToCatMapping.json'
with open (AspTermToCapMapFName) as FH: AspTermToCapMap = json.load(FH)


#plot count bars
SangSangCntDict = GetTimeCounts (SangSangFName, StartIndex=3000, EndIndex=4000)
ShanCntDict = GetTimeCounts (ShanFName)
MergedCntDict = {K: V + SangSangCntDict[K] for K, V in ShanCntDict.iteritems()}
PlotCntBars(MergedCntDict)

