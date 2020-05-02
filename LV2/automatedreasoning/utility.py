from automatedreasoning import knowledge as k

def loadClauseFromFile(clauses_file) :
    # Loading starting state
    logic = k.Logic()

    line = readLine(clauses_file)
    if(not line):
        return logic
    nextLine = readLine(clauses_file)

    while(not nextLine==""):
        logic.addClause(k.Clause(line), False)
        line = nextLine
        nextLine = readLine(clauses_file)
        
    logic.addClause(k.Clause(line), True)

    return logic
    

def readLine(file) :
    line = file.readline().strip()
    while(line.startswith("#")) :
        line = file.readline().strip()
    return str(line)