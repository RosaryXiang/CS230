import sys
import json
f = open(sys.argv[1],'r')
lines = f.readlines()
dic = {}
list = []
for line in lines:
    line = line.strip() 
    two = line.split("\t")
    value = two[0]
    index = two[1]
    index = index.lstrip('\"')
    index = index.rstrip('\"')
    value = float(value)
    dic[value] = index
    list.append(value)

list.sort()
g = open("./output/doc_index_to_headline.json", "r")
doc_id_to_headline = json.loads(g.read())

if len(list) >= 10:
    for i in range(10):
        print(str(i+1) +". " + doc_id_to_headline[dic[list[i]]])
else:
    cnt = 1
    for i in list:
        cnt += 1
        print(str(cnt) +". " + doc_id_to_headline[dic[i]])