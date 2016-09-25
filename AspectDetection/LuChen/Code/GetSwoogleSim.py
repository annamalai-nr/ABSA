from requests import get
from time import time
from pprint import pprint
import numpy as np
from joblib import Parallel,delayed

sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"
def sss(s1, s2, type='relation', corpus='webbase', index1=0,index2=0):
    if index1 < index2:
        # print '{} and {} not a part of lower triangle'.format(index1,index2)
        return 0.0
    if s1 == s2:
        print 'same term found: ', s1, s2
        return 1.0
    try:
        t0 = time()
        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
        sim = float(response.text.strip())
        print 'completed similarty for {} and {} to be {} in {} sec'.format(s1,s2,round(sim,2),round(time()-t0,2))
        return sim
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return -1.0

def GetSimWithAllTerms (TgtTerm, TgtTermIndex, AllTerms):
    Sims = Parallel(n_jobs=8)(delayed(sss)(TgtTerm, Term, index1=TgtTermIndex, index2=Index)
                               for Index, Term in enumerate(AllTerms))
    return Sims

# AspTermsFName = '/mnt/AnnaLaptop/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_AspTermsAfterRemNonGooglew2v.txt'
AspTermsFName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_TV_AspTermsAfterRemNonGooglew2v.txt'
AspTerms = [l.strip() for l in open(AspTermsFName).xreadlines()]#[:40]
print 'loaded {} asp terms from {}'.format(len(AspTerms), AspTermsFName)


SwoogleSim = []
for Index, Term in enumerate(AspTerms):
    Sims = GetSimWithAllTerms(Term, Index, AspTerms)
    SwoogleSim.append(Sims)

OpFName = AspTermsFName.replace('AspTermsAfterRemNonGooglew2v.txt','SwoogleSimList_Laptop.txt')
with open (OpFName,'w') as FH:
    for Row in SwoogleSim:
        print>>FH, (' '.join([str(S) for S in Row]))

SwoogleSim = np.array (SwoogleSim)
for RInd in xrange(len(AspTerms)):
    for CInd in xrange(len(AspTerms)):
        if RInd<CInd:
            SwoogleSim[RInd, CInd] = SwoogleSim[CInd, RInd]

print 'obtained SwoogleSimMat of shape', SwoogleSim.shape
OpFName = AspTermsFName.replace('AspTermsAfterRemNonGooglew2v.txt','SwoogleSimLaptop.txt')
np.savetxt(OpFName,SwoogleSim,fmt='%.4f')