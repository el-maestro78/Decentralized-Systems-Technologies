class Node:
    """Pastry Node\n
    :param str node_id: Node's id
    :param int m: m-bit Keys and Nodes
    """

    nodes_cnt = 0

    def __init__(self, node_id, m=4):
        self.node_id = node_id
        self.m = m
        self.nodes_num = 2**m
        # self.neighborhood_set = []
        # self.predecessor = self
        # self.successor = self
        self.leaf_set = {"left": [], "right": []}
        # self.right_leaf = []
        # self.left_leaf = []
        self.routing_table = [[None] * self.nodes_num for _ in range(m)]
        self.data = {}
        Node.nodes_cnt += 1

    def lcp(self, key):
        """Calculate the Longest Common Prefix (LCP) between the node's id and the key"""
        lcp = ""
        if len(key) > len(self.node_id):
            for i in range(len(self.node_id)):
                if key[i] == self.node_id[i]:
                    lcp += lcp.join(key[i])
        else:
            for i in range(len(key)):
                if key[i] == self.node_id[i]:
                    lcp += lcp.join(key[i])
        if lcp != "":
            return lcp
        else:
            return -1

    def find_node_place(self, node_id):
        """Βρίσκει τη θέση του κόμβου"""
        lcp = self.lcp(node_id)
        max_lcp = lcp
        least_diff = 0
        if int(node_id) < int(self.node_id):
            for node in self.leaf_set["left"]:
                lcp = node.lcp(node_id)
                if lcp == -1 or lcp == "" or lcp is None:
                    continue
                elif int(lcp) > int(max_lcp):
                    max_lcp = lcp
        elif int(node_id) > int(self.node_id):
            for node in self.leaf_set["right"]:
                lcp = node.lcp(node_id)
                if lcp == -1 or lcp == "" or lcp is None:
                    continue
                elif int(lcp) > int(max_lcp):
                    max_lcp = lcp

        if lcp == -1 or lcp == "" or lcp is None:
            for node in self.routing_table:
                lcp = node.lcp(node_id)
                if lcp == -1 or lcp == "" or lcp is None:
                    continue
                elif int(lcp) > int(max_lcp):
                    # if lcp
                    max_lcp = lcp

        return max_lcp

    def lookup(self, key):
        """Perform tree traversal search to find the node responsible for the given key"""
        current_node = self
        while True:
            # Calculate the LCP between the current node and the key
            lcp = current_node.lcp(key)
            # Check if the key matches the current node's identifier
            if lcp == len(str(current_node.node_id)) and lcp == len(key):
                return current_node  # Found the responsible node
            # Check if the LCP points to a node in the routing table
            if lcp < len(str(current_node.node_id)):
                next_hop = current_node.routing_table[
                    lcp
                ]  # [int(current_node.node_id[lcp], 16)]
                if next_hop:
                    current_node = next_hop
                else:
                    return current_node  # No more specific route in the routing table
            # Check the leaf set for a closer node
            elif lcp < len(key):
                if int(key[lcp], 16) < int(current_node.node_id[lcp], 16):
                    current_node = current_node.leaf_set["left"]
                else:
                    current_node = current_node.leaf_set["right"]
            # No specific route found, return the current node
            else:
                return current_node


node = Node("999")
node2 = Node("354353")
node3 = Node("1234")
node4 = Node("5678")
node5 = Node("1")
node5.routing_table = [node, node2, node3, node4]
node5.leaf_set = {"left": [], "right": [node, node2, node3, node4]}
fnp = node5.find_node_place("123")
print(fnp)
# lkp = node5.lookup("123")
# print(lkp)
