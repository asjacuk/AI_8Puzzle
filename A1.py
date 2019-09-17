from queue import PriorityQueue

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
        self.g = 0
        self.h = 0
        self.f = 0

    """
    Overriding the comparison operators to allow Vertex class to be easily comparable
    using their f values for priority queue implememtation to be used during searches
    """
    # equality
    def __eq__(self, other):
        return self.f == other.f
    # less than
    def __lt__(self, other):
        return self.f < other.f
    # less than or equal
    def __le__(self, other):
        return self.f <= other.f
    # greater than
    def __gt__(self, other):
        return self.f > other.f
    # greater than or equal
    def __ge__(self, other):
        return self.f >= other.f
    # not equal (inequality)
    def __ne__(self, other):
        return self.f != other.f

    """"
    Heuristic Functions
    -------------------------------------------------------------------------------------------------
    These functions are intended to be used in order to calculate h(n) of a Vertex with h() being the 
    heuristic function selected for the search and n being any node processed during that search.
    The value of h(n) is used to determine the value of f(n) = g(n) + h(n) in order to identify which
    Vertex should be expanded next.
    -------------------------------------------------------------------------------------------------
    misplacedTiles - calculates the number of tiles that are in the incorrect position when compared
        to the goal positions and both stores and returns this value for further use
    
    manhattanDistance - calculates the Manhattan Distance of moves required to get the current state
        to the goal state and both stores and returns this value for further use

    gaschnig - calculates the Gaschnig value resulting from the number of moves needed to solve the
        puzzle from the current state to the goal state using the relaxed rules that any tile can be
        moved to the blank spot in a single move, regardless of other tiles, and both stores and 
        returns this value
    """"
    # takes a goal array and returns number of misplaced tiles from current puzzle state to goal
    def misplacedTiles(self, goal):
        self.h = sum(1 for i, j in zip(self.arr, goal) if i != j)
        return self.h
            

    # calculates Manhattan Distance for puzzle according to passed in goal array
    def manhattanDistance(self, goal):
        manhattan = 0
        for i in range(len(self.arr)):
            goal_index = goal.index(self.arr[i])
            manhattan += ( abs((i // 3) - (goal_index // 3)) +  # calculate number of rows needed to move
                            abs((i % 3) - (goal_index % 3)) ) # calculate number of columns needed to move
        self.h = manhattan
        return manhattan

    # calculates Gaschnig's heuristic from current puzzle state to goal
    def gaschnig(self, goal):
        gaschnig = 0
        complete = False
        while not complete:
            blank_index = self.arr.index(' ') # get index of ' ' in current puzzle
            if goal[blank_index] != ' ': # ' ' not at same spot in goal
                target_index = self.arr.index(goal[blank_index])
                self.arr[blank_index] = goal[blank_index] # swap ' ' with correct number from goal
                self.arr[target_index] = ' '
                gaschnig += 1
            else: # ' ' matched, check puzzle for completeness
                for i in range(len(self.arr)):
                    if self.arr[i] != goal[i]: # mismatch, puzzle not complete
                        self.arr[blank_index] = self.arr[i]
                        self.arr[i] = ' '
                        gaschnig += 1
                        break
                complete = True # all done
        self.h = gaschnig
        return gaschnig


            
    
    
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
    
    def a_star_search(start, goal, h_func):
        # initialize the priority queue and add start
        q = PriorityQueue()
        q.put((0, start))

        parent_path = {} # empty dict to store parents of each Vertex expanded

        # initialize g and f dictionaries with Vertex as key and corresponding g and f values
        g = {start:0}
        f = {start:h_func(start)}

        while not q.empty():
            current = q.get()

class a_star:
    
    def __init__(self, start, goal, h_func):
        open_nodes = [start]
        self.goal = goal
        self.h_func = h_func
        g = {start:0}
        f = {start:h_func(start, goal.arr)}
        print(f[start])
        self.a_star_search()

    def a_star_search(self):

        while len(open_nodes) != 0:
            current = getMinF()
        
    def getMinF(self):
        return min(open_nodes)

class Main:

    ax = [1,2,3,4,8,5,7,' ',6]
    goalAX = [1,2,3,4,5,6,7,8,' ']
    
    nv = Vertex(ax, 0, None, False, [])
    goal = Vertex(goalAX)
    a_star(nv, goal, Vertex.misplacedTiles)
    
    Graph.initTree(nv, goalAX)
    
    print("\nOpen Nodes: ", Vertex.finalNodes)
    

  