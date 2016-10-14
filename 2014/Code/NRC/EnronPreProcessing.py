import os, json, sys
from pprint import pprint


FName = '../../Data/SelectedAspSubjSent6K_Ankit.csv'
Lines = [l.strip() for l in open (FName) if l.strip()]
Sentences = [l.strip().split('~')[0] for l in open (FName) if l.strip()]
AspTerms = [list(l.strip().split('~')[1].split(';'))  for l in open (FName) if l.strip()]
Polarities = []
for L in open (FName):
    L = L.strip()
    if  L:
        Pol = L.split('~')[-1][:-1].split(';')
        # print L
        # print Pol
        # raw_input()
        Polarities.append(Pol)

# pprint (zip(Sentences, AspTerms, Polarities))

for Index, ATList in enumerate(AspTerms):
    for Item in ATList:
        if Item in {'positive','negative','neutral'}:
            print Lines[Index], Index*2
            raw_input()

UniqueAspTerms = list(set([ATerm for ATList in AspTerms for ATerm in ATList if ATerm and 'policy' not in ATerm]))
UniqueAspTerms.sort()
pprint (UniqueAspTerms)
print len(UniqueAspTerms)