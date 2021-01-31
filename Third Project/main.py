import re
from collections import defaultdict

poets = ['molavi', 'hafez', 'ferdowsi']
dictionary = defaultdict(lambda: defaultdict())
models = defaultdict(lambda: defaultdict(lambda: defaultdict()))
directories = {'molavi': 'AI_P3/train_set/molavi_train.txt',
               'hafez': 'AI_P3/train_set/hafez_train.txt',
               'ferdowsi': 'AI_P3/train_set/ferdowsi_train.txt',
               'test': 'AI_P3/test_set/test_file.txt'}
lambdas = [0.01, 0.9, 0.09]
epsilon = 0.1

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

def readTestFile():
    with open(directories['test'], 'r', encoding='UTF-8') as src:
        lines = src.readlines()

    return {line.split('\t')[1].rstrip(): line[0] for line in lines}

def backOff(words, poet):
    bigram = models[poet]['bigram'][words] if words in models[poet]['bigram'] else 0
    unigram = models[poet]['unigram'][words[0]] if words[0] in models[poet]['unigram'] else 0
    return lambdas[0] * bigram + lambdas[1] * unigram + lambdas[2] * epsilon

def randomLambdas():
    import random
    lambdas = [random.random() for _ in range(3)]
    return [l / sum(lambdas) for l in lambdas]

def test():
    testLines = readTestFile()
    poetMapping = {'1': 'ferdowsi',
                   '2': 'hafez',
                   '3': 'molavi'}

    correctPredicts = 0
    for line, truePoet in testLines.items():
        bigrams = []
        words = line.split()
        for i in range(len(words) - 2):
            bigrams.append((words[i], words[i+1]))

        maxProbability = -1
        predictedPoet = None
        for poet in poets:
            temp = 1
            for bigram in bigrams:
                temp *= backOff(bigram, poet)
            if temp > maxProbability:
                maxProbability = temp
                predictedPoet = poet

        print('Predicted {} for line {}. Correct poet is {}.'.format(predictedPoet, line, poetMapping[truePoet]))
        if predictedPoet == poetMapping[truePoet]:
            correctPredicts += 1

for poet in poets:
    dictionary[poet] = creatingDictionary(poet)
    models[poet]['unigram'], models[poet]['bigram'] = learn(poet)
test()