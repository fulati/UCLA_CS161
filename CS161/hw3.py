##############
# Homework 3 #
##############


###################
# Read This First #
###################


# All functions that you need to modify are marked with 'EXERCISE' in their header comments.
# Do not modify astar.py
# This file also contains many helper functions. You may call any of them in your functions.


# Due to the memory limitation, the A* algorithm may crash on some hard sokoban problems if too many
# nodes are generated. Improving the quality of the heuristic will mitigate
# this problem, as it will allow A* to solve hard problems with fewer node expansions.


# Remember that most functions are not graded on efficiency (only correctness).
# Efficiency can only influence your heuristic performance in the competition (which will affect your score).


# Load the astar.py and do not modify it.
import astar
# Load the numpy package and the state is represented as a numpy array during this homework.
import numpy as np


# a_star perform the A* algorithm with the start_state (numpy array), goal_test (function), successors (function) and
# heuristic (function). a_star prints the solution from start_state to goal_state (path), calculates the number of
# generated nodes (node_generated) and expanded nodes (node_expanded), and the solution depth (len(path)-1). a_star
# also provides the following functions for printing states and moves: prettyMoves(path): Translate the solution to a
# list of moves printlists(path): Visualize the solution and Print a list of states
def a_star(start_state, goal_test, successors, heuristic):
    goal_node, node_generated, node_expanded = astar.a_star_search(start_state, goal_test, successors, heuristic)
    if goal_node:
        node = goal_node
        path = [node.state1]
        while node.parent:
            node = node.parent
            path.append(node.state1)
        path.reverse()

        # print('My path:{}'.format(path))
        # print(prettyMoves(path))
        # printlists(path)
        print('Nodes Generated by A*: {}'.format(node_generated))
        print('Nodes Expanded by A*: {}'.format(node_expanded))
        print('Solution Depth: {}'.format(len(path) - 1))
    else:
        print('no solution found')


# A shortcut function
# Transform the input state to numpy array. For other functions, the state s is presented as a numpy array.
# Goal-test and next-states stay the same throughout the assignment
# You can just call sokoban(init-state, heuristic function) to test the result
def sokoban(s, h):
    return a_star(np.array(s), goal_test, next_states, h)


# Define some global variables
blank = 0
wall = 1
box = 2
keeper = 3
star = 4
boxstar = 5
keeperstar = 6


# Some helper functions for checking the content of a square
def isBlank(v):
    return (v == blank)


def isWall(v):
    return (v == wall)


def isBox(v):
    return (v == box)


def isKeeper(v):
    return (v == keeper)


def isStar(v):
    return (v == star)


def isBoxstar(v):
    return (v == boxstar)


def isKeeperstar(v):
    return (v == keeperstar)


# Help function for get KeeperPosition
# Given state s (numpy array), return the position of the keeper by row, col
# The top row is the zeroth row
# The first (right) column is the zeroth column
def getKeeperPosition(s):
    row = s.shape[0]
    col = s.shape[1]
    for i in range(row):
        for j in range(col):
            if (isKeeper(s[i, j]) or isKeeperstar(s[i, j])):
                return i, j


# For input list s_list, remove all None element
# For example, if s_list = [1, 2, None, 3], returns [1, 2, 3]
def cleanUpList(s_list):
    clean = []
    for state in s_list:
        if state is not None:
            clean.append(state)
    return clean


# EXERCISE: Modify this function to return Ture
# if and only if s (numpy array) is a goal state of a Sokoban game.
# (no box is on a non-goal square)
# Remember, the number of goal can be larger than the number of box.
def goal_test(s):
    # The goal_test function takes an input of s (numpy array), and returns a boolean value of True or False 
    # This function loops through the entire Sokoban board and checks if we come across a box 
    # If we do come across a box that is not in a goal square, then we return False, else we return True
    row = s.shape[0]
    col = s.shape[1]
    for i in range(row):
        for j in range(col):
            if s[i,j] == box: 
                return False
    return True


# EXERCISE: Modify this function to return the list of
# successor states of s (numpy array).
#
# This is the top-level next-states (successor) function.
# Some skeleton code is provided below.
# You may delete them totally, depending on your approach.
# 
# If you want to use it, you will need to set 'result' to be 
# the set of states after moving the keeper in each of the 4 directions.
#
# You can define the function try-move and decide how to represent UP,DOWN,LEFT,RIGHT.
# Any None result in the list can be removed by cleanUpList.
#
# When generated the successors states, you may need to copy the current state s (numpy array).
# A shallow copy (e.g, direcly set s1 = s) constructs a new compound object and then inserts references 
# into it to the objects found in the original. In this case, any change in the numpy array s1 will also affect
# the original array s. Thus, you may need a deep copy (e.g, s1 = np.copy(s)) to construct an indepedent array.


def get_square(S, r, c):
    # The get_square function takes in inputs state S, row number r, and column number c, then it returns the integer content of state S at square (r, c)
    # It first checks and makes sure r and c values are within the valid range, if it is, then it returns the integer content of state S at square (r, c)
    # If not, then it returns the value of the wall
    if r >= 0 and r < S.shape[0] and c >= 0 and c < S.shape[1]:
        return S[r,c]
    return wall

def isValidKeeperMove(v): 
    # The isValidKeeperMove function takes in a value v for the square content, and returns boolean value of True or False
    # This function checks if the given value at the square is either blank or is a star, if it is either, then it returns True
    # If it is neither, then returns False
    return isBlank(v) or isStar(v)

def move_keeper_only(S, old_r, old_c, new_r, new_c, new_v):
    # The move_keeper_only function takes inputs state S, old keeper row -> old_r, old keeper column -> old_c, new keeper row -> new_r, 
    # new keeper col -> new_c, and value of goal square. Then it returns new_S with the updated square values after the move. 
    # First it creates a deep copy of the current state S. 
    # Then it clears the current position of the keeper in order to move to next
    # After clearing current position of the keeper, it then moves the keeper to its goal square and changes the values at the new square based on wether its keeper or keeperstar.  
    new_S = np.copy(S)

    # Clear the old keeper position
    if isKeeperstar(S[old_r, old_c]):
        new_S[old_r, old_c] = star
    else: 
        new_S[old_r, old_c] = blank

    # Move the keeper
    if isStar(new_v) or isBoxstar(new_v):
        new_S[new_r, new_c] = keeperstar
    else: 
        new_S[new_r, new_c] = keeper

    return new_S

def isValidBoxMove(box_v, goal_v):
    # The isValidBoxMove function takes in a value box_v for the current box square content and goal_v for the goal box square content, and returns boolean value of True or False
    # First it checks if the given value at the current box square is either box or is a Boxstar, if it is either, then it returns True. If it is neither, then returns False
    # Then it checks if the given value at the goal box square is either blank or is a star, if it is either, then it returns True. If it is neither, then returns False
    # Finally, it combines the result of the two checks and returns True if both are true, else returns False if either of them is false. 
    return (isBox(box_v) or isBoxstar(box_v)) and (isBlank(goal_v) or isStar(goal_v))

def move_keeper_and_box(S, keeper_r, keeper_c, box_r, box_c, box_goal_r, box_goal_c, new_box_v):
    # The move_keeper_and_box function takes inputs state S, keeper row -> keeper_r, keeper column -> keeper_c, box row -> box_r, box col -> box_c 
    # goal box row -> box_goal_r, goal box col -> box_goal_c, and value of goal box square. Then it returns new_S with the updated square values after the move. 
    # First it creates a deep copy of the current state S. 
    # Then it calls the move_keeper_only function to clear and move the keeper first.
    # Then it then moves the box to its goal square and changes the values at the new square based on wether its box or boxstar.  
    new_S = np.copy(S)

    # Clear the old keeper position and move the keeper
    new_S = move_keeper_only(new_S, keeper_r, keeper_c, box_r, box_c, S[box_r, box_c])

    # Move the box 
    if isStar(new_box_v):
        new_S[box_goal_r, box_goal_c] = boxstar
    else:
        new_S[box_goal_r, box_goal_c] = box
    
    return new_S


def try_move(S, D):
    # The try_move function takes input state S and direction D, then returns either the new State if the move is valid or None if the move is invalid
    # First we assign variables to the current keeper position, next keeper position, next box location, next keeper position's square value, next box position's square value
    # then we check if we are moving only the keeper or both keeper and the box, and based on each result, we call the corresponding function. 
    # if there is no valid move, then we return None
    keeper_r, keeper_c = getKeeperPosition(S)

    next_keeper_r, next_keeper_c = keeper_r + D[0], keeper_c + D[1]
    next_box_r, next_box_c = keeper_r + (D[0] * 2), keeper_c + (D[1] * 2)

    next_square_value = get_square(S, next_keeper_r, next_keeper_c)
    next_box_square_value = get_square(S, next_box_r, next_box_c)

    # Only keeper move
    if isValidKeeperMove(next_square_value):
        return move_keeper_only(S, keeper_r, keeper_c, next_keeper_r, next_keeper_c, next_square_value)

    # Keeper and box move
    elif isValidBoxMove(next_square_value, next_box_square_value):
        return move_keeper_and_box(S, keeper_r, keeper_c, next_keeper_r, next_keeper_c, next_box_r, next_box_c, next_box_square_value)

    # Move is invalid
    else: 
        return None

def next_states(s):
    # The next_states function takes input state S, and returns the cleaned up state without None values of the list of next states
    # First we have an empty list to store the result states and directions for up, down, left, right
    # Then we loop through each direction and append the list of possible moves into the result list
    s_list = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # up, down, left, right

    for d in directions:
        s_list.append(try_move(s, d))   

    return cleanUpList(s_list)


# EXERCISE: Modify this function to compute the trivial
# admissible heuristic.
def h0(s):
    # Just returns the constant 0 for trivial admissible heuristic
    return 0

# EXERCISE: Modify this function to compute the
# number of misplaced boxes in state s (numpy array).
def h1(s):
    # Goes through the each row and col in the state and finds the number of boxes that aren't in a goal yet, then returns that number
    count_box = 0
    row = s.shape[0]
    col = s.shape[1]
    for i in range(row):
        for j in range(col):
            if s[i,j] == box: 
                count_box += 1
    return count_box

# EXERCISE: Is this heuristic admissible? Return true if yes, false if no. Explain your reasoning
# as comments in this function.
def h1_admissible():
    #h1 is admissable because it returns the number of boxes that are not on goal position
    #It never overestimates the cost, since each box must be moved at least once
    return True


# EXERCISE: 
# This function will be tested in various hard examples.
# Objective: make A* solve problems as fast as possible.
def h2(s):
    # The h2 heuristic function takes input state S, and returns minimum sum distance sum_dist. 
    # I tried following the pattern of h0 -> h1, and what came to my mind for next step was that since h1 was assuming next step of each box was the goal,
    # so I thought that for h2, we could calculate the distance between the box and the goal, without considering the wall in between. And I came up with 
    # calculating the minimum Manhattan distance between each individual box and any goal that is closest to the box. Then storing results of each box and adding for total distance. 

    # First we have list to store all the box location and the goal locations
    # Then we loop through the row and col and append each box location and the goal locations to corresponding lists
    # Then we loop through each individual box in the box list and have a condition to check if any box is stuck in a corner, where if it is, then it is impossible to solve
    # Within the inner loop, we loop through the goal in the goal list, and get the manhattan distance 
    # from the box to the goal (without acknowledging the walls), and we try to get the minimum distance for that specific box to one of the goals
    # after we get the minimum distance from each box to one of the goals, we add those distances and return the sum of the distances. 
    box_list = []
    goal_list = []

    row = s.shape[0]
    col = s.shape[1]
    for i in range(row):
        for j in range(col):
            if s[i,j] == box: 
                box_list.append((i,j))
            elif s[i,j] == star or s[i, j] == boxstar: 
                goal_list.append((i,j))

    sum_dist = 0
    # loop through each box to find closest goal using Manhattan distance
    for box_position in box_list: 
        
        # Check for corner boxes, where the boxes are stuck unless its already in a goal
        if box_position not in goal_list:
            if (
                # Top-left
                ((box_position[0] > 0 and box_position[1] > 0) and 
                 (s[box_position[0]-1, box_position[1]] == wall and s[box_position[0], box_position[1]-1] == wall)) or
                # Top-right
                ((box_position[0] > 0 and box_position[1] < col-1) and
                 (s[box_position[0]-1, box_position[1]] == wall and s[box_position[0], box_position[1]+1] == wall)) or
                # Bottom-left
                (box_position[0] < row-1 and box_position[1] > 0 and
                 (s[box_position[0]+1, box_position[1]] == wall and s[box_position[0], box_position[1]-1] == wall)) or
                # Bottom-right
                ((box_position[0] < row-1 and box_position[1] < col-1) and
                 (s[box_position[0]+1, box_position[1]] == wall and s[box_position[0], box_position[1]+1] == wall))
            ):
                return float('inf')

        min_dist = float('inf')
        for goal in goal_list: 
            manhattan_dist = abs(box_position[0] - goal[0]) + abs(box_position[1] - goal[1])

            min_dist = min(min_dist, manhattan_dist)
        
        sum_dist += min_dist
    
    return sum_dist


# Some predefined problems with initial state s (array). Sokoban function will automatically transform it to numpy
# array. For other function, the state s is presented as a numpy array. You can just call sokoban(init-state,
# heuristic function) to test the result Each problem can be visualized by calling prettyMoves(path) and printlists(
# path) in a_star function
#
# Problems are roughly ordered by their difficulties.
# For most problems, we also provide 2 additional number per problem:
#    1) # of nodes expanded by A* using our next-states and h0 heuristic.
#    2) the depth of the optimal solution.
# These numbers are located at the comments of the problems. For example, the first problem below 
# was solved by 80 nodes expansion of A* and its optimal solution depth is 7.
# 
# Your implementation may not result in the same number of nodes expanded, but it should probably
# give something in the same ballpark. As for the solution depth, any admissible heuristic must 
# make A* return an optimal solution. So, the depths of the optimal solutions provided could be used
# for checking whether your heuristic is admissible.
#
# Warning: some problems toward the end are quite hard and could be impossible to solve without a good heuristic!


# [80,7]
s1 = [[1, 1, 1, 1, 1, 1],
      [1, 0, 3, 0, 0, 1],
      [1, 0, 2, 0, 0, 1],
      [1, 1, 0, 1, 1, 1],
      [1, 0, 0, 0, 0, 1],
      [1, 0, 0, 0, 4, 1],
      [1, 1, 1, 1, 1, 1]]

# [110,10],
s2 = [[1, 1, 1, 1, 1, 1, 1],
      [1, 0, 0, 0, 0, 0, 1],
      [1, 0, 0, 0, 0, 0, 1],
      [1, 0, 0, 2, 1, 4, 1],
      [1, 3, 0, 0, 1, 0, 1],
      [1, 1, 1, 1, 1, 1, 1]]

# [211,12],
s3 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 0, 0, 0, 1, 0, 0, 0, 1],
      [1, 0, 0, 0, 2, 0, 3, 4, 1],
      [1, 0, 0, 0, 1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1, 1, 1, 1, 1]]

# [300,13],
s4 = [[1, 1, 1, 1, 1, 1, 1],
      [0, 0, 0, 0, 0, 1, 4],
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 1, 1, 1, 0, 0],
      [0, 0, 1, 0, 0, 0, 0],
      [0, 2, 1, 0, 0, 0, 0],
      [0, 3, 1, 0, 0, 0, 0]]

# [551,10],
s5 = [[1, 1, 1, 1, 1, 1],
      [1, 1, 0, 0, 1, 1],
      [1, 0, 0, 0, 0, 1],
      [1, 4, 2, 2, 4, 1],
      [1, 0, 0, 0, 0, 1],
      [1, 1, 3, 1, 1, 1],
      [1, 1, 1, 1, 1, 1]]

# [722,12],
s6 = [[1, 1, 1, 1, 1, 1, 1, 1],
      [1, 0, 0, 0, 0, 0, 4, 1],
      [1, 0, 0, 0, 2, 2, 3, 1],
      [1, 0, 0, 1, 0, 0, 4, 1],
      [1, 1, 1, 1, 1, 1, 1, 1]]

# [1738,50],
s7 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [0, 0, 1, 1, 1, 1, 0, 0, 0, 3],
      [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
      [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
      [0, 2, 1, 0, 0, 0, 0, 0, 1, 0],
      [0, 0, 1, 0, 0, 0, 0, 0, 1, 4]]

# [1763,22],
s8 = [[1, 1, 1, 1, 1, 1],
      [1, 4, 0, 0, 4, 1],
      [1, 0, 2, 2, 0, 1],
      [1, 2, 0, 1, 0, 1],
      [1, 3, 0, 0, 4, 1],
      [1, 1, 1, 1, 1, 1]]

# [1806,41],
s9 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 0, 0, 1, 1, 1, 1],
      [1, 0, 0, 0, 0, 0, 2, 0, 1],
      [1, 0, 1, 0, 0, 1, 2, 0, 1],
      [1, 0, 4, 0, 4, 1, 3, 0, 1],
      [1, 1, 1, 1, 1, 1, 1, 1, 1]]

# [10082,51],
s10 = [[1, 1, 1, 1, 1, 0, 0],
       [1, 0, 0, 0, 1, 1, 0],
       [1, 3, 2, 0, 0, 1, 1],
       [1, 1, 0, 2, 0, 0, 1],
       [0, 1, 1, 0, 2, 0, 1],
       [0, 0, 1, 1, 0, 0, 1],
       [0, 0, 0, 1, 1, 4, 1],
       [0, 0, 0, 0, 1, 4, 1],
       [0, 0, 0, 0, 1, 4, 1],
       [0, 0, 0, 0, 1, 1, 1]]

# [16517,48],
s11 = [[1, 1, 1, 1, 1, 1, 1],
       [1, 4, 0, 0, 0, 4, 1],
       [1, 0, 2, 2, 1, 0, 1],
       [1, 0, 2, 0, 1, 3, 1],
       [1, 1, 2, 0, 1, 0, 1],
       [1, 4, 0, 0, 4, 0, 1],
       [1, 1, 1, 1, 1, 1, 1]]

# [22035,38],
s12 = [[0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
       [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
       [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
       [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 1, 0, 1, 4, 0, 4, 1],
       [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]]

# [26905,28],
s13 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 4, 0, 0, 0, 0, 0, 2, 0, 1],
       [1, 0, 2, 0, 0, 0, 0, 0, 4, 1],
       [1, 0, 3, 0, 0, 0, 0, 0, 2, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 4, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# [41715,53],
s14 = [[0, 0, 1, 0, 0, 0, 0],
       [0, 2, 1, 4, 0, 0, 0],
       [0, 2, 0, 4, 0, 0, 0],
       [3, 2, 1, 1, 1, 0, 0],
       [0, 0, 1, 4, 0, 0, 0]]

# [48695,44],
s15 = [[1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 2, 2, 0, 1],
       [1, 0, 2, 0, 2, 3, 1],
       [1, 4, 4, 1, 1, 1, 1],
       [1, 4, 4, 1, 0, 0, 0],
       [1, 1, 1, 1, 0, 0, 0]]

# [91344,111],
s16 = [[1, 1, 1, 1, 1, 0, 0, 0],
       [1, 0, 0, 0, 1, 0, 0, 0],
       [1, 2, 1, 0, 1, 1, 1, 1],
       [1, 4, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 5, 0, 5, 0, 1],
       [1, 0, 5, 0, 1, 0, 1, 1],
       [1, 1, 1, 0, 3, 0, 1, 0],
       [0, 0, 1, 1, 1, 1, 1, 0]]

# [3301278,76],
# Warning: This problem is very hard and could be impossible to solve without a good heuristic!
s17 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 3, 0, 0, 1, 0, 0, 0, 4, 1],
       [1, 0, 2, 0, 2, 0, 0, 4, 4, 1],
       [1, 0, 2, 2, 2, 1, 1, 4, 4, 1],
       [1, 0, 0, 0, 0, 1, 1, 4, 4, 1],
       [1, 1, 1, 1, 1, 1, 0, 0, 0, 0]]

# [??,25],
s18 = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 4, 1, 0, 0, 0, 0]]

# [??,21],
s19 = [[0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 4],
       [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
       [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 2, 0, 4, 1, 0, 0, 0]]


# Utility functions for printing states and moves.
# You do not need to understand any of the functions below this point.


# Helper function of prettyMoves
# Detect the move from state s --> s1
def detectDiff(s, s1):
    row, col = getKeeperPosition(s)
    row1, col1 = getKeeperPosition(s1)
    if (row1 == row + 1):
        return 'Down'
    if (row1 == row - 1):
        return 'Up'
    if (col1 == col + 1):
        return 'Right'
    if (col1 == col - 1):
        return 'Left'
    return 'fail'


# Translates a list of states into a list of moves
def prettyMoves(lists):
    initial = 0
    action = []
    for states in (lists):
        if (initial != 0):
            action.append(detectDiff(previous, states))
        initial = 1
        previous = states
    return action


# Print the content of the square to stdout.
def printsquare(v):
    if (v == blank):
        print(' ', end='')
    if (v == wall):
        print('#', end='')
    if (v == box):
        print('$', end='')
    if (v == keeper):
        print('@', end='')
    if (v == star):
        print('.', end='')
    if (v == boxstar):
        print('*', end='')
    if (v == keeperstar):
        print('+', end='')


# Print a state
def printstate(s):
    row = s.shape[0]
    col = s.shape[1]
    for i in range(row):
        for j in range(col):
            printsquare(s[i, j])
        print('\n')


# Print a list of states with delay.
def printlists(lists):
    for states in (lists):
        printstate(states)
        print('\n')


if __name__ == "__main__":
    sokoban(s1, h0)

    sokoban(s2, h0)

    sokoban(s3, h0)
    
    sokoban(s4, h0)
