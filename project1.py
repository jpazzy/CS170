import copy
import time
import math
import queue


#UCS here utilizes FIFO for nodes.
def ucs_queueing_func(nodes, children):
  for child in children:
    nodes.put(child)
  return nodes


#The misplaced queuing functuction calcualated the heuristic cost of a child
#then puts it into the priority queue
def misplaced_queueing_func(nodes, children):
  for child in children:
    child.heuristic_cost = misplaced_tile(child.state)
    nodes.put(child)
  return nodes

#The manhattan queuing functuction calcualated the heuristic cost of a child
#then puts it into the priority queue
def manhattan_queueing_func(nodes, children):
  for child in children:
    child.heuristic_cost = manhattan_distance(child.state)
    nodes.put(child)
  return nodes


# The misplaced tile heuristic simply counts the amount of tiles that are
# in the incorrect location
def misplaced_tile(state):
  misplaced = 0
  proper_arrangement = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
  # Iterate through the grid and count the amount misplaced
  for i in range(len(state[0])):
    for j in range(len(state)):
      if state[i][j] != 0 and state[i][j] != proper_arrangement[i][j]:
        misplaced += 1

  return misplaced


#The Manhattan_distance counts the amount of squares off each square is from its goal state
def manhattan_distance(state):
  proper_arrangement = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
  dist = 0
  for i in range(len(state[0])):
    for j in range(len(state)):
      #See here if its misplaced
      if state[i][j] != 0 and state[i][j] != proper_arrangement[i][j]:
        #Now calculate the location for the proper square
        row = math.floor(state[i][j] / len(proper_arrangement))
        #Adjustment for starting at 1
        col = (state[i][j] - 1) % len(proper_arrangement[0])
        dist += (abs(row - i) + abs(col - j))
  return dist


#Create the initial queue
def make_queue(init_state):
  q = queue.PriorityQueue()
  q.put(Node(init_state))
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
      if node.state[i][j] == 0:
        row = i
        column = j

  #Now we must perform all valid operations on
  #the current state

  #Check to see if the space can move left, if so do it
  if column > 0:
    left_copy = copy.deepcopy(node.state)
    temp = left_copy[row][column - 1]
    left_copy[row][column - 1] = 0
    left_copy[row][column] = temp
    #Check to see if this is a duplicate state, if so ignore
    if tuple(map(tuple, left_copy)) not in searched_states:
      children.append(Node(left_copy, node.depth + 1))
      searched_states.add(tuple(map(tuple, left_copy)))

  #Check to see if the space can move right, if so do it
  if column < 2:
    right_copy = copy.deepcopy(node.state)
    temp = right_copy[row][column + 1]
    right_copy[row][column + 1] = 0
    right_copy[row][column] = temp
    #Check to see if this is a duplicate state, if so ignore
    if tuple(map(tuple, right_copy)) not in searched_states:
      children.append(Node(right_copy, node.depth + 1))
      searched_states.add(tuple(map(tuple, right_copy)))
  #Check to see if the space can move up, if so do it
  if row > 0:
    up_copy = copy.deepcopy(node.state)
    temp = up_copy[row - 1][column]
    up_copy[row - 1][column] = 0
    up_copy[row][column] = temp
    #Check to see if this is a duplicate state, if so ignore
    if tuple(map(tuple, up_copy)) not in searched_states:
      children.append(Node(up_copy, node.depth + 1))
      searched_states.add(tuple(map(tuple, up_copy)))

  #Check to see if the space can move down, if so do it
  if row < 2:
    down_copy = copy.deepcopy(node.state)
    temp = down_copy[row + 1][column]
    down_copy[row + 1][column] = 0
    down_copy[row][column] = temp
    #Check to see if this is a duplicate state, if so ignore
    if tuple(map(tuple, down_copy)) not in searched_states:
      children.append(Node(down_copy, node.depth + 1))
      searched_states.add(tuple(map(tuple, down_copy)))
  return children


#This general search function stems from the given psuedo code from Prof. Keogh's slides
def general_search(problem, queueing_function):
  nodes = make_queue(problem.init_state)
  maxQ = 0
  nodesExpanded = 0
  searched_states = set()
  start = time.time()
  #If set to True, this will print out the trace of expanded nodes

  TRACE = True
  while (1):
    if not nodes:
        return "Failure"
    if maxQ < nodes.qsize():
        maxQ = nodes.qsize()
    node = nodes.get()
    nodesExpanded += 1
    if TRACE:
        print("The best node to expand with a h(n) of",node.depth,"and g(n) of", node.heuristic_cost," is")
        for i in node.state:
            print(i)
    if problem.goal_test(node.state):
        print("We have reached the goal state!")
        print("DEPTH IS", node.depth)
        print("MAX QUEUE SIZE IS", maxQ)
        print("NODES EXPANDED IS", nodesExpanded)
        end = time.time()
        print("SEARCH TOOK :", end - start, "seconds!")

        return node
    #Update the node pqueue with the new pqueue with newly expanded nodes!
    nodes = queueing_function(nodes, expand(node, searched_states))

#Node class in order to contain all the node data
class Node:
  def __init__(self, state, depth=0, heuristic_cost=0):
    self.state = state
    self.depth = depth
    self.heuristic_cost = heuristic_cost

  #Less than operator overload to ensure proper ordering
  def __lt__(self, other):
    if (self.depth + self.heuristic_cost) == (other.depth +
                                              other.heuristic_cost):
      return self.depth < other.depth
    return (self.depth + self.heuristic_cost) < (other.depth +
                                                 other.heuristic_cost)

  #Greater than operator overload to ensure proper ordering
  def __gt__(self, other):
    if (self.depth + self.heuristic_cost) == (other.depth +
                                              other.heuristic_cost):
      return self.depth > other.depth
    return (self.depth + self.heuristic_cost) > (other.depth +
                                                 other.heuristic_cost)


class Problem:
  def __init__(self, state):
    self.init_state = state

  def goal_test(self, state):
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    if state == goal_state:
      return True

    return False


def driver():
  print("Welcome to Justin's 8-Tile Puzzle Project")
  state = [[], [], []]
  choice = ''
  print(
    "Please enter the starting state you would like to start at! Please enter in this format:"
  )
  print("1 2 3 ")
  print("With a space between each number and hitting enter after each line")
  #Take in all the input from the user
  r1 = input("Enter Row 1: ")
  row1 = r1.split()
  r2 = input("Enter Row 2: ")
  row2 = r2.split()
  r3 = input("Enter Row 3: ")
  row3 = r3.split()
  state = [row1, row2, row3]
  #Convert the strings to ints
  for i in range(len(row1)):
    for j in range(len(state)):
      state[i][j] = int(state[i][j])

  problem = Problem(state)
  print("Enter 1 If you would like to search using Uniform Cost Search")
  print(
    "Enter 2 If you would like to search using A* and the Misplaced Tile Heuristic"
  )
  print(
    "Enter 3 If you would like to search using A* and the Manhattan Heuristic")
  choice = input()

  if choice == '1':
    general_search(problem, ucs_queueing_func)
  elif choice == '2':
    general_search(problem, misplaced_queueing_func)
  elif choice == '3':
    general_search(problem, manhattan_queueing_func)


driver()
