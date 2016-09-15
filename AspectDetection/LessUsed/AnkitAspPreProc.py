import os, sys
from pprint import pprint
import ast
from wordcloud import WordCloud
import matplotlib.pyplot as plt

print os.getcwd()
Lines = [l.strip().replace('[','').replace(']','').split(',') for l in open ('Random3KEmailApsetcsFromAnkit.txt')]

Asps = []
for Line in Lines:
    for Asp in Line:
        if not Asp: continue
        if '@' in Asp: continue
        if '_' in Asp: continue
        Asps.append(Asp.strip())
AspsStr = ' '.join (Asps)
text = AspsStr.replace(' month ','').replace(' mmbtu ','').replace('mmbtu','').replace(' cc ','').replace(' charset ','')\
.replace(' forwarded ','').replace(' rrb ','').replace('SORRY','').replace(' pm ','').replace(' folder ','').replace(' bc ','')\
.replace(' time ','').replace(' mesagedate ','').replace(' Aspects ','').replace(' re ','').replace(' mesage ','').replace(' message ','')\
.replace(' pst ','').replace(' pdt ','').replace(' content ','').replace(' text ','').replace(' filename ','').replace(' filenamensf ','')\
.replace(' date ','').replace(' year ','').replace(' week ','').replace(' LONG ','').replace(' SENTENCE ','').\
replace(' folderitems ','').replace(' email ','').replace(' . ','').replace(' january ','').replace(' mime ','')\
.replace(' friday ','').replace(' subject ','').replace(' april ','').replace(' july ','').replace(' dec ','').replace(' february ','')

wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
plt.figure(dpi=600)
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
# OpFName = FName.replace('.txt','_WC.png')
# OpFName = FName.replace('.txt','_WC.png')
# plt.savefig(OpFName, dpi=600,)

