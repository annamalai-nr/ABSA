import nltk
import os
import sys
import re
import subprocess
import pickle
import email
import time
import random
from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
from nltk.collocations import * 

def get_jj_nn_bigrams():

  with open("all_tagged_words.pickle", "rb") as f: 
    all_tagged_words = pickle.load(f)
  
  os.chdir(result_dir)

  bigram_measures = nltk.collocations.BigramAssocMeasures()
  
  # A convoluted  and manual way to get the variable name in Python
  bigram_measure_dict = dict(bigram_measures_raw_freq=bigram_measures.raw_freq, bigram_measures_pmi=bigram_measures.pmi, \
  	bigram_measures_likelihood_ratio=bigram_measures.likelihood_ratio, bigram_measures_student_t=bigram_measures.student_t, \
  	bigram_measures_chi_sq=bigram_measures.chi_sq)

  finder = BigramCollocationFinder.from_words(all_tagged_words, window_size=2)
  #finder = BigramCollocationFinder.from_words(all_tagged_words, window_size = 10)

  finder.apply_freq_filter(60) # freq > 60 for bigrams

  for k, v in bigram_measure_dict.items():
    collos = finder.nbest(v, 80000)
    jj_nn_collos = [ collo for collo in collos if collo[0][1][:2]=='JJ' and collo[1][1][:2]=='NN' ]
    #jj_nn_collos = [ collo for collo in collos if re.match('JJ.?', collo[0][1]) and re.match('NN.?', collo[1][1]) ]

    # Each token must contain at least one alphanumeric character
    jj_nn_collos = filter(lambda x:re.match(r'[\w]+',x[0][0]), jj_nn_collos)
    jj_nn_collos = list(jj_nn_collos)
    jj_nn_collos = filter(lambda x:re.match(r'[\w]+',x[1][0]), jj_nn_collos)

    with open('jj_nn_bigram_window10.' + k + '.txt', 'w') as f: 
      for jj_nn in jj_nn_collos: print(jj_nn, file=f)

def get_nn_bigrams(pickle_file):
  os.chdir(pickle_dir)
  with open(pickle_file, "rb") as f: 
    all_tagged_words = pickle.load(f)
  
  os.chdir(result_dir)

  # nn-nn bigrams
  finder = BigramCollocationFinder.from_words(all_tagged_words, window_size=2)
  finder.apply_freq_filter(100) # freq > 100 for bigrams

  bigram_measures = nltk.collocations.BigramAssocMeasures()
  collos = finder.nbest(bigram_measures.pmi, 10000)
  
  nn_collos = [ collo for collo in collos if re.match('NN.?', collo[0][1]) and re.match('NN.?', collo[1][1]) ]
  
  # Each token has to contain at least one alphanumeric character
  nn = filter(lambda x:re.match(r'[\w]+',x[0][0]), nn_collos)
  nn = list(nn)
  nn = filter(lambda x:re.match(r'[\w]+',x[1][0]), nn)

  # Print out results to with
  with open('nn_nn_bigram.txt', 'w') as f:
    for n in nn: print(n[0][0]+" "+n[1][0]+" : "+n[0][1]+" "+n[1][1], file=f)

def get_nnn_trigams(pickle_file):

  os.chdir(pickle_dir)
  with open(pickle_file, "rb") as f: 
    all_tagged_words = pickle.load(f)
  
  os.chdir(result_dir)
  
  # nn-nn-nn trigram
  finder = TrigramCollocationFinder.from_words(all_tagged_words, window_size=3)
  finder.apply_freq_filter(50)

  trigram_measures = nltk.collocations.TrigramAssocMeasures()
  collos = finder.nbest(trigram_measures.raw_freq, 30000) # raw_freq is easy to compute, 30000 to get more results
  
  nnn_collos = [collo for collo in collos if re.match('NN.?', collo[0][1]) and re.match('NN.?', collo[1][1]) and re.match('NN.?', collo[2][1])]
  
  nn = filter(lambda x:re.match(r'[\w]+',x[0][0]), nnn_collos)
  nn = list(nn)
  nn = filter(lambda x:re.match(r'[\w]+',x[1][0]), nn)
  nn = list(nn)
  nn = filter(lambda x:re.match(r'[\w]+',x[2][0]), nn)

  with open('nn_nn_nn_trigram.txt', 'w') as f:
    for n in nn: print(n[0][0]+" "+n[1][0]+" "+n[2][0] + " : "+n[0][1]+" "+n[1][1]+" " +n[2][1], file=f)

if __name__ == '__main__':
  
  result_dir = '/Users/luz1sgp/code/nltk-code/enron/freq_result_unigram_bigram/'
  pickle_dir ='/Users/luz1sgp/code/nltk-code/enron/freq_pickles/'
  pickle_file = "all_tagged_words.sent.sent_items.pickle"

  os.chdir(pickle_dir)
  #get_nn_bigrams(pickle_file)
  get_nnn_trigams(pickle_file)
