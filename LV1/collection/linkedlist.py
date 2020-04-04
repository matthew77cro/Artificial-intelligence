class Node:
    # attributes: next(Node); prev(Node); object(obj); #
    def __init__(self, object, prev, next) :
        if(next is not None and not isinstance(next, Node)) :
            raise Exception("next type error")
        self.__object = object
        self.__next = next
        self.__prev = prev

    def getNext(self) :
        return self.__next

    def setNext(self, next) :
        if(next is not None and not isinstance(next, Node)) :
            raise Exception("next type error")
        self.__next = next

    def getPrev(self) :
        return self.__prev

    def setPrev(self, prev) :
        if(prev is not None and not isinstance(prev, Node)) :
            raise Exception("next type error")
        self.__prev = prev

    def getObject(self) :
        return self.__object

    def setObject(self, object) :
        self.__object = object

class LinkedList:
    # attributes: start(Node); end(Node); length(int); #
    def __init__(self) :
        self._start = None
        self._end = None
        self._length = 0

    def getLength(self) :
        return self._length

    def get(self, index) :
        if(not isinstance(index, int) or index < 0 or index >= self._length) :
            raise Exception("Argument exception")
        ret = None
        if(index <= int(self._length/2)) :
            ret = self._start
            for i in range(0, index, 1) :
                ret = ret.getNext()
        else :
            ret = self._end
            for i in range(self._length - 1, index, -1) :
                ret = ret.getPrev()
        return ret.getObject()

    def remove(self, index) :
        self.pop(index)

    def pop(self, index) :
        if(not isinstance(index, int) or index < 0 or index >= self._length) :
            raise Exception("Argument exception")

        if(index == 0) :
            ret = self._start.getObject()
            if(self._length == 1) :
                self._start = None
                self._end = None
            else :
                self._start = self._start.getNext()
                self._start.setPrev(None)
            self._length -= 1
            return ret

        if(index == self._length-1) :
            ret = self._end.getObject()
            self._end = self._end.getPrev()
            self._end.setNext(None)
            self._length -= 1
            return ret

        if(index <= int(self._length/2)) :
            ret = self._start
            for i in range(0, index, 1) :
                ret = ret.getNext()
        else :
            ret = self._end
            for i in range(self._length - 1, index, -1) :
                ret = ret.getPrev()
        ret.getPrev().setNext(ret.getNext())
        ret.getNext().setPrev(ret.getPrev())
        self._length -= 1
        return ret.getObject()

    def insert(self, object, index) :
        if(not isinstance(index, int) or index < 0 or index > self._length) :
            raise Exception("Argument exception")

        if(index == 0) :
            if(self._length == 0) :
                self._start = Node(object, None, None)
                self._end = self._start
            else :
                n = Node(object, None, self._start)
                self._start.setPrev(n)
                self._start = n
            self._length += 1
            return

        if(index == self._length) :
            n = Node(object, self._end, None) 
            self._end.setNext(n)
            self._end = n
            self._length += 1
            return

        if(index <= int(self._length/2)) :
            ret = self._start
            for i in range(0, index, 1) :
                ret = ret.getNext()
        else :
            ret = self._end
            for i in range(self._length - 1, index, -1) :
                ret = ret.getPrev()
        n = Node(object, ret.getPrev(), ret)
        ret.getPrev().setNext(n)
        ret.setPrev(n)
        self._length += 1

    def __iter__(self) :
        return LinkedListIterator(self, self._start)

class LinkedListIterator() :
    def __init__(self, linked_list, start_node) :
        if(not (isinstance(linked_list, LinkedList) and (start_node is None or isinstance(start_node, Node)))) :
            raise Exception("Argument type exception")
        self.__ll = linked_list
        self.__start = start_node
        self.__starting_len = linked_list.getLength()
        self.__curent_index = 0

    def __next__(self):
        if(not self.__starting_len == self.__ll.getLength()) :
            raise Exception("Concurrent modification exception")
        if(self.__curent_index >= self.__starting_len) :
            raise StopIteration()
        self.__curent_index += 1
        ret = self.__start
        self.__start = self.__start.getNext()

        return ret.getObject()