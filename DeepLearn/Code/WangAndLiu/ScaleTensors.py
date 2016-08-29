import os,sys,json,nltk
import numpy as np
from pprint import pprint
import networkx as nx
from nltk.tree import Tree

def ScaleAllSentenceTensors ():
    return None

ROOT = 'ROOT'
ParStr = 'Root'
GrandPar = ''

def GetLabelsUniqueIndex (NodePosLabel, Ht, NodeNxLabels):
    NodeLabelsInSameGt = [Label for Label in NodeNxLabels if int(Label.split('_')[0]) == Ht and Label.split('_')[1] == NodePosLabel]
    return len (NodeLabelsInSameGt)+1

def GetNodeNxLabel (NodePosLabel, Ht, NodeNxLabels):
    return str(Ht)+'_'+str(NodePosLabel)+'_'+ str(GetLabelsUniqueIndex (NodePosLabel, Ht, NodeNxLabels))

def getNodes(TreeBeginningAtRoot, NodeNxLabels = [], NxEdges = []):
    global ParStr, GrandPar
    for Node in TreeBeginningAtRoot:
        if type(Node) is nltk.Tree:
            NodePosLabel = Node.label();Ht = Node.height()
            NodeNxLab = GetNodeNxLabel (NodePosLabel, Ht, NodeNxLabels)
            NodeNxLabels.append(NodeNxLab)
            # print "Label: ",NodeNxLab
            Edge = (ParStr, NodeNxLab)
            NxEdges.append(Edge)
            GrandPar = ParStr
            ParStr = NodeNxLab
            getNodes(Node, NodeNxLabels)

        else:
            NodePosLabel = Node; Ht = 1
            NodeNxLab = GetNodeNxLabel (NodePosLabel, Ht, NodeNxLabels)
            NodeNxLabels.append(NodeNxLab)
            # print "Label: ", NodeNxLab
            Edge = (ParStr, NodeNxLab)
            NxEdges.append(Edge)
            ParStr = GrandPar
    return NodeNxLabels, NxEdges


def GetChildren(SubTree):
    Children = []
    for Node in SubTree:
        if type(Node) is nltk.Tree:
            Children.append(Node.label(), Node.height())
        else:
            Children.append(Node)
    return Children


def MyTest (TreeBeginningAtRoot):
    for Node in TreeBeginningAtRoot:
        if type(Node) is nltk.Tree:
            print 'Node: {}, Ht: {}'.format(Node.label(), Node.height())
            pprint (GetChildren(Node))

        else:
            print 'Node: {}, Ht: {}'.format(str(Node), '1')


def MakeNxParseTrees (TreeStr):
    SentTree = Tree.fromstring (TreeStr)
    # NodeNxLabels, NxEdges = getNodes(SentTree)
    # pprint (NodeNxLabels)
    # pprint (NxEdges)
    MyTest (SentTree)
    SentTree.pretty_print()
    # NxTree = nx.DiGraph()
    # NxTree.add_edges_from(NxEdges)
    # pprint (NxTree.edges())


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
