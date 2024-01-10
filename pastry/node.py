import pprint
import sys


class Node:
    """Pastry Node\n
    :param str node_id: Node's id
    :param int m: m-bit Keys and Nodes
    """

    nodes_cnt = 0

    def __init__(self, node_id, m=4):
        self.node_id = str(node_id)
        self.nodes_num = 2**m  # Network's ring size
        self.leaf_set = {"left": [], "right": []}
        self.routing_table = [[None] * self.nodes_num for _ in range(m)]
        self.data = {}
        Node.nodes_cnt += 1

    def __str__(self):
        return str(self.node_id)

    def print_routing_table_and_leaf_set(self):  # DONE
        print(f"ID: {self.node_id}")
        print(f"Κοντινότερος: {self.closest_preceding_node().node_id}")
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

    def lcp(self, key):  # DONE
        """Calculate the Longest Common Prefix (LCP) between the node's id and the key.
        :param str key: Node's id or data key
        :return: Least common prefix between self and key.
        :rtype: int"""
        key = str(key)
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

    def join(self, node_id):  # DONE
        """Βάζει τον κόμβο στο δίκτυο.
        Η τιμή του κόμβου είναι ήδη hashed
        :param str node_id: Node's ID
        :return: Nothing.
        :rtype: None
        """
        # node_place = node_id.find_node_place(self.node_id)
        self.update_routing_table(node_id, "INSERT")
        self.update_leaf_set(node_id, "INSERT")

    def leave(self):  # ?
        """Αφαιρεί τον κόμβο"""
        closest_node = self.closest_preceding_node()
        # closest_node.routing_table = self.routing_table ?
        closest_node.data = {
            **closest_node.data,
            **self.data,
        }  # add node's data to the closest node with dict unpacking

    def find_node_place(self, node_id):  # ?
        """Βρίσκει τη θέση του κόμβου.
        Αν υπάρχει common prefix, ελέγχει ένα εκ των 2 φύλλων του leaf_set ανάλογα με την τιμή του node_id.
        Αλλιώς πηγαίνει στο routing table
        :param str node_id: Node's ID
        :return: Closest Node node.
        :rtype: Node
        """
        # check if it is first or second node
        if self.nodes_cnt == 0 or self.nodes_cnt == 1:
            return self.nodes_cnt
        lcp = self.lcp(node_id)
        max_lcp = lcp  # find the longest prefix
        node_list = []
        if int(node_id) <= int(self.node_id):
            for node in self.leaf_set["left"]:
                lcp = node.lcp(node_id)
                print(f"left {lcp}")
                if lcp == -1 or lcp == "" or lcp is None:
                    continue
                elif int(lcp) >= int(max_lcp):
                    max_lcp = lcp
                    node_list.append(node.node_id)
        elif int(node_id) > int(self.node_id):
            for node in self.leaf_set["right"]:
                lcp = node.lcp(node_id)
                if lcp == -1 or lcp == "" or lcp is None:
                    continue
                elif int(lcp) >= int(max_lcp):
                    max_lcp = lcp
                    node_list.append(node.node_id)
        if lcp == -1 or lcp == "" or lcp is None:
            for node in self.routing_table:
                lcp = node.lcp(node_id)
                if lcp == -1 or lcp == "" or lcp is None:
                    continue
                elif int(lcp) >= int(max_lcp):
                    max_lcp = lcp
                    node_list.append(node.node_id)
        node_list.append(self.node_id)
        if len(node_list) == 1:
            return self.node_id
        node_list.sort()
        node_index = node_list.index(node_id)
        # print(f'Nodes Index: {node_index}')
        if node_index == 0:
            return node_list[node_index + 1]  # returns suc or pre if is it on edges of the list
        if node_index + 1+ 1 > len(node_list):
            return node_list[node_index - 1]

        successor = node_list[node_index + 1]
        predecessor = node_list[node_index - 1]
        suc_distance = self.distance(self.node_id, successor.node_id)
        pre_distance = self.distance(self.node_id, predecessor.node_id)
        if suc_distance <= pre_distance:
            return successor
        else:
            return predecessor  # must have same prefix

    def update_routing_table(self, node_id, action):  # DONE
        """Ανανεώνει το routing table για τον κόμβο"""
        if action == "INSERT":
            # if node_id in self.routing_table:
            if Node.nodes_cnt == 0:
                self.routing_table.insert(0, node_id)
            else:
                node_place = self.find_node_place(node_id)
                if node_place.node_id == node_id:  # TODO
                    least_dist = sys.maxsize  # max int
                    for node in self.routing_table:
                        dist = self.distance(node.node_id, node_id)
                        if dist < least_dist:
                            node_place = node
                nodes_index = self.routing_table.index(node_place)
                if self.routing_table[nodes_index] is not None:
                    self.routing_table.insert(nodes_index, node_id)
                else:
                    self.routing_table[nodes_index] = node_id
        elif action == "DELETE":
            self.routing_table = [
                None if x == node_id else x for x in self.routing_table
            ]
        else:
            print("ERROR")

    def update_leaf_set(self, node_id, action):  # DONE
        """Ανανεώνει το leaf set για τον κόμβο.

        :param str node_id: Node's id.
        :param str action: Either INSERT or DELETE.
        :return: None"""
        if self.lcp(node_id) != -1:
            if int(node_id) >= int(self.node_id):
                leaf = "right"
            else:
                leaf = "left"
            if action == "INSERT":  # TODO
                node_place = self.find_node_place(node_id)
                if node_place.node_id == node_id:
                    least_dist = sys.maxsize  # max int
                    for node in self.leaf_set[leaf]:
                        dist = self.distance(node.node_id, node_id)
                        if dist < least_dist:
                            node_place = node
                nodes_index = self.leaf_set[leaf].index(node_place)
                if self.leaf_set[leaf] is not None:
                    self.leaf_set[leaf].insert(nodes_index, node_id)
                else:
                    self.leaf_set[leaf][nodes_index] = node_id
            elif action == "DELETE":
                self.routing_table = [
                    None if x == node_id else x for x in self.leaf_set[leaf]
                ]
            else:
                print("ERROR")

    def closest_preceding_node(self):  # , node, h_key):  # TODO
        """Βρίσκει τον κόμβο που είναι πιο κοντά στον κόμβο."""
        min_distance = sys.maxsize  # max integer
        closest_node = self
        for leaf in ["left", "right"]:
            for node in self.leaf_set[leaf]:
                distance = self.distance(self.node_id, node.node_id)
                if distance < min_distance:
                    min_distance = distance
                    closest_node = node

        return closest_node  # closest_node.node_id
        # if closest_node != self:
        #     return closest_node
        # else:
        #     return -1

    def distance(self, n1, n2):  # DONE
        """Υπολογισμός απόστασης μεταξύ 2 κόμβων στο δίκτυο"""
        n1 = int(n1)
        n2 = int(n2)
        if n1 <= n2:
            return n2 - n1
        else:
            return self.nodes_num - n1 + n2

    def find_successor(self, key):
        """Βρίσκει τον κόμβο που έχει την ευθύνη για το key"""
        closest_node = self.closest_preceding_node()
        if self.node_id == key:
            return self
        if self.lcp(key) <= closest_node.lcp(key):
            return closest_node.find_successor(key)
        elif self.lcp(key) >= closest_node.lcp(key):
            dist1 = self.distance(self.node_id, key)
            dist2 = self.distance(closest_node.node_id, key)
            if dist2 > dist1:
                return closest_node
            else:
                return self
