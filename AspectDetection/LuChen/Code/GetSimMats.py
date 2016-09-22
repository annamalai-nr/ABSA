import json, os, sys
import numpy as np
from Utils.MatOps import NormAMat

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