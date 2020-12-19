from typing import Set
from Essentials import *

totalExploredNodes = 0
totalCreatedNodes = 0

def DepthLimitedSearch(currentNode: Node, limit, explored: Set[Node]):
    global totalCreatedNodes, totalExploredNodes
    if currentNode.state.checkTermination(): return currentNode
    if limit == 0: return 'cutoff'

    cutoffOccured = False
    currentState = currentNode.state
    currentActions = currentNode.actions
    childDepth = currentNode.depth + 1
    explored.add(currentNode)
    totalExploredNodes += 1

    for action in currentState.validActions():
        fromColumn, toColumn = action
        childState = deepcopy(currentState)
        card = childState.columns[fromColumn].removeCardFromTop()
        childState.columns[toColumn].putCardOnTop(card) 
        childNode = Node(childState, currentNode, currentActions, childDepth)
        childNode.actions.append((str(card), fromColumn, toColumn))

        if childNode not in explored:
            totalCreatedNodes += 1
            result = DepthLimitedSearch(childNode, limit-1, explored)
            if result == 'cutoff': cutoffOccured = True
            elif result != 'failure': return result
        else: continue

    return 'cutoff' if cutoffOccured else 'failure'

def IterativeDeepeningSearch(initialState, limit):
    result = 'failure'
    while result == 'failure' or result == 'cutoff':
        result = DepthLimitedSearch(Node(initialState, depth=0), limit, set())
        limit += 1
    return result

def main():

    inputs = readInputs('input.txt')
    initialState = inputs['Initial state']
    result = IterativeDeepeningSearch(initialState, 0)
    showResults(result, initialState, totalCreatedNodes, totalExploredNodes)

if __name__ == '__main__':
    main()