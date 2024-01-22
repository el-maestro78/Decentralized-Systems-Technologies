from node import Node
from hash import hash_function
from csv_to_dict import create_education_dictionary
import networkx as nx
import matplotlib.pyplot as plt
from filter_table import filter_table

class Network:
    """Pastry Network
    :param int m: number of bits of the id, routing table size
    :param list node_ids: Node ids list
    """

    def __init__(self, m, node_ids):
        self.nodes = []
        self.m = m
        self.r_size = 2 ** m
        self.add_first_node(node_ids[0])
        self.first_node = self.nodes[0]
        self.pastry_ring = nx.Graph()
        self.node_ids = node_ids
        node_ids.pop(0)

    def __str__(self):
        start = "---------------\n"
        quantity = f"Πλήθος: {len(self.nodes)} κόμβοι\n"
        capacity = f"Χωρητικότητα: {self.r_size} κόμβοι\n"
        routing_table_size = f"Μέγεθος Routing Table: {self.m}\n"
        first_node_id = f"Πρώτος Κόμβος: {self.first_node.node_id}\n"
        end = "---------------\n"
        return f"{start}{quantity}{capacity}{routing_table_size}{first_node_id}{end}"

    def print_network(self):
        print(self)
        for node in self.nodes:
            print(node.node_id)
            node.print_routing_table()
            print("---------------")

    def add_first_node(self, node_id):
        """Αρχικοποίηση του 1ου κόμβου"""
        node = Node(node_id, self.m)
        self.nodes.append(node)

    def update_sets_and_tables(self, node, action):
        self.update_routing_tables(node, action)
        self.update_leaf_sets(node, action)

    def update_leaf_sets(self, node, action):
        """Ανανεώνει τα leaf sets για όλους τους κόμβους του δικτύου
        :param Node node: Node.
        :param str action: Either Insert or Delete. The action will be performed.
        :return: Nothing.
        :rtype: None
        """
        if action != "INSERT" and action != "DELETE":
            print("Error")
        else:
            for n in self.nodes:
                n.update_leaf_set(node, action)

    def update_routing_tables(self, node, action):
        """Ανανεώνει το routing table για όλους τους κόμβους του δικτύου
        :param Node node: Node.
        :param str action: Either Insert or Delete. The action will be performed.
        :return: Nothing.
        :rtype: None"""
        if action != "INSERT" and action != "DELETE":
            print("Error")
        else:
            for n in self.nodes:
                n.update_routing_table(node, action)

    def add_node(self, node_id):
        """Προσθέτει έναν κόμβο"""
        new_node = Node(node_id, self.m)
        self.nodes.append(new_node)
        node = self.nodes[-1]
        for n in self.nodes:
            n.join(new_node)
        # self.first_node.join(new_node)
        self.update_routing_tables(new_node, "INSERT")
        self.update_leaf_sets(new_node, "INSERT")

    def remove_node(self, node):
        """Αφαιρεί έναν κόμβο"""
        node.leave()
        self.update_routing_tables(node, "DELETE")
        self.update_leaf_sets(node, "DELETE")

    def lookup(self, data, threshold):
        """Ψάχνει για το key στους κόμβους"""
        h_key = hash_function(data)
        node = self.first_node
        node = node.find_successor(h_key)
        # current_node = self
        found_data = node.data.get(h_key, None)
        if found_data is not None:
            found = False
            print(
                f'Βρέθηκε το key \'{data}\' στον κόμβο {node.node_id} με hash {h_key}')
            for scientists in found_data['value']:
                if scientists[1] >= threshold:
                    found = True
                    print(
                        f'{scientists[0]}: {scientists[1]} βραβεία')
            if not found:
                print(f'Δεν υπάρχουν επιστήμονες με >= {threshold} βραβεία')
        else:
            print(f'Το \'{data}\' δεν υπάρχει σε κανένα κόμβο')
        """
        while True:
            # Calculate the LCP between the current node and the key
            lcp = current_node.lcp(data)
            # Check if the key matches the current node's identifier
            if lcp == len(current_node.node_id) and lcp == len(data):
                return current_node  # Found the responsible node
            # Check if the LCP points to a node in the routing table
            if lcp < len(current_node.node_id):
                next_hop = current_node.routing_table[lcp][
                    int(current_node.node_id[lcp], 16)
                ]
                if next_hop:
                    current_node = next_hop
                else:
                    return current_node  # No more specific route in the routing table
            # Check the leaf set for a closer node
            elif lcp < len(data):
                if int(data[lcp], 16) < int(current_node.node_id[lcp], 16):
                    current_node = current_node.leaf_set["left"]
                else:
                    current_node = current_node.leaf_set["right"]
            # No specific route found, return the current node
            else:
                return current_node
        """

    def add_data(self, n):
        """Βάζει τα δεδομένα στους κόμβους"""
        my_dict = create_education_dictionary(n)
        for key, values in my_dict.items():
            node = self.first_node
            h_key = hash_function(key)
            suc = node.find_successor(h_key)
            if suc is not None:
                print(
                    f"Αποθήκευση του key '{key}' με hash {h_key} στον κόμβο {suc.node_id}"
                )
                suc.data[h_key] = {"key": key, "value": values}
            else:
                print(f"Δεν βρέθηκε διάδοχος για το key '{key}' με hash {h_key}")

    def visualize_pastry(self):
        plt.figure()
        self.pastry_ring.clear()
        sorted_nodes = sorted(self.nodes, key=lambda x: x.node_id, reverse=True)
        # Προσθέτει τους κόμβους στο γράφο
        for node in sorted_nodes:
            self.pastry_ring.add_node(node.node_id)
        # Προσθέτει ακμές από κάθε κόμβο στον επόμενο του
        for i in range(len(sorted_nodes)):
            # node = sorted_nodes[i]
            # # successor = sorted_nodes[i].find_successor(node)
            # successor = sorted_nodes[i].closest_preceding_node(node)
            # self.pastry_ring.add_edge(sorted_nodes[i].node_id, successor.node_id)
            # # Προσθέτει ακμές σε κάθε κόμβο του fingers table του
            # for j in sorted_nodes[i].routing_table:
            #     if isinstance(j, Node):
            #         self.pastry_ring.add_edge(sorted_nodes[i].node_id, j.node_id)
            node = sorted_nodes[i]
            for sublist in node.routing_table:
                for rt_node in sublist:
                    if isinstance(rt_node, Node):
                        if self.pastry_ring.has_edge(node.node_id, rt_node.node_id):
                            pass
                        else:
                            self.pastry_ring.add_edge(node.node_id, rt_node.node_id)
                # # if node.node_id == n.node_id and self.pastry_ring.has_edge(n, Node):
                # for sublist in n.routing_table:
                #     for rt_node in sublist:
                #         if isinstance(rt_node, Node):
                #             if node.node_id == rt_node.node_id:
                #                 if self.pastry_ring.has_edge(node.node_id, rt_node.node_id):
                #                     pass
                #                 else:
                #                     self.pastry_ring.add_edge(node.node_id, rt_node.node_id)
        rotated_pos = {
            node: (-y, x)
            for node, (x, y) in nx.circular_layout(self.pastry_ring).items()
        }
        nx.draw(
            self.pastry_ring,
            rotated_pos,
            with_labels=True,
            node_color="lightgreen",
            node_size=1000,
            font_size=10,
        )
        plt.title("Pastry DHT")
        plt.gca().set_aspect("equal", adjustable="box")
        plt.pause(0.001)
        plt.ioff()
