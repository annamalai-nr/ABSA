import jsonrpc,json
from simplejson import loads
from pprint import pprint
from joblib import Parallel, delayed


def ParseSingleSentence (Index, S):
    for Try in xrange(5):
        try:
            PS = loads(server.parse(S))
            print 'processed ', Index
            return PS
        except:
            print 'FAILED!!! to process sentence: {} try number: {}'.format(Index, Try)
            continue
    return {}


server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),
                             jsonrpc.TransportTcpIp(addr=("127.0.0.1", 8080)))

SentsAspectsLabelsFName = '../../2014/Data/RestAspCatABSA.csv'
SentsAspectsLabelsFName = '../../../../2014/Data/RestAspCatABSA.csv'
Sentences = [''.join(l.strip().split(';')[:-2]).lower() for l in open(SentsAspectsLabelsFName).xreadlines()][:5]
# ParsedSentences = Parallel(n_jobs=8)(delayed(ParseSingleSentence)(Index, S) for Index, S in enumerate(Sentences))
ParsedSentences = []
for Index, S in enumerate(Sentences):
    ParsedSentences.append(ParseSingleSentence(Index, S))

# with open ('CoreNLPParsed.json','w') as FH:
#     json.dump(ParsedSentences, FH, indent=4)

print 'parsed and saved all output in CoreNLPParsed.json'