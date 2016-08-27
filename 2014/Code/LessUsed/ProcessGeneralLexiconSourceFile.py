import os, sys, json
from pprint import pprint


FName = '/home/annamalai/Desktop/ABSASemEval2014/Lex/NRC-Emotion-Lexicon-v0.92/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt'
Neg = [l.strip().split('\t')[0] for l in open (FName).xreadlines() if '\tnegative' in l if l.endswith('1\n')]
Pos = [l.strip().split('\t')[0] for l in open (FName).xreadlines() if '\tpositive' in l if l.endswith('1\n')]
Neg = list(set(Neg)); Neg.sort()
Pos = list(set(Pos)); Pos.sort()
with open ('NRCEmotionsNegative.txt','w') as FH:
    for N in Neg:
        print >>FH, N
with open ('NRCEmotionsPositive.txt','w') as FH:
    for P in Pos:
        print >>FH, P



FName = '/home/annamalai/Desktop/ABSASemEval2014/Lex/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff'
Pos = [l.strip().split('word1=')[1].split()[0] for l in open (FName).xreadlines() if 'priorpolarity=positive' in l]
Neg = [l.strip().split('word1=')[1].split()[0] for l in open (FName).xreadlines() if 'priorpolarity=negative' in l]
Neg = list(set(Neg)); Neg.sort()
Pos = list(set(Pos)); Pos.sort()
with open ('SubjNegative.txt','w') as FH:
    for N in Neg:
        print >>FH, N
with open ('SubjPositive.txt','w') as FH:
    for P in Pos:
        print >>FH, P