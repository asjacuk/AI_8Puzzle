from queue import PriorityQueue

class Vertex:    
    """Class representing each puzzle."""
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
        return self.arr == other.arr
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

    
    """
    Utility Functions
    -------------------------------------------------------------------------------------------------
    """
    # overriding __str__ to provide print()-ability of puzzle states
    def __str__(self):
        row1 = str(self.arr[0:3])
        row2 = str(self.arr[3:6])
        row3 = str(self.arr[6:9])
        message = "{r1}\n{r2}\n{r3}\n".format(r1 = row1, r2 = row2, r3 = row3)
        return message

    # overriding hashing behavior for use of class as a key in dict
    def __hash__(self):
        return hash(tuple(self.arr))


    """
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
    """
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
        q.put(start)

        parent_path = {} # empty dict to store parents of each Vertex expanded

        # initialize g and f dictionaries with Vertex as key and corresponding g and f values
        g = {start:0}
        f = {start:h_func(start)}

        while not q.empty():
            current = q.get() # get lowest 

class PuzzleSolver:

    def __init__(self, start = Vertex(), goal = Vertex(), h_func = None):
        self.start = start # start puzzle state Vertex
        self.goal = goal # goal puzzle state Vertex
        self.h_func = __hfunc(h_func) # mapping Vertex h function
        self.path_track = {} # empty dict to keep track of puzzle paths
        self.expanded = 0 # counter for number of expanded nodes during search

        # initialize PriorityQueue for tracking open nodes
        self.open_nodes = PriorityQueue()
        self.open_nodes.put(start)

        self.closed_nodes = [] # storing previously expanded nodes for reference

    # mapping h_func strings to actual functions in Vertex class
    def __hfunc(self, h_func):
        return {
            'misplaced' : Vertex.misplacedTiles,
            'manhattan' : Vertex.manhattanDistance,
            'gaschnig' : Vertex.gaschnig
        }.get(h_func, -1)

    # trace path for current back to start and print from start to current (goal)
    def traceToParent(self, current):
        path = []
        while current in path_track:
            path.append(current)
            current = path_track[current]
        while path:
            print(path.pop(0))

    def expand(self, current):
        pos = current.arr.index(' ')
        n = 0 # number of iterations counter
        children = [] # list to store children expanded off of current node
        child_arr = current.arr.copy()

        if pos % 3 == 0 or pos % 3 == 1: # can move blank right
            child_arr[pos] = current.arr[pos+1]
            child_arr[pos+1] = ' '
            children.append(Vertex(arr = child_arr, parent = current, ))


    def search(self):
        while not self.open_nodes.empty():
            current = open_nodes.get() # get lowest f score node

            if current == goal: # found solution, get the path
                return self.traceToParent(current)
            
            closed_nodes.append(current)
            for child in expand(current):
                open_nodes.put(child)
            


    


class Main:

    ax = [1,2,3,4,8,5,7,' ',6]
    goalAX = [1,2,3,4,5,6,7,8,' ']
    
    nv = Vertex(ax, 0, None, False, [])
    print(nv)
    goal = Vertex(goalAX)
    
    Graph.initTree(nv, goalAX)
    
    print("\nOpen Nodes: ", Vertex.finalNodes)
    

  