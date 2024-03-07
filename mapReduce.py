from mrjob.job import MRJob
import json
import math
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import bisect

print('Loading...')

inverted_index = open('./output/inverted_index.json')
inverted_index = inverted_index.read()
inverted_index = json.loads(inverted_index)

#loading tf-idf-matrix
matrix = open("tf_idf.txt",'r')
lines = matrix.readlines()
# tf_idf_table = scipy.sparse.load_npz('./output/matrix.npy.npz')
# tf_idf_table = tf_idf_table.tocsr()

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
#change input into a vector
query_vector = tf_idf_q(query_stems)

doc_ids={}
for x in query_stems:
    if inverted_index.get(x)!=None:
        ids=inverted_index[x]
        for id in ids:
            if doc_ids.get(id)==None:
                doc_ids[id]=1
stem_id = []
for stem in query_stems:
    if stem in word_to_num.keys():
        stem_id.append(word_to_num[stem]) 

f = open("./output/doc_index_to_headline.json")
content = f.read()
doc_index_to_headline = json.loads(content)

def cos(query_vector, doc_info):
    if query_vector[0] == -1:
        return 0
    ans = 0
    fenmu1 = 0
    fenmu2 = 0
    for item in doc_info:
        col = int(item[0])
        value = float(item[1])
        fenmu2 = fenmu2+value*value
        if col in stem_id:
            ans = ans+query_vector[col]*value
    for col in stem_id:
        fenmu1 = fenmu1 + query_vector[col] * query_vector[col]
    fenmu1 = math.sqrt(fenmu1)
    fenmu2 = math.sqrt(fenmu2)
    fenmu = fenmu1*fenmu2
    return ans/(fenmu)

class MRWordFrequencyCount(MRJob):
    # def __init__(self):
    #     self.ans = []
    ans = []
    def mapper(self, _, lines):
        lines = lines.rstrip().split("\t")
        for line in lines:
            row, col, value = line.rstrip().split(",")
            yield row, (col, value) #key=row index(doc id), value=tuple(col,value)

    def reducer(self, key, values):
        # values is a generator
        doc_info = []
        for v in values:
            col = int(v[0])
            value = float(v[1])
            doc_info.append((col, value))
        res = cos(query_vector, doc_info)
        if res-0 >= 0.00001:
            bisect.insort(self.ans, (res,key)) 

    def output(self):
        return self.ans

mr = MRWordFrequencyCount()
mr.run()
ans = mr.output()
for i in range(10):
    if(ans[-i-1][0] != 0):
        print(str(i+1) + ". " + doc_index_to_headline[str(ans[-1-i][1])])
