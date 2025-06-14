# 1. The function BFS(TREE) takes a tree called TREE as the input and returns a tuple of leaf nodes. 
# This BFS function goes through a left-to-right breadth-first search using a queue, and stores leaf nodes in list called leafs.
# It first checks if the TREE is empty, then returns empty tuple if it is.
# It then loop through the queue, which goes through the TREE starting at the root node. 
# It then appends curr to the leafs list, if curr is a leaf nodes which are strings. If curr is not leaf node and is a tuple, then it is appends the notes in the tuple to the queue. 
# In the end, it returns the tuple of all the leaf nodes in the order they are visited. 
def BFS(TREE): 
    if not TREE:
        return ()

    queue = [TREE]
    leafs = []

    while queue: 

        curr = queue.pop(0)
        
        if type(curr) == str:
            leafs.append(curr)
        else: 
            for node in curr: 
                queue.append(node)
    
    return tuple(leafs)


# 2. The function DFS(TREE) takes a tree called TREE as the input and returns a tuple of leaf nodes. 
# This DFS function recursively goes through a left-to-right depth-first search, and stores leaf nodes in tuple called leafs.
# It first checks if the TREE is empty, then returns empty tuple if it is.
# It then checks if TREE is a leaf node (str), if it is, then returns that leaf node as a tuple. 
# Otherwise, it goes through each subTREE in TREE, and recursively calls DFS on the subTREE while adding it to the leafs tuple
# In the end, it returns the tuple of all the leaf nodes in the order they are visited. 
def DFS(TREE): 
    if not TREE:
        return ()

    if type(TREE) == str:
        return tuple([TREE])

    leafs = ()
    for subTREE in TREE:
        leafs += DFS(subTREE)
    
    return leafs


# 3. 
# The function Depth_Limited_Search(TREE, depth) takes a tree and an integer depth as the two inputs, then returns a tuple of leaf nodes visited in right-to-left order. 
# This Depth_Limited_Search function recursively goes through a right-to-left depth-limited search, and stores leaf nodes in tuple called leafs. 
# It first checks if the depth is less than 0, where it returns empty tuple. 
# It then checks if TREE is a leaf node (str), where it returns that leaf node as a tuple. 
# Otherwise, it goes through each subTREE in TREE, and recursively calls Depth_Limited_Search with depth - 1 argument on the subTREE while adding it to the leafs tuple
# In the end, it returns the tuple of all the leaf nodes in the order they are visited. 
def Depth_Limited_Search(TREE, depth): 
    if depth < 0: 
        return ()

    if type(TREE) == str:
        return tuple([TREE])

    leafs = ()
    for subTREE in reversed(TREE):
        leafs += Depth_Limited_Search(subTREE, depth -1)
    
    return leafs

# The function DFID(TREE, D) takes a tree called TREE and an integer D as the two inputs, then returns a tuple of leaf nodes visited in right-to-left order. 
# This DFID function goes through a right-to-left depth-first iterative-deepening search, and stores leaf nodes in tuple called leafs.
# It loops through the depth from 0 to D and runs the Depth_Limited_Search function on each depth levle while adding the leaf nodes to the leafs tuple. 
# In the end, it returns the tuple of all the leaf nodes in the order they are visited. 
def DFID(TREE, D):
    leafs = ()
    for depth in range(D+1):
        leafs += Depth_Limited_Search(TREE, depth)
    
    return leafs


# 4. ----------------------------------------------------------------------------

# These functions implement a depth-first solver for the homer-baby-dog-poison
# problem. In this implementation, a state is represented by a single tuple
# (homer, baby, dog, poison), where each variable is True if the respective entity is
# on the west side of the river, and False if it is on the east side.
# Thus, the initial state for this problem is (False False False False) (everybody
# is on the east side) and the goal state is (True True True True).

# The main entry point for this solver is the function DFS_SOL, which is called
# with (a) the state to search from and (b) the path to this state. It returns
# the complete path from the initial state to the goal state: this path is a
# list of intermediate problem states. The first element of the path is the
# initial state and the last element is the goal state. Each intermediate state
# is the state that results from applying the appropriate operator to the
# preceding state. If there is no solution, DFS_SOL returns [].
# To call DFS_SOL to solve the original problem, one would call
# DFS_SOL((False, False, False, False), [])
# However, it should be possible to call DFS_SOL with any intermediate state (S)
# and the path from the initial state to S (PATH).

# First, we define the helper functions of DFS_SOL.

# FINAL_STATE takes a single argument S, the current state, and returns True if it
# is the goal state (True, True, True, True) and False otherwise.
def FINAL_STATE(S):  # This function checks if the input S is equal to (True, True, True, True), where if it is, then it returns True. Otherwise, it returns false.
    if S == (True, True, True, True): 
        return True
    else: 
        return False


# NEXT_STATE returns the state that results from applying an operator to the
# current state. It takes two arguments: the current state (S), and which entity
# to move (A, equal to "h" for homer only, "b" for homer with baby, "d" for homer
# with dog, and "p" for homer with poison).
# It returns a list containing the state that results from that move.
# If applying this operator results in an invalid state (because the dog and baby,
# or poisoin and baby are left unsupervised on one side of the river), or when the
# action is impossible (homer is not on the same side as the entity) it returns [].
# NOTE that NEXT_STATE returns a list containing the successor state (which is
# itself a tuple)# the return should look something like [(False, False, True, True)].
def NEXT_STATE(S, A):  # This function assign each entity with their corresponding values from S, then checks if the move A is valid and safe. Return the next state if valid, else return []
    h, b, d, p = S  

    if A == "h": 
        h = not h   

    elif A == "b" and h == b:
        h = not h
        b = not b

    elif A == "d" and h == d:
        h = not h
        d = not d

    elif A == "p" and h == p:
        h = not h
        p = not p

    else: 
        return []

    if (d == b and h != b) or (p == b and h != b): #if invalid state, then return []
        return []

    return [(h, b, d, p)] 


# SUCC_FN returns all of the possible legal successor states to the current
# state. It takes a single argument (S), which encodes the current state, and
# returns a list of each state that can be reached by applying legal operators
# to the current state.
def SUCC_FN(S):  # This function applies each legal move and returns all valid successor states from the current state S
    successor_states = []
    legal_operators = ["h", "b", "d", "p"]

    for A in legal_operators: 
        new_S = NEXT_STATE(S, A)
        if new_S != []:   # Use the NEXT_STATE returned value to check if the resulting state is valid and safe
            successor_states += new_S

    return successor_states


# ON_PATH checks whether the current state is on the stack of states visited by
# this depth-first search. It takes two arguments: the current state (S) and the
# stack of states visited by DFS (STATES). It returns True if S is a member of
# STATES and False otherwise.
def ON_PATH(S, STATES):  # This function check if S is already in STATES
    if S in STATES: 
        return True
    else: 
        return False


# MULT_DFS is a helper function for DFS_SOL. It takes two arguments: a list of
# states from the initial state to the current state (PATH), and the legal
# successor states to the last, current state in the PATH (STATES). PATH is a
# first-in first-out list of states# that is, the first element is the initial
# state for the current search and the last element is the most recent state
# explored. MULT_DFS does a depth-first search on each element of STATES in
# turn. If any of those searches reaches the final state, MULT_DFS returns the
# complete path from the initial state to the goal state. Otherwise, it returns
# [].
def MULT_DFS(STATES, PATH): # This function recursively looks through the successor states using depth-first search for a complete path
    for S in STATES: 
        if FINAL_STATE(S): # Check if S is already the goal state
            return PATH + [S]
        
        successors = SUCC_FN(S) # valid successors
        extended_path = PATH + [S] # Add current state to the PATH
        next_states = [] # Unvisited successor states

        for succ in successors: # Loop through the valid successor states
            if ON_PATH(succ, extended_path): # Check if succ has already been visited
                continue
            next_states.append(succ)
        
        complete_path = MULT_DFS(next_states, extended_path) # Recursively call MULT_DFS to look through the next_states 
        if complete_path != []: 
            return complete_path
    
    return []


# DFS_SOL does a depth first search from a given state to the goal state. It
# takes two arguments: a state (S) and the path from the initial state to S
# (PATH). If S is the initial state in our search, PATH is set to []. DFS_SOL
# performs a depth-first search starting at the given state. It returns the path
# from the initial state to the goal state, if any, or [] otherwise. DFS_SOL is
# responsible for checking if S is already the goal state, as well as for
# ensuring that the depth-first search does not revisit a node already on the
# search path (i.e., S is not on PATH).
def DFS_SOL(S, PATH): # This function performs depth-first search from state S, returns a path to goal if one exists. 
    if FINAL_STATE(S): # Check if S is already the goal state
        return PATH + [S]
    
    if ON_PATH(S, PATH): # Check if S was already visited before
        return []
    
    successors = SUCC_FN(S) # valid successors
    extended_path = PATH + [S] # The path plus the current state
    
    return MULT_DFS(successors, extended_path)




