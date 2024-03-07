import json
import math
from re import L
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus.reader import indian
from nltk.util import filestring, invert_dict, pr
from nltk.stem.porter import PorterStemmer
import scipy.sparse
import numpy as np
import bisect

print('Loading...')

inverted_index = open('./output/inverted_index.json')
inverted_index = inverted_index.read()
inverted_index = json.loads(inverted_index)

tf_idf_table = scipy.sparse.load_npz('./output/matrix.npy.npz')
tf_idf_table = tf_idf_table.tocsr()

f = open('./output/inverted_index_count.json')
content = f.read()
inverted_index_count = json.loads(content)

f = open('./output/len_doc.txt')
line = f.readline()
len_doc = int(line)
len_words = len(inverted_index_count)

cast2 = open('./output/word_to_num.json')
cast2_content = cast2.read()
word_to_num = json.loads(cast2_content)

def tf_idf_q(q):
    table = {}
    res = [0 for i in range(len_words)]
    tf = [0 for i in range(len_words)]
    df = [0 for i in range(len_words)]
    for word in q:
        if word_to_num.get(word)!=None:
            if table.get(word)!=None:
                table[word] = table[word]+1
            else:
                table[word] = 1
    if(len(table.keys()) == 0):
        return [-1 for i in range(len_words)]
    for word in table.keys():
        tf[word_to_num[word]] = table[word]
        df[word_to_num[word]] = len(inverted_index_count[word])
    i = 0
    while i < len(res):
        if (df[i] == 0):
            res[i] = 0
        else:
            res[i] = (1+math.log10(tf[i]))*(math.log10(len_doc/(df[i])))
        i = i+1
    return res


search = input('Please type in keywords:')
content = search.strip()
searching_words = word_tokenize(content)
query_stems = []
for w in searching_words:
    stem = PorterStemmer().stem(w)
    query_stems.append(stem)

query_vector = tf_idf_q(query_stems)


def cos(doc_id, query_vector):
    if query_vector[0] == -1:
        return 0
    ans = 0
    for xxx in query_stems:
        if word_to_num.get(xxx)!=None:
            ans = ans+query_vector[word_to_num[xxx]]*tf_idf_table[doc_id,word_to_num[xxx]]
    fenmu1 = 0
    fenmu2 = 0
    for xxx in query_stems:
        if word_to_num.get(xxx)!=None:
            fenmu1 = fenmu1+query_vector[word_to_num[xxx]]*query_vector[word_to_num[xxx]]
    fenmu1 = math.sqrt(fenmu1)
    for i in range(len_words):
        fenmu2 = fenmu2+tf_idf_table[doc_id,i]*tf_idf_table[doc_id,i]
    fenmu2 = math.sqrt(fenmu2)
    fenmu = fenmu1*fenmu2
    return ans/(fenmu)


ans = []
doc_ids={}

for x in query_stems:
    if inverted_index.get(x)!=None:
        ids=inverted_index[x]
        for id in ids:
            if doc_ids.get(id)==None:
                doc_ids[id]=1

for id in doc_ids.keys():
    bisect.insort(ans,(cos(id,query_vector),id))   

f = open("./output/doc_index_to_headline.json")
content = f.read()
doc_index_to_headline = json.loads(content)

print("respond: ")
for i in range(10):
    if(ans[-i-1][0] != 0):
        print(str(i+1) + ". " + doc_index_to_headline[str(ans[-1-i][1])])
