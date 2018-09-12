
# coding: utf-8

# ## Functions

# In[1]:


def preprocess(s, case = "L"):
    """
    Preprocesses text in a corpus for transformation

    """ 
    if case == "L":
        s = s.lower()
    elif case == "U":
        s = s.upper()
    return s


# ## Implementation

# In[2]:


import glob
#path = "/Users/jordanchisam/Desktop/ProgrammingTextAnalysis/corpora/plz/*.txt"
path = "/Users/jordanchisam/Desktop/ProgrammingTextAnalysis/corpora/shakespeare_plaintext/*.txt"
filepaths = glob.glob(path)

documents = []
punctuations = "-,.?!;: \n\t"

for fn in filepaths:
    s = open(fn, 'r').read()
    s = preprocess(s, "L")
    documents.append(s)

texts = [[word.strip(punctuations) for word in document.split()]for document in documents]
            
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
        
texts = [[token for token in text if frequency[token] > 1]for text in texts]

print len(texts)
print texts[:1]
            


# In[3]:


from gensim import corpora
import re, string, nltk
dictionary = corpora.Dictionary(texts) #built in func for txt vectorization to get unique words to build text dictionary
dictionary.save("/Users/jordanchisam/Desktop/ProgrammingTextAnalysis/corpora/practiceraw.dict")
print(dictionary.token2id)


# In[4]:


corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/Users/jordanchisam/Desktop/ProgrammingTextAnalysis/corpora/corpusraw.mm', corpus)  # store to disk, for later use
print corpus[:10]


# In[5]:


from gensim import models, similarities
import os

if (os.path.exists('/Users/jordanchisam/Desktop/ProgrammingTextAnalysis/corpora/practiceraw.dict')):
    dictionary = corpora.Dictionary.load('/Users/jordanchisam/Desktop/ProgrammingTextAnalysis/corpora/practiceraw.dict')
    corpus = corpora.MmCorpus("/Users/jordanchisam/Desktop/ProgrammingTextAnalysis/corpora/corpusraw.mm")
    print("Lets get to work")
else:
    print("Invalid data set provided")


# ## Model
# 
# Decided to continue with TF IDF model as opposed to measuring raw word count values or other frequency weigting methods because TF IDF works well for measuring the significance of words. Additionally, it properly shows the similarilty and differences in texts.

# In[6]:


tfidf = models.TfidfModel(corpus)


# In[7]:


from pprint import pprint

corpus_tfidf = tfidf[corpus] #converts counts to tfidf scores
for doc in corpus_tfidf:
    pprint(doc[:10])


# ## Begin LSI Transformation

# In[8]:


lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
corpus_lsi = lsi[corpus_tfidf]
lsi.save('model.lsi')
lsi = models.LsiModel.load('model.lsi')


#Similarity Searching
dictionary = corpora.Dictionary.load("/Users/jordanchisam/Desktop/ProgrammingTextAnalysis/corpora/practiceraw.dict")
corpus = corpora.MmCorpus("/Users/jordanchisam/Desktop/ProgrammingTextAnalysis/corpora/corpusraw.mm")
print(corpus)

#multi-dimensional space
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=10)
corpus_lsi = lsi[corpus]

print corpus_lsi[0]
print len(corpus_lsi[0])

#convert to new lsi space
user_text_choice = "Macbeth.txt"
fn = "/Users/jordanchisam/Desktop/ProgrammingTextAnalysis/corpora/shakespeare_plaintext/"+user_text_choice
doc = open(fn, 'r').read()

vec_bow = dictionary.doc2bow(doc.lower().split())

print
print vec_bow

vec_lsi = lsi[vec_bow] # convert the query to LSI space

print
print(vec_lsi)
print
print dir(vec_lsi)
print
print len(vec_lsi)


# In[9]:


#init query structure
index = similarities.MatrixSimilarity(lsi[corpus])
index.save('shakeLSI.index')
index = similarities.MatrixSimilarity.load('shakeLSI.index')
sims = index[vec_lsi] # perform a similarity query against the corpus
print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples
len(sims)


# In[10]:


print "Initial Comparative Text"
print
print user_text_choice.replace('.txt', ' ').title()
print 
print "---------------------------------------------------------"
print
labels = []
ll = []
sims = sorted(enumerate(sims), key=lambda item: -item[1])
for s in sims:
    #(os.path.split(fn)[1])[:-3]
    l = os.path.split(filepaths[s[0]])[1][:-3].replace('_', ' ').title(), s[1]
    ll.append((s[0], s[1], l[0].replace(".", " ")))
    labels.append(l)
    print l
print
print "Similarity Indexing Across Texts"
print
print(sims)


# In[11]:


get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt1

p1tf = [x[0] for x in sims]
p2tf = [x[1] for x in sims]

plt1.figure(figsize=(17,15))
print 
lll = sorted(ll, key=lambda x: x[0])
print lll
print
print "-----------------"
print
plt1.scatter(p1tf, p2tf, s=200, alpha=.5)
for l in lll:
    plt1.text(l[0], l[1], l[2])
    
plt1.xlabel("Texts represented by their index")
plt1.ylabel("Similarity Index")
plt1.title("Latent Semantic Index Similarity Compared Against --> " + user_text_choice.replace("-", " ").replace(".txt", " "))

