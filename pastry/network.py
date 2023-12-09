from node import Node
import hashlib
from csv_to_dict import create_education_dictionary
import networkx as nx
import matplotlib.pyplot as plt


class Network:

    def __init__(self, m, node_ids):
        self.nodes = []
        self.m = m
        self.r_size = m ** 2
        self.first_node = node_ids

    def __str__(self):
        start = '---------------\n'
        quantity = f'Πλήθος: {len(self.nodes)} κόμβοι\n'
        capacity = f'Χωρητικότητα: {self.r_size} κόμβοι\n'
        routing_table_size = f'Μέγεθος Routing Table: {self.m}\n'
        first_node_id = f'Πρώτος Κόμβος: {self.first_node.node_id}\n'
        end = '---------------\n'
        return f'{start}{quantity}{capacity}{routing_table_size}{first_node_id}{end}'

    def print_network(self):
        print(self)

    def add_first_node(self, node_id):
        """Αρχικοποίηση του 1ου κόμβου"""
        node = Node(node_id, self.m)
        self.nodes.append(node)

    def update_routing_tables(self):
        """Ανανεώνει το routing table για όλους τους κόμβους του δικτύου"""
        self.first_node.update_routing_table()
        curr = self.first_node.routing_table[0]

        while curr != self.first_node:
            curr.update_routing_table()
            curr = curr.routing_table[0]

    def calculate_prefix(self, key):
        """
            Calculate the longest common prefix (LCP) between the current node's identifier and the destination key.
            Use the LCP to determine the next hop in the routing table.
            Forward the message to the node with the closest identifier in terms of the LCP.
            """
        lcp = 0
        while lcp < len(key) and lcp < len(self.identifier) and key[lcp] == self.identifier[lcp]:
            lcp += 1
        return lcp

    def hash_function(self, key):
        """Κάνει hash στο key του κόμβου"""
        hs = hashlib.md5(b'node')
        return hs.hexdigest()

    def add_node(self, node_id):
        """Προσθέτει έναν κόμβο"""
        pass

    def remove_node(self, node_id):
        """Αφαιρεί έναν κόμβο"""
        pass
        self.update_routing_tables()

    def lookup(self, data, threshold):
        """Ψάχνει για το key στους κόμβους """
        pass

    def add_data(self, n):
        """Βάζει τα δεδομένα στους κόμβους"""
        my_dict = create_education_dictionary(n)
        for key, values in my_dict.items():
            node = self.first_node

            h_key = self.hash_function(key)
            print(
                f'Αποθήκευση του key \'{key}\' με hash {h_key} στον κόμβο {node.find_successor(h_key).node_id}')
            suc = node.find_successor(h_key)

            suc.data[h_key] = {'key': key, 'value': values}

    def visualize_pastry(self):
        pass
