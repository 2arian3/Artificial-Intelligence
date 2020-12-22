import re
from copy import deepcopy
from enum import Enum
from typing import *

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

    def __init__(self, cards: List[Card] = []):
        self.cards = deepcopy(cards)

    def __repr__(self):
        return str(self.cards)

    def __str__(self):
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

    def __init__(self, columns: List[Column] = []):
        self.columns = deepcopy(columns)

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

    def __init__(self, state: State=None, actions=[], depth=0):
        self.state = state
        #stores the actions that has been done from the root to current node
        self.actions = deepcopy(actions)
        self.depth = depth

    def __eq__(self, node):
        return type(node) == type(self) and self.state == node.state

    def __hash__(self):
        return hash(self.state.columns.__str__())

    def heuristic(self):
        h = 0
        for column in self.state.columns:
            if column.cards:
                temp = column.cards[0].number
                for card in column.cards[1:]:
                    #counts the cards that should be moved
                    if card.color != column.cards[0].color or card.number >= temp:
                        h += len(column.cards) - column.cards.index(card)
                        break
                    temp = card.number          
        return h
    
def child(action, childState, currentActions, childDepth):
    fromColumn, toColumn = action
    card = childState.columns[fromColumn].removeCardFromTop()
    childState.columns[toColumn].putCardOnTop(card) 
    childNode = Node(childState, currentActions, childDepth)
    childNode.actions.append((str(card), fromColumn, toColumn))
    return childNode

def readInputs(fileName=None):
    initialState, read, inputFile = State(), input, None
    if fileName: 
        inputFile = open(fileName, 'r')
        read = inputFile.readline
    #Reading inputs possible from both terminal or text file

    numberOfColumns, colors, numbers = map(int, read().split(' '))
    initialState.columns = [Column() for _ in range(numberOfColumns)]
    for i in range(numberOfColumns):
        line = read().rstrip()
        if line != '#':
            for card in line.split(' '):
                number, color = map(str, re.split('(\d+)', card)[1:])
                initialState.columns[i].putCardOnTop(Card(int(number), color))
    
    if inputFile: inputFile.close()
    return {
        "Columns": numberOfColumns,
        "Colors": colors,
        "Numbers": numbers,
        "Initial state": initialState
    }

def showResults(goalNode: Node, initialState: State, totalCreatedNodes, totalExploredNodes):
    print('***RESULTS***')
    print('Total created nodes: ', totalCreatedNodes)
    print('Total explored nodes: ', totalExploredNodes)
    print('Goal state depth: ', goalNode.depth, '\n')
    print('***STATES***')
    print('Initial state: ', initialState.columns)
    print('Final state: ', goalNode.state.columns, '\n')
    print('***Actions***')
    for card, fromColumn, toColumn in goalNode.actions:
        print('Moved card {} from columns {} to column {}'.format(card, fromColumn+1, toColumn+1))
        initialState.columns[toColumn].putCardOnTop(initialState.columns[fromColumn].removeCardFromTop())
        print(initialState.columns, '\n')