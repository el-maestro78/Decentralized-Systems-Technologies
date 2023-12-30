from node import Node
from hash import hash_function
from csv_to_dict import create_education_dictionary
import networkx as nx
import matplotlib.pyplot as plt

"""
#  DONE
#  ?
#  TODO
"""


class Network:
    """Pastry Network
    :param int m: number of bits of the id, routing table size
    :param list node_ids: Node ids list
    """

    def __init__(self, m, node_ids):
        self.nodes = []
        self.m = m
        self.r_size = m**2
        self.add_first_node(node_ids[0])
        self.first_node = self.nodes[0]
        self.pastry_ring = nx.Graph()

    def __str__(self):
        start = "---------------\n"
        quantity = f"Πλήθος: {len(self.nodes)} κόμβοι\n"
        capacity = f"Χωρητικότητα: {self.r_size} κόμβοι\n"
        routing_table_size = f"Μέγεθος Routing Table: {self.m}\n"
        first_node_id = f"Πρώτος Κόμβος: {self.first_node.node_id}\n"
        end = "---------------\n"
        return f"{start}{quantity}{capacity}{routing_table_size}{first_node_id}{end}"

    def print_network(self):  # DONE
        print(self)
        for node in self.nodes:
            print(node.node_id)
            node.print_routing_table()
            print("---------------")

    def add_first_node(self, node_id):  # DONE
        """Αρχικοποίηση του 1ου κόμβου"""
        node = Node(node_id, self.m)
        self.nodes.append(node)

    def update_leaf_sets(self):
        for node in self.nodes:
            node.update_leaf_set()

    def update_routing_tables(self):  # ?
        """Ανανεώνει το routing table για όλους τους κόμβους του δικτύου"""
        # self.first_node.update_routing_table()
        # for node in self.nodes:
        #    if node is not self.first_node:
        #       node.update_routing_table()
        for node in self.nodes:
            node.update_routing_table()

    def add_node(self, node_id):  # DONE
        """Προσθέτει έναν κόμβο"""
        new_node = Node(node_id, self.m)
        self.nodes.append(new_node)
        node = self.nodes[-1]
        node.join(self.first_node)
        self.update_routing_tables()
        self.update_leaf_sets()

    def remove_node(self, node_id):  # DONE
        """Αφαιρεί έναν κόμβο"""
        node_id.leave()
        for node in self.nodes:
            if node_id in node.routing_table:
                node.routing_table.remove(node_id)
        self.update_routing_tables()

        for node in self.nodes:
            if node_id in node.leaf_set["left"]:
                node.leaf_set["left"].remove(node_id)
        for node in self.nodes:
            if node_id in node.leaf_set["right"]:
                node.leaf_set["right"].remove(node_id)
        self.update_leaf_sets()

    def lookup(self, data, threshold):  # TODO
        """Ψάχνει για το key στους κόμβους"""
        pass

    def add_data(self, n):  # TODO
        """Βάζει τα δεδομένα στους κόμβους"""
        my_dict = create_education_dictionary(n)
        for key, values in my_dict.items():
            node = self.first_node

            h_key = hash_function(key)
            print(
                f"Αποθήκευση του key '{key}' με hash {h_key} στον κόμβο {node.find_successor(h_key).node_id}"
            )
            suc = node.find_successor(h_key)

            suc.data[h_key] = {"key": key, "value": values}

    def visualize_pastry(self):
        pass
