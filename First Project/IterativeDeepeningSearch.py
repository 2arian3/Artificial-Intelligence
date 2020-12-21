from Essentials import *
from collections import deque

totalExploredNodes = 0
totalCreatedNodes = 1

def DepthLimitedSearch(initialNode: Node, limit):
    global totalCreatedNodes, totalExploredNodes
    frontier = deque([initialNode])

    while frontier:
        currentNode: Node = frontier.pop()
        currentState: State = currentNode.state
        currentActions = currentNode.actions
        childDepth = currentNode.depth + 1
        totalExploredNodes += 1

        if currentState.checkTermination(): return currentNode
        elif currentNode.depth != limit:
            for action in currentState.validActions():
                childNode = child(action, deepcopy(currentState), currentActions, childDepth)
                frontier.append(childNode)
                totalCreatedNodes += 1
    
    return False

def IterativeDeepeningSearch(initialNode, limit):
    result = False
    while result is False:
        result = DepthLimitedSearch(initialNode, limit)
        limit += 1
    return result

def main():
    #could be used to read input from a text file => inputs = readInputs('input.txt')
    #in the case below it reads the inputs from terminal
    inputs = readInputs('input.txt')
    initialState = inputs['Initial state']
    limit = int(input('Enter the initial depth to be searched:'))
    result = IterativeDeepeningSearch(Node(initialState), limit)
    showResults(result, initialState, totalCreatedNodes, totalExploredNodes)

if __name__ == '__main__':
    main()