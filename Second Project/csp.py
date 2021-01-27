from copy import deepcopy
from abc import abstractmethod
from math import inf
from random import choice
from typing import Dict, List, Tuple

'''
CSP class implemented to solve colorized sudoku.
'''
class CSP:
    
    def __init__(self, variables: List[Tuple], domains: Dict[Tuple, Dict]):
        self.variables = variables
        self.domains = domains
        self.constraints = {}
        for variable in variables:
            self.constraints[variable] = []

    def addConstraint(self, constraint):
        for variable in constraint.variables:
            self.constraints[variable].append(constraint)

    def consistent(self, variable: Tuple, assignments: Dict[Tuple, Dict]):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignments):
                return False
        return True

    def minimumRemainingValue(self, domains: Dict[Tuple, Dict], assignments: Dict[Tuple, Dict], unassigned: List[Tuple]):
        remainingValues = {}
        for variable in unassigned:
            remainingValue = 1 if 'color' in assignments[variable] else len(domains[variable]['color'])
            remainingValue = 1 * remainingValue if 'number' in assignments[variable] else len(domains[variable]['number']) * remainingValue
            remainingValues[variable] = remainingValue
        minimum = inf
        for variable in remainingValues:
            if minimum > remainingValues[variable]:
                minimum = remainingValues[variable]
        return [variable for variable, remainingValue in remainingValues.items() if remainingValue == minimum]

    def degree(self, assignments: Dict[Tuple, Dict], unassigned: List[Tuple]):
        degrees = {}
        for variable in unassigned:
            count = 0
            for constraint in self.constraints[variable]:
                    if type(constraint) == ColorConstraint:
                        count += 1 if any(['color' not in assignments[defectiveVariable] for defectiveVariable in constraint.variables if defectiveVariable != variable]) else 0
                    elif type(constraint) == NumberConstraint:
                        count += 1 if any(['number' not in assignments[defectiveVariable] for defectiveVariable in constraint.variables if defectiveVariable != variable]) else 0
            degrees[variable] = count
        maximum = -1
        for variable in degrees:
            if maximum < degrees[variable]:
                maximum = degrees[variable]
        return [variable for variable, remainingValue in degrees.items() if remainingValue == maximum]

    def selectVariable(self, domains: Dict[Tuple, Dict], assignments: Dict[Tuple, Dict]):
        unassigned = [variable for variable in self.variables if 'color' not in assignments[variable] or 'number' not in assignments[variable]]
        degree = self.degree(assignments, unassigned) 
        mrv = self.minimumRemainingValue(domains, assignments, unassigned)
        return mrv[0] if len(mrv) == 1 else degree[0]

    '''
    Updating unassigned variable domains based on 
    new assignment.
    returns false if one of the domains got empty.
    '''
    def forwardChecking(self, toBeAssigned, variable: Tuple, domains: Dict[Tuple, Dict], assignments: Dict[Tuple, Dict]):
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

    '''
    Simple backtrack algorithm.
    Used MRV and degree heuristics for variable selection.
    '''
    def backtrack(self, domains: Dict[Tuple, Dict], assignments: Dict[Tuple, Dict]):
        if all([len(assignment) == 2 for assignment in list(assignments.values())]):
            return assignments
        variable = self.selectVariable(domains, assignments)
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

'''
Satisfied method to be overridden.
'''
class Constraint:

    def __init__(self, variables: List):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignments: Dict[Tuple, Dict]):
        pass

class ColorConstraint(Constraint):

    '''
    Storing color priorities in colors list
    '''
    colors = []
    def __init__(self, cell1, cell2):
        super().__init__([cell1, cell2])
        self.cell1 = cell1
        self.cell2 = cell2
    
    def satisfied(self, assignments: Dict[Tuple, Dict]):
        if 'color' not in assignments[self.cell1] or 'color' not in assignments[self.cell2]:
            return True
        if 'number' not in assignments[self.cell1] or 'number' not in assignments[self.cell2]:
            return assignments[self.cell1]['color'] != assignments[self.cell2]['color']
        cell1Color = assignments[self.cell1]['color']
        cell2Color = assignments[self.cell2]['color']
        cell1Number = assignments[self.cell1]['number']
        cell2Number = assignments[self.cell2]['number']
        return ((ColorConstraint.colors.index(cell1Color) < ColorConstraint.colors.index(cell2Color) and cell1Number > cell2Number)
                or (ColorConstraint.colors.index(cell1Color) > ColorConstraint.colors.index(cell2Color) and cell1Number < cell2Number))

class NumberConstraint(Constraint):

    def __init__(self, cells: List[Tuple]):
        super().__init__(cells)
    
    def satisfied(self, assignments: Dict[Tuple, Dict]):
        numberAssignments = [assignments[variable]['number'] for variable in self.variables if 'number' in assignments[variable]]
        return len(numberAssignments) == len(set(numberAssignments))