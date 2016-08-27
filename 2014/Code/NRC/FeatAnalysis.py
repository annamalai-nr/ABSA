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
from scipy.sparse import csr_matrix
from scipy.sparse import hstack

from LexFeatsProcessor import LoadStemmedLex, GetLexFeats
from Simple5FoldClassifier import SpaceTokenizer, GetYFromStringLabels, GetLexFeats, GetXYVocab

X, Y, Vocab = GetXYVocab()
X_train, X_test, y_train, y_test = train_test_split (X, Y, test_size = 0.2,random_state=randint(0,100))
print 'train and test shapes', X_train.shape, X_test.shape, np.array(y_train).shape, np.array(y_test).shape
Classifier = LinearSVC(C=10)
Classifier.fit(X_train, y_train)
Preds = Classifier.predict(X_test)
Acc = accuracy_score(y_true = y_test, y_pred=Preds)
P = precision_score(y_true = y_test, y_pred=Preds)
R = recall_score(y_true = y_test, y_pred=Preds)
F = f1_score(y_true = y_test, y_pred=Preds)
print (Acc,P,R,F)
print classification_report (y_test, Preds)

