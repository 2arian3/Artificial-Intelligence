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
        return self.number == card.number and self.color == card.color

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
        return len(self.cards) == len(column.cards) and all([self.cards[i] == column.cards[i] for i in range(len(self.cards))])

    def checkAvailability(self, card):
        if self.cards: return self.cards[-1].compare(card) == cardComparisons.SameColorSmallerNumber or self.cards[-1].compare(card) == cardComparisons.DifferentColorSmallerNumber
        return True

    def putCardOnTop(self, card):
        self.cards.append(card)
    
    def removeCardFromTop(self):
        return self.cards.pop()

    def checkValidation(self):
        return all([self.cards[i].compare(self.cards[i+1]) == cardComparisons.SameColorSmallerNumber for i in range(len(self.cards)-1)])

class State:

    def __init__(self, columns=[]):
        self.columns = copy.deepcopy(columns)
    
    def __repr__(self):
        return self.columns

    def __eq__(self, state):
        return len(self.columns) == len(state.columns) and all([self.columns[i] == state.columns[i] for i in range(len(self.columns))])

    #checks whether the current state is a goal state or not
    def checkTermination(self):
        return all([column.checkValidation() for column in self.columns])
    
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

    def __init__(self, state=None, parent=None, actions=[]):
        self.state = state
        self.parent = parent
        self.childs = []
        #stores the actions that has been done from the root to current node
        self.actions = copy.deepcopy(actions)

    def __eq__(self, node):
        return self.state == node.state