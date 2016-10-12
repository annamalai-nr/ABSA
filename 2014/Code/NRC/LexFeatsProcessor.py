from nltk.stem.porter import PorterStemmer
from MakeNRCFeats import tokenize


stemmmer = PorterStemmer()

def LoadStemLexWord (PosFName, NegFName):
    Pos = [l.strip().lower() for l in open (PosFName).xreadlines()]
    Neg = [l.strip().lower() for l in open (NegFName).xreadlines()]
    Pos = set([stemmmer.stem(W) for W in Pos])
    Neg = set([stemmmer.stem(W) for W in Neg])
    return Pos, Neg

def LoadStemmedLex ():
    HuLiu = LoadStemLexWord ('../../Lex/HuAndLiu/HuLiuPositive.txt', '../../Lex/HuAndLiu/HuLiuNegative.txt')
    Nrc = LoadStemLexWord ('../../Lex/NRC-Emotion-Lexicon-v0.92/NRCEmotionsPositive.txt',
                                    '../../Lex/NRC-Emotion-Lexicon-v0.92/NRCEmotionsNegative.txt')
    Subj = LoadStemLexWord ('../../Lex/subjectivity_clues_hltemnlp05/SubjPositive.txt',
                                  '../../Lex/subjectivity_clues_hltemnlp05/SubjNegative.txt')
    StemmedLexicons = [HuLiu, Nrc, Subj]
    return StemmedLexicons

def GetLexTriplet (Tokens, PosLex, NegLex):
    PosScore = []
    NegScore = []
    for T in Tokens:
        if T in PosLex:
            PosScore.append(T)
            continue
        if T in NegLex:
            NegScore.append(T)
    # print Tokens
    # print PosScore
    # print NegScore
    NumPos = len (PosScore)
    NumNeg = len(NegScore)
    SumPosNeg = NumPos - NumNeg
    Triplet = (NumPos, NumNeg, SumPosNeg)
    # print Triplet
    # raw_input()
    return Triplet

def GetLexFeats(Sent, StemmedLexicons):
    # print Sent
    try:
        HLPos, HLNeg = StemmedLexicons[0]
        NrcPos, NrcNeg = StemmedLexicons[1]
        SubjPos, SubjNeg = StemmedLexicons[2]
        Tokens = tokenize(Sent.lower())
        HLScores = GetLexTriplet (Tokens, PosLex = HLPos, NegLex = HLNeg)
        NrcScores = GetLexTriplet (Tokens, PosLex = NrcPos, NegLex = NrcNeg)
        SubjScores = GetLexTriplet (Tokens, PosLex = SubjPos, NegLex = SubjNeg)
        AllLexFeats = [HLScores, NrcScores, SubjScores]
        AllLexFeats = [item for sublist in AllLexFeats for item in sublist]
        return AllLexFeats
    except:
        return [0,0,0,0,0,0,0,0,0]

def Main ():
    print 'no test code added here'

if __name__ == '__main__':
    Main()
