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

def get_email_body(mail_file):
  """
  http://stackoverflow.com/questions/17874360/python-how-to-parse-the-body-from-a-raw-email-given-that-raw-email-does-not
  """
  try:
    file = open(mail_file, 'r')
    b = email.message_from_file(file)
    file.close()
  except: #UnicodeDecodeError, IsADirectoryError etc
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

def process_text(mail_file):
  """
  tokenization
  """
  text = get_email_body(mail_file)
  tokens = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]
  #tokens = filter(lambda word: word not in ',-.', tokens)
  #tokens = filter(lambda word: len(word)>1, tokens)
  return list(tokens)

def filter_sender_from_counter(first_name, last_name, counter):
  ne_list = list(counter)
  for word in ne_list:
    if first_name in word[0] or last_name in word[0]:
      del counter[word]
  
  return counter

def tag_all_mails(*files):
  
  all_tagged_words = []
  for file in files:
    tagged_words = nltk.pos_tag(process_text(file))
    all_tagged_words += tagged_words

  return all_tagged_words
  
if __name__ == '__main__':
  
  maildir = '/Users/luz1sgp/code/nltk-code/enron/maildir/'
  pickle_dir ='/Users/luz1sgp/code/nltk-code/enron/freq_pickles'
  filename = "all_tagged_words.sent.sent_items.pickle"

  os.chdir(pickle_dir)
  if os.path.exists(filename) and os.path.isfile(filename):
    print(filename + " exist! Just load it! ")
    sys.exit()
  
  os.chdir(maildir)
  persons = subprocess.getoutput('ls -1')
  persons = persons.split('\n')
  
  all_tagged_words = []
  
  genesis_time = time.time()
  for person in persons:
    person_start_time = time.time()
    try:
      os.chdir(maildir + person + '/sent')
    except FileNotFoundError:
      print("No 'sent' folder for %s." % person)
    else:
      files = subprocess.getoutput('ls -1 | sort -n')
      files = files.split('\n')
      all_tagged_words += tag_all_mails(*files)

    try:
      os.chdir(maildir + person + '/sent_items')
    except FileNotFoundError:
      print("No 'sent_items' folder for %s." % person)
    else:
      files = subprocess.getoutput('ls -1 | sort -n')
      files = files.split('\n')
      all_tagged_words += tag_all_mails(*files)

    lap_time = time.time() - person_start_time # lap_time for one person
    elapsed_time = time.time() - genesis_time
    print("Sender: %s | Time taken: %f | Total time: %f" % (person, lap_time, elapsed_time))

  print("Total number of words %d" % len(all_tagged_words))

  # Pickle the result
  os.chdir(pickle_dir)
  with open(filename, 'wb') as f: pickle.dump(all_tagged_words, f)
