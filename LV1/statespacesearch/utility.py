from statespacesearch import statespace as ss

def loadFromFiles(state_space_descriptor, heuristic_descriptor) :
    # Loading starting state
    line = readLine(state_space_descriptor)
    starting_state = ss.State(line, True, False)

    # Loading end states
    line = readLine(state_space_descriptor).split()
    for s in line :
        ss.State(s, False, True)

    # Loading transitions
    line = readLine(state_space_descriptor)
    while(not (line=="")) :
        line = line.split()
        name = line[0][0:-1]
        line.pop(0)
        if(not ss.existsState(name)) :
            ss.State(name, False, False)
        state = ss.getState(name)
        for transition in line :
            transition_split = transition.split(",")
            if(not ss.existsState(transition_split[0])) :
                ss.State(transition_split[0], False, False)
            state.addTransition(transition_split[0], float(transition_split[1]))
        line = readLine(state_space_descriptor)

    for line in heuristic_descriptor :
        if(line.startswith("#")) :
            continue
        line = line.split()
        name = line[0][0:-1]
        heuristic = float(line[1])
        ss.getState(name).setHeuristic(heuristic)

def readLine(file) :
    line = file.readline().strip()
    while(line.startswith("#")) :
        line = file.readline().strip()
    return line