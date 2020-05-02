class Clause:

    def __init__(self, clause=""):
        if(not isinstance(clause, str)):
            raise Exception("Clause not type of str")
        self.__all = dict() # dict : literal (str) -> exists (bool)
 
        split = str(clause).split()
        for i in split:
            i = str(i).lower()
            if(i=="v"):
                continue

            self.__all[i] = True

    def containsLiteral(self, literal):
        if(not isinstance(literal, str)):
            raise Exception("Type error")
        literal = str(literal).lower()
        return literal in self.__all

    def removeLiteral(self, literal):
        if(not isinstance(literal, str)):
            raise Exception("Type error")
        literal = str(literal).lower()
        if(literal not in self.__all):
            return False

        del self.__all[literal]
        return True

    def addLiteral(self, literal):
        if(not isinstance(literal, str)):
            raise Exception("Type error")
        literal = str(literal).lower()
        if(literal in self.__all):
            return False

        self.__all[literal] = True

        return True

    def getLiterals(self):
        return self.__all.keys()

    def copy(self):
        c = Clause()
        c.__all = self.__all.copy()
        return c

    def toString(self):
        ret = ""
        keys = list(self.__all.keys())

        if(len(keys)==0):
            return ret

        ret += keys[0]
        for i in range(1, len(keys)):
            ret += " v "
            ret += str(keys[i])

        return ret
            
    def __hash__(self):
        return hash(tuple(self.__all.keys()))

    def __eq__(self, value):
        if(not isinstance(value, Clause)):
            return False
        return self.__all == value.__all

class Logic:
    
    def __init__(self):
        self.__version = 0
        self.__clauses = dict() # dict : clause (Clause) -> exists (bool)
        self.__goalClause = None

    def addClause(self, clause, goalClause):
        if(not isinstance(clause, Clause) or not isinstance(goalClause, bool)):
            raise Exception("Type error")
        if(not goalClause and not (clause in self.__clauses)):
            self.__clauses[clause] = True
        elif(goalClause):
            self.__goalClause = clause
        self.__version+=1

    def removeClause(self, clause):
        self.__clauses.pop(clause, None)
        if(self.__goalClause==clause):
            self.__goalClause = None
        self.__version+=1

    def getClauses(self):
        return self.__clauses.keys()

    def getGoalClause(self):
        return self.__goalClause

    def copy(self):
        l = Logic()
        l.__goalClause = self.__goalClause.copy()
        for k, v in self.__clauses.items():
            l.__clauses[k] = v
        return l

    def clauses(self):
        savedVersion = self.__version
        for i in self.__clauses:
            if(savedVersion!=self.__version):
                raise Exception("Concurrent modification")
            yield i