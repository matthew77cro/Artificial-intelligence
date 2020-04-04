import copy

starting_state_name = None    # type : string
finish_state_names = []       # type : list of strings

states = {}                   # type : dict: state_name(string) -> state(State)

def getState(state_name) :
    return states[state_name]
def existsState(state_name) :
    return state_name in states
def getAllStates() :
    return copy.deepcopy(states)
def getStartingStateName() :
    return starting_state_name
def getAllFinishStateNames() :
    return copy.deepcopy(finish_state_names)
def isFinishState(state_name) :
    return state_name in finish_state_names

class State:
    # attributes : name(string) - unique id; next(dict: state_name -> cost); heuristic(float); start(bool); end(bool) #
    def __init__(self, name, start, end) :
        global states
        global starting_state_name
        global finish_state_names

        if(not (isinstance(name, str) and isinstance(start, bool) and isinstance(end, bool))) :
            raise Exception("Argument exception")
        if(start and end) :
            raise Exception("Argument exception : start and end both True")
        if(start and starting_state_name is not None) :
            raise Exception("Starting state already exists!")
        if(name in states) :
            raise Exception("State name already exists : " + name)
        self.__name = name
        self.__next = {}
        self.__heuristic = float(0)
        self.__start = start
        self.__end = end
        
        states[name] = self
        if(start) :
            starting_state_name = name
        if(end) :
            finish_state_names.append(name)

    def getName(self) :
        return self.__name

    def addTransition(self, state_name, cost) :
        if(not isinstance(state_name, str) or not isinstance(cost, float)) :
            raise Exception("Argument exception")
        if(not existsState(state_name)) :
            raise Exception("State with that state name does not exist : " + state_name)
        if(state_name in self.__next) :
            return False
        self.__next[state_name] = cost
        return True

    def getTransitionCost(self, state_name) :
        if(not isinstance(state_name, str)) :
            raise Exception("Argument exception")
        if(not (state_name in self.__next)) :
            return -1
        return self.__next[state_name]

    def getAllTransitions(self) :
        return self.__next

    def isStartingState(self) :
        return self.__start

    def isFinishState(self) :
        return self.__end

    def getHeuristic(self) :
        return self.__heuristic

    def setHeuristic(self, heuristic) :
        if(not isinstance(heuristic, float)) :
            raise Exception("Heuristic not float! Got: " + heuristic)
        self.__heuristic = float(heuristic)

    def __eq__(self, value):
        if(not isinstance(value, State)) :
            return False
        return self.__name == value.getName()