import re

class Card:

    def __init__(self, number, color):
        self.number = number
        self.color = color

    def __repr__(self):
        return 'Number : ' + str(self.number) + '\n' + 'Color : ' + self.color

class Column :

    def __init__(self):
        self.state = []

    def __repr__(self):
        return str(self.state)

    def putCardOnTop(self, card):
        self.state.append(card)
    
    def removeCardFromTop(self):
        return self.state.pop()

columns = []
with open('input.txt', 'r') as src:
    numberOfColumns, colors, numbers = map(int, src.readline().split(' '))
    for _ in range(numberOfColumns): 
        columns.append(Column())
        line = src.readline().rstrip()
        if line != '#':
            for card in line.split(' '):
                number, color = map(str, re.split('(\d+)', card)[1:])
                columns[-1].putCardOnTop(Card(int(number), color))

print(columns[0])