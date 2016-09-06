import numpy as np
from random import shuffle
from collections import Counter
import keras
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D, MaxPooling1D, AveragePooling2D
from time import time

def LoadData ():
    # X = np.loadtxt ('UnscaledX.txt')
    X = np.loadtxt ('ScaledX.txt')
    Y = [l.strip() for l in open ('Y.txt').xreadlines()]
    print 'loaded a X and Y matrices of shapes: ', X.shape, len(Y)
    return X, Y

def RandomizeXY (X, Y):
    Z = list(zip(X, Y))
    shuffle(Z)
    X, Y = zip(*Z)
    print 'randomized zip (X,Y)'
    return X, Y

def GetTrainTestSplit(X, Y, TrainPercent=0.8):
    TrCutOff = int(len(Y) * TrainPercent - 1)
    TeCutoff = TrCutOff - len(Y)
    print 'training and test cutoff:', TrCutOff, TeCutoff

    X_train = np.array(X[:TrCutOff])
    Y_train = np.array(Y[:TrCutOff])
    X_test = np.array(X[TeCutoff:])
    Y_test = np.array(Y[TeCutoff:])

    print 'X_train, Y_train, X_test, Y_test shapes'
    print X_train.shape
    print Y_train.shape
    print X_test.shape
    print Y_test.shape

    return X_train, Y_train, X_test, Y_test

def MakeYAsNum (Y):
    Ytmp = []
    for y in Y:
        if 'positive' == y:
            Ytmp.append (1)
        elif 'negative' == y:
            Ytmp.append(2)
        elif 'conflict' == y:
            Ytmp.append(3)
        else:
            Ytmp.append(0)
    return Ytmp


def Main ():
    X, Y = LoadData()
    X, Y = RandomizeXY (X, Y)
    X_train, Y_train, X_test, Y_test =  GetTrainTestSplit(X, Y, TrainPercent=0.8)

    MaxFeatsWithPadd = 69
    WordVecDims = 300

    X_train = X_train.reshape(X_train.shape[0],1, MaxFeatsWithPadd, WordVecDims)
    X_test = X_test.reshape(X_test.shape[0],1, MaxFeatsWithPadd, WordVecDims)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    print('X_train shape:', X_train.shape)
    print('X_test shape:', X_test.shape)
    print(X_train.shape[0], 'train samples')
    print(X_test.shape[0], 'test samples')


    Y_train = MakeYAsNum(Y_train)
    Y_test = MakeYAsNum(Y_test)

    print(Counter(Y_train))
    print(Counter(Y_test))

    nb_classes = 4

    Y_train = np_utils.to_categorical(Y_train, nb_classes)
    Y_test = np_utils.to_categorical(Y_test, nb_classes)


    nb_filters = 100
    nb_pool = 3
    model = Sequential()

    model.add(Convolution2D(nb_filters, 3, 3,
                            border_mode='valid',
                            input_shape=(1, 69, 300)))
    model.add(Activation('relu'))
    #model.add(Convolution2D(nb_filters, 3, 3))
    #model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])

    model.fit(X_train, Y_train, batch_size=50, nb_epoch=50,
              verbose=1, validation_data=(X_test, Y_test))
    T0 = time()
    score = model.evaluate(X_test, Y_test, verbose=1)
    print (time() - T0)


if __name__ == '__main__':
    Main ()