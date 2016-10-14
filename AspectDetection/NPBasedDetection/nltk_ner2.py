import nltk
import os
import subprocess
import pickle
import email
import time
import numpy as np
from nltk import pos_tag
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
from collections import Counter

enron_dir = '/home/luz1sgp/nltk-code/enron'

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
    return "" # Return an empty string

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

# Process text  
def process_text(mail_file):
  
  text = get_email_body(mail_file)

  tokens = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]
  #tokens = filter(lambda word: word not in ',-.', tokens)
  tokens = filter(lambda word: len(word)>1, tokens)
  return list(tokens)

# NLTK POS and NER taggers   
def nltk_tagger(token_text):
  tagged_words = nltk.pos_tag(token_text)
  ne_tagged = nltk.ne_chunk(tagged_words)
  return(ne_tagged)

# Parse named entities from tree
def structure_ne(ne_tree):
  ne = []
  for subtree in ne_tree:
    if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
      ne_label = subtree.label()
      ne_string = " ".join([token for token, pos in subtree.leaves()])
      ne.append((ne_string, ne_label))
  return ne

def filter_sender_from_counter(first_name, last_name, counter):
  ne_list = list(counter)
  for word in ne_list:
    if first_name in word[0] or last_name in word[0]:
      del counter[word]
  
  return counter

def freq_counter_per_sender(*files):
  """
  Take a list of email files, which must be sent by a single person.
  Outputs and pickles a counter object of named entities. 
  """
  first_name, last_name = get_sender_name(files[0])
  first_name = first_name[0].upper() + first_name[1:]
  last_name = last_name[0].upper() + last_name[1:]

  cnt = Counter()
  start_time = time.time()
  num_files = 0
  for file in files:
    nltk_stanford_ne = structure_ne(nltk_tagger(process_text(file)))
    for t in nltk_stanford_ne:
      cnt[t] += 1

    elapsed_time = time.time() - start_time
    num_files += 1
    print("Sender: %s | Finished file: %s | Number of files processed: %s | Time taken: %s" % (first_name, file, str(num_files), str(elapsed_time)))
  
  # Remove the first_name and last_name of the sender
  cnt = filter_sender_from_counter(first_name, last_name, cnt)

  os.chdir(enron_dir + '/pickles')
  cnt_file = open(first_name +'.' + last_name + ".cnt.pickle", "wb")
  pickle.dump(cnt, cnt_file)
  cnt_file.close()
  print(cnt.most_common(10))
  os.chdir(enron_dir + '/maildir')

if __name__ == '__main__':
  
  os.chdir(enron_dir + '/maildir')
  persons = subprocess.getoutput('ls -1')
  persons = persons.split('\n')
  
  for person in persons:
    try:
      os.chdir( enron_dir + '/maildir/' + person + '/sent')
    except FileNotFoundError:
      print('No "sent" folder found for %s.' % person) 
      continue

    files = subprocess.getoutput('ls -1')
    files = files.split('\n')
    freq_counter_per_sender(*files)
