import os, json
from pprint import pprint
import numpy as np
from math import log

AspTermsFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_GPS_AspTermsAfterRemNonGooglew2v.txt'
AspTermsDFFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_GPS_AspTermsDFs.json'
CoOccurMatFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_GPS_CoOccurMat.txt'
N = 500 # total num of rev docs

# AspTermsFName = sys.argv[1]
# AspTermsDFFName = sys.argv[2]
# CoOccurMatFName = sys.argv[3]
# N = int (sys.argv[4]) # total num of rev docs

AspTerms = [l.strip() for l in open (AspTermsFName)]
print 'loaded {} aspect terms from {}'.format(len(AspTerms), AspTermsFName)


with open (AspTermsDFFName) as FH:
    AspTermsDF = json.load(FH)
print 'loaded term\'s DF info from file', AspTermsDFFName

Tmp = {}
for Term, DF in AspTermsDF.iteritems():
    if DF == 0:
        DF = 1
    Tmp[Term] = DF
AspTermsDF = Tmp



SentenceLevelCoOccurMat = np.loadtxt(fname=CoOccurMatFName)
print 'senetence level co-occurances of shape: {} from file: {}'.format(SentenceLevelCoOccurMat.shape,
                                                                        CoOccurMatFName)

NPMIMat = np.zeros (shape=(len(AspTerms),len(AspTerms)))
for RIndex, RowT in enumerate(AspTerms):
    for CIndex, ColT in enumerate(AspTerms):
        if RIndex == CIndex:
            Fxixj = AspTermsDF[RowT]
        else:
            Fxixj = SentenceLevelCoOccurMat[RIndex][CIndex]
        if 0 == Fxixj:
            Frac = -1
        else:
            Fxi = AspTermsDF[RowT]
            Fxj = AspTermsDF[ColT]

            Nr = log((float(N)*Fxixj)/(Fxi*Fxj))
            Dr = -log (float(Fxixj)/N)
            Frac = float(Nr)/Dr
        NPMIMat[RIndex][CIndex] = Frac

#Rescale NPMI from [-1, 1] to [0,1]
NPMIMat = (NPMIMat+1)/2

print 'NPI matrix for each asp term is obtained and its shape: {}'.format(NPMIMat.shape)
OpFName = CoOccurMatFName.replace('_CoOccurMat.txt','_NPMI.txt')
np.savetxt(fname=OpFName, X=NPMIMat, fmt='%.4f')