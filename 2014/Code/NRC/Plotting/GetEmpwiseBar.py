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


def PlotAspCatBars(AuthCountMapping, CatNames):
    # fig = plt.figure(figsize=(6, 8))
    Colors = ['green','r','b','gray','y','pink','orange','crimson','brown']
    Patterns = ['-', '+', 'x', '\\', '*', 'o', 'O', '.']
    CatNamesToBarDataMap = {Cat:[CountDict[Cat] for CountDict in AuthCountMapping.itervalues()] for Cat in CatNames}
    CatNamesToBarDataArray = np.array(CatNamesToBarDataMap.values())
    # pprint (CatNamesToBarDataArray)
    # raw_input()
    Xticks = AuthCountMapping.keys()
    B = []
    for Index,Cat in enumerate(CatNames):
        B.append(plt.bar(range(len(Xticks)), height=CatNamesToBarDataMap[Cat],
                         bottom = CatNamesToBarDataArray[0:Index].sum(0),
                         color=Colors[randint(0,len(Colors)-1)],
                         hatch=Patterns[randint(0,len(Patterns)-1)]))
    #    B2 = plt.bar(range(len(Xticks)), height=NegHt, bottom=[Nu + Po for Nu, Po in zip(NuHt, PosHt)], color='red')
    plt.xticks([i + 0.5 for i in range(len(Xticks))], Xticks, size=20, rotation=90)
    plt.xlabel('Email Authors', size=20)
    plt.ylabel('# of sentences', size=20)
    plt.yticks(size=20)
    plt.legend([I[0] for I in B], CatNamesToBarDataMap.keys(),loc='best')
    plt.grid(True)
    # plt.tight_layout()
    plt.show()


def GetAuthorCounts (FName, StartIndex=0, EndIndex=-1):
    Lines = [l.strip() for l in open (FName) if l.strip()][StartIndex:EndIndex]
    Polarities = [L.split('~')[-1].split(';') for L in Lines]
    Authors = [L.split('~')[-3].split(';')[0] for L in Lines]
    CleanPols = []
    for Pol in Polarities:
        Tmp = [P.replace('.','').replace(' ','').lower() for P in Pol]
        CleanPols.append(Tmp)

    D = defaultdict(list)
    for Index, Auth in enumerate(Authors):
        D[Auth].extend (CleanPols[Index])

    D = {Auth:Counter(PolList) for Auth, PolList in D.iteritems()}
    return D


def GetAuhtorAspDict (FName, AspTermToCatMap, StartIndex=0, EndIndex=-1):
    Lines = [l.strip() for l in open(FName) if l.strip()][StartIndex:EndIndex]
    AspTerms = [L.split('~')[1].split(';') for L in Lines]
    Authors = [L.split('~')[-3].split(';')[0] for L in Lines]
    D = defaultdict(list)
    for Index, Auth in enumerate(Authors):
        D[Auth].extend([AspTermToCatMap.get(Term) for Term in AspTerms[Index]])

    D = {Auth: Counter(PolList) for Auth, PolList in D.iteritems()}
    return D

#File names
SangSangFName = '../../Data/EnronStuff/SelectedAspSubjSent6K_SangSang.csv'
ShanFName = '../../Data/EnronStuff/SelectedAspSubjSent6K_Shan_Processed.csv'
AspTermToCapMapFName = '../../Data/EnronStuff/CommonAspTermToCatMapping.json'
with open (AspTermToCapMapFName) as FH: AspTermToCapMap = json.load(FH)


#plot count bars
# SangSangCntDict = GetAuthorCounts (SangSangFName, StartIndex=3000, EndIndex=4000)
# ShanCntDict = GetAuthorCounts (ShanFName)
# MergedCntDict = {K: V + ShanCntDict[K] for K, V in SangSangCntDict.iteritems()}
# PlotCntBars(MergedCntDict)

#plot catgeory bars
SangSangAspCatDict = GetAuhtorAspDict (SangSangFName, AspTermToCatMap=AspTermToCapMap,StartIndex=3000, EndIndex=4000)
ShanAspCatDict = GetAuhtorAspDict (ShanFName, AspTermToCatMap=AspTermToCapMap)
MergedAspCatDict = {K: V + ShanAspCatDict[K] for K, V in SangSangAspCatDict.iteritems()}
CatNames = list(set(AspTermToCapMap.values()))
CatNames.sort()
# PlotAspCatBars(MergedAspCatDict,CatNames)

pprint(MergedAspCatDict)

LinesToWrite = []
Line1 = ','+','.join(MergedAspCatDict.keys())
LinesToWrite.append(Line1)
for Cat in CatNames:
    print Cat
    Line = str(Cat)+ ',' + ','.join([str(V[Cat]) for V in MergedAspCatDict.values()])
    LinesToWrite.append(Line)
with open('AuthCatCount.csv','w') as FH:
    for L in LinesToWrite:
        print >>FH, L