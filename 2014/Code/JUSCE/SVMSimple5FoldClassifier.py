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


def GetXYVocab (NSamples = -1):
    Samples = [' ## '.join (l.strip().split(' ## ')[:-1]) for l in open ('../../Data/JUSCEFeats.txt').xreadlines()][:NSamples]
    Labels = [l.strip().split(';')[-1] for l in open ('../../Data/RestAspCatABSA.csv')][:NSamples]
    Y = GetYFromStringLabels(Labels)
    print 'loaded {} samples'.format(len(Samples))
    print 'Label dist: ', pprint (dict(Counter(Y)))
    CountVecter = CountVectorizer(lowercase=False,dtype=np.float64,binary=False)#,max_df=0.95)
    X = CountVecter.fit_transform(Samples)
    X = Normalizer().fit_transform(X)
    print 'shape of X matrix ', X.shape
    Vocab = CountVecter.get_feature_names()
    return X,Y,Vocab


def Main():
    X, Y, Vocab = GetXYVocab()
    Accs = [];Ps = [];Rs = [];Fs = []
    for i in xrange (5):
        print 'run ',i+1
        X_train, X_test, y_train, y_test = train_test_split (X, Y, test_size = 0.2,random_state=randint(0,100))
        print 'train and test shapes', X_train.shape, X_test.shape, np.array(y_train).shape, np.array(y_test).shape
        Params = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}
        Classifier = grid_search.GridSearchCV(LinearSVC(), Params, n_jobs=-1, cv=3)
        Classifier.fit(X_train, y_train)
        print 'best estimator after 5 fold CV: ', Classifier.best_estimator_
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


if __name__ == '__main__':
    Main()