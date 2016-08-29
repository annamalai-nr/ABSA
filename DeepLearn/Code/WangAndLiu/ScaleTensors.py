import os,sys,json,nltk
import numpy as np
from pprint import pprint
import networkx as nx
from nltk.tree import Tree

def ScaleAllSentenceTensors ():
    return None

ROOT = 'ROOT'

def GetLabelsUniqueIndex (NodePosLabel, Ht, NodeNxLabels):
    NodeLabelsInSameGt = [Label for Label in NodeNxLabels if int(Label.split('_')[0]) == Ht and Label.split('_')[1] == NodePosLabel]
    return len (NodeLabelsInSameGt)+1

def GetNodeNxLabel (NodePosLabel, Ht, NodeNxLabels):
    return str(Ht)+'_'+str(NodePosLabel)+'_'+ str(GetLabelsUniqueIndex (NodePosLabel, Ht, NodeNxLabels))

def getNodes(TreeBeginningAtRoot, NodeNxLabels = []):
    for Node in TreeBeginningAtRoot:
        if type(Node) is nltk.Tree:
            NodePosLabel = Node.label();Ht = Node.height()
            NodeNxLab = GetNodeNxLabel (NodePosLabel, Ht, NodeNxLabels)
            NodeNxLabels.append(NodeNxLab)
            # print "Label: ",NodeNxLab
            getNodes(Node, NodeNxLabels)
        else:
            NodePosLabel = Node; Ht = 1
            NodeNxLab = GetNodeNxLabel (NodePosLabel, Ht, NodeNxLabels)
            NodeNxLabels.append(NodeNxLab)
            # print "Label: ", NodeNxLab
    return NodeNxLabels

# def getEdges(TreeBeginningAtRoot, NodeNxLabels = [], NodeNxEdges = []):
#     for Node in TreeBeginningAtRoot:
#         if type(Node) is nltk.Tree:
#             NodePosLabel = Node.label();Ht = Node.height()
#             ParNodeNxLab = GetNodeNxLabel (NodePosLabel, Ht, NodeNxLabels)
#             NodeNxLabels.append(ParNodeNxLab)
#             for ChildNode in Node.child ():
#                 if type(ChildNode) is nltk.Tree:
#                     ChildNodePosLabel = ChildNode.label()
#                     ChildNodeHt = Ht - 1
#                     ChildNodeNxLab = GetNodeNxLabel(ChildNodePosLabel, ChildNodeHt, NodeNxLabels)
#                 else:
#                     ChildNodePosLabel = ChildNode.label()
#                     ChildNodeHt = 1
#                     ChildNodeNxLab = GetNodeNxLabel(ChildNodePosLabel, ChildNodeHt, NodeNxLabels)
#                 NodeNxEdges.append(ParNodeNxLab, ChildNodeNxLab)
#     return NodeNxEdges


def MakeNxParseTrees (TreeStr):
    SentTree = Tree.fromstring (TreeStr)
    NodeNxLabels = getNodes(SentTree)
    # Edges = getEdges(SentTree)
    pprint (NodeNxLabels)
    raw_input()
    # pprint(Edges)
    # raw_input()
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
