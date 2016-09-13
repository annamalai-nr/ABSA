import os, json
from sentiment import Sentiment
from time import time
from joblib import Parallel, delayed
from pprint import pprint

def ProcessSingleFile (FName, MailNumber):
    T0 = time()
    # try:
    EmailText = [open(FName).read()]
    SentAnalyzer = Sentiment()
    Res = SentAnalyzer.analyze(EmailText)
    pprint (Res)
    SentSentimentPol = zip(Res['sentences'],Res['sentiments'],Res['scores'])
    SentSentimentPol = [ThreeTuple for ThreeTuple in SentSentimentPol if ThreeTuple[1] != 'neutral']
    print 'processed email {} in {} sec'.format(MailNumber, round(time()-T0))
    return SentSentimentPol
    # except:
    #     print 'failed to process email ', MailNumber
    #     return []


SkillingDir = '/mnt/AnnaLaptop/Moscato/Datasets/enron_mails_dir/skilling-j/discussion_threads'
SkillingFiles = [os.path.join (SkillingDir,F) for F in os.listdir(SkillingDir) if os.path.isfile(os.path.join (SkillingDir,F))][:-1]
SkillingFiles.sort()
print 'found {} files from skilling inbox'.format (len(SkillingFiles))
raw_input('hit any key to continue...')

T0 = time()
EmailsSubjRes = Parallel(n_jobs=36)(delayed(ProcessSingleFile)(F, I) for I, F in enumerate(SkillingFiles))
# EmailsSubjRes = []
# for I, F in enumerate(SkillingFiles):
#     EmailsSubjRes.append (ProcessSingleFile(F, I))
#     raw_input()
print 'processed emails in {} sec'.format(round(time()-T0))

try:
    Tmp = {os.path.basename(FName): EmailsSubjRes[FIndex] for FIndex, FName in enumerate(SkillingFiles)}
    with open('SkillingEmails_Subj.json', 'w') as FH:
        json.dump(obj=Tmp, fp=FH, indent=4)
except:
    Tmp = {os.path.basename(FName):unicode(str(EmailsSubjRes[FIndex]), errors='replace') for FIndex, FName in enumerate(SkillingFiles)}
    with open('SkillingEmails_Subj.json', 'w') as FH:
        json.dump(obj=Tmp, fp=FH, indent=4)