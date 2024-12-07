# This python program will allow me to automatically link together notes in my obsidian
# vault based on how close they are in topic.


import os
import re
import markdown
import string
import nltk
nltk.download('stopwords')
nltk.download('wordnet')  
nltk.download('omw-1.4')  
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora
from gensim.models import LsiModel
import codecs
from sklearn import feature_extraction
import mpld3



path = "C:/Users/ebyd2/Documents/Obsidian Vault - Copy"

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

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

# from https://www.datacamp.com/tutorial/what-is-topic-modeling

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = "".join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

# I am going to use two related lists instead of a dictionary to make it easier to use the 
# clean function

vaultPath = []
vaultContents = []
subdir, dirpath, files, filepath = run_fast_scandir(path, [".md"])
for x in filepath:
    indx = filepath.index(x)
    f = open(x, 'r')
    try:
        htmlmarkdown = markdown.markdown(f.read())
        #print(htmlmarkdown)
        vaultContents.append(htmlmarkdown)
        vaultPath.append(x)
        #print(filepath)
        #print(vaultPath[0])
        #print(vaultContents[0])
        #break
    except:
        print("something went wrong")






# ---------- Replacing --------------


clean_corpus = [clean(doc).split() for doc in vaultContents]

#print(clean_corpus)
dictionary = corpora.Dictionary(clean_corpus)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in clean_corpus]
#print(doc_term_matrix)

lsa = LsiModel(doc_term_matrix, num_topics=3, id2word= dictionary)

print(lsa.print_topics(num_topics=3, num_words=3))

from gensim.models import LdaModel

# LDA model
lda = LdaModel(doc_term_matrix, num_topics=3, id2word = dictionary)

# Results
