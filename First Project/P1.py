import re

class Card:

    def __init__(self, number, color):
        self.number = number
        self.color = color

    def __repr__(self):
        return 'Number : ' + str(self.number) + '\n' + 'Color : ' + self.color

    def compare(self, card):
        if self.color == card.color:
            if self.number > card.number:
                return 1
            return 0
        return -1

class Column :

    def __init__(self):
        self.state = []

    def __repr__(self):
        return str(self.state)

    def putCardOnTop(self, card):
        self.state.append(card)
    
    def removeCardFromTop(self):
        return self.state.pop()

    def checkValidation(self):
        return all([self.state[i].compare(self.state[i+1]) == 1 for i in range(len(self.state)-1)])
        
columns = []

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