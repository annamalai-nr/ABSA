import os, sys,json
from pprint import pprint
import numpy as np
from Utils.MatOps import NormAMat

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

SemanticSimMat2 = (SemanticSimMat+1)/2

# SemanticSimMat3 = NormAMat(SemanticSimMat)



print 'obtained termwise semantic sim mat of shape: {} from file: {}'.format(SemanticSimMat.shape, FName)
OpFName = FName.replace('AspTermsVects.json','SemanticSim.txt')
np.savetxt(fname=OpFName, X=SemanticSimMat2, fmt='%.4f')
# np.savetxt(fname=OpFName.replace('.txt','_RerangedPlusOneBy2.txt'), X=SemanticSimMat2, fmt='%.4f')
# np.savetxt(fname=OpFName.replace('.txt','_ReRangedFormula.txt'), X=SemanticSimMat3, fmt='%.4f')

print 'check ', OpFName