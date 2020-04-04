from statespacesearch import statespace as ss
from collection import linkedlist as ll
from collection import prioritylist as pl

class Node :
    'Node used to build search tree'
    # attributes: state_name(String); prev(Node); next(list of Node); cost(float) - cost to this node; heuristic(float) - from this node to the end node #
    def __init__(self, state_name, prev, next, cost, heuristic) :
        if(not (isinstance(state_name, str) and (prev is None or isinstance(prev, Node)) and isinstance(next, list) and isinstance(cost, float) and isinstance(heuristic, float))) :
            raise Exception("Argument exception")
        self.state_name = state_name
        self.prev = prev
        self.next = next
        self.cost = cost
        self.heuristic = heuristic

    def printTree(rootNode) :
        if(not isinstance(rootNode, Node)) :
            raise Exception("Argument type exception")
        Node.__printRecur(rootNode, 0)

    def __printRecur(node, indentLevel) :
        print(" " * indentLevel + node.state_name + "; cost: " + str(node.cost))
        for n in node.next :
            Node.__printRecur(n, indentLevel+2)

def breadth_first_search(starting_state_name) :
    ### BFS ###
    open = ll.LinkedList()
    open.insert(Node(starting_state_name, None, [], 0.0, 0.0), 0)
    visited = []
    solution = None
    while(not (open.getLength()==0)) :
        n = open.pop(0)
        if(ss.isFinishState(n.state_name)) :
            solution = n
            break
        visited.append(n.state_name)
        for state_name, cost in ss.getState(n.state_name).getAllTransitions().items() :
            if(not state_name in visited) :
                newNode = Node(state_name, n, [], 0.0, 0.0)
                n.next.append(newNode)
                open.insert(newNode, open.getLength())
    ### BFS ###

    return (visited, solution)

def uniform_cost_search(starting_state_name) :
    ### UCS ###
    open = pl.PriorityList()
    open.insertPriority(Node(starting_state_name, None, [], 0.0, 0.0), 0.0)
    visited = []
    solution = None
    while(not (open.getLength()==0)) :
        n = open.pop(0)
        if(ss.isFinishState(n.state_name)) :
            solution = n
            break
        visited.append(n.state_name)
        for state_name, cost in ss.getState(n.state_name).getAllTransitions().items() :
            if(not state_name in visited) :
                newNode = Node(state_name, n, [], n.cost + ss.getState(n.state_name).getTransitionCost(state_name), 0.0)
                n.next.append(newNode)
                open.insertPriority(newNode, newNode.cost)
    ### UCS ###

    return (visited, solution)

def astar(starting_state_name) :
    ### A* ###
    open = pl.PriorityList()
    start_state_heuristic = ss.getState(starting_state_name).getHeuristic()
    open.insertPriority(Node(starting_state_name, None, [], 0.0, start_state_heuristic), start_state_heuristic)
    closed = []
    solution = None
    while(not (open.getLength()==0)) :
        n = open.pop(0)
        if(ss.isFinishState(n.state_name)) :
            solution = n
            break
        closed.append(n)
        for state_name, cost in ss.getState(n.state_name).getAllTransitions().items() :
            newNode = Node(state_name, n, [], n.cost + ss.getState(n.state_name).getTransitionCost(state_name), ss.getState(state_name).getHeuristic())
            
            # Looking for the same state node in list open
            shouldContinue = False
            found = False
            index = 0
            for node in open :
                if(node.state_name == newNode.state_name) :
                    if(node.cost < newNode.cost) :
                        shouldContinue = True
                        found = True
                        break
                    else :
                        open.remove(index)
                        found = True
                        break
                index += 1
            
            # Looking for the same state node in list closed
            if(not found) :
                index = 0
                for node in closed :
                    if(node.state_name == newNode.state_name) :
                        if(node.cost < newNode.cost) :
                            shouldContinue = True
                            break
                        else :
                            open.remove(index)
                            break
                    index += 1
            if(shouldContinue) :
                continue

            n.next.append(newNode)
            open.insertPriority(newNode, newNode.cost + newNode.heuristic)
    ### A* ###

    return (closed, solution)

def path_len_to_start_and_rev_path(search_tree_node) :
    if(not isinstance(search_tree_node, Node)) :
        raise Exception("Argument exception")

    tmp = search_tree_node
    path_len = 0
    path_rev = []
    while(tmp is not None) :
        path_rev.append(tmp.state_name)
        path_len += 1
        tmp = tmp.prev

    return (path_len, path_rev)
