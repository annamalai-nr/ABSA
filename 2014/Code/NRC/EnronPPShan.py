import os, json, sys
from pprint import pprint

with open ('../../Data/EnronStuff/EnronCommonAspectTerms.json') as FH:
    SelectedAspTerms = json.load(FH)
SelectedAspTerms = set(SelectedAspTerms)
with open ('../../Data/EnronStuff/CommonAspTermToCatMapping.json') as FH:
    AspTermToCatMapping = json.load(FH)

FName = '../../Data/EnronStuff/SelectedAspSubjSent6K_Shan_Processed.csv'
Lines = [l.strip() for l in open (FName) if l.strip()]
Sentences = [l.strip().split('~')[0] for l in Lines]
AspTerms = [list(l.strip().split('~')[1].split(';'))  for l in Lines]
Polarities = [L.split('~')[-1].split(';') for L in Lines]
NewPol = []
for PolList in Polarities:
    NewPol.append([Item.lower().replace(' ','') for Item in PolList])
Triplets = zip(Sentences, AspTerms, NewPol)

# pprint (Triplets)
# raw_input()
CleanedTriplets = []
for Index, ThreeTup in enumerate(Triplets):
    FoundUnkownAspTerm = False
    AspTerms = ThreeTup[1]
    AspTermsInKnownList = SelectedAspTerms.intersection(set(AspTerms))
    if len(AspTerms) == len(AspTermsInKnownList):
        AspCats = [AspTermToCatMapping[Term] for Term in ThreeTup[1]]
        CleanPol = [P.replace('.','') for P in ThreeTup[-1]]
        CleanTup = (ThreeTup[0], AspCats, CleanPol)
        CleanedTriplets.append(CleanTup)

# pprint (CleanedTriplets)
# raw_input()
LinesToWrite = []
ErrorTriples = []
for ThreeTup in CleanedTriplets:
    Sent = ThreeTup[0]
    for Index, ACat in enumerate(ThreeTup[1]):
        try:
            Pol = ThreeTup[-1][Index]
            LinesToWrite.append(';'.join([Sent, ACat, Pol]))
        except:
            ErrorTriples.append(ThreeTup)
            break
print 'Num of err triplets: ', len(ErrorTriples)

with open('EnronAspCatsShanSents.csv','w') as FH:
    for L in LinesToWrite:
        print >>FH, L

print 'done'