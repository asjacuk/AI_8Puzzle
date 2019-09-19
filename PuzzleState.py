class PuzzleState:


    def __init__(self, puzzle_arr = [], g = 0, h_func = 0, goal = [1,2,3,4,5,6,7,8,0]):

        self.puzzle_arr = puzzle_arr
        self.g = g
        self.h = self.__h_func(h_func, goal)
        self.f = self.g + self.h

    # mapping h_func strings to actual functions in PuzzleState class
    def __h_func(self, h_func, goal):
        if h_func == 0:
            return 0
        elif h_func == 1:
            return self.misplacedTiles(goal)
        elif h_func == 2:
            return self.manhattanDistance(goal)
        elif h_func == 3:
            return self.gaschnig(goal)
        else:
            print(h_func)
            return 0
        
            
        
        
        # if h_func == 'misplaced': 
        #     return self.misplacedTiles(goal)
        # elif h_func == 'manhattan': 
        #     return self.manhattanDistance(goal)
        # elif h_func == 'gaschnig': 
        #     return self.gaschnig(goal)
        # else:
        #     return 0
    
    """
    Overriding the comparison operators to allow Vertex class to be easily comparable
    using their f values for priority queue implememtation to be used during searches
    """
    # equality
    def __eq__(self, other):
        return self.puzzle_arr == other.puzzle_arr
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

    # overriding __str__ to provide print()-ability of puzzle states
    def __str__(self):
        row1 = str(self.puzzle_arr[0:3]) + "\th = " + str(self.h)
        row2 = str(self.puzzle_arr[3:6]) + "\tg = " + str(self.g)
        row3 = str(self.puzzle_arr[6:9]) + "\tf = h+g = " + str(self.f)
        message = "\n\t{r1}\n\t{r2}\n\t{r3}".format(r1 = row1, r2 = row2, r3 = row3)
        return message
    
    # overriding hashing behavior for use of class as a key in dict
    def __hash__(self):
        return hash(tuple(self.puzzle_arr))

    def getBlank(self):
        return self.puzzle_arr.index(0)






    """
    Heuristic Functions
    -------------------------------------------------------------------------------------------------
    These functions are intended to be used in order to calculate h(n) of a Vertex with h() being the 
    heuristic function selected for the search and n being any node processed during that search.
    The value of h(n) is used to determine the value of f(n) = g(n) + h(n) in order to identify which
    Vertex should be expanded next.
    -------------------------------------------------------------------------------------------------
    misplacedTiles - calculates the number of tiles that are in the incorrect position when compared
        to the goal positions and returns this value for further use
    
    manhattanDistance - calculates the Manhattan Distance of moves required to get the current state
        to the goal state and returns this value for further use

    gaschnig - calculates the Gaschnig value resulting from the number of moves needed to solve the
        puzzle from the current state to the goal state using the relaxed rules that any tile can be
        moved to the blank spot in a single move, regardless of other tiles, and returns this value
    """
    
    def misplacedTiles(self, goal):
        return sum(1 for i, j in zip(self.puzzle_arr, goal) if i != j)
            

    # calculates Manhattan Distance for puzzle according to passed in goal array
    def manhattanDistance(self, goal):
        manhattan = 0
        for i in range(len(self.puzzle_arr)):
            goal_index = goal.index(self.puzzle_arr[i])
            manhattan += ( abs((i // 3) - (goal_index // 3)) +  # calculate number of rows needed to move
                            abs((i % 3) - (goal_index % 3)) ) # calculate number of columns needed to move
        return manhattan

    # calculates Gaschnig's heuristic from current puzzle state to goal
    def gaschnig(self, goal):
        gaschnig = 0
        test_arr = self.puzzle_arr.copy()
        while test_arr != goal:
            blank_index = test_arr.index(0)
            if goal[blank_index] != 0: # blank not in goal position
                mismatch_index = test_arr.index(goal[blank_index])
                test_arr[blank_index] = goal[blank_index] # swap with correct tile
                test_arr[mismatch_index] = 0
                gaschnig += 1
            else: # blank in goal position
                for i in range(len(self.puzzle_arr)): # look for a mismatch
                    if test_arr[i] != goal[i]:
                        test_arr[blank_index] = test_arr[i]
                        test_arr[i] = 0
                        gaschnig += 1
                        break
        return gaschnig
    
        