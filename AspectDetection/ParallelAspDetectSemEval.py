import os, sys, json
from pprint import pprint
from time import time
from joblib import Parallel, delayed
import commands
from nltk.tokenize import RegexpTokenizer

def ExecCmdLine (S, I, CleanPunc=True):
    if len (S) > 1200:
        print 'sentence is too long... hence avoiding processing'
        return ['SENTENCE TOO LONG']
    T0=time()
    S= S.lower()
    if CleanPunc:
        Tokenizer = RegexpTokenizer(r'\w+')
        S = ' '.join (Tokenizer.tokenize(S))

    try:
        JarFName = '/mnt/AnnaLaptop/Desktop/ABSA/AspectDetection/aspect_par1.jar'
        # JarFName = '/home/annamalai/Desktop/ABSA/AspectDetection/aspect_par1.jar'
        Cmd = 'java -jar '+JarFName+' "'+S+'".'
        print 'executing command', Cmd
        ResString = commands.getstatusoutput(Cmd)
        Asp = ResString[-1]
        # print Asp
        Asp = Asp.split('Aspects--')[-1].replace('[','').replace(']','')
        Asp = Asp.split(',')
        Asp = [A.strip() for A in Asp]
        print 'processes sent {} in {} sec'.format(I, round(time()-T0,2))
        print S
        print Asp
        # raw_input()
        return Asp

    except:
        print 'unable to process sebt ', I
        return []

IpFName = '/mnt/AnnaLaptop/Desktop/ABSA/2014/Data/LaptopAspTermDict.json'
# IpFName = '/home/annamalai/Desktop/ABSA/2014/Data/RestAspTermDict.json'
with open (IpFName) as FH:
    GTSentAspTermDict = json.load(FH)

Sents = GTSentAspTermDict.keys()#[:10]
print 'loaded {} sentences from {}'.format(len(Sents), IpFName)
raw_input('hit any key to continue...')

# AnkitSentAspTermDict = {Sent:[] for Sent in Sents}
# for I, S in enumerate(Sents):
#     AspTermList = ExecCmdLine (S,I)
    # print S
    # print AspTermList
    # raw_input()
    # AnkitSentAspTermDict[S] = AspTermList

AspPerSent = Parallel(n_jobs=36)(delayed(ExecCmdLine)(S, I) for I, S in enumerate(Sents))
AnkitSentAspTermDict = dict(zip (Sents, AspPerSent))
OpFName = IpFName.replace('LaptopAspTermDict', 'AnkitCodeLaptopAspTermDict')
with open (OpFName,'w') as FH:
    json.dump(obj=AnkitSentAspTermDict, fp=FH, indent=4)
