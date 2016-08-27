import os, sys, json, numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.svm import LinearSVC
from pprint import pprint
from sklearn.cross_validation import train_test_split
from collections import Counter
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn import grid_search
from random import randint, shuffle
from itertools import chain
from collections import OrderedDict
from copy import deepcopy

import nltk
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import RandomizedSearchCV

import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

def TrainTestSplit (x, y, test_size = 0.2,random_state=42):
    Tmp = zip (x, y)
    shuffle (Tmp)
    x, y = zip (*Tmp)
    train_size = 1 - test_size
    CutOff = int(train_size *len(x))
    x_train = x[:CutOff]
    y_train = y[:CutOff]
    x_test = x[CutOff:]
    y_test = y[CutOff:]
    return x_train, x_test, y_train, y_test

def GetYFromStringLabels (Labels):
    Y = []
    for L in Labels:
        if 'positive' == L:
            Y.append([1])
        elif 'negative' == L:
            Y.append([-1])
        elif 'neutral' == L:
            Y.append([0])
        elif 'conflict' == L:
            Y.append([2])
        else:
            # print 'error case'
            Y.append([0])
    return Y

def GetListOfDict (X):
    X_OP = []
    for Sents in X:
        ListOfDict = []
        SentAsDict = OrderedDict()
        for Index, SentFeat in enumerate(Sents):
            SentAsDict[str(Index)] = str(SentFeat)
        ListOfDict.append(SentAsDict)
        X_OP.append(ListOfDict)
    # print len(X_OP)
    # print len(X_OP[0])
    # print X_OP[0]
    # raw_input()
    return X_OP

X = [l.strip().split() for l in open ('../Data/JUSCEFeats.txt').xreadlines()]
Y = [[str(l.strip().split(';')[-1])] for l in open ('../Data/RestAspCatABSA.csv')]
print 'loaded {} samples and {} labels'.format(len(X), len (Y))
X_train, X_test, y_train, y_test = TrainTestSplit (X, Y, test_size = 0.2,random_state=randint(0,100))
print 'train and test shapes', len(X_train), len(X_test), len(y_train), len(y_test)
X_train = GetListOfDict(X=X_train)
X_test = GetListOfDict(X=X_test)
# print '****'
print X_test[0]
print y_test[0]
# raw_input()
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(X_train, y_train)

Preds = crf.predict(X_test)
Acc = accuracy_score(y_true = y_test, y_pred=Preds)
P = precision_score(y_true = y_test, y_pred=Preds)
R = recall_score(y_true = y_test, y_pred=Preds)
F = f1_score(y_true = y_test, y_pred=Preds)
print (Acc,P,R,F)



