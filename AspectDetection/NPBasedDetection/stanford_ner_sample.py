import nltk
import os
import subprocess
import pickle
import email
import time
import random
import numpy as np
from nltk import pos_tag
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
from collections import Counter

enron_dir = '/home/luz1sgp/nltk-code/enron'
stanford_jar_dir = '/home/luz1sgp/nltk-code'

def get_email_body(mail_file):
  """
  http://stackoverflow.com/questions/17874360/python-how-to-parse-the-body-from-a-raw-email-given-that-raw-email-does-not
  """
  try:
    file = open(mail_file, 'r')
    b = email.message_from_file(file)
    file.close()
  except UnicodeDecodeError as e:
    print(e)
    return "Dummy body" # Return
  except FileNotFoundError:
    print("File %s not found!" % mail_file)
    return "Dummy body"

  all_payload=''
  if b.is_multipart():
    for payload in b.get_payload():
      # if payload.is_multipart(): ...
      all_payload += payload.get_payload()
  else:
    all_payload = b.get_payload()

  return all_payload

def get_sender_name(mail_file):
  file = open(mail_file, 'r')
  msg = email.message_from_file(file)
  file.close()
  
  name = msg['From'].split('@')[0]
  last_name = name.split('.')[0]
  first_name = name.split('.')[1]
  
  return (first_name, last_name)

def filter_sender_from_counter(first_name, last_name, counter):
  ne_list = list(counter)
  for word in ne_list:
    if first_name in word[0] or last_name in word[0]:
      del counter[word]
  
  return counter

def sample_n(start, end, n):
  """
  Given int start and end, both inclusive, return a list of n samples.
  """
  if end-start+1 <= n:
   return list(range(start, end+1))

  random_set = set() # Return a unique set of samples

  while len(random_set) < n:
    random_set.add(random.randint(start,end))
  return sorted(list(random_set))

"""
Named entity recoginiztion pipeline starts
"""
# Tokenization 
def tokenize_text(txt_file):
  
  text = get_email_body(txt_file)

  tokens = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]
  tokens = filter(lambda word: word not in ',-.;:?!', tokens)
  tokens = filter(lambda word: len(word)>=2, tokens)
  return list(tokens)

# Stanford NER tagger    
def stanford_tagger(token_text):

  st = StanfordNERTagger(stanford_jar_dir + "/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz",
    stanford_jar_dir + "/stanford-ner-2015-12-09/stanford-ner.jar", encoding="utf-8")

  ne_tagged = st.tag(token_text)
  return(ne_tagged)

# Tag tokens with standard NLP BIO tags
def bio_tagger(ne_tagged):
  bio_tagged = []
  prev_tag = "O"
  for token, tag in ne_tagged:
    if tag == "O": #O
      bio_tagged.append((token, tag))
      prev_tag = tag
      continue
  
    if tag != "O" and prev_tag == "O": # Begin NE
      bio_tagged.append((token, "B-"+tag))
      prev_tag = tag
    elif prev_tag != "O" and prev_tag == tag: # Inside NE
      bio_tagged.append((token, "I-"+tag))
      prev_tag = tag
    elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
      bio_tagged.append((token, "B-"+tag))
      prev_tag = tag

  return bio_tagged

# Create tree       
def stanford_tree(bio_tagged):
  tokens, ne_tags = zip(*bio_tagged)
  pos_tags = [pos for token, pos in pos_tag(tokens)]

  conlltags = [(token, pos, ne) for token, pos, ne in zip(tokens, pos_tags, ne_tags)]
  ne_tree = conlltags2tree(conlltags)
  return ne_tree

# Parse named entities from tree
def structure_ne(ne_tree):
  ne = []
  for subtree in ne_tree:
    if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
      ne_label = subtree.label()
      ne_string = " ".join([token for token, pos in subtree.leaves()])
      ne.append((ne_string, ne_label))
  return ne

def freq_counter_per_sender(*files):
  """
  Take a list of email files, which must be sent by a single person.
  Outputs and pickles a counter object of named entities. 
  """
  first_name, last_name = get_sender_name(files[0])
  first_name = first_name[0].upper() + first_name[1:]
  last_name = last_name[0].upper() + last_name[1:]

  cnt = Counter()
  stanford_ne = []
  start_time = time.time()
  num_files = 0
  for file in files:
    try:
      stanford_ne = structure_ne(stanford_tree(bio_tagger(stanford_tagger(tokenize_text(file)))))
    except: # Throw away all errors
      print("File %s is corrupted" % file)
      continue

    for t in stanford_ne: cnt[t] += 1 # Accumulate the counters
    elapsed_time = time.time() - start_time
    total_time = time.time() - genesis_time
    num_files += 1
    print("Sender: %s | Finished file: %s | Number of files processed: %d | Time taken: %f | Total time: %f" % (first_name, file, num_files, elapsed_time, total_time))
  
  # Remove the first_name and last_name of the sender
  cnt = filter_sender_from_counter(first_name, last_name, cnt)

  os.chdir(enron_dir + '/stanford-pickles')
  cnt_file = open(first_name +'.' + last_name + "stanford.cnt.pickle", "wb")
  pickle.dump(cnt, cnt_file)
  cnt_file.close()
  print(cnt.most_common(10))
  os.chdir(enron_dir + '/maildir')

global genesis_time

if __name__ == '__main__':
  
  os.chdir(enron_dir + '/maildir')
  persons = subprocess.getoutput('ls -1')
  persons = persons.split('\n')
  
  genesis_time = time.time()

  for person in persons:
    try:
      os.chdir( enron_dir + '/maildir/' + person + '/sent')
    except FileNotFoundError:
      print('No "sent" folder found for %s.' % person) 
      continue

    files = subprocess.getoutput('ls -1 | sort -n')
    files = files.split('\n')
    
    # Create dictionary
    file_index = range(len(files))
    file_dict = dict(zip(file_index, files))
    
    # Sampling
    samples = sample_n(0, len(files)-1, 100)
    sample_files = [ file_dict[k] for k in samples ]
    
    #print(sample_files)
    freq_counter_per_sender(*sample_files)
