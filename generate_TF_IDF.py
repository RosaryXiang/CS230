import json
import math
import numpy as np
import scipy.sparse
from scipy.sparse import coo_matrix
from scipy.sparse import lil_matrix

from scipy.sparse import coo

inverted_index_count = open('./output/inverted_index_count.json')
inverted_index_count = inverted_index_count.read()
inverted_index_count = json.loads(inverted_index_count)

len_doc = open('./output/len_doc.txt')
len_doc = int(len_doc.read())
# print(len_doc)

len_word=len(inverted_index_count)

matrix =  lil_matrix((len_doc,len_word),dtype=np.float64)
print("matrix initialization completed")

def tf_idf(t, d): #t for term, d for document
    tf = inverted_index_count[t][d]
    df = len(inverted_index_count[t])
    return (1+math.log10(tf))*(math.log(len_doc/df))

word_to_num = {}
word_index=-1
for word in inverted_index_count.keys():
    word_index = word_index+1
    word_to_num[word] = word_index
    for doc in inverted_index_count[word]:
        matrix[int(doc),word_index] = np.float64(tf_idf(word, doc))

print("matrix's data filled")

mm = coo_matrix(matrix)

print("changed to coo matrix")

f_w_t_n = open('./output/word_to_num.json', 'w')
dic = json.dumps(word_to_num)
f_w_t_n.write(dic)
f_w_t_n.close()

scipy.sparse.save_npz('./output/matrix.npy',mm,True)

print("coo matrix saved")
print("Completed!")