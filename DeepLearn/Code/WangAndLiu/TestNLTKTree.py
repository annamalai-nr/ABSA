from nltk.tree import ParentedTree
from collections import OrderedDict
import nltk
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint
import json
from networkx.drawing.nx_agraph import write_dot

Par = ''
NodeNxLabels = []

def GetLabelsUniqueIndex (NodePosLabel, Ht, NodeNxLabels):
    NodeLabelsInSameGt = [Label for Label in NodeNxLabels if int(Label.split('_')[0]) == int(Ht) and Label.split('_')[1] == NodePosLabel]
    return len (NodeLabelsInSameGt)+1

def GetNodeNxLabel (NodePosLabel, Ht, NodeNxLabels):
    return str(Ht)+'_'+str(NodePosLabel)+'_'+ str(GetLabelsUniqueIndex (NodePosLabel, Ht, NodeNxLabels))

def GetParNodeNxLabel(ParPosLabel, ParHt, NodeNxLabels):
    if ParPosLabel.lower() == 'root':
        return ParPosLabel
    ParLevelNodes = [Node for Node in NodeNxLabels if int(Node.split('_')[0]) == int(ParHt) and Node.split('_')[1]==ParPosLabel]
    MaxParLevelNodeIndex = max([int(Node.split('_')[-1]) for Node in ParLevelNodes])
    ParNodeNxLabel = str(ParHt)+'_'+str(ParPosLabel)+'_'+str(MaxParLevelNodeIndex)
    return ParNodeNxLabel

def traverse(t, Edges = []):

    global Par
    global NodeNxLabels
    try:
        t.label()
    except AttributeError:
        return
    else:
        for child in t:
            # print '*'*10
            try:
                Ht = child.height()
                NodeNxLab = GetNodeNxLabel(child.label(), Ht,NodeNxLabels)
                NodeNxLabels.append(NodeNxLab)
                ParHt = child.parent().height()
                ParentNxLab =  GetParNodeNxLabel(child.parent().label(),ParHt, NodeNxLabels)
                Par = deepcopy(NodeNxLab)
                # print NodeNxLab, ParentNxLab
                Edges.append((ParentNxLab, NodeNxLab))
            except:
                NodeNxLab = GetNodeNxLabel(child, 1,NodeNxLabels)
                NodeNxLabels.append(NodeNxLab)
                # print NodeNxLab, Par
                Edges.append((Par, NodeNxLab))

            # print '*' * 10
            # raw_input()
            traverse(child, Edges)

# TreeStr = '(ROOT (S (NP (JJ Congressional) \
#     (NNS representatives)) (VP (VBP are) (VP (VBN motivated) \
#     (PP (IN by) (NP (NP (ADJ shiny) (NNS money))))))) (. .))'
# TreeStr = '(ROOT (NP (NP (JJ great) (NN food)) (, ,) (NP (NP (JJ great) (NN decor)) (, ,) (NP (JJ great) (NN service))) (. .)))'

with open ('../../Data/CoreNLPParsed.json') as FH:
    CoreNLPParsedSents = json.load(FH)

OpCoreNLPParsedSents = deepcopy(CoreNLPParsedSents)

for TextSampleIndex, TextSample in enumerate(CoreNLPParsedSents):
    for SentenceIndex, SentenceDict in enumerate(TextSample['sentences']):
        TreeStr = SentenceDict['parsetree']
        SentTree = nltk.tree.ParentedTree.fromstring(TreeStr)
        SentTree.pretty_print()
        ptree = ParentedTree.fromstring(TreeStr)
        Edges = []
        traverse(ptree, Edges)
        G = nx.DiGraph()
        G.add_edges_from(Edges)
        OpCoreNLPParsedSents[TextSampleIndex]['sentences'][SentenceIndex]['NxGraph'] = deepcopy(G)
        DotFName = str(TextSampleIndex)+'_'+str(SentenceIndex)+'.dot'
        write_dot(G, DotFName)
        raw_input(DotFName)


