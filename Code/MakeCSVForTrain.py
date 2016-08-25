import json
from pprint import pprint

with open ('../Restaurants_Train.xml.json') as FH:
    SentsDict = json.load (FH)

Lines = []
for Id, SentStruct in SentsDict.iteritems():
    Sent = SentStruct['Sentence']
    for Index,Cat in enumerate(SentStruct['CatAndPolarity']['Cat']):
        Pol = SentStruct['CatAndPolarity']['Polarity'][Index]
        Tup = (Sent,Cat,Pol)
        Lines.append (';'.join(Tup))


OPFName = 'RestAspCatABSA.data'
with open (OPFName,'w') as FH:
    for L in Lines:
        print >>FH, L
