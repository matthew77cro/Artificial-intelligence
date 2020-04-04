from statespacesearch import statespace as ss
from statespacesearch import utility as ss_util
from statespacesearch import algorithms as ss_alg
from statespacesearch import heuristiccheckers as hc

def printinfo(visited, solution) :
    if(solution is None) :
        print("Solution not found")
        return

    path_len, path_rev = ss_alg.path_len_to_start_and_rev_path(solution)

    print("States visited = " + str(len(visited)))
    print("Found path of length " + str(path_len) + " with total cost " + str(solution.cost) + ":")
    for i in range(len(path_rev) - 1, 0, -1) :
        print(path_rev[i] + " =>")
    print(path_rev[0])

class Context :
    
    def __init__(self) :
        self.__commands = dict()

    def getInput(self) :
        return input("> ")

    def print(self, obj) :
        print(obj, end='')

    def printLine(self, obj = "") :
        print(obj, end='\n')

    def registerCommand(self, invoke, command) :
        if(not isinstance(command, Command) or not isinstance(invoke, str)) :
            raise Exception("Argument exception")

        self.__comands[invoke] = command

    def getCommand(self, invoke) :
        return self.__commands[invoke]

    def getCommands(self) :
        return self.__commands

    def setCommands(self, commands) :
        if(not isinstance(commands, dict)) :
            raise Exception("Argument exception")

        self.__commands = commands

class Command :

    def __init__(self) :
        self.short_desc = str()
        self.long_desc = str()

    def getShortDesc(self) :
        return self.short_desc

    def getLongDesc(self) :
        return self.long_desc

    def execute(self, context) :
        if(not isinstance(context, Context)) :
            raise Exception("Argument type exception")

class LoadFilesCommand(Command) :

    def __init__(self) :
        self.short_desc = "Load new files"
        self.long_desc = "Loads new states and heuristics from given state descriptor and heuristic descriptor files"

    def execute(self, context) :
        super().execute(context)
        context.printLine("Enter the name of a state space descriptor file: ")
        ssd_file_name = context.getInput()
        context.printLine("Enter the name of a heuristic descriptor file: ")
        hd_file_name = context.getInput()

        state_space_descriptor = None
        heuristic_descriptor = None
        try :
            state_space_descriptor = open(ssd_file_name, "r", encoding="utf8")
            heuristic_descriptor = open(hd_file_name, "r", encoding="utf8")
            ss.states.clear()
            ss.starting_state_name = None
            ss.finish_state_names = []
            ss_util.loadFromFiles(state_space_descriptor, heuristic_descriptor)
        except :
            print("An error occured. Try again")
            ss.states.clear()
            ss.starting_state_name = None
            ss.finish_state_names = []
        finally :
            if(state_space_descriptor is not None) :
                state_space_descriptor.close()
            if(heuristic_descriptor is not None) :
                heuristic_descriptor.close()

        return True

class ExitCommand(Command) :

    def __init__(self) :
        self.short_desc = "Exits"
        self.long_desc = "Terminates the application"

    def execute(self, context) :
        super().execute(context)
        context.printLine("Goodbye!")
        return False

class BfsCommand(Command) :

    def __init__(self) :
        self.short_desc = "State space search (bfs)"
        self.long_desc = "Performs a breadth first search on a loaded state space"

    def execute(self, context) :
        super().execute(context)
        if(len(ss.states) == 0) :
            context.printLine("States not loaded")
            return True

        context.printLine("Running bfs:")
        visited, solution = ss_alg.breadth_first_search(ss.getStartingStateName())
        printinfo(visited, solution)
        return True

class UcsCommand(Command) :

    def __init__(self) :
        self.short_desc = "State space search (ucs)"
        self.long_desc = "Performs an uniform cost search on a loaded state space"

    def execute(self, context) :
        super().execute(context)
        if(len(ss.states) == 0) :
            context.printLine("States not loaded")
            return True

        context.printLine("Running ucs:")
        visited, solution = ss_alg.uniform_cost_search(ss.getStartingStateName())
        printinfo(visited, solution)
        return True

class AstarCommand(Command) :

    def __init__(self) :
        self.short_desc = "State space search (a*)"
        self.long_desc = "Performs an astar search on a loaded state space"

    def execute(self, context) :
        super().execute(context)
        if(len(ss.states) == 0) :
            context.printLine("States not loaded")
            return True

        context.printLine("Running astar:")
        closed, solution = ss_alg.astar(ss.getStartingStateName())
        printinfo(closed, solution)
        return True

class AdmissibilityCheckCommand(Command) :

    def __init__(self) :
        self.short_desc = "Heuristic admissibility check"
        self.long_desc = "Performs an admissibility check on a loaded heuristic"

    def execute(self, context) :
        super().execute(context)
        if(len(ss.states) == 0) :
            context.printLine("States not loaded")
            return True

        context.printLine("Checking if heuristic is optimistic.")
        if(hc.check_admissibility()) :
            context.printLine("Heuristic is optimistic")
        else :
            context.printLine("Heuristic is not optimistic")
        return True

class ConsistencyCheckCommand(Command) :

    def __init__(self) :
        self.short_desc = "Heuristic consistency check"
        self.long_desc = "Performs an consistency check on a loaded heuristic"

    def execute(self, context) :
        super().execute(context)
        if(len(ss.states) == 0) :
            context.printLine("States not loaded")
            return True

        context.printLine("Checking if heuristic is consistent.")
        if(hc.check_consistency()) :
            context.printLine("Heuristic is consistent")
        else :
            context.printLine("Heuristic is not consistent")
        return True

class PrintLoadedStatesCommand(Command) :

    def __init__(self) :
        self.short_desc = "Print loaded states"
        self.long_desc = "Prints all loaded states along with their heuristic and transitions"

    def execute(self, context) :
        super().execute(context)
        for state_name, state in ss.getAllStates().items() :
            context.printLine(state_name + "; start: " + str(state.isStartingState()) + "; end: " + str(state.isFinishState()) + "; heuristic: " + str(state.getHeuristic()))
            for trans_name, cost in state.getAllTransitions().items() :
                context.printLine("\t" + trans_name + "," + str(cost))
        return True

class PrintNumberOfStatesCommand(Command) :

    def __init__(self) :
        self.short_desc = "Print number of loaded states"
        self.long_desc = "Prints loaded states count"

    def execute(self, context) :
        super().execute(context)
        context.printLine(len(ss.states))
        return True

class PrintRegisteredCommandsCommand(Command) :

    def __init__(self) :
        self.short_desc = "Help"
        self.long_desc = "Prints all registered commands"

    def execute(self, context) :
        super().execute(context)
        for invoke, command in context.getCommands().items() :
            context.printLine(invoke + " - " + command.getShortDesc() + " : " + command.getLongDesc())
        return True