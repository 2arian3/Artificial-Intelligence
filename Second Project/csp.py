from essentials import * 
from copy import deepcopy
from abc import abstractmethod

class CSP:
    
    def __init__(self, variables, domains):
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

    def forwardChecking(self, variable, domains, assignment):
        tempDomains = deepcopy(domains)
        for constraint in self.constraints[variable]:
            for defectiveVariable in constraint.variables:
                if defectiveVariable != variable and defectiveVariable not in assignment:
                    temp = []
                    tempAssignment = deepcopy(assignment)
                    for value in tempDomains[defectiveVariable]:
                        tempAssignment[defectiveVariable] = value
                        if constraint.satisfied(tempAssignment): temp.append(value)
                    if len(temp) == 0:
                        return False
                    tempDomains[defectiveVariable] = temp
        return tempDomains

    def backtrack(self, domains, assignment):
        if len(assignment) == len(self.variables):
            return assignment
        unassigned = [variable for variable in self.variables if variable not in assignment]
        variable = unassigned[0]

        for value in domains[variable]:
            tempAssignment = deepcopy(assignment)
            tempAssignment[variable] = value

            if self.consistent(variable, tempAssignment):
                tempDomains = self.forwardChecking(variable, domains, tempAssignment)
                if tempDomains == False: return False
                print(tempDomains)
                result = self.backtrack(tempDomains, tempAssignment)
                if result != False:
                    return result
        return False

class Constraint:

    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment):
        pass

class DifferentColorConstraint(Constraint):

    def __init__(self, cell1, cell2):
        super().__init__([cell1, cell2])
        self.cell1 = cell1
        self.cell2 = cell2
    
    def satisfied(self, colorAssignment):
        if self.cell1 not in colorAssignment or self.cell2 not in colorAssignment:
            return True
        return colorAssignment[self.cell1] != colorAssignment[self.cell2]

class DifferentNumberConstraint(Constraint):

    def __init__(self, cells):
        super().__init__(cells)
    
    def satisfied(self, numberAssignment):
        assignments = [numberAssignment[variable] for variable in self.variables if variable in numberAssignment]
        return len(assignments) == len(set(assignments))
        
def main():
    inputs = readInputs('input.txt')
    n = inputs['n']
    colors = inputs['colors']
    board = inputs['board']

    numberAssignments = {}
    colorAssignments = {}
    '''Calculating initial assignments'''
    for position, cell in board.items():
        if cell.number != '*': numberAssignments[position] = cell.number
        if cell.color != '#': colorAssignments[position] = cell.color
    variables = [(i, j) for i in range(n) for j in range(n)]
    numberDomains = {}
    for variable in variables: 
        numberDomains[variable] = [number for number in range(1, n+1) if variable not in numberAssignments]
    colorDomains = {}
    for variable in variables: 
        colorDomains[variable] = [color for color in colors if variable not in colorAssignments]
    
    numberCSP = CSP(deepcopy(variables), numberDomains)
    colorCSP = CSP(deepcopy(variables), colorDomains)

    for i in range(n):
        columnCells = []
        lineCells = []
        for j in range(n):
            columnCells.append((j, i))
            lineCells.append((i, j))
        numberCSP.addConstraint(DifferentNumberConstraint(columnCells))
        numberCSP.addConstraint(DifferentNumberConstraint(lineCells))

    legalMoves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            currentCell = (i, j)
            neighbours = [(i+x, j+y) for x, y in legalMoves if 0 <= i+x < n and 0 <= j+y < n]
            for neighbour in neighbours: colorCSP.addConstraint(DifferentColorConstraint(currentCell, neighbour))

if __name__ == '__main__':
    main()