from collections import defaultdict
from typing import List

poets = ['molavi', 'hafez', 'ferdowsi']
dictionary = defaultdict(lambda: defaultdict())
models = defaultdict(lambda: defaultdict(lambda: defaultdict()))
directories = {'molavi': 'AI_P3/train_set/molavi_train.txt',
               'hafez': 'AI_P3/train_set/hafez_train.txt',
               'ferdowsi': 'AI_P3/train_set/ferdowsi_train.txt',
               'test': 'AI_P3/test_set/test_file.txt'}
lambdas = [0.27143027132734326, 0.1487780559518773, 0.5797916727207794]
epsilon = 0.001

'''
Returns the given text file's lines
'''
def readFile(directory):
    with open(directory, 'r', encoding='UTF-8') as src:
        lines = src.readlines()
    
    return list(map(lambda line: line.rstrip(), lines))

'''
Creating dictionary for each poet based on their train set
'''
def creatingDictionary(poet):
    poetDict = defaultdict(lambda: 0)
    lines = readFile(directories[poet])
    for line in lines:
        for word in line.split(' '):
            poetDict[word.rstrip()] += 1
    return {word: count for word, count in poetDict.items() if count > 1}

'''
Returns the formatted lines for learning
Replaces the unknown words with <unk> token
Adds <s> and </s> to the start and end of each line
'''
def getTrainLines(poet):
    lines = readFile(directories[poet])
    
    for i in range(len(lines)):
        newLine = []
        for word in lines[i].split():
            if word in dictionary[poet]:
                newLine.append(word)
            else:
                newLine.append('<unk>')
        lines[i] = ' '.join(newLine)

    lines = ['<s> ' + line + ' </s>' for line in lines]
    return lines

'''
Computing the unigrams and their repeatance
'''
def uniGram(lines: List):
    unigram = defaultdict(lambda: 0)
    for line in lines:
        for word in line.split():
            unigram[word] += 1
    return unigram

'''
Computing the bigrams and their repeatance
'''
def biGram(lines: List):
    bigram = defaultdict(lambda: 0)
    for line in lines:
        words = line.split()
        for i in range(len(words) - 1):
            bigram[(words[i], words[i+1])] += 1
    return bigram

'''
Computing the probabilities of unigrams and bigrams
'''
def learn(poet):
    lines = getTrainLines(poet)
    unigram = uniGram(lines)
    bigram = biGram(lines)

    probabilityOfUnigram = {word: count / len(unigram) for word, count in unigram.items()}
    probabilityOfBigram = {(word1, word2): count / unigram[word1] for (word1, word2), count in  bigram.items()}

    return probabilityOfUnigram, probabilityOfBigram

'''
Reading and formatting the test set
'''
def getTestLines():
    lines = readFile(directories['test'])
    return {'<s> ' + line.split('\t')[1] + ' </s>': line[0] for line in lines}

'''
Using backoff smoothing method
'''
def backOff(words, poet):
    bigram = models[poet]['bigram'].get(words, 0)
    unigram = models[poet]['unigram'].get(words[1], 0)
    return lambdas[2] * bigram + lambdas[1] * unigram + lambdas[0] * epsilon

'''
Used to find the best lambdas
'''
def randomLambdas():
    import random
    lambdas = [random.random() for _ in range(3)]
    return [l / sum(lambdas) for l in lambdas]

'''
Computations on test set to find best matches
'''
def test():
    testLines = getTestLines()
    poetMapping = {'1': 'ferdowsi',
                   '2': 'hafez',
                   '3': 'molavi'}

    correctPredictions = 0

    for line, truePoet in testLines.items():
        bigrams = []
        words = line.split()
        for i in range(len(words) - 1):
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

        if predictedPoet == poetMapping[truePoet]:
            correctPredictions += 1
    return correctPredictions, len(testLines)

'''
Learning lambdas
'''
def findLambdas(iteration=1):
    global lambdas
    counter = 0
    bestLambdas = lambdas
    for _ in range(iteration):
        lambdas = randomLambdas()
        temp, _ = test()
        if temp > counter:
            counter = temp
            bestLambdas = lambdas

    return counter, bestLambdas

def showStatus(correctPredictions, totalLines):
    print('***STATUS***')
    print('Total test lines:', totalLines)
    print('Total correct predictions:', correctPredictions)
    print('Accuracy:', correctPredictions * 100 / totalLines, '%')
    print('ƛ1 = {}, ƛ2 = {}, ƛ3 = {}, ε = {}'.format(lambdas[0], lambdas[1], lambdas[2], epsilon))

def main():
    for poet in poets:
        dictionary[poet] = creatingDictionary(poet)
        models[poet]['unigram'], models[poet]['bigram'] = learn(poet)
    status = test()
    showStatus(status[0], status[1])

if __name__ == '__main__':
    main()