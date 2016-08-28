import os,sys,json,string,nltk
from gensim.models import word2vec
import numpy as np
import networkx as nx
from time import time
from pprint import pprint
from GetSentenceVectors import GetAllSentenceTensors
from ScaleTensors import ScaleAllSentenceTensors

def Main():
    NSamples = -1
    SentsAspectsLabelsFName = '../../../2014/Data/RestAspCatABSA.csv'
    Sentences = [''.join(l.strip().split(';')[:-2]).lower() for l in open(SentsAspectsLabelsFName).xreadlines()][:NSamples]
    Aspects = [''.join(l.strip().split(';')[-2]) for l in open(SentsAspectsLabelsFName).xreadlines()][:NSamples]
    Labels = [''.join(l.strip().split(';')[-1]) for l in open(SentsAspectsLabelsFName).xreadlines()][:NSamples]
    print 'loaded {} sentences, {} aspects and {} labels'.format(len(Sentences), len(Aspects), len(Labels))

    UnscaledSentenceTensors = GetAllSentenceTensors(Sentences)
    print 'obtained {} sentence 2D tensors'.format(len(UnscaledSentenceTensors))


if __name__ == '__main__':
    Main()
