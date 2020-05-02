from automatedreasoning import knowledge as k
from automatedreasoning import utility as u
from automatedreasoning import algorithms as a
import sys

def main():
    argc = len(sys.argv)
    argv = sys.argv
    
    options = ["resolution", "cooking_test", "cooking_interactive"]
    if(argv[1] not in options):
        return

    option = argv[1]
    pathClause = argv[2]
    pathCommands = ""
    verbose = False

    if(argc > 3):
        if(argv[3]=="verbose"):
            verbose = True
        else:
            pathCommands = argv[3]

    if(argc > 4):
        if(argv[4]=="verbose"):
           verbose = True

    run(option, pathClause, pathCommands, verbose, options)

def run(option, pathClause, pathCommands, verbose, options):
    file = open(pathClause)
    logic = u.loadClauseFromFile(file)
    file.close()

    if(option == options[0]):
        (boolean, info) = a.resolutionRefutation(logic)
        if(verbose):
            print(info, end='')
        if(boolean):
            print(logic.getGoalClause().toString() + " is true")
        else:
            print(logic.getGoalClause().toString() + " is unknown")
    elif(option == options[1]):
        logic.addClause(logic.getGoalClause(), False)
        file = open(pathCommands)
        for line in file:
            line = str(line).strip()
            executeCommand(line, logic, False, verbose)
    elif(option == options[2]):
        logic.addClause(logic.getGoalClause(), False)
        while(True):
            query = input("\nPlease enter your query\n>>> ").strip()
            executeCommand(query, logic, True, verbose)

def executeCommand(command, logic, addRemoveInfo, verbose):
    command = str(command).strip()
    if(command.endswith("?")):
        clause = k.Clause(command[:-2])
        logic.addClause(clause, True)
        (boolean, info) = a.resolutionRefutation(logic)
        if(verbose):
            print(info, end='')
        if(boolean):
            print(logic.getGoalClause().toString() + " is true")
        else:
            print(logic.getGoalClause().toString() + " is unknown")
    elif(command.endswith("+")):
        clause = k.Clause(command[:-2])
        logic.addClause(clause, False)
        if(addRemoveInfo):
            print("added " + clause.toString())
    elif(command.endswith("-")):
        clause = k.Clause(command[:-2])
        logic.removeClause(clause)
        if(addRemoveInfo):
            print("removed " + clause.toString())
    elif(query=="exit"):
        exit(0)

main()