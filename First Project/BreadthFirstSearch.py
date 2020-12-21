from Essentials import *
from collections import deque

totalExploredNodes = 0
totalCreatedNodes = 1

def BreadthFirstSearch(initialNode: Node):
    global totalExploredNodes, totalCreatedNodes
    currentNode: Node = initialNode

    frontier = deque([currentNode])
    explored: Set[Node] = set()

    while frontier:
        currentNode: Node = frontier.popleft()
        currentState: State = currentNode.state
        currentActions = currentNode.actions
        childDepth = currentNode.depth + 1
        explored.add(currentNode)
        totalExploredNodes += 1

        if currentState.checkTermination(): return currentNode

        for action in currentState.validActions():
            childNode = child(action, deepcopy(currentState), currentActions, childDepth)
            if childNode not in explored:
                frontier.append(childNode)
                totalCreatedNodes += 1
        
    return False

def main():
    #could be used to read input from a text file => inputs = readInputs('input.txt')
    #in the case below it reads the inputs from terminal
    inputs = readInputs('input.txt')
    initialState = inputs['Initial state']
    result = BreadthFirstSearch(Node(initialState))
    if result != False: showResults(result, initialState, totalCreatedNodes, totalExploredNodes)
    
if __name__ == '__main__':
    main()