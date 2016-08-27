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

def MakeListofListsAsList (LL):
    L = [List[0] for List in LL]
    return L


def TrainTestSplit (x, y, test_size = 0.2, random_state=42):
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

X = [l.strip().split() for l in open ('../../Data/JUSCEFeats.txt').xreadlines()]
Y = [[str(l.strip().split(';')[-1])] for l in open ('../../Data/RestAspCatABSA.csv')]
print 'loaded {} samples and {} labels'.format(len(X), len (Y))


Accs = [];Ps = [];Rs = [];Fs = []
for i in xrange (5):
    print 'run ',i+1
    X_train, X_test, y_train, y_test = TrainTestSplit (X, Y, test_size = 0.2,random_state=randint(0,100))
    print 'train and test shapes', len(X_train), len(X_test), len(y_train), len(y_test)
    X_train = GetListOfDict(X=X_train)
    X_test = GetListOfDict(X=X_test)
    print '***for understanding***'
    print 'first test sample', X_test[0]
    print 'firsy test label', y_test[0]
    print '***for understanding***'

    # crf = sklearn_crfsuite.CRF(
    #     algorithm='lbfgs',
    #     max_iterations=100,
    #     all_possible_transitions=True
    # )
    # params_space = {
    #     'c1': scipy.stats.expon(scale=0.5),
    #     'c2': scipy.stats.expon(scale=0.05),
    # }
    # f1_scorer = make_scorer(metrics.flat_f1_score,
    #                         average='weighted')
    # rs = RandomizedSearchCV(crf, params_space,
    #                         cv=3,
    #                         verbose=1,
    #                         n_jobs=-1,
    #                         n_iter=50,
    #                         scoring=f1_scorer)
    # # crf.fit(X_train, y_train)
    # rs.fit(X_train, y_train)
    # print('best params:', rs.best_params_)
    # print('best CV score:', rs.best_score_)
    # print('model size: {:0.2f}M'.format(rs.best_estimator_.size_ / 1000000))
    # crf = rs.best_estimator_

    '''
    Fitting 3 folds for each of 50 candidates, totalling 150 fits
    [Parallel(n_jobs=-1)]: Done  34 tasks      | elapsed:   51.3s
    [Parallel(n_jobs=-1)]: Done 150 out of 150 | elapsed:  3.7min finished
    ('best params:', {'c2': 0.091369303934476731, 'c1': 0.32303608698891828})
    ('best CV score:', 0.54852921207232364)
    '''
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.32,
        c2=0.09,
        max_iterations=100,
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)
    Preds = crf.predict(X_test)
    y_test = MakeListofListsAsList (y_test)
    Preds = MakeListofListsAsList (Preds)

    Acc = accuracy_score(y_true = y_test, y_pred=Preds)
    P = precision_score(y_true = y_test, y_pred=Preds)
    R = recall_score(y_true = y_test, y_pred=Preds)
    F = f1_score(y_true = y_test, y_pred=Preds)
    # print Acc,P,R,F
    print classification_report (y_test, Preds)
    Accs.append(Acc); Ps.append(P); Rs.append(R); Fs.append(F)

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
