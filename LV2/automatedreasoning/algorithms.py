from automatedreasoning import knowledge as k

indexClause1 = 0
indexClause2 = 0
index = 0

def resolutionRefutation(logic):
    global indexClause1
    global indexClause2
    global index
    logic = logic.copy()

    info = ""

    if(not isinstance(logic, k.Logic)):
        raise Exception("Type error")
    clauses = logic.getClauses()
    goalLiterals = logic.getGoalClause().getLiterals()

    index = 0
    allClauses = dict() # dict : index (int) -> clause (Clause)
    setOfSupport = dict() # dict : index (int) -> clause (Clause)
    for c in clauses:
        allClauses[index] = c
        info += str(index+1) + ". " + c.toString() + "\n"
        index += 1
    info += "=============\n"
    for l in goalLiterals:
        c = k.Clause("~" + l)
        setOfSupport[index] = c
        info += str(index+1) + ". " + c.toString() + "\n"
        index += 1
    info += "=============\n"

    indexClause1 = 0
    indexClause2 = len(allClauses)

    resolvedClauses = dict() # dict : resolved pair (2-tuple of clauses) -> resolved (bool)

    while True:
        removeRedundant(allClauses, setOfSupport)
        removeTautologies(allClauses, setOfSupport)
        selected = selectClauses(allClauses, setOfSupport, resolvedClauses) # list of tuples (index1, index2, c1, c2)
        if(len(selected)==0):
            return (False, info)

        found = False
        for (index1, index2, c1, c2) in selected:
            resolvent = plResolve(c1, c2)
            resolvedClauses[(c1, c2)] = True

            if(resolvent==None):
                continue
            if(len(list(resolvent.getLiterals()))==0):
                info += str(index+1) + ". NIL (" + str(index1+1) + ", " + str(index2+1) + ")\n"
                info += "=============\n"
                return (True, info)
            if(resolvent not in set(allClauses.values()) and resolvent not in set(setOfSupport.values())):
                found = True
                setOfSupport[index] = resolvent
                info += str(index+1) + ". " + resolvent.toString() + " (" + str(index1+1) + ", " + str(index2+1) + ")\n"
                index+=1

        if(not found):
            if(len(setOfSupport) > 1):
                info += "=============\n"
            return (False, info)

def removeRedundant(allClauses, setOfSupport):
    numOfClauses = len(allClauses) + len(setOfSupport)
    toRemove = set()
    for i1 in range(0, numOfClauses-1):
        c1 = getClause(allClauses, setOfSupport, i1)
        if(c1 is None):
            continue
        for i2 in range(i1+1, numOfClauses):
            c2 = getClause(allClauses, setOfSupport, i2)
            if(c2 is None):
                continue
            set1 = set(c1.getLiterals())
            set2 = set(c2.getLiterals())
            if(set1.issubset(set2)):
                toRemove.add(i2)
            elif(set2.issubset(set1)):
                toRemove.add(i1)
    for i in toRemove:
        removeClause(allClauses, setOfSupport, i)

def removeTautologies(allClauses, setOfSupport):
    toRemove = list()
    for index, clause in set(allClauses.items()).union(set(setOfSupport.items())):
        literals = set(clause.getLiterals())
        tautology = True
        for l in literals:
            l = str(l)
            if(l.startswith("~") and not l[1:] in literals):
                tautology = False
                break
            elif(not l.startswith("~") and not str("~" + l) in literals):
                tautology = False
                break
        if(tautology):
            toRemove.append(index)

    for i in toRemove:
        removeClause(allClauses, setOfSupport, i)

def selectClauses(allClauses, setOfSupport, resolvedClauses):
    global indexClause1
    global indexClause2
    global index

    toReturn = list()
    while(indexClause2 < index):
        c2 = getClause(allClauses, setOfSupport, indexClause2)
        while(c2 is None and indexClause2 < index):
            indexClause2 += 1
            c2 = getClause(allClauses, setOfSupport, indexClause2)
        if(indexClause2 >= index):
            break
        while(indexClause1 < indexClause2):
            c1 = getClause(allClauses, setOfSupport, indexClause1)
            while(c1 is None and indexClause1 < indexClause2):
                indexClause1 += 1
                c1 = getClause(allClauses, setOfSupport, indexClause1)
            if(indexClause1 >= indexClause2):
                break
            if((c1, c2) not in resolvedClauses):
                toReturn.append((indexClause1, indexClause2, c1, c2))
            indexClause1 += 1
        indexClause1 = 0
        indexClause2 += 1
    return toReturn

def getClause(allClauses, setOfSupport, index):
    if(index in allClauses):
        return allClauses[index]
    elif(index in setOfSupport):
        return setOfSupport[index]
    else:
        return None

def removeClause(allClauses, setOfSupport, index):
    if(index in allClauses):
        del allClauses[index]
    elif(index in setOfSupport):
        del setOfSupport[index]

def plResolve(c1, c2):
    resolvent = k.Clause()

    lit1 = set(c1.getLiterals())
    lit2 = set(c2.getLiterals())

    found = False
    cancel = set()

    for l in lit1:
        l = str(l)
        opposite = str()
        if(l.startswith("~")):
            opposite = l[1:]
        else:
            opposite = "~" + l

        if(opposite in lit2):
            found = True
            cancel.add(l)
            cancel.add(opposite)

    if(not found):
        return None

    for l in lit1.union(lit2):
        l = str(l)
        if(l not in cancel):
            resolvent.addLiteral(l)

    return resolvent
        