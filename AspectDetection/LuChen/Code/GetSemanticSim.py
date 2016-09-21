import os, sys,json
from pprint import pprint
import numpy as np

FName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_GPS_AspTermsVects.json'
with open (FName) as FH:
    TermToVectDict = json.load(FH)

Tmp = {}
for T, V in TermToVectDict.iteritems():
    Tmp[T] = np.array (V)
TermToVectDict = Tmp

Terms = TermToVectDict.keys(); Terms.sort()
SemanticSimMat = []
for T in Terms:
    # print T
    ThisV = TermToVectDict[T]
    # print ThisV
    SemanticSimVect = [np.dot(ThisV, TermToVectDict[OtherTerm].T) for OtherTerm in Terms]
    # pprint (SemanticSimVect)
    # print (len(SemanticSimVect))
    # raw_input()
    SemanticSimMat.append(SemanticSimVect)

SemanticSimMat = np.array(SemanticSimMat)

print 'obtained termwise semantic sim mat of shape: {} from file: {}'.format(SemanticSimMat.shape, FName)
OpFName = FName.replace('AspTermsVects.json','SimG.txt')
np.savetxt(fname=OpFName, X=SemanticSimMat, fmt='%.4f')
print 'check ', OpFName