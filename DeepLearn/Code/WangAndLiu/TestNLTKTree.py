from nltk.tree import ParentedTree
import nltk
from copy import deepcopy
import networkx as nx
from pprint import pprint
import json
from networkx.drawing.nx_agraph import write_dot
from time import time

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

def traverse(t, Edges):
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
                Edges.append((ParentNxLab,NodeNxLab))
            except:
                NodeNxLab = GetNodeNxLabel(child, 1,NodeNxLabels)
                NodeNxLabels.append(NodeNxLab)
                # print NodeNxLab, Par
                Edges.append((Par,NodeNxLab))

            # print '*' * 10
            # raw_input()
            traverse(child, Edges)

def ProcessSingleSentenceTree (TreeStr, TextSampleIndex = 0, SentenceIndex = 0):
    global Par
    global NodeNxLabels

    # T0 = time()
    Par = ''
    NodeNxLabels = []
    PTree = ParentedTree.fromstring(TreeStr)
    # PTree.pretty_print()
    Edges = []
    traverse(PTree, Edges)
    G = nx.DiGraph();G.add_edges_from(Edges)
    # print 'done with sentence {} in {} sec'.format(str(TextSampleIndex)+'_'+str(SentenceIndex),
    #                                                round(time() - T0, 2))
    # DotFName = str(TextSampleIndex)+'_'+str(SentenceIndex)+'.dot'
    # write_dot(G, DotFName)
    # raw_input(DotFName)
    return G


def Main (CoreNLPDictFName = '../../Data/CoreNLPParsed.json'):
    T0 = time()
    with open (CoreNLPDictFName) as FH:
        CoreNLPParsedSents = json.load(FH)
    print 'gonna process {} sentences from {}'.format(len(CoreNLPParsedSents), CoreNLPDictFName)

    OpCoreNLPParsedSents = deepcopy(CoreNLPParsedSents)

    for TextSampleIndex, TextSample in enumerate(CoreNLPParsedSents):
        try:
            for SentenceIndex, SentenceDict in enumerate(TextSample['sentences']):
                TreeStr = SentenceDict['parsetree']
                G = ProcessSingleSentenceTree (TreeStr, TextSampleIndex, SentenceIndex)
                OpCoreNLPParsedSents[TextSampleIndex]['sentences'][SentenceIndex]['NxGraphEdges'] = G.edges()
        except:
            print 'unable to process text sample number: ', TextSampleIndex


    OPFName = CoreNLPDictFName.replace ('.json','.ParseTreeConvertedAsNxGraph.json')
    with open(OPFName,'w') as FH:
        json.dump(OpCoreNLPParsedSents, FH, indent=4)

    print 'processed all {} sentences and made nx graphs in {} sec'.format(len(CoreNLPParsedSents), round(time()-T0,2))
if __name__ == '__main__':
    Main()

