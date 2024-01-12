import pprint
import sys
from filter_table import filter_table


class Node:
    """Pastry Node\n
    :param str node_id: Node's id
    :param int m: m-bit Keys and Nodes
    """

    nodes_cnt = 0

    def __init__(self, node_id, m=4):
        self.node_id = str(node_id)
        self.nodes_num = m**2
        self.leaf_set = {"left": [], "right": []}
        self.routing_table = [[None] * self.nodes_num for _ in range(m)]
        self.data = {}
        Node.nodes_cnt += 1

    def __str__(self):
        return str(self.node_id)

    def print_routing_table_and_leaf_set(self):
        print(f"ID: {self.node_id}")
        print(f"Κοντινότερος: {self.closest_preceding_node(self).node_id}")
        print(f"Δεδομένα: ")
        pprint.pprint(self.data, depth=5)
        print(f"Routing Table: ")
        for i in range(int(self.node_id)):
            print(
                f"{(self.node_id + 2 ** i) % self.nodes_num} : {self.routing_table[i].node_id}"
            )
        for leaf in ["left", "right"]:
            print(f"{leaf.capitalize()} Leaf:")
            for node in self.leaf_set[leaf]:
                print(node.node_id)

    def lcp(self, key):
        """Calculate the Longest Common Prefix (LCP) between the node's id and the key.
        :param str key: Node's id or data key
        :return: Least common prefix between self and key.
        :rtype: int"""
        key = str(key)
        self.node_id = str(self.node_id)
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
        # node_place = node_id.find_node_place(self.node_id)
        self.update_routing_table(node, "INSERT")
        self.update_leaf_set(node, "INSERT")

    def leave(self):
        """Αφαιρεί τον κόμβο"""
        closest_node = self.closest_preceding_node(self)
        # closest_node.routing_table = self.routing_table ?
        closest_node.data = {
            **closest_node.data,
            **self.data,
        }  # add node's data to the closest node with dict unpacking

    def find_node_place(self, node):  # ?
        """Βρίσκει τη θέση του κόμβου.
        Αν υπάρχει common prefix, ελέγχει ένα εκ των 2 φύλλων του leaf_set ανάλογα με την τιμή του node_id.
        Αλλιώς πηγαίνει στο routing table
        :param Node node: Node
        :return: Closest Node.
        :rtype: Node
        """
        # check if it is first or second node
        if Node.nodes_cnt == 1 or Node.nodes_cnt == 2:
            return self
        lcp = self.lcp(node.node_id)
        max_lcp = lcp  # find the longest prefix
        node_list = []
        if lcp == -1 or lcp == "":
            # check on Routing Table, it's not on the leaf set
            clean_routing_table = filter_table(self.routing_table)
            for n in clean_routing_table:
                lcp = n.lcp(node.node_id)
                if int(lcp) >= int(max_lcp):
                    max_lcp = lcp
                    node_list.append(n)
        if int(node.node_id) <= int(self.node_id):  # It's on Leaf set
            for n in self.leaf_set["left"]:
                lcp = n.lcp(node.node_id)
                if int(lcp) >= int(max_lcp):
                    max_lcp = lcp
                    node_list.append(n)
        elif int(node.node_id) > int(self.node_id):
            for n in self.leaf_set["right"]:
                lcp = n.lcp(node.node_id)
                if int(lcp) >= int(max_lcp):
                    max_lcp = lcp
                    node_list.append(n)
        if len(node_list) == 0:
            #  if it's not on the routing table
            min_distance = sys.maxsize
            closest_node = self
            clean_routing_table = filter_table(self.routing_table)
            for n in clean_routing_table:
                distance = self.distance(n.node_id, node.node_id)
                if distance < min_distance:
                    min_distance = distance
                    closest_node = node
            if closest_node != self:
                return closest_node.find_node_place(node)
        node_list.append(node)
        sorted_node_list = sorted(node_list, key=lambda node_in_list: node_in_list.node_id)
        if len(sorted_node_list) == 1:
            return self
        node_index = sorted_node_list.index(node)
        if node_index == 0:
            return sorted_node_list[node_index + 1]  # returns suc or pre if is it on edges of the list
        if node_index + 1 >= len(sorted_node_list):
            return sorted_node_list[node_index - 1]

        successor = sorted_node_list[node_index + 1]
        predecessor = sorted_node_list[node_index - 1]
        suc_distance = self.distance(self.node_id, successor.node_id)
        pre_distance = self.distance(self.node_id, predecessor.node_id)
        if suc_distance <= pre_distance:
            return successor
        else:
            return predecessor  # must have same prefix

    def update_routing_table(self, node, action):  # DONE
        """Ανανεώνει το routing table για τον κόμβο
        :param Node node: Node.
        :param str action: Either Insert or Delete. The action will be performed.
        :return: Nothing.
        :rtype: None
        """
        if action == "INSERT":  # TODO
            if Node.nodes_cnt == 1:
                self.routing_table.insert(0, node)
            else:
                node_place = self.find_node_place(node)
                if node_place.node_id != node.node_id:
                    least_dist = sys.maxsize  # max int
                    clean_routing_table = filter_table(self.routing_table)
                    for n in clean_routing_table:
                        dist = self.distance(node.node_id, n.node_id)
                        if dist < least_dist:
                            node_place = n
                nodes_index = self.routing_table.index(node_place)
                if self.routing_table[nodes_index] is not None:
                    self.routing_table.insert(nodes_index, node)
                else:
                    self.routing_table[nodes_index] = node
        elif action == "DELETE":
            self.routing_table = [
                None if x.node_id == node.node_id else x for x in self.routing_table
            ]
        else:
            print("ERROR")

    def update_leaf_set(self, node, action):  # DONE
        """Ανανεώνει το leaf set για τον κόμβο.
        :param Node node: Node.
        :param str action: Either Insert or Delete. The action will be performed.
        :return: Nothing.
        :rtype: None"""
        # node_id = node.node_id
        if self.lcp(node.node_id) != -1:
            if int(node.node_id) >= int(self.node_id):
                leaf = "right"
            else:
                leaf = "left"
            if action == "INSERT":  # TODO
                node_place = self.find_node_place(node)
                if node_place.node_id == node.node_id:
                    least_dist = sys.maxsize  # max int
                    for n in self.leaf_set[leaf]:
                        dist = self.distance(node.node_id, n.node_id)
                        if dist < least_dist:
                            node_place = n
                nodes_index = self.leaf_set[leaf].index(node_place)
                if self.leaf_set[leaf] is not None:
                    self.leaf_set[leaf].insert(nodes_index, node)
                else:
                    self.leaf_set[leaf][nodes_index] = node
            elif action == "DELETE":
                self.routing_table = [
                    None if x.node_id == node.node_id else x for x in self.leaf_set[leaf]
                ]
            else:
                print("ERROR")

    def closest_preceding_node(self, node):  # , h_key):  # TODO
        """Βρίσκει τον κόμβο που είναι πιο κοντά στον κόμβο.
        :return: Closest Node to Key.
        :rtype: Node"""
        min_distance = sys.maxsize  # max integer
        closest_node = node
        for leaf in ["left", "right"]:
            for n in self.leaf_set[leaf]:
                distance = self.distance(node.node_id, n.node_id)
                if distance < min_distance:
                    min_distance = distance
                    closest_node = n
        return closest_node

    def distance(self, n1, n2):
        """Υπολογισμός απόστασης μεταξύ 2 κόμβων στο δίκτυο"""
        n1 = int(n1)
        n2 = int(n2)
        if n1 <= n2:
            return n2 - n1
        else:
            return self.nodes_num - n1 + n2

    def find_successor(self, key):  # TODO
        """Βρίσκει τον κόμβο που έχει την ευθύνη για το key
        :param str key: Hashed Key.
        :return: Closest node to key.
        :rtype: Node"""
        if self.node_id == key:
            return self
        closest_node = self.closest_preceding_node(self)
        if self.lcp(key) == -1:
            # it has not the same prefix, check routing table
            clean_routing_table = filter_table(self.routing_table)
            for n in clean_routing_table:
                if n.lcp(key) != -1:
                    return n.find_successor(key)
        elif self.lcp(key) < closest_node.lcp(key):
            # we pass the key to the closest node
            return closest_node.find_successor(key)
        elif self.lcp(key) >= closest_node.lcp(key):
            dist1 = self.distance(self.node_id, key)
            dist2 = self.distance(closest_node.node_id, key)
            if dist2 > dist1:
                return closest_node
            else:
                return self
