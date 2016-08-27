import os,sys, string
import nltk.data
from pprint import pprint
from time import time
from nltk.corpus import sentiwordnet as swn
from joblib import Parallel, delayed

SentenceDetector = nltk.data.load('tokenizers/punkt/english.pickle')

def tokenize(text):
    text = text.lower()
    text = "".join([ch for ch in text if ch not in string.punctuation])
    tokens = nltk.word_tokenize(text)
    # tokens = [word for word in tokens if word not in stopwords.words('english')]
    return tokens

def GetNumOfSentences (Sent):
    return len(SentenceDetector.tokenize(Sent))

def GetPosTags (Sent):
    Tokens = tokenize(Sent)
    PosTaggedToks = nltk.pos_tag(Tokens)
    PosTagSeq = ' '.join([Item[1] for Item in PosTaggedToks])
    return PosTagSeq

def GetSentiWords (Sent):
    Tokens = tokenize(Sent)
    PosTaggedToks = nltk.pos_tag(Tokens)
    SentiWordsInRev = []
    for Token, POSTag in PosTaggedToks:
        PosScore = ''
        NegScore = ''
        if 'NN' == POSTag:
            if not swn.senti_synsets(Token, 'n'): continue
            PosScore = swn.senti_synsets(Token, 'n')[0].pos_score()
            NegScore = swn.senti_synsets(Token, 'n')[0].neg_score()
        elif 'VB' == POSTag:
            if not swn.senti_synsets(Token, 'v'): continue
            PosScore = swn.senti_synsets(Token, 'v')[0].pos_score()
            NegScore = swn.senti_synsets(Token, 'v')[0].neg_score()
        elif 'JJ' == POSTag:
            if not swn.senti_synsets(Token, 'a'): continue
            PosScore = swn.senti_synsets(Token, 'a')[0].pos_score()
            NegScore = swn.senti_synsets(Token, 'a')[0].neg_score()
        elif 'RB' == POSTag:
            if not swn.senti_synsets(Token, 'r'): continue
            PosScore = swn.senti_synsets(Token, 'r')[0].pos_score()
            NegScore = swn.senti_synsets(Token, 'r')[0].neg_score()
        else:
            # print 'ignoring', Token
            continue
        if 0 == PosScore and 0 == NegScore:
            SentiWordsInRev.append(Token + "_neu")
        elif PosScore >= NegScore:
            SentiWordsInRev.append(Token + "_pos")
        elif NegScore > PosScore:
            SentiWordsInRev.append(Token + "_neg")
        else:
            continue
    return ' '.join(SentiWordsInRev)

def GetJUSCEFeatsFromSent (Sent, Index):
    T0 = time()
    try:
        PosTags = GetPosTags(Sent)
        SentiWords = GetSentiWords(Sent)
        NumSents = str(GetNumOfSentences(Sent))
        print 'done with sent: {} in {} sec'.format(Index, round (time()-T0,2))
        return PosTags, SentiWords, NumSents
    except:
        return '','',''

AllRevSents = [';'.join(l.strip().split(';')[:-2]) for l in open ('../../Data/RestAspCatABSA.csv')]#[:5]
Cats = ['cat_'+l.strip().split(';')[-2] for l in open ('../../Data/RestAspCatABSA.csv')]#[:5]
Delim = ['##' for _ in xrange(len (Cats))]


# POSTags = []
# SentiWords = []
# NumSentsInEachRev = []
# for Sent in AllRevSents:
#     PosTag, SentiWrd, NumSent = GetJUSCEFeatsFromSent(Sent)
#     POSTags.append(PosTag)
#     SentiWords.append(SentiWrd)
#     NumSentsInEachRev.append(NumSent)

Res = Parallel(n_jobs=36)(delayed(GetJUSCEFeatsFromSent)(Sent, Index) for Index, Sent in enumerate(AllRevSents))
POSTags,  SentiWords, NumSentsInEachRev = zip (*Res)
Feats = zip (POSTags, Delim, SentiWords, Delim, NumSentsInEachRev, Delim, Cats)
Feats = [' '.join (list(F)) for F in Feats]

with open ('JUSCEFeats.txt','w') as FH:
    for i in xrange(len(AllRevSents)):
        print >>FH, Feats[i]
