import numpy as np
import random
'''
def make_pairs(words):
    for i in range(len(words) - 1):
        yield (words[i], words[i + 1])
print("1")
sentences = open('speeches.txt', encoding='utf8').read()
print("2")
words = sentences.split()
print("3")
pairs = make_pairs(words)

word_dict = {}
for word_1, word_2 in pairs:
    if word_1 in word_dict.keys():
        word_dict[word_1].append(word_2)
    else:
        word_dict[word_1] = [word_2]

#Randomly pick the first word
first_word = np.random.choice(words)

chain = [first_word]

#Initialize the number of stimulated words
n_words = 100

for i in range(n_words):
    chain.append(np.random.choice(word_dict[chain[-1]]))

print(' '.join(chain))
'''
'''
a = np.array([[0.2,0.6,0.2], [0.3,0,0.7], [0.5,0,0.5,]])
b = np.array([0, 1.0, 0])
while True:
    c = np.matmul(b,a)
    if str(c) == str(b):
        break
    else:
        b = c
    print(b)
a = np.array([[0.9,0.1],[0.2,0.8]])
print(np.matmul(a,a))
'''
def make_pairs(words):
    for i in range(len(words) - 1):
        yield (words[i], words[i + 1])
lisT = []
for a in range(0,100):
    lisT.append(random.randint(1,5))
print(lisT)
pairs = make_pairs(lisT)
word_dict = {}
for word_1, word_2 in pairs:
    if word_1 in word_dict.keys():
        word_dict[word_1].append(word_2)
    else:
        word_dict[word_1] = [word_2]
#print(word_dict)
a = []

for b in word_dict:
    temp = []
    temp2 = []
    temp.append([word_dict[b].count(1),word_dict[b].count(2),word_dict[b].count(3),word_dict[b].count(4),word_dict[b].count(5)])
    y = (sum(temp[0]))
    for x in temp[0]:
        temp2.append(x/y)
    a.append(temp2)
#print(a)
prob = np.array(a)
pi = np.array([1,0,0,0,0])
print(prob)
print("\n")
print(pi)
while True:
    c = np.matmul(pi,prob)
    if str(c) == str(pi):
        break
    else:
        pi = c
print("\n")
print(pi)
counter = 1
for a in pi:
    print(f"{counter} has the probability {round(a*100,2)}%")
    counter += 1
print(sum(pi))