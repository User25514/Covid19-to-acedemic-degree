import numpy as np
'''
def make_pairs(words):
    for i in range(len(words) - 1):
        yield (words[i], words[i + 1])

sentences = open('speeches.txt', encoding='utf8').read()
words = sentences.split()

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