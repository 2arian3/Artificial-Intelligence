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

    def __str__(self):
        return str(self.number) + self.color

    def __repr__(self):
        return str(self.number) + self.color

    def __eq__(self, card):
        return type(card) == type(self) and self.number == card.number and self.color == card.color

    def compare(self, card):
        if self.color == card.color:
            if self.number >= card.number:
                return cardComparisons.SameColorSmallerNumber
            return cardComparisons.SameColorBiggerNumber
        else:
            if self.number >= card.number:
                return cardComparisons.DifferentColorSmallerNumber
            return cardComparisons.DifferentColorBiggerNumber

class Column :

    def __init__(self, cards=[]):
        self.cards = copy.deepcopy(cards)

    def __repr__(self):
        return str(self.cards)
    
    def __eq__(self, column):
        return type(column) == type(self) and self.cards == column.cards

    def checkAvailability(self, card):
        return not self.cards or self.cards[-1].compare(card) == cardComparisons.SameColorSmallerNumber or self.cards[-1].compare(card) == cardComparisons.DifferentColorSmallerNumber

    def putCardOnTop(self, card):
        self.cards.append(card)
    
    def removeCardFromTop(self):
        return self.cards.pop()

    def checkValidation(self):
        return not any([self.cards[i].compare(self.cards[i+1]) != cardComparisons.SameColorSmallerNumber for i in range(len(self.cards)-1)])

class State:

    def __init__(self, columns=[]):
        self.columns = copy.deepcopy(columns)
    
    def __repr__(self):
        return self.columns

    def __eq__(self, state):
        return type(state) == type(self) and self.columns == state.columns

    #checks whether the current state is a goal state or not
    def checkTermination(self):
        return not any([column.checkValidation() == False for column in self.columns])
    
    def validActions(self):
        actions = []
        for i in range(len(self.columns)):
            fromColumn = self.columns[i]
            for j in range(len(self.columns)):
                toColumn = self.columns[j]
                #checks empty columns too => fromColumn.cards
                if i != j and fromColumn.cards and toColumn.checkAvailability(fromColumn.cards[-1]): actions.append((i, j))
        return actions

class Node:

    def __init__(self, state=None, parent=None, actions=[], depth=0):
        self.state = state
        self.parent = parent
        self.childs = []
        #stores the actions that has been done from the root to current node
        self.actions = copy.deepcopy(actions)
        self.depth = depth

    def __eq__(self, node):
        return type(node) == type(self) and self.state == node.state
    
    def __str__(self):
        pass

    def __repr__(self):
        pass

def readInputs(fileName):
    initialState = State()

    #Reading inputs from input.txt
    with open(fileName, 'r') as src:
        numberOfColumns, colors, numbers = map(int, src.readline().split(' '))
        initialState.columns = [Column() for _ in range(numberOfColumns)]
        for i in range(numberOfColumns):
            line = src.readline().rstrip()
            if line is not '#':
                for card in line.split(' '):
                    number, color = map(str, re.split('(\d+)', card)[1:])
                    initialState.columns[i].putCardOnTop(Card(int(number), color))
    return {
        "Columns": numberOfColumns,
        "Colors": colors,
        "Numbers": numbers,
        "Initial state": initialState
    }