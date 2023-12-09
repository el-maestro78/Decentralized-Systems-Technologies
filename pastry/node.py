import math
import pprint


class Node:
    """Pastry Node\n"""
    nodes_cnt = 0

    def __init__(self, node_id, nodes_num=16):
        self.node_id = node_id
        self.predecessor = self
        self.successor = self
        self.right_leaf = []
        self.left_leaf = []
        self.routing_table = [[None] * nodes_num for _ in range(int(math.sqrt(nodes_num)))]
        self.data = {}
        Node.nodes_cnt += 1

    def __str__(self):
        return str(self.node_id)

    def print_routing_table(self):
        pass

    def find_successor(self, key):
        """Βρίσκει τον κόμβο που έχει την ευθύνη για το key"""
        pass

    def join(self, node):
        """Βάζει τον κόμβο στο δίκτυο"""
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

    def closest_preceding_node(self, node, h_key):
        """Βρίσκει τον κόμβο που είναι πιο κοντά στο key"""
        pass

    def distance(self, n1, n2):
        """Υπολογισμός απόστασης μεταξύ 2 κόμβων στο δίκτυο"""
        pass


