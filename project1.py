import copy

searched_states = set()
# Each Node has at most 4 children 

#UCS here utilizes FIFO for nodes.
def ucs_queueing_func(nodes, children):
    for child in children:
        nodes.append(child)
    return nodes
def misplaced_tile(state):
    misplaced = 0
    proper_arrangement = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']]
    for i in range(len(state[0])):
        for j in range(len(state)):
            if state[i][j] != 0 and state[i][j] != proper_arrangement[i][j]:
                misplaced+=1
    
    return misplaced

            

def make_queue(init_state):
    q = []
    q.append(Node(init_state))
    return q

#Expand all of node's children
def expand(node, searched_states):
    # In this case we have a max of 4 children per 
    # node as the 0 can move left, right, up, and down
    children = []
    # First we must find where the 0 is located inside the 
    #Grid to see what moves are valid.

    row = 0
    column = 0
    for i in range(len(node.state[0])):
        for j in range(len(node.state)):
            if node.state[i][j] == '0':
                row = i 
                column = j 

    #Now we must perform all valid operations on 
    #the current state

    #Check to see if the space can move left, if so do it
    if column > 0:
        left_copy = copy.deepcopy(node.state)
        temp = left_copy[row][column-1]
        left_copy[row][column-1] = '0'
        left_copy[row][column] = temp
        #Check to see if this is a duplicate state, if so ignore
        if tuple(map(tuple, left_copy)) not in searched_states:
            children.append(Node(left_copy, node.depth+1))
            searched_states.add(tuple(map(tuple, left_copy)))
        
    #Check to see if the space can move right, if so do it
    if column < 2:
        right_copy = copy.deepcopy(node.state)
        temp = right_copy[row][column+1]
        right_copy[row][column+1] = '0'
        right_copy[row][column] = temp
         #Check to see if this is a duplicate state, if so ignore
        if tuple(map(tuple, right_copy)) not in searched_states:
            children.append(Node(right_copy, node.depth+1))
            searched_states.add(tuple(map(tuple, right_copy)))
    #Check to see if the space can move up, if so do it
    if row > 0:
        up_copy = copy.deepcopy(node.state)
        temp = up_copy[row-1][column]
        up_copy[row-1][column] = '0'
        up_copy[row][column] = temp
         #Check to see if this is a duplicate state, if so ignore
        if tuple(map(tuple, up_copy)) not in searched_states:
            children.append(Node(up_copy, node.depth+1))
            searched_states.add(tuple(map(tuple, up_copy)))

    
    #Check to see if the space can move down, if so do it
    if row < 2:
        down_copy = copy.deepcopy(node.state)
        temp = down_copy[row+1][column]
        down_copy[row+1][column] = '0'
        down_copy[row][column] = temp
         #Check to see if this is a duplicate state, if so ignore
        if tuple(map(tuple, down_copy)) not in searched_states :
            children.append(Node(down_copy, node.depth+1))
            searched_states.add(tuple(map(tuple, down_copy)))
    return children;


def general_search(problem,queueing_function):

    nodes = make_queue(problem.init_state)
    maxQ = 0
    nodesExpanded = 0;
    while(1):
        if not nodes:
            return "Failure"
        if maxQ < len(nodes):
            maxQ = len(nodes)
        node = nodes.pop(0)
        nodesExpanded+=1
        if problem.goal_test(node.state):
            print("DEPTH IS ", node.depth)
            print("MAX QUEUE SIZE IS ", maxQ)
            print("NODE EXPANDED IS", nodesExpanded)
            return node
        nodes= queueing_function(nodes,expand(node,searched_states))


state = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']]

class Node:
  def __init__(self, state, depth = 0):
    self.state = state
    self.depth = depth


class Problem:
    def __init__(self, state):
        self.init_state = state

    def goal_test(self, state):
        goal_state= [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']]
    
        if state == goal_state:
            return True

        return False


def driver():
    print("Welcome to Justins 8-Tile Puzzle Project")
    state = [['8', '6', '7'], ['2', '5', '4'], ['3', '0', '1']]
    problem = Problem(state)
    node = general_search(problem,ucs_queueing_func)
    print("FOUND THE SOLUTION",node.state)
    #expand(Node(state),searched_states)
        
driver()
        
        
        

