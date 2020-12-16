import copy
from Essentials import *
        
def BreadthFirstSearch(initialState):
    currentNode = Node(initialState)
    if initialState.checkTermination(): return currentNode

    frontier = [currentNode]
    explored = []

    while frontier:

        currentNode = frontier.pop(0)
        explored.append(currentNode)

        for action in currentNode.state.validActions():
            fromColumn, toColumn = action
            childState = copy.deepcopy(currentNode.state)
            childNode = Node(childState, currentNode, currentNode.actions)
            currentNode.childs.append(childNode)
            childState.columns[toColumn].putCardOnTop(childState.columns[fromColumn].removeCardFromTop()) 
            childNode.actions.append('Moved card ' + str(childState.columns[toColumn].cards[-1]) + ' from column ' + str(fromColumn) + ' to column ' + str(toColumn))
            if childNode not in explored and childNode not in frontier:
                if childState.checkTermination(): return childNode
                frontier.append(childNode)
        
    return False

def main():
    
    inputs = readInputs('input.txt')
    initialState = inputs['Initial state']

if __name__ == '__main__':
    main()