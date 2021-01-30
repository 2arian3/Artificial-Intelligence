import re
from collections import defaultdict

poets = ['molavi', 'hafez', 'ferdowsi']
dictionary = defaultdict(lambda: defaultdict())
models = defaultdict(lambda: defaultdict(lambda: defaultdict()))
directories = {'molavi': 'AI_P3/train_set/molavi_train.txt',
               'hafez': 'AI_P3/train_set/hafez_train.txt',
               'ferdowsi': 'AI_P3/train_set/ferdowsi_train.txt'}

def creatingDictionary(poet):
    poetDict = defaultdict(lambda: 0)
    with open(directories[poet], 'r', encoding='UTF-8') as src:
        line = src.readline().rstrip()
        while line:
            for word in line.split(' '):
                poetDict[word.rstrip()] += 1
            line = src.readline()
    return {word: count for word, count in poetDict.items() if count != 1}

def getTrainLines(poet):
    with open(directories[poet], 'r', encoding='UTF-8') as src:
        lines = src.readlines()
    
    lines = list(map(lambda line: line.rstrip(), lines))
    
    for i in range(len(lines)):
        for word in lines[i].split():
            if word not in dictionary[poet]:
                lines[i] = re.sub(word, '<unk>', lines[i])
    
    lines = ['<s> ' + line + ' </s>' for line in lines]
    return lines

def uniGram(lines):
    unigram = defaultdict(lambda: 0)
    for line in lines:
        for word in line.split():
            unigram[word] += 1
    return unigram

def biGram(lines):
    bigram = defaultdict(lambda: 0)
    for line in lines:
        words = line.split()
        for i in range(len(words) - 2):
            bigram[(words[i], words[i+1])] += 1
    return bigram

def learn(poet):
    lines = getTrainLines(poet)
    unigram = uniGram(lines)
    bigram = biGram(lines)

    probabilityOfUnigram = {word: count / len(unigram) for word, count in unigram.items()}
    probabilityOfBigram = {(word1, word2): count / unigram[word1] for (word1, word2), count in  bigram.items()}

    return probabilityOfUnigram, probabilityOfBigram

for poet in poets:
    dictionary[poet] = creatingDictionary(poet)
    models[poet]['unigram'], models[poet]['bigram'] = learn(poet)