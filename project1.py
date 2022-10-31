import queue


#UCS here utilizes FIFO for nodes.
def ucs_queueing_func(nodes, node):
    
    nodes.append(node);
    return queue

def make_queue(init_state):
    queue = queue.Queue()
    queue.put(init_state)
    return queue

def expand(node,operators):
    return "Test"
    
def general_search(problem,queueing_function):
    nodes = make_queue(problem.init_state)
    while(1):
        if(nodes.empty()):
            return "Failure"
        node = nodes.get()
        if(problem.goal_test(node.state)):
            return node
        nodes= queueing_function(nodes,expand(node,problem.operators))

    



        
        
        
        

