import os, sys, json, numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.svm import LinearSVC
from pprint import pprint
from sklearn.cross_validation import train_test_split
from collections import Counter
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn import grid_search
from random import randint
from nltk.stem.porter import PorterStemmer
from MakeNRCFeats import tokenize
from scipy.sparse import csr_matrix
from scipy.sparse import hstack

stemmmer = PorterStemmer()

def SpaceTokenizer (Str):
    return [l.strip().split() for l in Str.split('\n') if l]

def GetYFromStringLabels (Labels):
    Y = []
    for L in Labels:
        if 'positive' == L:
            Y.append(1)
        elif 'negative' == L:
            Y.append(-1)
        elif 'neutral' == L:
            Y.append(0)
        elif 'conflict' == L:
            Y.append(2)
        else:
            # print 'error case'
            Y.append(0)
    return Y

def PerformFeatAnalysis (Classifier, X_train, Y, Vocab):
    Coeff = Classifier.coef_
    print type(Coeff)
    print Coeff.shape
    raw_input()

def LoadStemLexWord (PosFName, NegFName):
    Pos = [l.strip().lower() for l in open (PosFName).xreadlines()]
    Neg = [l.strip().lower() for l in open (NegFName).xreadlines()]
    Pos = set([stemmmer.stem(W) for W in Pos])
    Neg = set([stemmmer.stem(W) for W in Neg])
    return Pos, Neg

def LoadStemmedLex ():
    HuLiu = LoadStemLexWord ('../Lex/HuAndLiu/HuLiuPositive.txt', '../Lex/HuAndLiu/HuLiuNegative.txt')
    Nrc = LoadStemLexWord ('../Lex/NRC-Emotion-Lexicon-v0.92/NRCEmotionsPositive.txt',
                                    '../Lex/NRC-Emotion-Lexicon-v0.92/NRCEmotionsNegative.txt')
    Subj = LoadStemLexWord ('../Lex/subjectivity_clues_hltemnlp05/SubjPositive.txt',
                                  '../Lex/subjectivity_clues_hltemnlp05/SubjNegative.txt')
    StemmedLexicons = [HuLiu, Nrc, Subj]
    return StemmedLexicons

def GetLexTriplet (Tokens, PosLex, NegLex):
    PosScore = []
    NegScore = []
    for T in Tokens:
        if T in PosLex:
            PosScore.append(T)
            continue
        if T in NegLex:
            NegScore.append(T)
    # print Tokens
    # print PosScore
    # print NegScore
    NumPos = len (PosScore)
    NumNeg = len(NegScore)
    SumPosNeg = NumPos - NumNeg
    Triplet = (NumPos, NumNeg, SumPosNeg)
    # print Triplet
    # raw_input()
    return Triplet

def GetLexFeats(Sent, StemmedLexicons):
    # print Sent
    HLPos, HLNeg = StemmedLexicons[0]
    NrcPos, NrcNeg = StemmedLexicons[1]
    SubjPos, SubjNeg = StemmedLexicons[2]
    Tokens = tokenize(Sent.lower())
    HLScores = GetLexTriplet (Tokens, PosLex = HLPos, NegLex = HLNeg)
    NrcScores = GetLexTriplet (Tokens, PosLex = NrcPos, NegLex = NrcNeg)
    SubjScores = GetLexTriplet (Tokens, PosLex = SubjPos, NegLex = SubjNeg)
    AllLexFeats = [HLScores, NrcScores, SubjScores]
    AllLexFeats = [item for sublist in AllLexFeats for item in sublist]
    return AllLexFeats



StemmedLexicons = LoadStemmedLex()
Lines = [l.strip() for l in open ('../AllNRCFeatsRestAspCatABSA.txt').xreadlines()]
Sentences = [''.join(l.strip().split(';')[:-2]) for l in open ('../RestAspCatABSA.csv').xreadlines()]
LexFeats = [GetLexFeats(Sent, StemmedLexicons) for Sent in Sentences]
LexFeats = np.array (LexFeats)
LexFeats = csr_matrix (LexFeats)
print 'loaded lexicon features of shape', LexFeats.shape

Samples, Labels = zip(*[tuple(L.split(';')) for L in Lines])
Y = GetYFromStringLabels(Labels)
print 'loaded {} samples'.format(len(Samples))
print 'Label dist: ', Counter(Y)

Accs = [];Ps = [];Rs = [];Fs = []
CountVecter = CountVectorizer(lowercase=False,dtype=np.float64,binary=False)#,max_df=0.95)
X = CountVecter.fit_transform(Samples)
# X = Normalizer().fit_transform(X)
print 'shape of X matrix before adding lex feats', X.shape
X = hstack([X,LexFeats])
print 'shape of X matrix after adding lex feats',X.shape
Vocab = CountVecter.get_feature_names() + ['HLPos', 'HLNeg', 'HLSum', 'NrcPos', 'NrcNeg', 'NrcSum', 'SubjPos', 'SubjNeg', 'SubjSum']
# print (Vocab[:10])
# pprint(np.dot(X[1],X[1].T).todense())
print 'FVs prepared of shape',X.shape
for i in xrange (5):
    print 'run ',i+1
    X_train, X_test, y_train, y_test = train_test_split (X, Y, test_size = 0.2,random_state=randint(0,100))
    print 'train and test shapes', X_train.shape, X_test.shape, np.array(y_train).shape, np.array(y_test).shape
    Params = {'C':[0.001,0.01,0.1,1,10,100,1000]}
    Classifier = grid_search.GridSearchCV(LinearSVC(), Params,n_jobs=-1,cv=5)
    print 'best estimator after 5 fold CV: ', Classifier.best_estimator_
    Classifier = LinearSVC(C=0.1,class_weight='balanced')
    Classifier.fit(X_train, y_train)

    # PerformFeatAnalysis (Classifier, X_train, Y, Vocab)

    Preds = Classifier.predict(X_test)
    Acc = accuracy_score(y_true = y_test, y_pred=Preds)
    P = precision_score(y_true = y_test, y_pred=Preds)
    R = recall_score(y_true = y_test, y_pred=Preds)
    F = f1_score(y_true = y_test, y_pred=Preds)
    Accs.append(Acc); Ps.append(P);Rs.append(R);Fs.append(F)
    print (Acc,P,R,F)
    print classification_report (y_test, Preds)

Accs = np.array (Accs)
Ps = np.array (Ps)
Rs = np.array (Rs)
Fs = np.array (Fs)
MeanA = np.mean(Accs); StdA = np.std(Accs)
MeanP = np.mean(Ps); StdP = np.std(Ps)
MeanR = np.mean(Rs); StdR = np.std(Rs)
MeanF = np.mean(Fs); StdF = np.std(Fs)

print 'Average Acc: {}, Prec: {}, Recall: {}, F1: {}'.format(MeanA, MeanP, MeanR, MeanF)
print 'Std Acc: {}, Prec: {}, Recall: {}, F1: {}'.format(StdA, StdP, StdR, StdF)


