import json
import math
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import scipy.sparse
import bisect

print('Loading')

inverted_index = open('./output/inverted_index.json')
inverted_index = inverted_index.read()
inverted_index = json.loads(inverted_index)

tf_idf_table = scipy.sparse.load_npz('./output/matrix.npy.npz')
tf_idf_table = tf_idf_table.tocsr()

f = open('./output/inverted_index_count.json')
content = f.read()
inverted_index_count = json.loads(content)
len_words = len(inverted_index_count)

g = open('./output/len_doc.txt')
len_doc = int(g.read())

word_to_num = {}

def tf_idf_q(stems):
    table = {}
    res = [0 for i in range(len_words)]
    tf = [0 for i in range(len_words)]
    df = [0 for i in range(len_words)]
    for word in stems:
        if word_to_num.get(word)!=None:
            if table.get(word)!=None:
                table[word] = table[word]+1
            else:
                table[word] = 1
    if(len(table.keys()) == 0):
        return [-1 for i in range(len_words)]
    for word in table.keys():
        tf[word_to_num[word]] = table[word]
        df[word_to_num[word]] = inverted_index_count[word]
    i = 0
    while i < len(res):
        if (df[i] == 0):
            res[i] = 0
        else:
            res[i] = (1+math.log10(tf[i]))*(math.log10(len_doc/df[i]))
        i = i+1
    return res


keywords = input('Please type in keywords:')
content = keywords.strip()
words = word_tokenize(content)
stems = []
for w in words:
    stem = PorterStemmer().stem(w)
    stems.append(stem)

value = tf_idf_q(stems)


def cos(doc_id, value):
    if value[0] == -1:
        return 0
    ans = 0
    for w in stems:
        if word_to_num.get(w)!=None:
            ans = ans+value[word_to_num[w]]*tf_idf_table[doc_id,word_to_num[w]]
    fenmu = 0
    fenmu1 = 0
    fenmu2 = 0
    for w in stems:
        if word_to_num.get(w)!=None:
            fenmu1 = fenmu1+value[word_to_num[w]]*value[word_to_num[w]]
    fenmu1 = math.sqrt(fenmu1)
    for w in stems:
        if word_to_num.get(w)!=None:
            fenmu2 = fenmu2+tf_idf_table[doc_id,word_to_num[w]]*tf_idf_table[doc_id,word_to_num[w]]
    fenmu2 = math.sqrt(fenmu2)
    fenmu = fenmu1*fenmu2
    return ans/(fenmu)


ans = []

doc_ids={}

# print(stems)

for x in stems:
    if inverted_index.get(x)!=None:
        ids=inverted_index[x]
        for id in ids:
            if doc_ids.get(id)==None:
                doc_ids[id]=1
print(doc_ids)

for id in doc_ids.keys():
    bisect.insort(ans,(cos(id,value),id))   

print(ans)
for i in range(10):
    if(ans[-i-1][0] != 0):
        print(str(ans[-1-i][1]))
