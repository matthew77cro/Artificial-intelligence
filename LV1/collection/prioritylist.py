from collection import linkedlist as ll

class PriorityNode(ll.Node) :

    def __init__(self, object, prev, next, score):
        super().__init__(object, prev, next)
        if(not isinstance(score, float)) :
            raise Exception("Argument type error")
        self._score = score

    def getScore(self) :
        return self._score

class PriorityList(ll.LinkedList) :

    def __init__(self):
        super().__init__()

    def insertPriority(self, object, score) :
        if(object is None) :
            raise Exception("Argument null error")

        if(self._length==0) :
            self._start = PriorityNode(object, None, None, score)
            self._end = self._start
            self._length += 1
            return

        self._length += 1

        if(self._start.getScore() >= score) :
            tmp = PriorityNode(object, None, self._start, score)
            self._start.setPrev(tmp)
            self._start = tmp
            return

        if(self._end.getScore() < score) :
            tmp = PriorityNode(object, self._end, None, score)
            self._end.setNext(tmp)
            self._end = tmp
            return

        iter = self._start
        while(iter.getScore() < score) :
            iter = iter.getNext()

        tmp = PriorityNode(object, iter.getPrev(), iter, score)
        iter.getPrev().setNext(tmp)
        iter.setPrev(tmp)

    def insert(self, object, index):
        raise Exception("Unsupported operation exception")