import sys,json
from pprint import pprint
from xml.etree import ElementTree
from collections import OrderedDict

def Main ():
    FName = sys.argv[1]

    with open(FName, 'rt') as f:
        tree = ElementTree.parse(f)

    print 'File: {} loaded using python xml parser'.format(FName)

    Sents = OrderedDict()
    for node in tree.iter():
        # print node, node.tag, node.attrib
        if node.tag == 'sentence':
            Id = node.attrib['id']
            Sents[Id] = OrderedDict ()
            Sents[Id]['Sentence'] = ''
            Sents[Id]['CatAndPolarity'] = OrderedDict()
            Sents[Id]['CatAndPolarity']['Cat'] = []
            Sents[Id]['CatAndPolarity']['Polarity'] = []
        if 'text' == node.tag:
            Sentence = "".join(node.itertext())
            Sents[Id]['Sentence'] = Sentence
        if 'aspectCategory' == node.tag:
            Sents[Id]['CatAndPolarity']['Cat'].append(node.attrib['category'])
            Sents[Id]['CatAndPolarity']['Polarity'].append(node.attrib['polarity'])

    OPFName = FName + '.json'
    with open (OPFName,'w') as FH:
        json.dump(Sents,FH,indent=4)

    print 'All sentences, asp categories and their polarity saved python dict in file ', OPFName


if __name__ == '__main__':
    Main()