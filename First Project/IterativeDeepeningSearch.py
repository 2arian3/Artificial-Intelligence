from Essentials import *

totalExploredNodes = 1
totalCreatedNodes = 1

def DepthLimitedSearch(currentNode: Node, limit, explored: Set[Node]):
    global totalCreatedNodes, totalExploredNodes
    if currentNode.state.checkTermination(): return currentNode
    if limit == 0: return 'cutoff'

    cutoffOccured = False
    currentState: State = currentNode.state
    currentActions = currentNode.actions
    childDepth = currentNode.depth + 1
    explored.add(currentNode)
    totalExploredNodes += 1

    for action in currentState.validActions():
        fromColumn, toColumn = action
        childState = deepcopy(currentState)
        card = childState.columns[fromColumn].removeCardFromTop()
        childState.columns[toColumn].putCardOnTop(card) 
        childNode = Node(childState, currentActions, childDepth)
        childNode.actions.append((str(card), fromColumn, toColumn))

        if childNode not in explored:
            totalCreatedNodes += 1
            result = DepthLimitedSearch(childNode, limit-1, explored)
            if result == 'cutoff': cutoffOccured = True
            elif result != 'failure': return result

    return 'cutoff' if cutoffOccured else 'failure'

def IterativeDeepeningSearch(initialNode, limit):
    result = 'failure'
    while result == 'failure' or result == 'cutoff':
        result = DepthLimitedSearch(initialNode, limit, set())
        limit += 1
    return result

def main():
    #could be used to read input from a text file => inputs = readInputs('input.txt')
    #in the case below it reads the inputs from terminal
    inputs = readInputs()
    initialState = inputs['Initial state']
    result = IterativeDeepeningSearch(Node(initialState), 0)
    showResults(result, initialState, totalCreatedNodes, totalExploredNodes)

if __name__ == '__main__':
    main()