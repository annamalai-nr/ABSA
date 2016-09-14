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
        Cmd = 'java -jar '+JarFName+' "'+S+'".'
        print 'executing command', Cmd
        ResString = commands.getstatusoutput(Cmd)
        Asp = ResString[-1]
        # print Asp
        Asp = Asp.split('Aspects--')[-1].replace('[','').replace(']','')
        Asp = Asp.split(',')
        Asp = [A.strip() for A in Asp]
        print 'processes sent {} in {} sec'.format(I, round(time()-T0,2))
        # print Asp
        # raw_input()
        return Asp

    except:
        print 'unable to process sebt ', I
        return []

TgtFolder = '/mnt/AnnaLaptop/Desktop/ABSA/SubjAnalysis/usent/ToDelSkillingSubjRes'
FilesToProcess = [os.path.join(TgtFolder,F) for F in os.listdir(TgtFolder) if F.endswith('_Subj.json')]
print 'have to process {} json files from {}'.format(len(FilesToProcess), TgtFolder)
raw_input('hit any key to proceed...')

for FName in FilesToProcess:
    with open (FName) as FH:
        SubjDict = json.load(fp=FH)
    Sents = [ThreeTup[0] for MailNum, Sentences in SubjDict.iteritems() for ThreeTup in Sentences]#[2:4]
    print 'loaded {} subj sentences from {}'.format(len(Sents), FName)

    # for I, S in enumerate(Sents):
    #     ExecCmdLine (S,I)

    AspPerSent = Parallel(n_jobs=36)(delayed(ExecCmdLine)(S, I) for I, S in enumerate(Sents))
    ResTuple = zip (Sents, AspPerSent)
    OpFName = FName.replace('.json', '_ApsPerSent.json')
    with open (OpFName,'w') as FH:
        json.dump(obj=ResTuple, fp=FH, indent=4)
