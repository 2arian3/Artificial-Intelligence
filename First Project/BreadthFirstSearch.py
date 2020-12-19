from typing import Set
from Essentials import *
from collections import deque

totalExploredNodes = 0
totalCreatedNodes = 1

def BreadthFirstSearch(initialState: State):
    global totalExploredNodes, totalCreatedNodes
    currentNode = Node(initialState, depth=0)
    if initialState.checkTermination(): return currentNode

    frontier = deque([currentNode])
    explored: Set[Node] = set()

    while frontier:

        currentNode = frontier.popleft()
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
                if childState.checkTermination(): return childNode
                frontier.append(childNode)
                totalCreatedNodes += 1
        
    return False

def main():
    
    inputs = readInputs('input.txt')
    initialState = inputs['Initial state']
    result = BreadthFirstSearch(initialState)
    if result != False: showResults(result, initialState, totalCreatedNodes, totalExploredNodes)
    
if __name__ == '__main__':
    main()