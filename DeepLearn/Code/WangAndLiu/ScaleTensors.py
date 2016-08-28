import os,sys,json
import numpy as np
from pprint import pprint
import networkx as nx
from nltk.tree import Tree

def ScaleAllSentenceTensors ():
    return None

def MakeNxParseTrees (TreeStr):
    SentTree = Tree.fromstring (TreeStr)
    # for Elem in  SentTree.pop():
    #     print Elem
    #     raw_input()
    SentTree.pretty_print()
    NxTree = nx.DiGraph()

def Main ():
    CoreNLPParsedFName = '../../Data/CoreNLPParsed.json'
    with open (CoreNLPParsedFName) as FH:
        CoreNLPParsedSents = json.load(FH)
    print 'loaded {} sentences that are pased by core nlp'.format(len(CoreNLPParsedSents))

    # NxParseTrees = [MakeNxParseTrees(SentDict['sentences']['text']) for SentDict in CoreNLPParsedSents]
    for SentDict in CoreNLPParsedSents:
        TreeStr = SentDict['sentences'][0]['parsetree']
        MakeNxParseTrees(TreeStr)
        raw_input()

if __name__ == '__main__':
    Main()
