from statespacesearch import statespace as ss
from statespacesearch import algorithms as ss_alg
from collection import linkedlist as ll

def check_admissibility():
    admissible = True

    open = [ss.getStartingStateName()]
    index = 0
    while(index < len(open)) :
        n = ss.getState(open[index])
        visited, solution = ss_alg.uniform_cost_search(n.getName())
        if(n.getHeuristic() > solution.cost) :
            print("[ERR] h(" + n.getName() + ") > h*: " + str(n.getHeuristic()) + " > " + str(solution.cost))
            admissible = False

        for state_name, cost in n.getAllTransitions().items() :
            if(state_name in open) :
                continue
            open.append(state_name)

        index += 1

    return admissible

def check_consistency():
    consistent = True

    open = [ss.getStartingStateName()]
    index = 0
    while(index < len(open)) :
        n = ss.getState(open[index])

        for state_name, cost in n.getAllTransitions().items() :
            state = ss.getState(state_name)
            if(n.getHeuristic() > state.getHeuristic() + cost) :
                print("[ERR] h(" + n.getName() + ") > h(" + state_name + ") + c: " + str(n.getHeuristic()) + " > " + str(state.getHeuristic()) + " + " + str(cost))
                consistent = False

            if(state_name in open) :
                continue
            open.append(state_name)

        index += 1

    return consistent
