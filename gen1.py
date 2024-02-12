import json
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re

stopwords_f = open('./input/stop_words.txt', 'r')
stopwords = {}
for line in stopwords_f:
    line = line.strip()
    stopwords[line]=1
interpunctuations = [',', '.', ':', ';', '?','(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '|', '``']

for i in interpunctuations:
    stopwords[i] = 1
stopwords1={}
for w in stopwords:
    stopwords1[PorterStemmer().stem(w)]=1

dataset = './input/News_Category_Dataset_v3.json'
f = open(dataset)
content = f.read()
json_content = json.loads(content)

print(len(json_content))
len_doc = open('./output/len_doc.txt', 'w')
len_doc.write(str(len(json_content)))

inverted_index ={}  # words to a list of article indexes
inverted_index_count = {} # numbers of words in different articles 

for index in range(len(json_content)):
    article = json_content[index]
    words = word_tokenize(article["short_description"])
    for w in words:
        word = PorterStemmer().stem(w)
        if re.match(r'(^[a-z]+$)',word) and len(word)>2 and stopwords1.get(word)==None:
            # maintaining inverted_index
            if inverted_index.get(word)== None:
                inverted_index[word] =[index]
            elif index != inverted_index[word][-1]:
                inverted_index[word].append(index)
            # maintaining inverted_index_count
            if inverted_index_count.get(word)== None:
                inverted_index_count[word] = {index: 1}
            else:
                if inverted_index_count[word].get(index) != None:
                    inverted_index_count[word][index]=inverted_index_count[word][index]+1
                else:
                    inverted_index_count[word][index]=1

# print(inverted_index)
print("generation completed")

print(len(inverted_index_count))
len_doc = open('./output/len_word.txt', 'w')
len_doc.write(str(len(inverted_index_count)))

# path = '/home/zhangjia/桌面/实验一/dataset/US_Financial_News_Articles'
# folders = os.listdir(path)
# i = -1
# inverted_index = {}
# inverted_index1 = {}
# num_to_path={}
# for folder in folders:
#     path_now = path + "/"+folder
#     files = os.listdir(path_now)
#     for file in files:
#         i = i+1
#         if not os.path.isdir(file):
#             f = open(path_now+"/"+file)
#             num_to_path[i]=path_now+"/"+file
#             content = f.read()
#             jcon = json.loads(content)
#             words = word_tokenize(jcon['text'])
#             stems = []
#             for w in words:
#                 word = PorterStemmer().stem(w)
#                 if re.match(r'(^[a-z]+$)',word) and len(word)>2:
#                     if(stopwords1.get(word)==None):
#                         if inverted_index.get(word)!=None:
#                             if i != inverted_index[word][-1]:
#                                 inverted_index[word].append(i)
#                         else:
#                             inverted_index[word] = [i]
#                         if inverted_index1.get(word)!=None:
#                             if inverted_index1[word].get(i) != None:
#                                 inverted_index1[word][i]=inverted_index1[word][i]+1
#                             else:
#                                 inverted_index1[word][i]=1
#                         else:
#                             inverted_index1[word]={i:1}

out=open('./output/inverted_index_count.json', 'w')
dd = json.dumps(inverted_index_count)
out.write(dd)
out.close()

print("inverted_index_count output completed")

output = open('./output/inverted_index.json', 'w')
dic = json.dumps(inverted_index)
output.write(dic)
output.close()

print("inverted_index output completed")
print("Complete!")
