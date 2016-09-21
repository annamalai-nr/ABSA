import json, os, sys
import numpy as np

def NormAMat (Mat):
    NormedMat = np.zeros(shape=Mat.shape)
    OldMax = Mat.max()
    OldMin = Mat.min()
    OldRange = OldMax - OldMin
    NewMax = 1.0
    NewMin = 0.0
    NewRange = NewMax - NewMin

    print 'for the given mat moving from range[{},{}] to [0,1]'.format(OldMin, OldMax)

    for RIndex in xrange(Mat.shape[0]):
        for CIndex in xrange(Mat.shape[1]):
            OldVal = Mat[RIndex][CIndex]
            NewValue = (((OldVal - OldMin) * NewRange) / OldRange) + NewMin
            NormedMat[RIndex][CIndex] = NewValue
    return  NormedMat


SemanticSimMatFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_SemanticSim.txt'
NPMIMatFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_NPMI.txt'
SemanticSimMat = np.loadtxt (SemanticSimMatFName)
NPMIMat = np.loadtxt (NPMIMatFName)
print 'loaded both semantic sim and npmi matrices of shapes: ', SemanticSimMat.shape, NPMIMat.shape

SimG = np.zeros (shape=SemanticSimMat.shape)
SimT = np.zeros (shape=SemanticSimMat.shape)
for RIndex in xrange (SemanticSimMat.shape[0]):
    for CIndex in xrange (SemanticSimMat.shape[0]):
        SimG[RIndex][CIndex] = np.dot (SemanticSimMat[RIndex], SemanticSimMat[CIndex].T)
        # print SemanticSimMat[RIndex]
        # print SemanticSimMat[CIndex].T
        # print SimG[RIndex][CIndex]
        # raw_input()
print 'obtained simg'

for RIndex in xrange (NPMIMat.shape[0]):
    for CIndex in xrange (NPMIMat.shape[0]):
        SimT[RIndex][CIndex] = np.dot (NPMIMat[RIndex], NPMIMat[CIndex].T)
print 'obtained simt'

SimG = NormAMat (SimG)
SimT = NormAMat (SimT)
SimGT = np.maximum (SimG, SimT)
print 'obtained simgt'

SimGFName = SemanticSimMatFName.replace('SemanticSim.txt','SimG.txt')
SimTFName = NPMIMatFName.replace('NPMI.txt','SimT.txt')
SimGTFName = NPMIMatFName.replace('NPMI.txt','SimGT.txt')

np.savetxt (fname=SimGFName, X = SimG, fmt='%.4f')
np.savetxt (fname=SimTFName, X = SimT, fmt='%.4f')
np.savetxt (fname=SimGTFName, X = SimGT, fmt='%.4f')