from commands import command as c

commands = dict() # dict : int -> command
commands["exit"] = c.ExitCommand()
commands["load"] = c.LoadFilesCommand()
commands["states"] = c.PrintLoadedStatesCommand()
commands["len(states)"] = c.PrintNumberOfStatesCommand()
commands["bfs"] = c.BfsCommand()
commands["ucs"] = c.UcsCommand()
commands["astar"] = c.AstarCommand()
commands["optim"] = c.AdmissibilityCheckCommand()
commands["consist"] = c.ConsistencyCheckCommand()
commands["help"] = c.PrintRegisteredCommandsCommand()

context = c.Context()
context.setCommands(commands)

print("Choose one of the options:")
commands["help"].execute(context)

result = True
while(result) :

    option = context.getInput()
    if(option not in commands) :
        context.printLine("Unknown command")
        context.printLine()
        continue

    result = commands[option].execute(context)

    context.printLine()