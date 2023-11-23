# A Distributed Hash Table implementation

class Node:
    def __init__(self, ID, nxt=None, prev=None):
        self.ID = ID
        self.data = dict()  # Use a dictionary to store keys and lists of values
        self.prev = prev
        self.fingerTable = [nxt]

    def updateFingerTable(self, dht, k):
        del self.fingerTable[1:]
        for i in range(1, k):
            self.fingerTable.append(dht.findNode(dht._startNode, self.ID + 2 ** i))


class DHT:
    def __init__(self, k):
        self._k = k
        self._size = 2 ** k
        self._startNode = Node(0, k)
        self._startNode.fingerTable[0] = self._startNode
        self._startNode.prev = self._startNode
        self._startNode.updateFingerTable(self, k)

    def getHashId(self, key):
        return hash(key) % self._size

    def distance(self, n1, n2):
        if n1 == n2:
            return 0
        if n1 < n2:
            return n2 - n1
        return self._size - n1 + n2

    def getNumNodes(self):
        if self._startNode is None:
            return 0
        node = self._startNode
        n = 1
        while node.fingerTable[0] != self._startNode:
            n = n + 1
            node = node.fingerTable[0]
        return n

    def findNode(self, start, key):
        hashId = self.getHashId(key)
        curr = start
        numJumps = 0
        while True:
            if curr.ID == hashId:
                return curr
            if self.distance(curr.ID, hashId) <= self.distance(curr.fingerTable[0].ID, hashId):
                return curr.fingerTable[0]
            tabSize = len(curr.fingerTable)
            i = 0
            nextNode = curr.fingerTable[-1]
            while i < tabSize - 1:
                if self.distance(curr.fingerTable[i].ID, hashId) < self.distance(curr.fingerTable[i + 1].ID, hashId):
                    nextNode = curr.fingerTable[i]
                i = i + 1
            curr = nextNode
            numJumps += 1

    def lookup(self, start, key):
        nodeForKey = self.findNode(start, key)
        if key in nodeForKey.data:
            print(f"The key {key} is in node {nodeForKey.ID}")
            return nodeForKey.data[key]
        return None

    def store(self, start, key, value):
        nodeForKey = self.findNode(start, key)
        
        if key not in nodeForKey.data:
            # If the key is not present, create a new list for the key
            nodeForKey.data[key] = [value]
        else:
            # If the key is already present, append the value to the existing list
            nodeForKey.data[key].append(value)

    def join(self, newNode):
        origNode = self.findNode(self._startNode, newNode.ID)
        if origNode.ID == newNode.ID:
            print("There is already a node with the same id!")
            return

        for key in origNode.data:
            hashId = self.getHashId(key)
            if self.distance(hashId, newNode.ID) < self.distance(hashId, origNode.ID):
                newNode.data.setdefault(key, []).extend(origNode.data[key])

        prevNode = origNode.prev
        newNode.fingerTable[0] = origNode
        newNode.prev = prevNode
        origNode.prev = newNode
        prevNode.fingerTable[0] = newNode

        newNode.updateFingerTable(self, self._k)

        for key in list(origNode.data.keys()):
            hashId = self.getHashId(key)
            if self.distance(hashId, newNode.ID) < self.distance(hashId, origNode.ID):
                del origNode.data[key]

    def leave(self, node):
        for k, v_list in node.data.items():
            node.fingerTable[0].data.setdefault(k, []).extend(v_list)
        if node.fingerTable[0] == node:
            self._startNode = None
        else:
            node.prev.fingerTable[0] = node.fingerTable[0]
            node.fingerTable[0] = prev = node.prev
            if self._startNode == node:
                self._startNode = node.fingerTable[0]

    def updateAllFingerTables(self):
        self._startNode.updateFingerTable(self, self._k)
        curr = self._startNode.fingerTable[0]
        while curr != self._startNode:
            curr.updateFingerTable(self, self._k)
            curr = curr.fingerTable[0]

    def printFingerTables(self):
        current_node = self._startNode

        while True:
            finger_table_ids = [node.ID for node in current_node.fingerTable]
            print(f"Finger Table for Node {current_node.ID}: {finger_table_ids}")

            current_node = current_node.fingerTable[0]
            if current_node == self._startNode:
                break
