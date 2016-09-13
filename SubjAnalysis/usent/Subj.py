import os
import sys
import nltk
import pickle
import string
from nltk.stem.porter import PorterStemmer
from pprint import pprint
from my_sentiment import Sentiment


def ProcessSingleFile (FName):
    EmailText = [open(FName).read()]
    # sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    # Sents = sent_detector.tokenize(Text.strip())
    SentAnalyzer = Sentiment()
    # pprint (Sents)
    Sents = [u'I feel great. She is horrible. Test is ok. This is ok!']
    # Res = SentAnalyzer.analyze(Sents)
    Res = SentAnalyzer.analyze(EmailText)
    # pprint (Sents)
    # pprint (Res)
    pprint (zip(Res['sentences'],Res['sentiments'], Res['scores']))
    raw_input()


SkillingDir = '/home/annamalai/Moscato/Datasets/enron_mails_dir/skilling-j/inbox'
SkillingFiles = [os.path.join (SkillingDir,F) for F in os.listdir(SkillingDir) if os.path.isfile(os.path.join (SkillingDir,F))]
SkillingFiles.sort()
print 'found {} files from skilling inbox'.format (len(SkillingFiles))
for F in SkillingFiles:
    print F
    ProcessSingleFile (F)
    raw_input()