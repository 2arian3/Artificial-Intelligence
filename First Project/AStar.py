from Essentials import *
from queue import PriorityQueue

totalExploredNodes = 0
totalCreatedNodes = 1

def AStar(initialNode: Node):
    global totalExploredNodes, totalCreatedNodes
    currentNode: Node = initialNode
    frontier = PriorityQueue()
    frontier.put((0, id(currentNode), currentNode))
    costs: Dict[Node: int] = {}
    costs[currentNode] = 0

    while frontier:
        currentNode: Node = frontier.get()[2]
        currentState: State = currentNode.state
        currentActions: List = currentNode.actions
        childDepth = currentNode.depth + 1
        totalExploredNodes += 1

        if currentState.checkTermination(): return currentNode

        for action in currentState.validActions():
            childNode = child(action, deepcopy(currentState), currentActions, childDepth)
            childCost = costs[currentNode] + 1
            if childNode not in costs:
                costs[childNode] = childCost
                priority = childCost + childNode.heuristic()
                frontier.put((priority, id(childNode), childNode))
                totalCreatedNodes += 1
    
    return False

def main():
    #could be used to read input from a text file => inputs = readInputs('input.txt')
    #in the case below it reads the inputs from text file
    inputs = readInputs('input.txt')
    initialState = inputs['Initial state']
    result = AStar(Node(initialState))
    if result != False: showResults(result, initialState, totalCreatedNodes, totalExploredNodes)

if __name__ == '__main__':
    main()