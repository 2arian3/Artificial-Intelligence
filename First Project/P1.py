import re
from enum import Enum

columns = []
cardComparisons = Enum('Comparison', [
    'SameColorBiggerNumber',
    'SameColorSmallerNumber',
    'DifferentColorBiggerNumber',
    'DifferentColorSmallerNumber'
])

class Card:

    def __init__(self, number, color):
        self.number = number
        self.color = color

    def __repr__(self):
        return 'Number : ' + str(self.number) + '\n' + 'Color : ' + self.color

    def compare(self, card):
        if self.color == card.color:
            if self.number > card.number:
                return cardComparisons.SameColorBiggerNumber
            return cardComparisons.SameColorSmallerNumber
        else:
            if self.number > card.number:
                return cardComparisons.DifferentColorBiggerNumber
            else:
                return cardComparisons.DifferentColorSmallerNumber

class Column :

    def __init__(self):
        self.state = []

    def __repr__(self):
        return str(self.state)

    def checkAvailability(self, card):
        if self.state:
            return self.state[-1].compare(card) == cardComparisons.SameColorBiggerNumber or self.state[-1].compare(card) == cardComparisons.DifferentColorBiggerNumber
        return True

    def putCardOnTop(self, card):
        self.state.append(card)
    
    def removeCardFromTop(self):
        return self.state.pop()

    def checkValidation(self):
        return all([self.state[i].compare(self.state[i+1]) == cardComparisons.SameColorBiggerNumber for i in range(len(self.state)-1)])

def checkTermination():
    return all([column.checkValidation() for column in columns])

columns.append(Column())
columns[-1].putCardOnTop(Card(5, 'g'))
columns[-1].putCardOnTop(Card(2, 'g'))
columns[-1].putCardOnTop(Card(1, 'g'))
columns[-1].putCardOnTop(Card(-1, 'g'))
print(columns[-1].checkValidation())

#Reading inputs from input.txt
with open('input.txt', 'r') as src:
    numberOfColumns, colors, numbers = map(int, src.readline().split(' '))
    columns = [Column() for _ in range(numberOfColumns)]
    lines = [src.readline().rstrip() for _ in range(numberOfColumns)]
    for i in range(numberOfColumns):
        if lines[i] is not '#':
            for card in lines[i].split(' '):
                number, color = map(str, re.split('(\d+)', card)[1:])
                columns[i].putCardOnTop(Card(int(number), color))
for i in range(numberOfColumns):
    for j in range(numberOfColumns):
        if i != j:
            print(columns[j].checkAvailability(columns[i].state[-1]), end=' ')
    print()