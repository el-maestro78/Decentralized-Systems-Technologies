import csv
import itertools

m = 4

class Node:
    def __init__(self, node_id, data = None):
        self.node_id = node_id
        self.successor = None
        self.predecessor = None
        self.finger_table = [self]*m
        self.data = data

    def find_successor(self, key):
        if self.node_id == key:
            return self
        elif self.node_id < key <= self.successor.node_id:
            return self.successor
        else:
            # Find the node responsible for the key in the finger table
            for i in range(m-1, 0, -1):
                if i in self.finger_table:
                    if self.finger_table[i].node_id <= key:
                        return self.finger_table[i].find_successor(key)
            return self

    def join(self, existing_node):
        self.successor = existing_node.find_successor(self.node_id)
        self.predecessor = self.successor.predecessor
        self.successor.predecessor = self
        self.predecessor.successor = self

        # Initialize finger table of the joining node
        for i in range(m):
            self.update_finger_table(self, i)

    def update_finger_table(self, other, i):
        # Calculate the start of the range for this finger table entry
        start = (self.node_id + 2 ** i) % (2 ** m)
        end = (start + 2 ** i) % (2 ** m)

        # Check if the other node falls within the range (exclusive)
        if start <= other.node_id < end:
            self.finger_table[i] = other
            p = self.predecessor
            p.update_finger_table(other, i)


    def print_finger_table(self):
        print(f"Finger table for Node {self.node_id}:")
        for i in range(0, m):
            print(f"  {i}: {self.finger_table[i].node_id}")
    
    def print_node(self):
        print(f"Node {self.node_id}: Successor = {self.successor.node_id}, Predecessor = {self.predecessor.node_id}")
        print(f"Education: {self.data['education']}")
        print(f"Scientist/Awards: {self.data['scientist']}")

# Συνάρτηση που δημιουργεί ένα dictionary για κάθε εγγραφή στο csv 
# και έχει ως key: education και ως value: surname, awards και επιστρέφει το dictionary
def create_education_dictionary(csv_file):
    education_dict = {}

    with open(csv_file, 'r', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            education = row['Education']
            surname = row['Surname']
            awards = row['#Awards']

            # Αν το education key δεν είναι στο dictionary το προσθέτει
            if education not in education_dict:
                education_dict[education] = [(surname, awards)]
            else:
                # Αν υπάρχει ήδη, το προσθέτει το στην ήδη υπάρχουσα λίστα 
                education_dict[education].append((surname, awards))
    
    # Αφαιρεί από το dictionary επιστήμονες με άδειο education
    education_dict.pop("[]")

    return education_dict

# Συνάρτηση που δημιουργεί ένα node για κάθε key/value pair του dictionary 
# και επιστρέφει μια λίστα με όλα τα αντικείμενα που δημιούργησε
def create_chord_nodes(education_dict):
    chord_nodes = []
    node_id = 0

    for key, value in education_dict.items():
        node_data = {'education': key, 'scientist': value}
        node = Node(node_id, node_data)
        chord_nodes.append(node)
        node_id += 1

    return chord_nodes

# Συνάρτηση που δημιουργεί το δίκτυο με τα nodes
def create_nodes_network(chord_nodes):
    for node_num in range(0, len(chord_nodes)):
        chord_nodes[node_num].join(chord_nodes[0])

        
if __name__ == '__main__':

    # Το path που περιέχει το csv αρχείο με τους επιστήμονες
    CSV_PATH = './computer_scientists_data.csv'

    # Αποθηκεύει το dictionary με τους επιστήμονες σε μια μεταβλητή
    education_dictionary = create_education_dictionary(CSV_PATH)

    # Κρατάει μόνο τα n πρώτα στοιχεία του dictionary 
    n = 12
    education_dictionary = dict(itertools.islice(education_dictionary.items(), n))

    # Αποθηκεύει τη λίστα με όλα τα nodes αντικείμενα σε μια μεταβλητή
    chord_nodes = create_chord_nodes(education_dictionary)

    print(len(chord_nodes)) 

    # Δημιουργεί το δίκτυο με τα nodes
    create_nodes_network(chord_nodes)

    print("Ring Status:")
    for item in chord_nodes:
        item.print_node()
        item.print_finger_table()
        print()