

class Vertex:    
    """Class representing each puzzle."""
    queList = []
    finished = False
    finalNodes = 0

    def __init__(self, arr=[], state= 0, parent = None, expanded = False, children = []):
        """Initializes Vertex object with default parameters."""
        self.arr = arr
        self.state = state
        self.parent = parent
        self.children = children
        self.expanded = expanded

    # calculates Manhattan Distance for puzzle according to passed in goal array
    def manhattanDistance(self, goal):
        manhattan = 0
        for i in range(9):
            goal_index = goal.index(self.arr[i])
            manhattan += ( abs((i / 3) - (goal_index / 3)) +  # calculate number of rows needed to move
                            abs((i % 3) - (goal_index % 3)) ) # calculate number of columns needed to move
        return manhattan
    
    
class Graph:
    
    arrayDict = []
    
    
    def printArr(arr):
        """Prints the array formatted in lines of three"""
        print()
        print(arr[:3])
        print(arr[3:6])
        print(arr[6:])
    
    
    
    def traceToParent(currentVertex):
        """Prints path to given vertex starting at head (state=0)"""
        """To use to display path to solution when found."""
        if currentVertex.state == 0:
            Graph.printArr(currentVertex.arr)
            print("STATE:", currentVertex.state)
            return
        else:
            Graph.traceToParent(currentVertex.parent)
            Graph.printArr(currentVertex.arr)
            print("STATE:", currentVertex.state)

    def createChildren(currentVertex, goalArr): ##Reference goal here?
        """Expands vertex (node) for all potential moves."""
        
        """TODO: code in goal solution rather than referencing by "goalArr"
                May have to fix number of open nodes. Double check number is accurate."""
    
        
        pos = currentVertex.arr.index(' ') #current position of empty space.

        nPos = 0 #Iteration of potitions to find potential moves.
        
        while(nPos < 9):
            tmpArr =  currentVertex.arr.copy()
            if abs(pos - nPos) in [1,3]:
                tmpArr[pos] = tmpArr[nPos]
                tmpArr[nPos] = ' '

                            
                if tmpArr == goalArr: #Solution found. Exit.
                    print("HOORAH")
                    currentVertex.expanded = True
                    tmpVertex = Vertex(tmpArr.copy(), currentVertex.state + 1, currentVertex, True, [])
                    currentVertex.children.append(tmpVertex)
                    Graph.arrayDict.append(tmpArr)
                    Graph.traceToParent(tmpVertex)
                    Vertex.finished = True
                    Vertex.finalNodes += 1
                    return 
                    
                else:
                    
                    if str(tmpArr) in Graph.arrayDict:
                        return #Array value already exists.
                    else:
                        Graph.arrayDict.append(tmpArr)
                        currentVertex.children.append(Vertex(tmpArr.copy(), currentVertex.state + 1, currentVertex, False, []))
                        Vertex.finalNodes += 1
                    
                    
                
                        
            nPos += 1
                        
        currentVertex.expanded = True;



        return
       
    def createNextState(head, goalArr, currState):
        
        tmpState = currState
        
        if Vertex.finished == True:
            return
            
        if head.expanded == False:
            Graph.createChildren(head, goalArr)

        
        
        for nextVertex in head.children:
            if tmpState == nextVertex.state:
                if nextVertex.expanded == False:
                    Graph.createChildren(nextVertex, goalArr)
            else:
                Graph.createNextState(nextVertex, goalArr, tmpState)
        tmpState += 1
        Graph.createNextState(head, goalArr, tmpState)

    def getParity(puzzleArr):
        parity = 0
        for i in range(8): # only go to 8 because we don't need to check the last number
            for j in range(i+1, 9):
                if puzzleArr[i] == ' ' or puzzleArr[j] == ' ': # ignore the blank space
                    continue
                if puzzleArr[i] > puzzleArr[j]: # inversion found, increase parity count
                        parity += 1
        return parity

    # determine if start parity matches goal parity
    def isSolvable(start, goal):
        return (Graph.getParity(start)) % 2 == (Graph.getParity(goal)) % 2
 
    def initTree(head, goalArr):
        if Graph.isSolvable(head.arr, goalArr):
            Graph.arrayDict.append(head.arr)
            Graph.createChildren(head, goalArr)

            Graph.createNextState(head, goalArr, 1)

        else:
            print("This puzzle is not solvable!")
            
    


    
class Main:

    ax = [1,2,3,4,8,5,7,' ',6]
    goalAX = [1,2,3,4,5,6,7,8,' ']
    
    nv = Vertex(ax, 0, None, False, [])
    
    Graph.initTree(nv, goalAX)
    
    print("\nOpen Nodes: ", Vertex.finalNodes)
    

  