import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from pprint import pprint
# import seaborn as sns

def PlotBar (AspwiseSentDict):
    fig = plt.figure(figsize=(16,7))
    PosHt = [Counter(InfoDict['Pol'])['positive'] for InfoDict in AspwiseSentDict.itervalues()]
    NegHt = [Counter(InfoDict['Pol'])['negative'] for InfoDict in AspwiseSentDict.itervalues()]
    NuHt = [Counter(InfoDict['Pol'])['neutral'] for InfoDict in AspwiseSentDict.itervalues()]
    Xticks = AspwiseSentDict.keys()
    B0 = plt.bar(range(len(Xticks)), height=NuHt,color='gold')
    B1 = plt.bar(range(len(Xticks)), height=PosHt,bottom=NuHt,color='green')
    B2 = plt.bar(range(len(Xticks)), height=NegHt,bottom=[Nu+Po for Nu, Po in zip(NuHt,PosHt)],color='red')
    # plt.bar(range(len(Xticks)), height=NegHt,bottom=PosHt,color='red')
    plt.xticks([i+0.5 for i in range(len(Xticks))], Xticks, size=20,rotation=90)
    plt.xlabel('Aspect Categories', size=20)
    plt.ylabel('# of sentences', size=20)
    plt.legend((B0[0], B1[0], B2[0]), ('Neutral', 'Positive', 'Negative'))
    plt.grid(True)
    plt.tight_layout(pad=1.5)
    plt.show()


FName = 'EnronAspCatsShanAndSangSangSents.csv'
Lines = [l.strip() for l in open(FName)]
AspwiseSentDict = defaultdict(dict)
for L in Lines:
    Parts = L.split(';')
    Pol = Parts[-1]
    AspCat = Parts[-2]
    Sent = ' '.join(Parts[:-2])
    if not AspwiseSentDict[AspCat]:
        AspwiseSentDict[AspCat]['Sent'] = []
        AspwiseSentDict[AspCat]['Pol'] = []
    AspwiseSentDict[AspCat]['Sent'].append(Sent)
    AspwiseSentDict[AspCat]['Pol'].append(Pol)


PlotBar (AspwiseSentDict)

