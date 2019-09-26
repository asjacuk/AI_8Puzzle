#8 Puzzle Solver with Informed and Uninformed Search

Solving 8 Puzzle configurations using a combination of uninformed and informed search algorithms.
Uninformed search is performed with breadth first search to provide a brute force optimal solution path.
Informed search is performed with A* search algorithm with three different heuristics:
    * Misplaced Tiles
    * Manhattan Distance
    * Gaschnig's Heuristic
    
The program allows for interactive user input of start and goal states, selection of desired search algorithm,
and provides a robust output consisting of the solution path starting from the start state to the goal state,
the number of nodes expanded in search of the solution path, and the maximum size of the search space during 
the search.
