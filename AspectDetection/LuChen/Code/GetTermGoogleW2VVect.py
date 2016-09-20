import os, sys,json
from pprint import pprint
from time import time
from gensim.models import word2vec
import numpy as np
from collections import OrderedDict


def LoadGoogleNewsW2VModel (ModelFName):
    T0 = time()
    print 'loading {} w2v model ...'.format(ModelFName)
    W2VModel = word2vec.Word2Vec.load_word2vec_format(ModelFName, binary=True)
    print 'loaded w2v model in {} sec.'.format(round(time()-T0,2))
    return W2VModel


FName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_GPS_AspTerms.txt'
# FName = sys.argv[1]
W2VModelFName = '/home/annamalai/Desktop/ABSA/Embeddings/GoolgeNews/GoogleNews-vectors-negative300.bin'

Terms = [l.strip() for l in open (FName).xreadlines()]
print 'loaded {} terms from {}'.format(len(Terms), FName)
D = OrderedDict()
W2VModel = LoadGoogleNewsW2VModel(W2VModelFName)
#to load syn0norm
W2VModel.most_similar('test','testing')
TermsToDel = []
for T in Terms:
    try:
        TIndex = W2VModel.vocab[T].index
    except:
        TermsToDel.append(T)
        continue
    Vec = W2VModel.syn0norm[TIndex]
    D[T] = Vec.tolist()

OpFName = FName.replace('AspTerms.txt','AspTermsVects.json')
with open (OpFName,'w') as FH:
    json.dump(obj=D, fp=FH, indent=4)

print 'check file ', OpFName

print '-'*80
print 'terms to be deleted from ',FName
pprint(TermsToDel)
print '-'*80
print 'after deleting'
print '-'*80
TermsToDel = set (TermsToDel)
for T in Terms:
    if T not in TermsToDel:
        print T
print '-'*80



