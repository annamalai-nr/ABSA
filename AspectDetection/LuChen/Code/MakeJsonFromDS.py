import os,json
from pprint import pprint
from collections import OrderedDict

FName = '/home/annamalai/Desktop/ABSA/AspectDetection/LuChen/DataAndGT/reviews_GPS.txt'
Lines = [l.strip() for l in open (FName).xreadlines()]
D = OrderedDict()
for LineInd, L in enumerate(Lines):
    if L.startswith('id: '):
        #new rev starts
        id = int (L.strip('id: '))
        D[id] = OrderedDict()
        D[id]['product_id'] = Lines[LineInd+1].split(': ')[-1]
        D[id]['product_name'] = Lines[LineInd+2].split(': ')[-1]
        D[id]['review_score'] = Lines[LineInd+3].split(': ')[-1]
        D[id]['review_title'] = Lines[LineInd+4].split(': ')[-1]
        D[id]['review_text'] = Lines[LineInd+5].split(': ')[-1]
        D[id]['parsed_review'] = Lines[LineInd+6].split(': ')[-1][1:-1]

        pros_raw_annotation = Lines[LineInd+7].split(': ')
        if len (pros_raw_annotation) == 1:
            D[id]['pros_raw_annotation'] = ''
        else:
            D[id]['pros_raw_annotation'] = pros_raw_annotation[-1]

        pros_feature = Lines[LineInd+8].split(': ')
        if len (pros_feature) == 1:
            D[id]['pros_feature'] = ''
        else:
            D[id]['pros_feature'] = pros_feature[-1]

        pros_aspect = Lines[LineInd+9].split(': ')
        if len(pros_aspect) == 1:
            D[id]['pros_aspect'] = ''
        else:
            D[id]['pros_aspect'] = pros_aspect[-1]


        cons_raw_annotation = Lines[LineInd+10].split(': ')
        if len (cons_raw_annotation) == 1:
            D[id]['cons_raw_annotation'] = ''
        else:
            D[id]['cons_raw_annotation'] = cons_raw_annotation[-1]

        cons_feature = Lines[LineInd+11].split(': ')
        if len(cons_feature) == 1:
            D[id]['cons_feature'] = ''
        else:
            D[id]['cons_feature'] = cons_feature[-1]

        cons_aspect = Lines[LineInd+12].split(': ')
        if len(cons_aspect) == 1:
            D[id]['cons_aspect'] = ''
        else:
            D[id]['cons_aspect'] = cons_aspect[-1]
        # pprint (D[id])
        # raw_input()

OpFName = FName.replace('.txt','.json')
with open (OpFName,'w') as FH:
    json.dump (obj=D, fp=FH, indent=4)
print 'pls chk file: ', OpFName
