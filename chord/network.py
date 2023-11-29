from node import Node
from csv_to_dict import create_education_dictionary
import hashlib
import networkx as nx
import matplotlib.pyplot as plt

class Network():
    def __init__(self, m, node_ids):
        self.nodes = []
        self.m = m
        self.r_size = 2 ** m
        self.add_first_node(node_ids[0])
        self.first_node = self.nodes[0]
        node_ids.pop(0)
        self.chord_ring = nx.Graph()
    
    # Δείχνει τα στοιχεία του δικτύου
    def __str__(self):
        return f'---------------\nΠλήθος: {len(self.nodes)} κόμβοι\nΧωρητικότητα: {self.r_size} κόμβοι\nΜέγεθος Fingers Table: {self.m}\nΠρώτος Κόμβος: {self.first_node.node_id}\n---------------'

    # Δείχνει τα fingers table και data όλων των κόμβων
    def print_network(self):
        print(self)
        for node in self.nodes:
            node.print_fingers_table()
            print('---------------')

    def add_first_node(self, node_id):
        node = Node(node_id, self.m)
        self.nodes.append(node)

    # Ανανεώνει το fingers table για όλους τους κόμβους του δικτύου
    def update_fingers_tables(self, node_left = None, leave = False):
        if leave:
            self.first_node.update_fingers_table(node_left, leave = True)
        else:
            self.first_node.update_fingers_table()

        curr = self.first_node.fingers_table[0]

        while curr != self.first_node:
            if leave:
                curr.update_fingers_table(node_left, leave = True)
            else:
                curr.update_fingers_table()
            curr = curr.fingers_table[0]


    # Κατακερματίζει το key
    def hash_function(self, key):
        num_bits = Node.m

        # μετατροπή του key σε hex και έπειτα σε bytes
        bt = hashlib.sha1(str.encode(key)).digest()

        # πόσα bytes θέλουμε για το id
        req_bytes = (num_bits + 7) // 8

        # μετατροπή σε int από bits
        hashed_id = int.from_bytes(bt[:req_bytes], 'big')

        # αναδίπλωση του κατακερματεισμένου id
        if num_bits % 8:
            hashed_id >>= 8 - num_bits % 8

        return hashed_id

    # Προσθέτει έναν κόμβο
    def add_node(self, node_id):
        new_node = Node(node_id, self.m)
        self.nodes.append(new_node)   
        node = self.nodes[-1]
        node.join(self.first_node)
        self.update_fingers_tables()

    # Αφαιρεί έναν κόμβο
    def remove_node(self, node_id):
        node = list(filter(lambda temp_node: temp_node.node_id ==
                               node_id, self.nodes))[0]
        node.leave()
        self.nodes.remove(node)
        # Καλεί την update με παράμετρο leave = True
        self.update_fingers_tables(node, leave = True)
        self.update_fingers_tables()

    # Ψάχνει για το key στους κόμβους
    def lookup(self, data, threshold):
        h_key = self.hash_function(data)
        node = self.first_node
        node = node.find_successor(h_key)

        found_data = node.data.get(h_key, None)
        if found_data != None:
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

    # Βάζει τα δεδομένα στους κόμβους
    def add_data(self, n):
        my_dict = create_education_dictionary(n)
        for key, values in my_dict.items():
            node = self.first_node

            h_key = self.hash_function(key)
            print(
            f'Αποθήκευση του key \'{key}\' με hash {h_key} στον κόμβο {node.find_successor(h_key).node_id}')
            suc = node.find_successor(h_key)

            suc.data[h_key] = {'key': key, 'value': values}

    def visualize_chord(self):
        plt.figure()
        self.chord_ring.clear()
        sorted_nodes = sorted(self.nodes, key=lambda x: x.node_id, reverse = True)
        # Προσθέτει τους κόμβους στο γράφο
        for node_id in sorted_nodes:
            self.chord_ring.add_node(node_id)

        # Προσθέτει ακμές από κάθε κόμβο στον επόμενο του
        for i in range(len(sorted_nodes)):
            self.chord_ring.add_edge(sorted_nodes[i], sorted_nodes[i].successor)
            # Προσθέτει ακμές σε κάθε κόμβο του fingers table του
            for j in sorted_nodes[i].fingers_table:
                self.chord_ring.add_edge(sorted_nodes[i], j)
        
        # Περιστρέφει το γράφο για να είναι ο μικρότερος κόμβος δεξιά
        rotated_pos = {node: (-y, x) for node, (x, y) in nx.circular_layout(self.chord_ring).items()}

        nx.draw(self.chord_ring, rotated_pos, with_labels=True, node_color='skyblue', node_size=1000, font_size=10)
        
        plt.title("Chord DHT")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.pause(0.001)
        plt.ioff() 