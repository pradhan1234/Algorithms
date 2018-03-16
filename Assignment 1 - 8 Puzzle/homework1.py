#import statements
from copy import deepcopy
import sys

#global variables
rowMovement = {0:["down"], 1:["down", "up"], 2:["up"]}
colMovement = {0:["right"], 1:["right", "left"], 2:["left"]}
goalIndices = {1:[0, 0],2:[0, 1],3:[0, 2],4:[1, 0],5:[1, 1],6:[1, 2],7:[2, 0],8:[2, 1],9:[2, 2]}
goalConfiguration = [[1,2,3],[4,5,6],[7,8,9]]


#function definitions

class Tree(object):
    def __init__(self):
        self.id = None
        self.parent = None
        self.heuristic = None
        self.action = None
        self.pathCost = None
        self.depth = 0
        self.configuration = None
        
def createGoal(goalConfiguration):
    goal = Tree()
    goal.id = createID(goalConfiguration)
    goal.configuration = goalConfiguration
    return goal
    
def createRoot(currentConfiguration):
    root = Tree()
    root.id = createID(currentConfiguration)
    root.parent = None
    root.action = None
    root.depth = 0
    root.pathCost = 0
    root.heuristic = computeHeuristic(root.pathCost, currentConfiguration)
    root.configuration = currentConfiguration
    return root

def createChild(parent, action):
    child = Tree()
    child.parent = parent
    child.action = action
    child.depth = parent.depth + 1
    child.pathCost = parent.pathCost + 1
    child.configuration = makeMove(parent.configuration, action)
    child.id = createID(child.configuration)
    child.heuristic = computeHeuristic(child.pathCost, child.configuration)
    return child

def createID(currentConfiguration):
    flat = [tile for row in currentConfiguration for tile in row]
    id = ''.join(str(tile) for tile in flat)
    return id

def distToTileGoalPosition(tile, rowIndex, colIndex):
    goalRowIndex, goalColIndex = goalIndices[tile]
    dist = abs(rowIndex - goalRowIndex) + abs(colIndex - goalColIndex)
    return dist

def computeHeuristic(g, currentConfiguration):
    h = 0
    for i in range(len(currentConfiguration)):
        for j in range(len(currentConfiguration[i])):
            if(currentConfiguration[i][j]!=9):
                h += distToTileGoalPosition(currentConfiguration[i][j], i, j)
    return g+h

def getPositionBlankTile(currentConfiguration):
    for i in range(len(currentConfiguration)):
        for j in range(len(currentConfiguration)):
            if(currentConfiguration[i][j] == 9):
                return [i, j]


#function to read the initial board configuration from console
def readBoardConfiguration():

	configuration = []
	row1 = input().strip().split(' ')
	row2 = input().strip().split(' ')
	row3 = input().strip().split(' ')

	for i in range(len(row1)):
		if(row1[i]=='*'):
			row1[i] = 9
		else:
			row1[i] = int(row1[i])
	for i in range(len(row2)):
		if(row2[i]=='*'):
			row2[i] = 9
		else:
			row2[i] = int(row2[i])
	for i in range(len(row3)):
		if(row3[i]=='*'):
			row3[i] = 9
		else:
			row3[i] = int(row3[i])

	configuration.append(row1)
	configuration.append(row2)
	configuration.append(row3)
	return configuration


def getValidMoves(rowIndex, colIndex):
    validMoves = []
    orderedMoves = []
    validMoves.extend(colMovement[colIndex])
    validMoves.extend(rowMovement[rowIndex])

    if("up" in validMoves):
        orderedMoves.append("up")    
    if("down" in validMoves):
        orderedMoves.append("down")
    if("left" in validMoves):
        orderedMoves.append("left")
    if("right" in validMoves):
        orderedMoves.append("right")
    return orderedMoves


def makeMove(currentConfiguration, moveType):
    
    rowIndex, colIndex = getPositionBlankTile(currentConfiguration)
    nextConfiguration = deepcopy(currentConfiguration)
    if(moveType=="up"):
        temp = nextConfiguration[rowIndex-1][colIndex]
        nextConfiguration[rowIndex-1][colIndex] = nextConfiguration[rowIndex][colIndex]
        nextConfiguration[rowIndex][colIndex] = temp
    elif(moveType=="down"):
        temp = nextConfiguration[rowIndex+1][colIndex]
        nextConfiguration[rowIndex+1][colIndex] = nextConfiguration[rowIndex][colIndex]
        nextConfiguration[rowIndex][colIndex] = temp
    elif(moveType=="left"):
        temp = nextConfiguration[rowIndex][colIndex-1]
        nextConfiguration[rowIndex][colIndex-1] = nextConfiguration[rowIndex][colIndex]
        nextConfiguration[rowIndex][colIndex] = temp
    elif(moveType=="right"):
        temp = nextConfiguration[rowIndex][colIndex+1]
        nextConfiguration[rowIndex][colIndex+1] = nextConfiguration[rowIndex][colIndex]
        nextConfiguration[rowIndex][colIndex] = temp
        
    return nextConfiguration
    
def printIterSol(node):
    arr = []
    count = 0
    while(node.parent!=None):
        arr.append(node)
        node = node.parent
        
    
    while(len(arr)>0):
        node = arr.pop()
        printBoard(node.configuration)
        print()

def printBoard(config):
    for i in range(len(config)):
        for j in range(len(config[i])):
            if(config[i][j] == 9):
                print("*", end=" ")
            else:
                print(config[i][j], end=" ")
        print()


def isGoalConfiguration(node):
    if(node.id==goal.id):
        return True
    else:
        return False


def depthFirstSearch(node, goal):
    count = 0
    openList = [node]
    closedList = []
    openListID = [node.id]
    closedListID = []
    
    while(True):
        count += 1
        #print(count)
        if(len(openList)==0):
            return False, len(openList)+len(closedList)
        
        currentNode = openList.pop()
        currentID = openListID.pop()
        
        closedList.append(currentNode)
        closedListID.append(currentID)
        
        if(isGoalConfiguration(currentNode)):
            return currentNode, len(openList)+len(closedList) 
        
        #apply actions on currentNode 
        rowIndex, colIndex = getPositionBlankTile(currentNode.configuration)
        actions = getValidMoves(rowIndex, colIndex)
        
        for action in actions:
            child = createChild(currentNode, action)
            #if child node not in open list or closed list, add to open list
            if((child.id not in openListID) and (child.id not in closedListID)):
                openList.append(child)
                openListID.append(child.id)
    
def iterativeDeepeningSearch(root, goal):
	i = 0
	while(True):
		i = i + 1
		result, states_enqueued = depthLimitedSearch(root, goal, i)
		if(result!=False):
			break
	return result, states_enqueued

def depthLimitedSearch(node, goal, limit):
    count = 0
    
    openList = [node]
    openListID = [node.id]
    
    closedList = []
    closedListID = []
    
    while(True):
        count += 1
        #print(count)
        if(len(openList)==0):
            return False, len(openList)+len(closedList)
        
        currentNode = openList.pop()
        currentID = openListID.pop()
        
        closedList.append(currentNode)
        closedListID.append(currentID)
        
        if(isGoalConfiguration(currentNode)):
            return currentNode, len(openList)+len(closedList)
        else:
            if(currentNode.depth != limit):
                
                #apply actions on currentNode 
                rowIndex, colIndex = getPositionBlankTile(currentNode.configuration)
                actions = getValidMoves(rowIndex, colIndex)

                for action in actions:
                    child = createChild(currentNode, action)
                    #if child node not in open list or closed list, add to open list
                    if((child.id not in openListID) and (child.id not in closedListID)):
                        openList.append(child)
                        openListID.append(child.id)

def aStarSearch(node, goal):
    count = 0
    
    openList = [node]
    openHeuristicList = [node.heuristic]
    openListID = [node.id]
    
    closedList = []
    closedHeuristicList = []
    closedListID = []
    
    while(True):
        count += 1
        #print(count)
        if(len(openList)==0):
            return False, len(openList)+len(closedList)
        
        #choose node to explore based on heuristic
        index = openHeuristicList.index(min(openHeuristicList))
        currentNode = openList.pop(index)
        currentID = openListID.pop(index)
        currentHeuristic = openHeuristicList.pop(index)
        
        
        closedList.append(currentNode)
        closedListID.append(currentID)
        closedHeuristicList.append(currentHeuristic)
        
        if(isGoalConfiguration(currentNode)):
            return currentNode, len(openListID) + len(closedListID)
        
        #apply actions on currentNode 
        rowIndex, colIndex = getPositionBlankTile(currentNode.configuration)
        actions = getValidMoves(rowIndex, colIndex)
        
        for action in actions:
            child = createChild(currentNode, action)
            #if child node not in open list or closed list, add to open list
            if((child.id not in openListID) and (child.id not in closedListID)):
                openList.append(child)
                openListID.append(child.id)
                openHeuristicList.append(child.heuristic)
    

#main method
if __name__ == "__main__":

	algorithm = sys.argv[1]
	#read the board configuration
	print("Input the initial board configuration:")
	currentConfiguration = readBoardConfiguration()

	goal = createGoal(goalConfiguration)
	root = createRoot(currentConfiguration)

	if(algorithm == "DEPTH_FIRST_SEARCH"):
		print("\nSolving 8 puzzle by", algorithm)
		goalDepthFirstSearch, states_enqueued = depthFirstSearch(root, goal)
		printBoard(root.configuration)
		print()
		printIterSol(goalDepthFirstSearch)
		print("Number of moves:", goalDepthFirstSearch.depth)
		print("Number of states enqueued:", states_enqueued)

	elif(algorithm == "ITERATIVE_DEEPENING_SEARCH"):
		print("\nSolving 8 puzzle by", algorithm)
		goalIterativeDeepening, states_enqueued = iterativeDeepeningSearch(root, goal)
		printBoard(root.configuration)
		print()
		printIterSol(goalIterativeDeepening)
		print("Number of moves:", goalIterativeDeepening.depth)
		print("Number of states enqueued:", states_enqueued)

	elif(algorithm == "A_STAR_SEARCH"):
		print("\nSolving 8 puzzle by", algorithm)
		goalAstar, states_enqueued = aStarSearch(root, goal)
		printBoard(root.configuration)
		print()
		printIterSol(goalAstar)
		print("Number of moves:", goalAstar.depth)
		print("Number of states enqueued:", states_enqueued)