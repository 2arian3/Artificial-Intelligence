from copy import deepcopy
from abc import abstractmethod
from math import inf
from typing import Dict, Set, Tuple
from collections import defaultdict

'''
CSP class implemented to solve colorized sudoku.
'''
totalAssignments = []
class CSP:
    
    def __init__(self, variables: Set[Tuple], domains: Dict[Tuple, Dict]):
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

    def minimumRemainingValue(self, domains: Dict[Tuple, Dict], assignments: Dict[Tuple, Dict], unassigned: Set[Tuple]):
        remainingValues = {}
        minimum = inf
        for variable in unassigned:
            remainingValue = 1 if 'color' in assignments[variable] else len(domains[variable]['color'])
            remainingValue = 1 * remainingValue if 'number' in assignments[variable] else len(domains[variable]['number']) * remainingValue
            remainingValues[variable] = remainingValue
            if minimum > remainingValue:
                minimum = remainingValue
        return [variable for variable, remainingValue in remainingValues.items() if remainingValue == minimum]

    def degree(self, assignments: Dict[Tuple, Dict], unassigned: Set[Tuple]):
        degrees = defaultdict(lambda: 0)
        maximum = -1
        for variable in unassigned:
            for constraint in self.constraints[variable]:
                    if type(constraint) == ColorConstraint:
                        for defectiveVariable in constraint.variables:
                            if defectiveVariable != variable and 'color' not in assignments[defectiveVariable]:
                                degrees[variable] += 1
                                break
                    elif type(constraint) == NumberConstraint:
                        for defectiveVariable in constraint.variables:
                            if defectiveVariable != variable and 'number' not in assignments[defectiveVariable]:
                                degrees[variable] += 1
                                break
            if maximum < degrees[variable]:
                maximum = degrees[variable]
        return [variable for variable, remainingValue in degrees.items() if remainingValue == maximum]

    def selectVariable(self, domains: Dict[Tuple, Dict], assignments: Dict[Tuple, Dict]):
        unassigned = {variable for variable in self.variables if len(assignments[variable]) != 2}
        mrv = self.minimumRemainingValue(domains, assignments, unassigned)
        return mrv[0] if len(mrv) == 1 else self.degree(assignments, set(mrv))[0]

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
                    temp = set()
                    tempAssignments = deepcopy(assignments)
                    for value in tempDomains[defectiveVariable][toBeAssigned]:
                        tempAssignments[defectiveVariable][toBeAssigned] = value
                        if constraint.satisfied(tempAssignments): temp.add(value)
                    if len(temp) == 0: return False
                    tempDomains[defectiveVariable][toBeAssigned] = temp
        return tempDomains

    '''
    Simple backtrack algorithm.
    Used MRV and degree heuristics for variable selection.
    '''
    def backtrack(self, domains: Dict[Tuple, Dict], assignments: Dict[Tuple, Dict]):
        if not any([len(assignments[variable]) != 2 for variable in self.variables]):
            return assignments
        variable = self.selectVariable(domains, assignments)
        toBeAssigned = 'number' if 'number' not in assignments[variable] else 'color'
        for value in domains[variable][toBeAssigned]:
            global totalAssignments
            tempAssignments = deepcopy(assignments)
            tempAssignments[variable][toBeAssigned] = value
            totalAssignments.append(tempAssignments)
            if self.consistent(variable, tempAssignments):
                tempDomains = self.forwardChecking(toBeAssigned, variable, domains, tempAssignments)
                if tempDomains:
                    result = self.backtrack(tempDomains, tempAssignments)
                    if result:
                        return result
        return False

'''
Satisfied method to be overridden.
'''
class Constraint:

    def __init__(self, variables: Set):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignments: Dict[Tuple, Dict]):
        pass

class ColorConstraint(Constraint):

    '''
    Storing color priorities in colors list
    '''
    colors = {}
    def __init__(self, cell1: Tuple, cell2: Tuple):
        super().__init__({cell1, cell2})
        self.cell1 = cell1
        self.cell2 = cell2
    
    def satisfied(self, assignments: Dict[Tuple, Dict]):
        if 'color' not in assignments[self.cell1] or 'color' not in assignments[self.cell2]:
            return True
        if 'number' not in assignments[self.cell1] or 'number' not in assignments[self.cell2]:
            return assignments[self.cell1]['color'] != assignments[self.cell2]['color']
        cell1Color, cell2Color = assignments[self.cell1]['color'], assignments[self.cell2]['color']
        cell1Number, cell2Number = assignments[self.cell1]['number'], assignments[self.cell2]['number']
        return ((ColorConstraint.colors[cell1Color] > ColorConstraint.colors[cell2Color] and cell1Number > cell2Number)
                or (ColorConstraint.colors[cell1Color] < ColorConstraint.colors[cell2Color] and cell1Number < cell2Number))

class NumberConstraint(Constraint):

    def __init__(self, cells: Set[Tuple]):
        super().__init__(cells)
    
    def satisfied(self, assignments: Dict[Tuple, Dict]):
        numberAssignments = set()
        for variable in self.variables:
            if 'number' in assignments[variable]:
                if assignments[variable]['number'] in numberAssignments: return False
                numberAssignments.add(assignments[variable]['number'])
        return True