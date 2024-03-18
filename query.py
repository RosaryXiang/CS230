from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import math
import json
import sys

inverted_index = open('./output/inverted_index.json')
inverted_index = inverted_index.read()
inverted_index = json.loads(inverted_index)

f = open('./output/inverted_index_count.json')
content = f.read()
inverted_index_count = json.loads(content)
len_words = len(inverted_index_count)

f = open('./output/len_doc.txt')
line = f.readline()
len_doc = int(line)

cast2 = open('./output/word_to_num.json')
cast2_content = cast2.read()
word_to_num = json.loads(cast2_content)

def tf_idf_q(q):
    table = {}
    res = {}
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
    while i < len_words:
        if df[i]!=0:
            res[str(i)] = (1+math.log10(tf[i]))*(math.log10(len_doc/(df[i])))
        i = i+1
    return res


search = str(sys.argv[1])
content = search.replace('/',' ')
searching_words = word_tokenize(content)
query_stems = []
for w in searching_words:
    stem = PorterStemmer().stem(w)
    query_stems.append(stem)
#change input into a vector
query_info = tf_idf_q(query_stems)
ret = ""
for i in query_info:
    ret += str(i)
    ret +=","
    ret += str(query_info[i])
    ret += str('/')
print(ret)