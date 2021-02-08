from graphics import visualize
from csp import * 

'''
Reads the inputs from the given file or the terminal 
if no directory is given.
'''
def readInputs(fileName=None):
    read, inputFile = input, None
    if fileName: 
        inputFile = open(fileName, 'r')
        read = inputFile.readline
    '''Reading inputs possible from both terminal or text file'''

    _, possibleNumbers = map(int, read().split(' '))
    colors = list(read().rstrip().split(' '))
    assignments = {}

    for i in range(possibleNumbers):
        cells = read().rstrip().split(' ')
        for j in range(possibleNumbers):
            number, color = cells[j][:-1], cells[j][-1]
            assignments[(i, j)] = {}
            if number != '*': assignments[(i, j)]['number'] = int(number)
            if color != '#': assignments[(i, j)]['color'] = color

    if inputFile: inputFile.close()
    return {
        'n': possibleNumbers,
        'colors': colors,
        'assignments': assignments
    }

def showStatus(n, assignments):
    print('***STATUS***')
    if not assignments:
        print('ERROR\nThere is NO possible assignment based on the given table...')
        return
    
    for i in range(n):
        for j in range(n):
            print(str(assignments[(i, j)]['number']) + assignments[(i, j)]['color'], end=' ')
        print()

def main():
    #inputs = readInputs('input.txt') if we want to read from text file.
    inputs = readInputs()
    n = inputs['n']
    colors = inputs['colors']
    assignments = inputs['assignments']

    ColorConstraint.colors = dict(zip(colors, range(len(colors), 0, -1)))
    variables = {(i, j) for i in range(n) for j in range(n)}
    domains = defaultdict(lambda: defaultdict())
    for variable in variables: 
        domains[variable]['number'] = {number for number in range(1, n+1) if variable not in assignments or 'number' not in assignments[variable]}
        domains[variable]['color'] ={color for color in colors if variable not in assignments or 'color' not in assignments[variable]}
    
    csp = CSP(variables, domains)

    legalMoves = {(-1, 0), (1, 0), (0, -1), (0, 1)}
    covered = []
    for i in range(n):
        for j in range(n):
            currentCell = (i, j)
            neighbours = [(i+x, j+y) for x, y in legalMoves if 0 <= i+x < n and 0 <= j+y < n]
            for neighbour in neighbours:
                if {neighbour, currentCell} not in covered: 
                    csp.addConstraint(ColorConstraint(currentCell, neighbour))
                    covered.append({neighbour, currentCell})
    
    for i in range(n):
        columnCells, lineCells = set(), set()
        for j in range(n):
            columnCells.add((j, i))
            lineCells.add((i, j))
        csp.addConstraint(NumberConstraint(columnCells))
        csp.addConstraint(NumberConstraint(lineCells))

    assignments = csp.backtrack(domains, assignments)
    showStatus(n, assignments)
    visualize(n, colors, totalAssignments) 

if __name__ == '__main__':
    main()