import pprint


class Node:
    """Pastry Node\n
    :param int node_id: Node's id
    :param int m: m-bit Keys and Nodes
    """
    nodes_cnt = 0

    def __init__(self, node_id, m=4):
        self.node_id = node_id
        self.nodes_num = m**2
        self.neighborhood_set = []
        # self.predecessor = self
        # self.successor = self
        self.leaf_set = {'left': [], 'right': []}
        # self.right_leaf = []
        # self.left_leaf = []
        self.routing_table = [[None] * self.nodes_num for _ in range(m)]
        self.data = {}
        Node.nodes_cnt += 1

    def __str__(self):
        return str(self.node_id)

    def print_routing_table(self):
        print(f'ID: {self.node_id}')
        print(f'Επόμενος: {self.successor.node_id}')
        print(f'Προηγούμενος: {self.predecessor.node_id}')
        """print('Right Leaf:') Idk if i should use list or dict ftm
        for _ in self.leaf_set:
            print(self.leaf_set['right'])
        print('Left Leaf:')
        for _ in self.leaf_set:
            print(self.leaf_set['left'])"""
        print(f'Δεδομένα: ')
        pprint.pprint(self.data, depth=5)
        print(f'Routing Table: ')
        for i in range(self.node_id):
            print(f'{(self.node_id + 2 ** i) % self.nodes_num} : {self.routing_table[i].node_id}')

    def calculate_lcp(self, key):
        # Calculate the Longest Common Prefix (LCP) between the node's identifier and the key
        lcp = 0
        while lcp < len(key) and lcp < len(self.node_id) and key[lcp] == self.node_id[lcp]:
            lcp += 1
        return lcp

    def traverse_tree_search(self, key):
        """Perform tree traversal search to find the node responsible for the given key"""
        current_node = self
        while True:
            # Calculate the LCP between the current node and the key
            lcp = current_node.calculate_lcp(key)
            # Check if the key matches the current node's identifier
            if lcp == len(current_node.identifier) and lcp == len(key):
                return current_node  # Found the responsible node
            # Check if the LCP points to a node in the routing table
            if lcp < len(current_node.identifier):
                next_hop = current_node.routing_table[lcp][int(current_node.identifier[lcp], 16)]
                if next_hop:
                    current_node = next_hop
                else:
                    return current_node  # No more specific route in the routing table
            # Check the leaf set for a closer node
            elif lcp < len(key):
                if int(key[lcp], 16) < int(current_node.identifier[lcp], 16):
                    current_node = current_node.leaf_set['left']
                else:
                    current_node = current_node.leaf_set['right']
            # No specific route found, return the current node
            else:
                return current_node

    def join(self, node):
        """ Βάζει τον κόμβο στο δίκτυο.
        Η τιμή του κόμβου είναι ήδη hashed """
        suc = node.find_successor(self.node_id)
        pre = suc.predecessor

        self.find_node_place(pre, suc)
        self.update_routing_table()

        # Παίρνει τα keys από το successor
        self.data = {key: self.successor.data[key] for key in sorted(
            self.successor.data.keys()) if key <= self.node_id}

        for key in sorted(self.data.keys()):
            if key in self.successor.data:
                del self.successor.data[key]

    def leave(self):
        """Αφαίρεση κόμβου από το δίκτυο"""
        # Διόρθωση successor, predecessor, και routing table αυτών
        self.predecessor.successor = self.successor
        self.predecessor.routing_table[0] = self.successor
        self.successor.predecessor = self.predecessor
        # Δίνει το key στον successor
        for key in sorted(self.data.keys()):
            self.successor.data[key] = self.data[key]

    def find_node_place(self, pre, suc):
        """Βρίσκει τη θέση του κόμβου"""
        pre.routing_table[0] = self
        pre.successor = self
        suc.predecessor = self
        self.routing_table[0] = suc
        self.successor = suc
        self.predecessor = pre

    def update_routing_table(self):
        """Ανανεώνει το routing table για τον κόμβο"""
        pass

    def update_leaf_set(self):
        """Ανανεώνει το routing table για τον κόμβο"""
        pass

    def closest_preceding_node(self, node, h_key):
        """Βρίσκει τον κόμβο που είναι πιο κοντά στο key"""
        pass

    def distance(self, n1, n2):
        """Υπολογισμός απόστασης μεταξύ 2 κόμβων στο δίκτυο"""
        pass

    def find_successor(self, key):
        """Βρίσκει τον κόμβο που έχει την ευθύνη για το key"""
        pass
