class Cell:

    def __init__(self, number='*', color='#'):
        self.number = number
        self.color = color

    def __repr__(self):
        return str(self.number) + self.color

    def __str__(self):
        return str(self.number) + self.color

    def changeNumber(self, number):
        self.number = number
    
    def changeColor(self, color):
        self.color = color

        
def readInputs(fileName=None):
    read, inputFile = input, None
    if fileName: 
        inputFile = open(fileName, 'r')
        read = inputFile.readline
    #Reading inputs possible from both terminal or text file

    possibleColors, possibleNumbers = map(int, read().split(' '))
    colors = list(read().rstrip().split(' '))
    board = dict()

    for i in range(possibleNumbers):
        cells = read().rstrip().split(' ')
        for j in range(possibleNumbers):
            number, color = cells[j][:-1], cells[j][-1]
            if number != '*': number = int(number)
            board[(i, j)] = Cell(number, color)

    if inputFile: inputFile.close()
    return {
        'n': possibleNumbers,
        'colors': colors,
        'board': board
    }

def showBoard(n, board):
    for i in range(n):
        for j in range(n):
            print(board[(i, j)], end=' ')
        print()