import os, json

IpFName = '/home/annamalai/Desktop/ABSA/2014/Data/RestAspTermABSA.csv'
Lines = [l.strip() for l in open (IpFName).xreadlines()]
Dict ={}
for L in Lines:
    Sent = ';'.join(L.split(';')[:-2])
    AspTerm = L.split(';')[-2]
    # print L, Sent, AspTerm
    # raw_input()
    if Sent not in Dict.keys():
        Dict[Sent] = []
    Dict[Sent].append (AspTerm)

OpFName = IpFName.replace('RestAspTermABSA.csv','RestAspTermDict.json')
with open (OpFName,'w') as FH:
    json.dump(Dict, fp=FH, indent=4)