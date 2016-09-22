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
