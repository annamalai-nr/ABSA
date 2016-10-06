import json
from collections import OrderedDict
from pprint import pprint

from GetSentsWithSelectedAsp import PlotBars


FName = '../Data/SelectedAspectSentsInfo.json'
with open(FName) as FH:
    SentInfoDict = json.load(FH)
print 'loaded sent info dict with {} keys'.format(len(SentInfoDict))

SubjSentInfoDict = OrderedDict()
for Sent, InfoDict in SentInfoDict.iteritems():
    for SubjAnalysedSent, SubjResDict in InfoDict['subj_analysis_res'].iteritems():
        if SubjResDict['sentiment'] == 'positive' or SubjResDict['sentiment'] == 'negative':
            SubjSentInfoDict[Sent] = InfoDict
            break

print 'from a total of {} sentences, found {} subjectives ones'.format(len(SentInfoDict), len(SubjSentInfoDict))
with open ('SubjSentencesInfo.json','w') as FH:
    json.dump(SubjSentInfoDict,FH,indent=4)
#
# PlotBars(SubjSentInfoDict)

CSVData = []
for Sent, InfoDict in SubjSentInfoDict.iteritems():
    # print [V for ListOfDict in InfoDict['subj_analysis_res'].values() for V in ListOfDict.values() if not isinstance(V, int) and not isinstance(V, float)]
    # raw_input()
    # continue
    Str='~'.join([Sent, ';'.join(InfoDict['aspects']), InfoDict['timestamp'],InfoDict['author'],
                  ';'.join([V for ListOfDict in InfoDict['subj_analysis_res'].values() for V in ListOfDict.values() if not isinstance(V, int) and not isinstance(V, float)])]).encode('utf-8').strip()
    CSVData.append(Str)

with open ('SelectedAspSubjSent.csv','w') as FH:
    for Line in CSVData:
        print >>FH, Line

