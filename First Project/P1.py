import re
import copy
from enum import Enum

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

    def __eq__(self, card):
        return self.number == card.number and self.color == card.color

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
        self.cards = []

    def __repr__(self):
        return str(self.cards)
    
    def __eq__(self, column):
        return len(self.cards) == len(column.cards) and all([self.cards[i] == column.cards[i] for i in range(len(self.cards))])

    def checkAvailability(self, card):
        if self.cards:
            return self.cards[-1].compare(card) == cardComparisons.SameColorBiggerNumber or self.cards[-1].compare(card) == cardComparisons.DifferentColorBiggerNumber
        return True

    def putCardOnTop(self, card):
        self.cards.append(card)
    
    def removeCardFromTop(self):
        return self.cards.pop()

    def checkValidation(self):
        return all([self.cards[i].compare(self.cards[i+1]) == cardComparisons.SameColorBiggerNumber for i in range(len(self.cards)-1)])

class State:

    def __init__(self, columns=[]):
        self.columns = copy.deepcopy(columns)
    
    def __eq__(self, state):
        return len(self.columns) == len(state.columns) and all([self.columns[i] == state.columns[i] for i in range(len(self.columns))])
        
def checkTermination(state):
    return all([column.checkValidation() for column in state.columns])

def BreadthFirstSearch():
    if checkTermination(): return True

initialState = State()

def main():
    #Reading inputs from input.txt
    with open('input.txt', 'r') as src:
        numberOfColumns, colors, numbers = map(int, src.readline().split(' '))
        initialState.columns = [Column() for _ in range(numberOfColumns)]
        lines = [src.readline().rstrip() for _ in range(numberOfColumns)]
        for i in range(numberOfColumns):
            if lines[i] is not '#':
                for card in lines[i].split(' '):
                    number, color = map(str, re.split('(\d+)', card)[1:])
                    initialState.columns[i].putCardOnTop(Card(int(number), color))

if __name__ == '__main__':
    main()