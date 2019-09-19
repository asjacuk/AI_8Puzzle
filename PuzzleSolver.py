#import sys 
#sys.path.append("C:/Users/andre/Documents/School/2019.fall/AI_A1/AI_8Puzzle")
#Kris, ignore the above...
#the above has been ignored by Kris.

from PuzzleState import PuzzleState
from queue import PriorityQueue
import time

class PuzzleSolver:
    
    def __init__(self, start = PuzzleState(), goal = [1,2,3,4,5,6,7,8,0], h_func = 0):
        self.start = PuzzleState(puzzle_arr = start, goal = goal, h_func = h_func) # start puzzle state PuzzleState
        self.goal = goal # goal puzzle state PuzzleState
        self.h_func = h_func # recording h function to be used for calculating f
        self.path_track = {self.start : 0} # empty dict to keep track of puzzle paths
        self.expanded = 0 # counter for number of expanded nodes during search
        self.max_search_space = 0 # tracker for max size of the search space during search

        # initialize PriorityQueue for tracking open nodes
        self.found_nodes = [self.start]
        self.open_nodes = PriorityQueue()
        self.open_nodes.put(self.start)

        self.closed_nodes = [] # storing previously expanded nodes for reference
  
    # takes a puzzle array and returns the parity value of that array
    def getParity(puzzle_arr):
        parity = 0
        for i in range(8): # only go to 8 because we don't need to check the last number
            for j in range(i+1, 9):
                if puzzle_arr[i] == 0 or puzzle_arr[j] == 0: # ignore the blank space
                    continue
                if puzzle_arr[i] > puzzle_arr[j]: # inversion found, increase parity count
                        parity += 1
        return parity

    # wrapper for determining if parities between two states are compatibile
    def solvable(start_arr, goal_arr):
        return PuzzleSolver.getParity(start_arr) % 2 == PuzzleSolver.getParity(goal_arr) % 2

    # trace path for current back to start and print from start to current (goal)
    def traceToParent(self, current):
        path = []
        while current in self.path_track:
            path.append(current)
            current = self.path_track[current]
        solLen = len(path)
        path.append(self.start)
        while path:
            node = path.pop()
            print(node)
        print("\n\tNodes expanded:", self.expanded)
        print("\tMax search space:", self.open_nodes.qsize())
        print("\tSolution length:", solLen)

    """
    Expands a node to determine possible children and checks to see if possible children
    have already been found. If they have, discards those children and returns a list of the
    viable children.
    """
    def expand(self, current):
        pos = current.getBlank()
        children = [] # list to store children expanded off of current node
        child_arr = current.puzzle_arr.copy()

        if pos % 3 == 0 or pos % 3 == 1: # can move blank right
            child_arr = current.puzzle_arr.copy()
            child_arr[pos] = current.puzzle_arr[pos+1]
            child_arr[pos+1] = 0
            new_child = PuzzleState(puzzle_arr = child_arr, goal = self.goal, g = current.g + 1, h_func = self.h_func)
            if new_child not in self.path_track:
                children.append(new_child)
                self.found_nodes.append(new_child)
        
        if pos % 3 == 1 or pos % 3 == 2: # can move blank left
            child_arr = current.puzzle_arr.copy()
            child_arr[pos] = current.puzzle_arr[pos-1]
            child_arr[pos-1] = 0
            new_child = PuzzleState(puzzle_arr = child_arr, goal = self.goal, g = current.g + 1, h_func = self.h_func)
            if new_child not in self.path_track:
                children.append(new_child)
                self.found_nodes.append(new_child)
        
        if pos // 3 == 0 or pos // 3 == 1: # can move blank down
            child_arr = current.puzzle_arr.copy()
            child_arr[pos] = current.puzzle_arr[pos+3]
            child_arr[pos+3] = 0
            new_child = PuzzleState(puzzle_arr = child_arr, goal = self.goal, g = current.g + 1, h_func = self.h_func)
            if new_child not in self.path_track:
                children.append(new_child)
                self.found_nodes.append(new_child)

        if pos // 3 == 1 or pos // 3 == 2: # can move blank up
            child_arr = current.puzzle_arr.copy()
            child_arr[pos] = current.puzzle_arr[pos-3]
            child_arr[pos-3] = 0
            new_child = PuzzleState(puzzle_arr = child_arr, goal = self.goal, g = current.g + 1, h_func = self.h_func)
            if new_child not in self.path_track:
                children.append(new_child)
                self.found_nodes.append(new_child)

        return children

    """
    A* Search Algorithm - solve()
    --------------------------------------------------------------------------------------------------------------------------
    This is an implementation of the A* search algorithm that processes discovered nodes according to the function:
                f(n)   =    g(n)    +   h(n)
    for any node n with:
            f(n) = fitness of node
            g(n) = distance from start to node
            h(n) = heuristic value of the node
    
    This implementation of the A* search algorithm is designed to search for solution paths to the 8 tile puzzle with
    puzzle states being represented externally as PuzzleStates and internally as an array form of the board state with
    f, g and h attributes. After finding a solution, solve() will output the board states of the solution path from
    start to goal and display the number of nodes expanded in order to determine the solution, the largest the search
    space (open nodes) reached at any point during the search, and the length of the solution path.
    """
    def solve(self):
        if not PuzzleSolver.solvable(self.start.puzzle_arr, self.goal):
            print("ERROR (parity): This puzzle is not solvable due to incompatible parities between start and goal states.")
            return

        while not self.open_nodes.empty():
            #if self.expanded > 150000:
            #    print("ERROR (search space): This puzzle is taking a very long time due to unoptimized expansion of search space.")
            #    return
            if self.open_nodes.qsize() > self.max_search_space:
                self.max_search_space = self.open_nodes.qsize()
            current = self.open_nodes.get() # get lowest f score node

            if current.puzzle_arr == self.goal: # found solution, get the path
                return self.traceToParent(current)
            
            self.closed_nodes.append(current)
            for child in self.expand(current):
                self.path_track[child] = current # track the path for use later
                # **** IMPORTANT: Check children for goal state before adding to queue ****
                if child.puzzle_arr == self.goal: 
                    return self.traceToParent(child)
                self.open_nodes.put(child) # add the new children to the queue
            
            self.expanded += 1 # increase in expanded counter

class Main:
    
    med_start    = [3,6,4,
                    0,1,2,
                    8,7,5]


    medium_goal  = [1,2,3,
                    8,0,4,
                    7,6,5]

    hard_start   = [8,0,6,
                    5,4,7,
                    2,3,1]
    
    hard_goal    = [0,1,2,
                    3,4,5,
                    6,7,8]
    menu_choice = 0
    startArr = []
    goalArr = []
    #goalArr = [1,2,3,4,5,6,7,8,0]
    while menu_choice != 'q':
        menu_choice = 0
        if len(startArr) < 9:
            print("Enter the values for tiles of your start array, pressing enter between each number (0 for blank):")
            while len(startArr) < 9:
                tmp = input(">> ")
                
                try:
                    tmpNum = int(tmp)
                    if tmpNum in startArr:
                        print("Number has already been entered into the start array. Enter another number.")
                    elif tmpNum not in range(0,9):
                        print("Number should be between 0 and 8. Enter another number.")
                    else:
                        startArr.append(tmpNum)
                        print ("\t",startArr[:3], "\n\t", startArr[3:6], "\n\t", startArr[6:])
                except ValueError:
                    print("Not a number. Try again.")
            
            print ("Your start array is the following:")
            print ("\t",startArr[:3], "\n\t", startArr[3:6], "\n\t", startArr[6:])

        if len(goalArr) < 9:
            print("Enter the values to build your goal array. Press enter between each value.")
            while len(goalArr) < 9:
                tmp = input(">> ")
                try:
                    tmpNum = int(tmp)
                    if tmpNum in goalArr:
                        print("Number has already been entered into goal array.")
                    elif tmpNum not in range(0,9):
                        print("Number should be between 0 and 8. Enter another number.")
                    else:
                        goalArr.append(tmpNum)
                        print("\t", goalArr[:3], "\n\t", goalArr[3:6], "\n\t", goalArr[6:])
                except ValueError:
                    print("Not a number. Try again.")
        

        print("Your arrays are the following:\nSTART:\t", startArr[:3], "\n\t", startArr[3:6], "\n\t", startArr[6:])    
        print("\nGOAL:\t", goalArr[:3], "\n\t", goalArr[3:6], "\n\t", goalArr[6:])

        searchAlgs = ["Breadth First Search", "Misplaced Tiles A* Search", "Manhattan Distance A* Search","Gaschnig A* Search"]
        print()

        for val in searchAlgs:
            print(searchAlgs.index(val), "\t", val)
        
        print("\nEnter the number corresponding to which search technique to use above:")
        validNum = 99
        
        while validNum not in range(0,4):
            tmp = input(">> ")
            try:
                tmpNum = int(tmp)
                if tmpNum in range(0,4):
                    validNum = tmpNum
            except ValueError:
                print("Try again.")
            
        
        
        
        cases = [(startArr, goalArr)]
        
        for start_state, goal_state in cases:
            start = time.time()
            val = searchAlgs[validNum]
            #for val in searchAlgs:
            print("\nTesting", val, "...")
            solver = PuzzleSolver(start = start_state, goal=goal_state, h_func = searchAlgs.index(val))
            solver.solve()
            end = time.time()
            print("\tSolution found in:", end - start, "seconds")
            print()
        
        control = ['n', 's', 'q']
        while menu_choice not in control:
            print("Please select from the following options, enter to confirm:")
            print()
            print(" Option | Description                               ")
            print("----------------------------------------------------")
            print("   N    | Input (N)ew arrays for search             ")
            print("   S    | Select new (S)earch algorithm, same arrays")
            print("   Q    | (Q)uit the program                        ")
            print()
            menu_choice = input(">> ")[0].lower()
        
        if menu_choice == 'n':
            startArr = []
            goalArr = []



        
        
        

    
    
    # easy_start   = [1,2,3,
    #                 4,8,5,
    #                 7,0,6]

   ##   medium_start = [3,6,4,
    #                 0,1,2,
    #                 8,7,5]
    # 
    # hard_start   = [8,0,6,
    #                 5,4,7,
    #                 2,3,1]
    # 
    # g26_start    = [7,2,4,
    #                 5,0,6,
    #                 8,3,1]

   ##   br_goal      = [1,2,3,
    #                 4,5,6,
    #                 7,8,0]

   ##   medium_goal  = [1,2,3,
    #                 8,0,4,
    #                 7,6,5]

   ##   tl_goal      = [0,1,2,
    #                 3,4,5,
    #                 6,7,8]
    # 
    # unsolvable   = [1,2,3,
    #                 4,5,6,
    #                 8,7,0]
    # 
    # test_cases = [(g26_start, tl_goal)]
    # 
    # for start_state, goal_state in test_cases:

   ##       print("\nTesting Breadth First Search...\n")
    #     solver = PuzzleSolver(start = start_state, goal = goal_state)
    #     solver.solve()

   ##       print("\nTesting Misplaced Tiles A* Search...\n")
    #     solver = PuzzleSolver(start = start_state, goal = goal_state, h_func = "misplaced")
    #     solver.solve() 

   ##       print("\nTesting Manhattan Distance A* Search...\n")
    #     solver = PuzzleSolver(start = start_state, goal = goal_state, h_func = "manhattan")
    #     solver.solve()

   ##       print("\nTesting Gaschnig A* Search...\n")
    #     solver = PuzzleSolver(start = start_state, goal = goal_state, h_func = "gaschnig")
    #     solver.solve()

