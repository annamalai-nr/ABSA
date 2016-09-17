from os import path
from wordcloud import WordCloud

d = path.dirname(__file__)

# Read the whole text.
FName = 'AllAspects.txt'
text = open(path.join(d, FName)).read()
text = text.replace(' jef ','').replace(' skiling ','').replace(' javamail ','').replace(' cc ','').replace(' charset ','')\
.replace(' sheri ','').replace(' sera ','').replace('SORRY','').replace(' jskilin ','').replace(' folder ','').replace(' bc ','')\
.replace(' time ','').replace(' mesagedate ','').replace(' Aspects ','').replace(' re ','').replace(' mesage ','').replace(' message ','')\
.replace(' pst ','').replace(' pdt ','').replace(' content ','').replace(' text ','').replace(' filename ','').replace(' filenamensf ','')\
.replace(' date ','').replace(' year ','').replace(' week ','').replace(' LONG ','').replace(' SENTENCE ','').\
replace(' folderitems ','').replace(' email ','').replace(' . ','').replace(' 40enron ','').replace(' mime ','')\
.replace(' imceanotes ','').replace(' folderinbox ','')

# Generate a word cloud image
wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.figure(dpi=600)
# plt.imshow(wordcloud)
plt.axis("off")

# take relative word frequencies into account, lower max_font_size
wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
plt.figure(dpi=600)
plt.imshow(wordcloud)
plt.axis("off")
# plt.show()
OpFName = FName.replace('.txt','_WC.png')
plt.savefig(OpFName, dpi=600,)