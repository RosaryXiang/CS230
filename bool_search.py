import json
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus.reader import indian
from nltk.util import filestring, invert_dict, pr
from nltk.stem.porter import PorterStemmer

stopwords_f = open(
    '/home/zhangjia/桌面/实验一/dataset/stop_words.txt', 'r')
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


f = open('/home/zhangjia/桌面/实验一/output/inverted_index.json')
content = f.read()
inverted_dicts = json.loads(content)

print(inverted_dicts.keys())
exit()


def search_one_word(word):
    return inverted_dicts.get(word,[])


def andd(a, b):
    ans = []
    i = 0
    j = 0
    while(i < len(a) and j < len(b)):
        if(a[i] == b[j]):
            ans.append(a[i])
            i = i+1
            j = j+1
        elif(a[i] > b[j]):
            j = j+1
        else:
            i = i+1
    return ans


def orr(a, b):
    ans = []
    i = 0
    j = 0
    while(i < len(a) and j < len(b)):
        if(a[i] < b[j]):
            ans.append(a[i])
            i = i+1
        elif (a[i] > b[j]):
            ans.append(b[j])
            j = j+1
        else:
            ans.append(a[i])
            i = i+1
            j = j+1
    while(i < len(a)):
        ans.append(a[i])
        i = i+1
    while(j < len(b)):
        ans.append(b[j])
        j = j+1
    return ans

choice = input('google: expression or one word, input 0 for expr, 1 for one word')

F = open('/home/zhangjia/桌面/实验一/output/num_to_path.json')
content = F.read()
table = json.loads(content)


if choice=='0':
    search = input("Google：")
    content = search.strip()
    words = word_tokenize(content)
    stems = []
    for w in words:
        stem = PorterStemmer().stem(w)
        stems.append(stem)

    stack = []
    for i in stems:
        stack.append(i)
        if i == ')':
            stack.pop()
            a = stack.pop()
            op = stack.pop()
            b = stack.pop()
            stack.pop()
            if(type(a)!=type([])):
                a = search_one_word(a)
            if type(b)!=type([]):
                b = search_one_word(b)
            if op == 'and':
                stack.append(andd(a, b))
            elif op == 'or':
                stack.append(orr(a, b))
            else:
                print(
                    "I can't understand. please input like this: ( ( aaa AND bbb ) or ccc )")

    
    output = []
    for num in stack[0]:
        name = table[str(num)]
        output.append(name)
    print(output)

elif choice=='1':
    search = input("Google：")
    content = search.strip()
    words = word_tokenize(content)
    stems = []
    for w in words:
        stem = PorterStemmer().stem(w)
        stems.append(stem)
    ans=search_one_word(words[0])
    ans2=[num_to_path(xx) for xx in ans]
    print(ans2)

else:
    print('ERROR')