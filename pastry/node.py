import pprint
import sys
from pastry.hash import hash_function


class Node:
    """Pastry Node.
    :param str node_id: Node's id
    :param int m: m-bit Keys and Nodes
    """

    nodes_cnt = 0

    def __init__(self, node_id, m=4):
        self.node_id = str(node_id)
        self.m = m
        self.nodes_num = m ** 2
        self.leaf_set = {"left": [], "right": []}
        self.routing_table = [[None] * self.nodes_num for _ in range(m)]
        self.data = {}
        Node.nodes_cnt += 1

    def __str__(self):
        return str(self.node_id)

    def __hash__(self):
        return hash_function(self.node_id)

    def print_routing_table(self):
        """Τυπώνει τα δεδομένα του routing table"""
        print(f"Routing Table for Node {self.node_id}:")
        for i, row in enumerate(self.routing_table):
            nodes = []
            for node in row:
                if isinstance(node, Node):
                    nodes.append(node.node_id)
            print(f"Row {i}: {nodes}")

    def print_leaf_sets(self):
        """Τυπώνει τα δεδομένα του leaf set"""
        for leaf in ["left", "right"]:
            print(f"{leaf.capitalize()} Leaf:")
            for node in self.leaf_set[leaf]:
                print(node.node_id)
            print("--------------")

    def print_routing_table_and_leaf_set(self):
        """Print routing table and leaf data"""
        print(f"ID: {self.node_id}")
        print(f"Κοντινότερος: {self.closest_preceding_node(self).node_id}")
        print(f"Δεδομένα: ")
        pprint.pprint(self.data, depth=5)
        self.print_routing_table()
        self.print_leaf_sets()

    def lcp(self, key):
        """Υπολογίζει το ελάχιστο κοινό prefix μεταξύ 2 ids'.
        :param str key: Node's id or data key
        :return: Least common prefix between self and key.
        :rtype: int"""
        key = str(key)
        node_id = str(self.node_id)
        lcp = ""
        # Ανάλογα με το ποιός είναι μεγαλύτερος κάνουμε τη σύγκριση
        # για να μη βγει out of index error
        if len(key) > len(node_id):
            for i in range(len(node_id)):
                for j in range(len(key)):
                    if key[j] == node_id[i]:
                        lcp += lcp.join(key[j])
                        # break αλλιώς για κάθε j που είναι ίδιο με το i
                        # θα έχουμε πολλαπλές του εμφανίσεις στο lcp
                        break
        else:
            for i in range(len(key)):
                for j in range(len(node_id)):
                    if key[i] == node_id[j]:
                        lcp += lcp.join(key[i])
                        break
        if lcp != "":
            return int(lcp)
        else:
            return -1

    def join(self, node):
        """Βάζει τον κόμβο στο δίκτυο.
        Η τιμή του κόμβου είναι ήδη hashed
        :param Node node: Node that we want to insert/join
        :return: Nothing.
        :rtype: None
        """
        if node == self:  # Έλεγχος αν είναι ο ίδιος κόμβος
            pass
        else:
            self.update_routing_table(node, "INSERT")
            self.update_leaf_set(node, "INSERT")

    def leave(self):
        """Αφαιρεί τον από το δίκτυο και διανέμει στον
        κοντινότερο τα δεδομένα του.
        :return: Nothing.
        :rtype: None
                """
        closest_node = self.closest_preceding_node(self)
        closest_node.data = {
            **closest_node.data,
            **self.data,
        }  # προσθέτουμε τα δεδομένα στον κοντινότερο κόμβο με dict unpacking

    def __eq__(self, other):
        return isinstance(other, Node) and self.node_id == other.node_id

    def update_routing_table(self, node, action):
        """Ανανεώνει το routing table για τον κόμβο
        :param Node node: Node.
        :param str action: Either Insert or Delete. The action will be performed.
        :return: Nothing.
        :rtype: None
        """
        if action == "INSERT":
            if Node.nodes_cnt == 1:
                self.routing_table[0][0] = [node]
            elif Node.nodes_cnt == 2:
                self.routing_table[1][0] = [node]
            # αν είναι άδειο το routing table προσθέτουμε σε μια θέση που περιέχει None
            elif Node.nodes_cnt < self.nodes_num:
                # το routing table είναι μια λίστα με m υπο-λίστες
                for row_index, row in enumerate(self.routing_table):
                    for row_node in row:  # μέσα σε μια υπο-λίστα
                        if isinstance(row_node, Node):
                            # Έλεγχος για κοινό lcp με το 1ο στοιχεί της γραμμής.
                            # Θέλουμε να γίνει κάποια ταξινόμηση μέσα στον πίνακα με βάση το prefix
                            if node.lcp(row_node.node_id) != -1:
                                if None in row:
                                    node_index = row.index(None)
                                    self.routing_table[row_index][node_index] = node
                                    return  # για να μην τον βάλει σε όλες τις γραμμές
                                else:  # αν υπάρχει lcp το προσθέτουμε στη γραμμή
                                    self.add_in_full_routing_table(node)
                        else:
                            node_index = row.index(None)
                            self.routing_table[row_index][node_index] = node
                            return
            else:  # για errors
                self.add_in_full_routing_table(node)

        elif action == "DELETE":
            for row_index, row in enumerate(self.routing_table):
                for i in range(len(row)):
                    n = row[i]
                    if isinstance(n, Node):
                        if node.node_id == n.node_id:
                            self.routing_table[row_index][i] = None
        else:
            print("ERROR")

    def add_in_full_routing_table(self, node):
        """Προσθέτει τον κόμβο στην κατάλληλη θέση αν είναι γεμάτο το Routing Table.
                :return: Nothing.
                :rtype: None"""
        for row_index, row in enumerate(self.routing_table):
            if None in row:
                # Η συνάρτηση καλείται επίσης για ταξινόμηση μέσα στο routing table,
                # οπότε δίνουμε προτεραιότητα στις None τιμές
                node_index = row.index(None)
                self.routing_table[row_index][node_index] = node
                break
            else:
                if row.count(None) == 0 and len(row) == self.m:
                    continue  # αν είναι γεμάτη συνέχισε
                for row_node in row:
                    if node.lcp(row_node.node_id) != -1:
                        # Εισάγουμε ελέγχοντας την απόσταση
                        new_row = sorted(row[:-1] + [node], key=lambda x: x.node_id)
                        self.routing_table[row_index] = new_row
                        break
        # Τελικός έλεγχος αν μπήκε
        for row_index, row in enumerate(self.routing_table):
            if node not in row:
                break
            if row_index == len(self.routing_table)-1:
                # Δεν έχει μπει επειδή δεν υπάρχει lcp με κανέναν. Εισάγουμε ελέγχοντας την απόσταση
                new_row = sorted(row[:-1] + [node])
                self.routing_table[row_index] = new_row

    def closest_preceding_node(self, node):
        """Βρίσκει τον κόμβο που είναι πιο κοντά στον κόμβο.
        :return: Closest Node to another.
        :rtype: Node"""
        min_distance = sys.maxsize  # max integer
        closest_node = node
        # ελέγχουμε πρώτα το leaf sets
        for leaf in ["left", "right"]:
            for n in self.leaf_set[leaf]:
                distance = self.distance(closest_node.node_id, n.node_id)
                if distance < min_distance:
                    min_distance = distance
                    closest_node = n
        # αν δε βρήκαμε τίποτα κοιτάμε routing table
        if closest_node == node:
            for index, row in enumerate(self.routing_table):
                for n in row:
                    if isinstance(n, Node):
                        distance = self.distance(node.node_id, n.node_id)
                        if distance < min_distance:
                            min_distance = distance
                            closest_node = n
        return closest_node

    def distance(self, n1, n2):
        """Υπολογισμός απόστασης μεταξύ 2 κόμβων στο δίκτυο
                :param str n1: First node's node id.
                :param str n2: First node's node id.
                :return: Distance between the 2 nodes' ids.
                :rtype: int"""
        n1 = int(n1)
        if isinstance(n2, Node):
            n2 = int(n2.node_id)
        else:
            n2 = int(n2)
        if n1 <= n2:
            return n2 - n1
        else:
            return self.nodes_num - n1 + n2

    def find_successor(self, key):
        """Βρίσκει τον κόμβο που έχει την ευθύνη για το key
        :param str key: Hashed Key.
        :return: Closest node to key.
        :rtype: Node or None"""
        closest_node = self.closest_preceding_node(self)
        if isinstance(self, Node) and isinstance(closest_node, Node):
            if self.lcp(key) == -1:
                # δεν έχουν κοινό prefix, ελέγχουμε routing table
                for n in self.routing_table:
                    if isinstance(n, Node) and n.lcp(key) != -1:
                        return n.find_successor(key)
            elif self.lcp(key) < closest_node.lcp(key):
                # ο έλεγχος περνάει στον κοντινότερο κόμβο
                return closest_node.find_successor(key)
            # αλλιώς κοιτάμε την απόσταση
            elif self.lcp(key) >= closest_node.lcp(key):
                dist1 = self.distance(self.node_id, key)
                dist2 = self.distance(closest_node.node_id, key)
                if dist2 > dist1:
                    return closest_node
                else:
                    return self
        else:
            print("ERROR: Not a Node")
            return None

    def update_leaf_set(self, node, action):
        """Ανανεώνει το leaf set για τον κόμβο.
        :param Node node: Node.
        :param str action: Either Insert or Delete. The action will be performed.
        :return: Nothing.
        :rtype: None"""
        node_place = self.closest_preceding_node(node)  # Κοντινότερος κόμβος
        if self.lcp(node.node_id) == -1 or node_place is None:
            pass
        else:
            # αν είναι μεγαλύτερο πρέπει να στο δεξί φύλλο
            if int(node.node_id) >= int(self.node_id):
                leaf = "right"
            else:
                leaf = "left"
            if action == "INSERT":
                self.leaf_set[leaf].append(node)
            elif action == "DELETE":
                # print(f"Node Place: {node_place}")  # Debug print
                # print(f"Leaf Set: {self.leaf_set}")  # Debug print
                self.leaf_set[leaf] = [x for x in self.leaf_set[leaf] if x != node]
            else:
                print("ERROR")
