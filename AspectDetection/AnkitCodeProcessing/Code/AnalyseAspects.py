import os, sys, json
from pprint import pprint
from collections import Counter
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts


TgtFolder = '/home/annamalai/Desktop/ABSA/SubjAnalysis/usent/ToDelSkillingSubjRes'
FilesToProcess = [os.path.join (TgtFolder, F) for F in os.listdir(TgtFolder) if F.endswith('ApsPerSent.json')]
FilesToProcess.sort()
Aspects = []

# FilesToProcess = ['/home/annamalai/Desktop/ABSA/SubjAnalysis/usent/ToDelSkillingSubjRes/SkillingEmails_Inbox_Subj_ApsPerSent.json']
for F in FilesToProcess:
    print 'processing ', F
    with open (F) as FH:
        FileContents = json.load(FH)
        Sents, AspsLists = zip (*FileContents)
        del Sents
        for AList in AspsLists:
            Aspects.extend(AList)

Cntr = Counter (Aspects)
pprint (Cntr)
AspStr = u' '.join((Aspects)).encode('utf-8').strip()
# tags = make_tags(get_tag_counts(AspStr), maxsize=120)
# create_tag_image(tags, 'cloud_large.png', size=(900, 600), fontname='Lobster')
with open ('aspects.txt', 'w') as FH:
    print >>FH, AspStr