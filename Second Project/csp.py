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

    def consistent(self, variable, assignments):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignments):
                return False
        return True

    def minimumRemainingValue(self, domains, unassigned):
        remainingValues = dict(zip(unassigned, list(map(lambda variable: len(domains[variable]), unassigned))))
        remainingValues = dict(sorted(remainingValues.items(), key= lambda item: item[1]))
        count = list(remainingValues.values()).count(list(remainingValues.values())[0])
        return count, list(remainingValues.keys())[0]


    def degree(self, unassigned):
        degrees = dict()
        for variable in unassigned:
            count = 0
            for constraint in self.constraints[variable]:
                count += 1 if any([defectiveVariable in unassigned for defectiveVariable in constraint.variables if defectiveVariable != variable]) else 0
            degrees[variable] = count
        degrees = dict(sorted(degrees.items(), key= lambda item: item[1]))
        count = list(degrees.values()).count(list(degrees.values())[-1])
        return count, list(degrees.keys())[-1]

    def selectVariable(self, domains, unassigned):
        ...

    def forwardChecking(self, toBeAssigned, variable, domains, assignments):
        tempDomains = deepcopy(domains)
        for constraint in self.constraints[variable]:
            for defectiveVariable in constraint.variables:
                if defectiveVariable != variable and toBeAssigned not in assignments[defectiveVariable]:
                    temp = []
                    tempAssignments = deepcopy(assignments)
                    for value in tempDomains[defectiveVariable][toBeAssigned]:
                        tempAssignments[defectiveVariable][toBeAssigned] = value
                        if constraint.satisfied(tempAssignments): temp.append(value)
                    if len(temp) == 0: return False
                    tempDomains[defectiveVariable][toBeAssigned] = temp
        return tempDomains

    def backtrack(self, domains, assignments):
        if all([len(assignment) == 2 for assignment in list(assignments.values())]):
            return assignments
        unassigned = [variable for variable in self.variables if 'color' not in assignments[variable] or 'number' not in assignments[variable]]
        variable = unassigned[0]
        toBeAssigned = 'number' if 'number' not in assignments[variable] else 'color'
        for value in domains[variable][toBeAssigned]:
            tempAssignments = deepcopy(assignments)
            tempAssignments[variable][toBeAssigned] = value

            if self.consistent(variable, tempAssignments):
                tempDomains = self.forwardChecking(toBeAssigned, variable, domains, tempAssignments)
                if tempDomains:
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
        if 'color' not in assignments[self.cell1] or 'color' not in assignments[self.cell2]:
            return True
        return assignments[self.cell1]['color'] != assignments[self.cell2]['color']

class DifferentNumberConstraint(Constraint):

    def __init__(self, cells):
        super().__init__(cells)
    
    def satisfied(self, assignments):
        numberAssignments = [assignments[variable]['number'] for variable in self.variables if 'number' in assignments[variable]]
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
        if 'color' not in assignments[self.cell1] or 'color' not in assignments[self.cell2] or 'number' not in assignments[self.cell1] or 'number' not in assignments[self.cell2]:
            return True
        cell1Color = assignments[self.cell1]['color']
        cell2Color = assignments[self.cell2]['color']
        cell1Number = assignments[self.cell1]['number']
        cell2Number = assignments[self.cell2]['number']
        return ((PriorityColorConstraint.colors.index(cell1Color) < PriorityColorConstraint.colors.index(cell2Color) and cell1Number > cell2Number)
                or (PriorityColorConstraint.colors.index(cell1Color) > PriorityColorConstraint.colors.index(cell2Color) and cell1Number < cell2Number))

def main():
    inputs = readInputs('input.txt')
    n = inputs['n']
    colors = inputs['colors']
    board = inputs['board']

    PriorityColorConstraint.colors = colors
    assignments = {}
    '''Calculating initial assignments'''
    for position, cell in board.items():
        assignments[position] = {}
        if cell.number != '*': assignments[position]['number'] = cell.number
        if cell.color != '#': assignments[position]['color'] = cell.color
    variables = [(i, j) for i in range(n) for j in range(n)]
    domains = {}
    for variable in variables: 
        domains[variable] = {} 
        domains[variable]['number'] = [number for number in range(1, n+1) if variable not in assignments or 'number' not in assignments[variable]]
        domains[variable]['color'] = [color for color in colors if variable not in assignments or 'color' not in assignments[variable]]
    
    csp = CSP(variables, domains)

    legalMoves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    covered = []
    for i in range(n):
        for j in range(n):
            currentCell = (i, j)
            neighbours = [(i+x, j+y) for x, y in legalMoves if 0 <= i+x < n and 0 <= j+y < n]
            for neighbour in neighbours:
                if {neighbour, currentCell} not in covered: 
                    csp.addConstraint(DifferentColorConstraint(currentCell, neighbour))
                    csp.addConstraint(PriorityColorConstraint(currentCell, neighbour))
                    covered.append({neighbour, currentCell})
    
    covered = []
    for i in range(n):
        columnCells = []
        lineCells = []
        for j in range(n):
            columnCells.append((j, i))
            lineCells.append((i, j))
        if set(columnCells) not in covered:
            csp.addConstraint(DifferentNumberConstraint(columnCells))
            covered.append(set(columnCells))
        if set(lineCells) not in covered:
            csp.addConstraint(DifferentNumberConstraint(lineCells))
            covered.append(set(lineCells))
    assignments = csp.backtrack(domains, assignments)
    for i in range(n):
        for j in range(n):
            print(str(assignments[(i, j)]['number']) + assignments[(i, j)]['color'], end=' ')
        print()

if __name__ == '__main__':
    main()