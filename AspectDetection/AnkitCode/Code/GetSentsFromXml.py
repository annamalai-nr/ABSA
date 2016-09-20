import os, sys, json
from pprint import pprint
FName = '/home/annamalai/Desktop/ABSA/2014/Data/Restaurants_Test_Data_phaseB.xml.term-polarity.json'
# FName = '/home/annamalai/Desktop/ABSA/2014/Data/Laptops_Test_Data_phaseB.xml.term-polarity.json'
with open (FName) as FH:
    Dict = json.load(FH)

Sents = [unicode.encode(V['Sentence'],errors='ignore') for K, V in Dict.iteritems()]
OpFName = FName.replace('.term-polarity.json','_Sentences.txt')
with open(OpFName, 'w') as FH:
    for S in Sents:
        print S
        print >>FH, S