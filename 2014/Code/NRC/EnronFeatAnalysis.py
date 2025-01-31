import numpy as np
from sklearn.svm import LinearSVC
from pprint import pprint
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from EnronSimple5FoldClassifier import GetXYVocab
from copy import deepcopy
from scipy.sparse import csr_matrix

def GetTopN (W, Vocab, N=20):
    FeatsAndVocab = zip(W.tolist(), Vocab)
    FeatsAndVocab.sort()
    FeatsAndVocab.reverse()
    return FeatsAndVocab[:N]

def AnalyseClassifierFeats (Classifier, Vocab, TopN=20):
    W = deepcopy(Classifier.coef_)
    NegW = W[0,:]
    NeuW = W[1,:]
    PosW = W[2,:]
    # ConfW = W[3,:]

    TopNeg = GetTopN(NegW, Vocab, TopN)
    TopNeu = GetTopN(NeuW, Vocab, TopN)
    TopPos = GetTopN(PosW, Vocab, TopN)
    # TopConf =  GetTopN(ConfW, Vocab, TopN)
    # return TopNeg, TopNeu, TopPos, TopConf
    return TopNeg, TopNeu, TopPos


def AnalyseSampleFeats(X, Y, Classifier, Vocab, Sentences):
    W = deepcopy(Classifier.coef_)
    for Index in xrange(X.shape[0]):
        Sent = Sentences[Index]
        Sample = X[Index,:]
        PredLabel = Classifier.predict(Sample)[0]
        ChosenW = csr_matrix(W[PredLabel, :])
        FeatsTimesW = ChosenW.multiply(Sample)
        FeatsTimesW = FeatsTimesW.todense().T.tolist()
        FeatsTimesW = [Val for List in FeatsTimesW for Val in List]
        FeatsTimesWAndVocab = zip(FeatsTimesW,Vocab)
        FeatsTimesWAndVocab.sort()
        FeatsTimesWAndVocab.reverse()

        print '*'*80
        print 'Sentence: {}    actual label:{},    pred label: {} '.format(Sent, Y[Index], PredLabel)
        print '-' * 80
        print 'Top 20 feats: '
        pprint (FeatsTimesWAndVocab[:20])
        print '*' * 80
        raw_input()


NumSamples = -1
X, Y, Vocab = GetXYVocab(NumSamples)
# Sentences = [l.strip() for l in open ('../../Data/RestAspCatABSA.csv').xreadlines()][:NumSamples]
Sentences = [l.strip() for l in open ('EnronAspCatsAnkitShanSangSangSents.csv').xreadlines()][:NumSamples]
Classifier = LinearSVC(C=0.01)
Classifier.fit(X, Y)
Preds = Classifier.predict(X)
Acc = accuracy_score(y_true = Y, y_pred=Preds)
print classification_report (Y, Preds)

X = csr_matrix(X)
TopN = 20
# TopNeg, TopNeu, TopPos, TopConf = AnalyseClassifierFeats (Classifier, Vocab, TopN)
TopNeg, TopNeu, TopPos = AnalyseClassifierFeats (Classifier, Vocab, TopN)
print '*'*80
print 'top {} pos feats: '.format(TopN);pprint (TopPos);print '*'*80
print 'top {} neg feats: '.format(TopN);pprint(TopNeg);print '*'*80
print 'top {} neu feats: '.format(TopN);pprint(TopNeu);print '*'*80
# print 'top {} conf feats: '.format(TopN);pprint(TopConf);print '*'*80


AnalyseSampleFeats(X, Y, Classifier, Vocab, Sentences)
