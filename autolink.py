# This python program will allow me to automatically link together notes in my obsidian
# vault based on how close they are in topic.
from __future__ import print_function

import os
import re
import markdown
import nltk
import numpy as np
import pandas as pd
nltk.download('stopwords')
from gensim import corpora, models, similarities 
from nltk.corpus import stopwords
from gensim import corpora



path = "C:/Users/ebyd2/Documents/Obsidian Vault - Copy"

# taken from http://brandonrose.org/clustering#Latent-Dirichlet-Allocation
# words that don't impact the topic
stopwords = stopwords.words('english')

# breaks a word down to its root
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            # adjusted to remove some of the markdown uglyness that inevitably will be common
            if not re.search('/', token):
                if len(token) > 1:

                    filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            
            # adjusted to remove some of the markdown uglyness that inevitably will be common
            if not re.search('/', token):
                if len(token) > 1:

                    filtered_tokens.append(token)
    return filtered_tokens








#dir_list = os.listdir(path)
def run_fast_scandir(dir, ext):    # dir: str, ext: list
    subdir, dirpath, files, filepath = [], [], [], []

    for f in os.scandir(dir):
        if f.is_dir() and '.' != f.name[0] and f.name != "templates" and f.name != "attachments":
            subdir.append(f.name)
            dirpath.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                filepath.append(f.path)
                files.append(f.name)

    
    for dir in list(dirpath):
        sd, dp, f, fp = run_fast_scandir(dir, ext)
        subdir.extend(sd)
        dirpath.extend(dp)
        files.extend(f)
        filepath.extend(fp)
    return subdir, dirpath, files, filepath


# These two lists will hold the useful data for our topic modeling
# I am going to use two related lists instead of a dictionary to make it easier to use the 
# clean function
# The index of each list will match up.
# the filepath for each file
vaultPath = []
# the contents of each file
vaultContents = []

# scan the vault
subdir, dirpath, files, filepath = run_fast_scandir(path, [".md"])
# loop through all the files in filepath. This allows us to read
# the text from the files
for x in filepath:
    #indx = filepath.index(x)
    f = open(x, 'r')
    try:
        htmlmarkdown = markdown.markdown(f.read())
        vaultContents.append(htmlmarkdown)
        vaultPath.append(x)
    except:
        print("something went wrong")


# taken from http://brandonrose.org/clustering#Latent-Dirichlet-Allocation
tokenized_text = [tokenize_and_stem(text) for text in vaultContents]

texts = [[word for word in text if word not in stopwords] for text in tokenized_text]
#print(texts)

dictionary = corpora.Dictionary(texts)

#remove extremes
dictionary.filter_extremes(no_below=1, no_above=0.8)

#convert the dictionary to a bag of words corpus for reference
corpus = [dictionary.doc2bow(text) for text in texts]

# this could be parallelized
lda = models.LdaModel(corpus, num_topics=5, 
                            id2word=dictionary, 
                            update_every=5, 
                            chunksize=10000, 
                            passes=100)

print(lda.show_topics())


# # ----- Below currently does not work --------
# topics_matrix = lda.show_topics(formatted=False, num_words=20)
# topics_matrix = np.array(topics_matrix)

# topic_words = topics_matrix[:,:,1]
# for i in topic_words:
#     print([str(word) for word in i])
#     print()

