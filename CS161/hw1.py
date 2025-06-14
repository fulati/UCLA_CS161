# 1. The function PAD(N) takes an integer N as input and returns the Nth Padovan number.
# The PAD function is a recursive function, where the base cases is if the N is less than or equal to 2 (N <= 2), it will return 1. 
# If N is greater than 2, it will return the sum of the Padovan numbers at positions N-2 and N-3.
def PAD(N):
    if N <= 2:
        return 1
    
    return PAD(N-2) + PAD(N-3)


# 2. The function SUMS(N) takes an integer N as input and returns the number of additions required by the PAD function above to compute the Nth Padovan number.
# The SUM function is a recursive function, where the base case is if the N is less than or equal to 2 (N <= 2), it will return 0 as it doesn't require any additions.
# If N is greater than 2, it will return the sum of the number of additions required to compute the Padovan numbers at positions N-2 and N-3, plus 1 for the current addition.
def SUMS(N): 
    if N <= 2:
        return 0
    
    return SUMS(N-2) + SUMS(N-3) + 1


# 3. The function ANON(TREE) takes a single argument TREE, and returns an anonymized tree with same structure but every leaf in tree is replaced by "?"
# The ANON function is a recursive function, where if the input TREE is a tuple, it will create a new list and loop through each subTree in the TREE, it will then call ANON function on each subTree and append the result to the new list.
# if the TREE is not a tuple, it will return "?" as the base case. In the end it will return a tuple of the new list with "?" replacing the leaves.
def ANON(TREE):
    if type(TREE) is tuple: 
        newTREE = []
        for subTree in TREE:
            newTREE.append(ANON(subTree))
        return tuple(newTREE)
    else: 
        return "?"
    

# 4. The function TREE_HEIGHT(TREE) takes a single argument TREE in tuples, and returns the height of the TREE.
# The TREE_HEIGHT function is a recursive function, where if the input TREE is a tuple, it will create a new list and loop through each subTree in the TREE, it will then call TREE_HEIGHT function on each subTree and append the result + 1 to the new list.
# If the TREE is not a tuple, it will return 0 as the base case. In the end it will return the maximum height of the tree.
def TREE_HEIGHT(TREE):
    if type(TREE) is tuple:
        height = []
        for subTree in TREE:
            height.append(TREE_HEIGHT(subTree) + 1)
        return max(height)
    else:
        return 0


# 5. The function TREE_ORDER(TREE) takes a single argument TREE in tuples, and returns a tuple that represents the postorder traversal of the numbers in TREE.
# The TREE_ORDER function is a recursive function, where if the input TREE is a tuple, it will take the L, m, R from the TREE and call the TREE_ORDER function on L and R, it will then return the result of L + R + (m,).
# If the TREE is not a tuple, it will return a tuple containing the TREE as the base case.
def TREE_ORDER(TREE):
    if type(TREE) is tuple:
        L, m, R = TREE
        return TREE_ORDER(L) + TREE_ORDER(R) + (m,)
    else:
        return (TREE,)


