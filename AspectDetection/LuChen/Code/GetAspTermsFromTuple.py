import os
from pprint import pprint
from ast import literal_eval as make_tuple

FName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_AspTermsAndPos.txt'
Terms = list(set([make_tuple(l.strip())[0] for l in open (FName).xreadlines()]))
Terms.sort()
OpFName = FName.replace('AspTermsAndPos.txt','AspTerms.txt')
with open (OpFName,'w') as FH:
    for T in Terms:
        print >>FH, T
