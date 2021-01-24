from essentials import * 
from copy import deepcopy
from abc import abstractmethod

count = 0

class CSP:
    
    def __init__(self, colorOrNumber, variables, domains):
        self.colorOrNumber = colorOrNumber
        self.variables = variables
        self.domains = domains
        self.constraints = {}
        for variable in variables:
            self.constraints[variable] = []

    def addConstraint(self, constraint):
        for variable in constraint.variables:
            self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def minimumRemainingValue(self, domains, unassigned):
        result = unassigned[0]
        for variable in unassigned:
            if len(domains[variable]) < len(domains[result]):
                result = variable
        return result

    def degree(self, unassigned):
        ...

    def forwardChecking(self, variable, domains, assignments):
        tempDomains = deepcopy(domains)
        for constraint in self.constraints[variable]:
            for defectiveVariable in constraint.variables:
                if defectiveVariable != variable and defectiveVariable not in assignments[self.colorOrNumber]:
                    temp = []
                    tempAssignments = deepcopy(assignments)
                    for value in tempDomains[defectiveVariable]:
                        tempAssignments[self.colorOrNumber][defectiveVariable] = value
                        if constraint.satisfied(tempAssignments): temp.append(value)
                    if len(temp) == 0:
                        return False
                    tempDomains[defectiveVariable] = temp
        return tempDomains

    def backtrack(self, domains, assignments):
        if len(assignments[self.colorOrNumber]) == len(self.variables):
            return assignments
        unassigned = [variable for variable in self.variables if variable not in assignments[self.colorOrNumber]]
        # variable = unassigned[0]
        global count
        count += 1
        variable = self.minimumRemainingValue(domains, unassigned)
        print(variable, domains)
        for value in domains[variable]:
            tempAssignments = deepcopy(assignments)
            tempAssignments[self.colorOrNumber][variable] = value

            if self.consistent(variable, tempAssignments):
                tempDomains = self.forwardChecking(variable, domains, tempAssignments)
                if tempDomains == False: return False
                result = self.backtrack(tempDomains, tempAssignments)
                if result != False:
                    return result
        return False

class Constraint:

    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignments):
        pass

class DifferentColorConstraint(Constraint):

    def __init__(self, cell1, cell2):
        super().__init__([cell1, cell2])
        self.cell1 = cell1
        self.cell2 = cell2
    
    def satisfied(self, assignments):
        if self.cell1 not in assignments['color'] or self.cell2 not in assignments['color']:
            return True
        return assignments['color'][self.cell1] != assignments['color'][self.cell2]

class DifferentNumberConstraint(Constraint):

    def __init__(self, cells):
        super().__init__(cells)
    
    def satisfied(self, assignments):
        numberAssignments = [assignments['number'][variable] for variable in self.variables if variable in assignments['number']]
        return len(numberAssignments) == len(set(numberAssignments))

class PriorityColorConstraint(Constraint):

    '''
    Storing color priorities in colors list
    '''
    colors = []
    def __init__(self, cell1, cell2):
        super().__init__([cell1, cell2])
        self.cell1 = cell1
        self.cell2 = cell2

    def satisfied(self, assignments):
        if self.cell1 not in assignments['color'] or self.cell2 not in assignments['color'] or self.cell1 not in assignments['number'] or self.cell2 not in assignments['number']:
            return True
        cell1Color = assignments['color'][self.cell1]
        cell2Color = assignments['color'][self.cell2]
        cell1Number = assignments['number'][self.cell1]
        cell2Number = assignments['number'][self.cell2]
        return ((PriorityColorConstraint.colors.index(cell1Color) < PriorityColorConstraint.colors.index(cell2Color) and cell1Number > cell2Number)
                or (PriorityColorConstraint.colors.index(cell1Color) > PriorityColorConstraint.colors.index(cell2Color) and cell1Number < cell2Number))

def main():
    inputs = readInputs('input.txt')
    n = inputs['n']
    colors = inputs['colors']
    board = inputs['board']

    PriorityColorConstraint.colors = colors
    assignments = {}
    assignments['color'] = dict()
    assignments['number'] = dict()
    '''Calculating initial assignments'''
    for position, cell in board.items():
        if cell.number != '*': assignments['number'][position] = cell.number
        if cell.color != '#': assignments['color'][position] = cell.color
    variables = [(i, j) for i in range(n) for j in range(n)]
    colorDomains = dict()
    numberDomains = dict()
    for variable in variables: 
        numberDomains[variable] = [number for number in range(1, n+1) if variable not in assignments['number']]
    for variable in variables: 
        colorDomains[variable] = [color for color in colors if variable not in assignments['color']]
    
    colorCSP = CSP('color', variables, colorDomains)
    numberCSP = CSP('number', variables, numberDomains)

    legalMoves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            currentCell = (i, j)
            neighbours = [(i+x, j+y) for x, y in legalMoves if 0 <= i+x < n and 0 <= j+y < n]
            for neighbour in neighbours: 
                colorCSP.addConstraint(DifferentColorConstraint(currentCell, neighbour))
                colorCSP.addConstraint(PriorityColorConstraint(currentCell, neighbour))
                numberCSP.addConstraint(PriorityColorConstraint(currentCell, neighbour))
    
    for i in range(n):
        columnCells = []
        lineCells = []
        for j in range(n):
            columnCells.append((j, i))
            lineCells.append((i, j))
        numberCSP.addConstraint(DifferentNumberConstraint(columnCells))
        numberCSP.addConstraint(DifferentNumberConstraint(lineCells))

    assignments = numberCSP.backtrack(numberDomains, assignments)
    assignments = colorCSP.backtrack(colorDomains, assignments)
    print(assignments, count)

if __name__ == '__main__':
    main()