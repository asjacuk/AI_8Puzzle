from PuzzleState import PuzzleState
from queue import PriorityQueue

class PuzzleSolver:
    
    def __init__(self, start = PuzzleState(), goal = [1,2,3,4,5,6,7,8,0], h_func = None):
        self.start = PuzzleState(puzzle_arr = start, goal = goal, h_func = h_func) # start puzzle state PuzzleState
        self.goal = goal # goal puzzle state PuzzleState
        self.h_func = h_func # recording h function to be used for calculating f
        self.path_track = {} # empty dict to keep track of puzzle paths
        self.expanded = 0 # counter for number of expanded nodes during search

        # initialize PriorityQueue for tracking open nodes
        self.found_nodes = [self.start]
        self.open_nodes = PriorityQueue()
        self.open_nodes.put(self.start)

        self.closed_nodes = [] # storing previously expanded nodes for reference
  
    def getParity(puzzle_arr):
        parity = 0
        for i in range(8): # only go to 8 because we don't need to check the last number
            for j in range(i+1, 9):
                if puzzle_arr[i] == 0 or puzzle_arr[j] == 0: # ignore the blank space
                    continue
                if puzzle_arr[i] > puzzle_arr[j]: # inversion found, increase parity count
                        parity += 1
        return parity

    def solvable(start_arr, goal_arr):
        return PuzzleSolver.getParity(start_arr) % 2 == PuzzleSolver.getParity(goal_arr) % 2

    # trace path for current back to start and print from start to current (goal)
    def traceToParent(self, current):
        path = []
        while current in self.path_track:
            path.append(current)
            current = self.path_track[current]
        path.append(self.start)
        while path:
            node = path.pop()
            print(node)
            print("h:", node.h)
            print("g:", node.g)
            print("f=h+g:", node.f)
        print("Nodes closed:", self.expanded)
        print("Nodes open:", self.open_nodes.qsize())

    def expand(self, current):
        pos = current.getBlank()
        n = 0 # number of iterations counter
        children = [] # list to store children expanded off of current node
        child_arr = current.puzzle_arr.copy()

        if pos % 3 == 0 or pos % 3 == 1: # can move blank right
            child_arr = current.puzzle_arr.copy()
            child_arr[pos] = current.puzzle_arr[pos+1]
            child_arr[pos+1] = 0
            new_child = PuzzleState(puzzle_arr = child_arr, goal = self.goal, g = current.g + 1, h_func = self.h_func)
            if new_child not in self.found_nodes:
                children.append(new_child)
                self.found_nodes.append(new_child)
        
        if pos % 3 == 1 or pos % 3 == 2: # can move blank left
            child_arr = current.puzzle_arr.copy()
            child_arr[pos] = current.puzzle_arr[pos-1]
            child_arr[pos-1] = 0
            new_child = PuzzleState(puzzle_arr = child_arr, goal = self.goal, g = current.g + 1, h_func = self.h_func)
            if new_child not in self.found_nodes:
                children.append(new_child)
                self.found_nodes.append(new_child)
        
        if pos // 3 == 0 or pos // 3 == 1: # can move blank down
            child_arr = current.puzzle_arr.copy()
            child_arr[pos] = current.puzzle_arr[pos+3]
            child_arr[pos+3] = 0
            new_child = PuzzleState(puzzle_arr = child_arr, goal = self.goal, g = current.g + 1, h_func = self.h_func)
            if new_child not in self.found_nodes:
                children.append(new_child)
                self.found_nodes.append(new_child)

        if pos // 3 == 1 or pos // 3 == 2: # can move blank up
            child_arr = current.puzzle_arr.copy()
            child_arr[pos] = current.puzzle_arr[pos-3]
            child_arr[pos-3] = 0
            new_child = PuzzleState(puzzle_arr = child_arr, goal = self.goal, g = current.g + 1, h_func = self.h_func)
            if new_child not in self.found_nodes:
                children.append(new_child)
                self.found_nodes.append(new_child)

        return children


    def solve(self):
        if not PuzzleSolver.solvable(self.start.puzzle_arr, self.goal):
            print("ERROR (parity): This puzzle is not solvable due to incompatible parities between start and goal states.")
            return

        while not self.open_nodes.empty():
            if self.expanded > 10000:
                print("ERROR (search space): This puzzle is taking a very long time due to unoptimized expansion of search space.")
                return
            current = self.open_nodes.get() # get lowest f score node

            if current.puzzle_arr == self.goal: # found solution, get the path
                return self.traceToParent(current)
            
            self.closed_nodes.append(current)
            for child in self.expand(current):
                self.open_nodes.put(child)
                self.path_track[child] = current
            
            self.expanded += 1 # increase in expanded counter

class Main:
    easy_start   = [1,2,3,
                    4,8,5,
                    7,0,6]

    medium_start = [3,6,4,
                    0,1,2,
                    8,7,5]
    
    hard_start   = [8,0,6,
                    5,4,7,
                    2,3,1]

    easy_goal    = [1,2,3,
                    4,5,6,
                    7,8,0]

    medium_goal  = [1,2,3,
                    8,0,4,
                    7,6,5]

    hard_goal    = [0,1,2,
                    3,4,5,
                    6,7,8]
    
    unsolvable   = [1,2,3,
                    4,5,6,
                    8,7,0]
    
    test_cases = [(unsolvable, easy_goal), 
                  (easy_start, easy_goal), 
                  (medium_start, medium_goal),
                  (hard_start, hard_goal)]
    for start_state, goal_state in test_cases:

        print("\nTesting Breadth First Search...\n")
        solver = PuzzleSolver(start = start_state, goal = goal_state)
        solver.solve()

        print("\nTesting Misplaced Tiles A* Search...\n")
        solver = PuzzleSolver(start = start_state, goal = goal_state, h_func = "misplaced")
        solver.solve() 

        print("\nTesting Manhattan Distance A* Search...\n")
        solver = PuzzleSolver(start = start_state, goal = goal_state, h_func = "manhattan")
        solver.solve()

        print("\nTesting Gaschnig A* Search...\n")
        solver = PuzzleSolver(start = start_state, goal = goal_state, h_func = "gaschnig")
        solver.solve()

