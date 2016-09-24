from requests import get
from time import time
from pprint import pprint
import numpy as np
from joblib import Parallel,delayed
from nltk.corpus import wordnet

def wordnet_sim(s1, s2, index1=0, index2=0):
    if index1 < index2:
        # print '{} and {} not a part of lower triangle'.format(index1,index2)
        return 0.0
    if s1 == s2:
        print 'same term found: ', s1, s2
        return 1.0
    try:
        t0 = time()
        wordnet_s1 = wordnet.synsets(s1)[0]
        wordnet_s2 = wordnet.synsets(s2)[0]
        sim = wordnet_s1.wup_similarity(wordnet_s2)
        if not sim:
            sim = 0.0
        # print sim
        # raw_input()
        # print 'completed similarty for {} and {} (i.e., {} and {}) to be {} in {} sec'.format(s1,s2,
        #                                                                                       wordnet_s1, wordnet_s2,
        #                                                                                       round(sim,2),round(time()-t0,2))
        return sim
    except:
        # print 'Error in getting similarity for words {} and {}'.format(s1,s2)
        return -0.0


AspTermsFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_AspTermsAfterRemNonGooglew2v.txt'
AspTerms = [l.strip() for l in open(AspTermsFName).xreadlines()]#[:10]
print 'loaded {} asp terms from {}'.format(len(AspTerms), AspTermsFName)

WordnetSim = np.zeros (shape=(len(AspTerms), len(AspTerms)))
for RTermIndex, RTerm in enumerate(AspTerms):
    T0 = time()
    for CTermIndex, CTerm in enumerate(AspTerms):
        if RTermIndex >= CTermIndex:
            Sim = wordnet_sim(RTerm, CTerm, RTermIndex, CTermIndex)
            WordnetSim[RTermIndex, CTermIndex] = Sim
    print 'processed row term {} in {} sec'.format(RTermIndex, time()-T0)


WordnetSim = np.array (WordnetSim)
for RTermIndex in xrange(len(AspTerms)):
    for CTermIndex in xrange(len(AspTerms)):
        if RTermIndex < CTermIndex:
            WordnetSim[RTermIndex, CTermIndex] = WordnetSim[CTermIndex, RTermIndex]

print 'obtained wordnet SimMat of shape', WordnetSim.shape
OpFName = AspTermsFName.replace('AspTermsAfterRemNonGooglew2v.txt','WordnetSim.txt')
np.savetxt(OpFName, WordnetSim, fmt='%.4f')