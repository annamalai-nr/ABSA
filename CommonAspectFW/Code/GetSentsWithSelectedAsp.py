import json
from collections import OrderedDict
from pprint import pprint
from collections import Counter
import matplotlib.pyplot as plt

def PlotBars(SentInfoDict, OPFName='Stats.png'):
    AuthorsStats = [V['author'] for V in SentInfoDict.itervalues()];AuthorsStats = Counter(AuthorsStats)
    TimelineStats = [V['timestamp'] for V in SentInfoDict.itervalues()];TimelineStats = Counter(TimelineStats)
    Fig = plt.figure(figsize=(18,12))
    Ax1 = Fig.add_subplot(121)
    Ax2 = Fig.add_subplot(122)
    Ax1.bar(left=range(len(AuthorsStats)), height=AuthorsStats.values())
    Ax1.set_xticks([V + 0.5 for V in range(len(AuthorsStats))])
    Ax1.set_xticklabels(AuthorsStats.keys(), rotation=90)
    Ax1.set_xlabel('Authors',fontsize=20)
    Ax1.set_ylabel('# of sentences with selected aspects',fontsize=20)

    Ax2.bar(left=range(len(TimelineStats)), height=TimelineStats.values())
    Ax2.set_xticks([V + 0.5 for V in range(len(TimelineStats))])
    Ax2.set_xticklabels(TimelineStats.keys(), rotation=90)
    Ax2.set_xlabel('Month',fontsize=20)
    Ax2.set_ylabel('# of sentences with selected aspects',fontsize=20)
    Fig.savefig(OPFName)
    print 'pls check file: {} for stats figure'.format(OPFName)


def Main():
    FName = '../Data/ReducedSentence4Tuple.json'
    with open(FName) as FH:
        SentInfoDict = json.load(FH)
    print 'loaded sent info dict with {} keys'.format(len(SentInfoDict))

    SelectedAspects = "policy,generation,chairman,bill,cash,costs,program,service,markets,president,problem,future,contracts,mark,prices,managment,governer,position,development,capacity,system,staff,report,enron,power,california,company,companies,energy, state,market,business,housten,utilities,electricity,delainey,team,process,interest,customers,project,issues,issue,agreement,price,ken,opportunity,place,order,work,money,changes,cost,value,services,access,review,support,deal"
    SelectedAspects = SelectedAspects.split(',')
    print 'loaded {} aspects that we manually chose'.format(len(SelectedAspects))

    AllPolicyAsps = set([Asp for V in SentInfoDict.itervalues() for Asp in V['aspects'] if 'policy' in Asp or 'polici' in Asp])
    print 'found {} aspects with policy'.format(len(AllPolicyAsps))
    SelectedAspects.extend(list(AllPolicyAsps))
    SelectedAspects = set(SelectedAspects)
    print 'found a total of {} aspects, finally'.format(len(SelectedAspects))


    SelectedAspSentInfoDict = OrderedDict()
    for Sent, InfoDict in SentInfoDict.iteritems():
        AspectsFound = list(set(InfoDict ['aspects']).intersection(SelectedAspects))
        if AspectsFound:
            SelectedAspSentInfoDict[Sent] = InfoDict
            SelectedAspSentInfoDict[Sent]['aspects'] = AspectsFound

    PlotBars(SentInfoDict)

    print 'from a total of {} sentences, found {} with selected aspects'.format(len(SentInfoDict), len(SelectedAspSentInfoDict))
    with open ('SelectedAspectSentsInfo.json','w') as FH:
        json.dump(SelectedAspSentInfoDict, FH, indent=4)


if __name__ == '__main__':
    Main()


