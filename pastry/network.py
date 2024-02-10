from node import Node
from hash import hash_function
from csv_to_dict import create_education_dictionary
import networkx as nx
import matplotlib.pyplot as plt
from filter_table import filter_table
import sys


class Network:
    """Pastry Network
    :param int m: number of bits of the id, routing table size
    :param list node_ids: Node ids list
    """

    def __init__(self, m, node_ids):
        self.nodes = []
        self.m = m
        self.r_size = 2 ** m
        # self.add_first_node(node_ids[0])
        self.first_node = node_ids[0]
        self.pastry_ring = nx.Graph()
        self.node_ids = node_ids
        # node_ids.pop(0)

    def __str__(self):
        """Τυπώνει τα δεδομένα όλου του δικτύου"""
        start = "---------------\n"
        quantity = f"Πλήθος: {len(self.nodes)} κόμβοι\n"
        capacity = f"Χωρητικότητα: {self.r_size} κόμβοι\n"
        routing_table_size = f"Μέγεθος Routing Table: {self.m}\n"
        first_node_id = f"Πρώτος Κόμβος: {self.first_node.node_id}\n"
        end = "---------------\n"
        return f"{start}{quantity}{capacity}{routing_table_size}{first_node_id}{end}"

    def print_network(self):
        """Τυπώνει τα Routing Tables όλου του δικτύου"""
        print(self)
        for node in self.nodes:
            print(node.node_id)
            node.print_routing_table()
            print("---------------")

    def get_node(self, nodeID):
        """Επιστρέφει τον κόμβο με το συγκεκριμένο node_id.
        :param int nodeID: Το node_id του κόμβου που ψάχνουμε.
        :return: Ο κόμβος με το συγκεκριμένο node_id, αν υπάρχει. Διαφορετικά, επιστρέφει None.
        :rtype: Node or None"""
        for node in self.nodes:
            if node.node_id == nodeID:
                return node
        return None

    def add_first_node(self, node_id):
        """Αρχικοποίηση του 1ου κόμβου
        :param str node_id: Το node_id του κόμβου που εισάγεται.
        :return: Nothing.
        :rtype: None"""
        node = Node(node_id, self.m)
        self.nodes.append(node)

    def update_sets_and_tables(self, node, action):
        """Ανανεώνει τα leaf sets και τα routing tables για όλους τους κόμβους του δικτύου"""
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
        """Προσθέτει έναν κόμβο
                :param str node_id: Node id of the new node.
                :return: Nothing.
                :rtype: None
        """
        new_node = Node(node_id, self.m)  # δημιουργείται ο νέος κόμβος
        self.nodes.append(new_node)
        for n in self.nodes:
            n.join(new_node)  # τον προσθέτουν όλοι οι υπόλοιποι
        # ενημερώνουν τα tables
        self.update_routing_tables(new_node, "INSERT")
        self.update_leaf_sets(new_node, "INSERT")

    def remove_node(self, node):
        """Αφαιρεί έναν κόμβο
         :param Node node: Node we remove from the network.
         :return: Nothing.
         :rtype: None
        """
        node.leave()  # Ο κόμβος χάνει τα δεδομένα του
        if node in self.nodes:
            self.nodes.remove(node)  # αφαιρείται από την λίστα αν δεν έχει ήδη αφαιρεθεί
        for n in self.nodes:  # αφαιρείται από τα routing & leaf tables.
            n.update_routing_table(node, "DELETE")
            n.update_leaf_set(node, "DELETE")

    def lookup(self, data, threshold):
        """Ψάχνει για το key στους κόμβους
        :param str data: Data we want to retrieve from the network.
        :param int threshold: User defined threshold for what we are looking for.
        :return: Nothing.
        :rtype: None
        """
        h_key = hash_function(data)
        # i = 0
        # node = self.nodes[i]
        # node = node.find_successor(h_key)
        # while node is None:
        #     i += 1
        #     node = self.nodes[i]
        #     node = node.find_successor(h_key)
        node = self.find_closest_to_key(h_key)
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

    def add_data(self, n):
        """Βάζει τα δεδομένα στους κόμβους
        :param int n: User defined threshold for what we are looking for.
        :return: Nothing.
        :rtype: None"""
        my_dict = create_education_dictionary(n)
        for key, values in my_dict.items():
            h_key = hash_function(key)
            suc = self.find_closest_to_key(h_key)
            if suc is not None:
                print(
                    f"Αποθήκευση του key '{key}' με hash {h_key} στον κόμβο {suc.node_id}"
                )
                suc.data[h_key] = {"key": key, "value": values}
            else:
                print(f"Δεν βρέθηκε διάδοχος για το key '{key}' με hash {h_key}")

    def find_closest_to_key(self, key):
        """Βρίσκει τον κοντινότερο στο key ανάμεσα σε όλους τους κόμβους
        ώστε να αποθηκευτούν εκεί data με το αντίστοιχο key.
        :param str key: Το data key που πρέπει να αποθηκευτεί στον κοντινότερο κόμβο
        :returns: Κοντινότερος κόμβος
        :rtype: Node"""
        not_data_nodes = []
        for n in self.nodes:
            if n.data == {}:  # ελέγχουμε αν ο κόμβος έχει ήδη δεδομένα, κάνουμε balancing το δίκτυο
                not_data_nodes.append(n)
        if len(not_data_nodes) > 0:
            # Υπάρχει έστω και ένας χωρίς δεδομένα, τα παίρνει αυτός. Πρέπει να έχει lcp
            closest = self.static_get_lcp(key, not_data_nodes)
        else:
            # Έχουν όλοι δεδομένα, βρές αυτόν με το μεγαλύτερο lcp
            closest = self.static_get_lcp(key, self.nodes)
        return closest

    def static_get_lcp(self, key, nodes_list):
        """Υπολογίζει το max lcp για όλους τους κόμβους και επιστρέφει τον κόμβο που το έχει
        :param str key: Το data key που πρέπει να αποθηκευτεί στον κοντινότερο κόμβο
        :param list nodes_list: Η λίστα με τους κόμβους που θέλουμε να ψάξουμε
        :returns: Κοντινότερος κόμβος
        :rtype: Node"""
        min_lcp = sys.maxsize
        closest = nodes_list[0]
        for n in nodes_list:
            new_lcp = n.lcp(key)
            if new_lcp > min_lcp:
                min_lcp = new_lcp
                closest = n
        return closest

    def visualize_pastry(self):
        """Οπτικοποιεί το δίκτυο Pastry"""
        plt.figure()
        self.pastry_ring.clear()
        sorted_nodes = sorted(self.nodes, key=lambda x: x.node_id, reverse=True)
        # Προσθέτει τους κόμβους στο γράφο
        for node in sorted_nodes:
            self.pastry_ring.add_node(node.node_id)
        # Προσθέτει ακμές από κάθε κόμβο στον επόμενο του
        for i in range(len(sorted_nodes)):
            node = sorted_nodes[i]
            for sublist in node.routing_table:
                for rt_node in sublist:
                    if isinstance(rt_node, Node):
                        if self.pastry_ring.has_edge(node.node_id, rt_node.node_id):
                            pass
                        else:
                            self.pastry_ring.add_edge(node.node_id, rt_node.node_id)
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

    def visualize_connections(self):
        """Οπτικοποιεί τις συνδέσεις του Pastry όπου γίνονται τα hops"""
        plt.figure()
        self.pastry_ring.clear()
        sorted_nodes = sorted(self.nodes, key=lambda x: x.node_id, reverse=True)
        # Προσθέτει τους κόμβους στο γράφο
        for node in sorted_nodes:
            self.pastry_ring.add_node(node.node_id)
        # Προσθέτει ακμές από κάθε κόμβο στον επόμενο του
        for i in range(len(sorted_nodes)):
            node = sorted_nodes[i]
            successor = sorted_nodes[i].find_successor(node)  # πάνω έχει το routing table
            self.pastry_ring.add_edge(node.node_id, successor.node_id)
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
