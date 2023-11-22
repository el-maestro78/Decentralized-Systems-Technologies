import hashlib
import csv

class ChordNode:
    def __init__(self, node_id, data=None):
        self.node_id = node_id
        self.successor = None
        self.predecessor = None
        self.finger_table = {}
        self.data = data

    def create_key(self, data):
        return data

    def find_successor(self, key):
        if self.node_id == key:
            return self
        elif self.node_id < key <= self.successor.node_id:
            return self.successor
        else:
            # Find the node responsible for the key in the finger table
            for i in range(482, 0, -1):
                if i in self.finger_table:
                    if self.finger_table[i].node_id <= key:
                        return self.finger_table[i].find_successor(key)
            return self

    def join(self, existing_node):
        self.successor = existing_node.find_successor(self.node_id)
        self.predecessor = self.successor.predecessor
        self.successor.predecessor = self
        self.predecessor.successor = self

    def update_finger_table(self, other, i):
        if self.node_id == other.node_id:
            return
        if other.node_id in range(self.node_id, self.finger_table[i].node_id) or \
                other.node_id == self.finger_table[i].node_id:
            self.finger_table[i] = other
            p = self.predecessor
            p.update_finger_table(other, i)

    def print_finger_table(self):
        print(f"Finger table for Node {self.node_id}:")
        for i in range(1, 482):
            if i in self.finger_table:
                print(f"  {i}: {self.finger_table[i].node_id}")
        print()

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

# Συνάρτηση που δημιουργεί ένα ChordNode αντικείμενο για κάθε key/value pair του dictionary 
# και επιστρέφει μια λίστα με όλα τα αντικείμενα που δημιούργησε
def create_chord_nodes(education_dict):
    chord_nodes = []

    for education, values in education_dict.items():
        # Συνένωση awards και surname ως το value του dictionary
        value = ''.join([f"{surname}, {awards} " for surname, awards in values])
        # Δημιουργεί ένα κενό ChordNode αντικείμενο και καλεί τη create_key σε αυτό
        node = ChordNode(None)
        node_id = node.create_key(education)
        node.node_id = node_id
        node.data = value
        chord_nodes.append(node)

    return chord_nodes

# Συνάρτηση που δημιουργεί το δίκτυο με τα ChordNodes
def create_nodes_network(chord_nodes):
    previousNode = chord_nodes[0]
    for node in chord_nodes:
        print(node.node_id)
        node.join(previousNode)
        previousNode = node
    
if __name__ == '__main__':

    # Το path που περιέχει το csv αρχείο με τους επιστήμονες
    csv_file_path = './computer_scientists_data.csv'
    # Αποθηκεύει το dictionary με τους επιστήμονες σε μια μεταβλητή
    education_dictionary = create_education_dictionary(csv_file_path)
    # Αποθηκεύει τη λίστα με όλα τα ChordNodes αντικείμενα σε μια μεταβλητή
    chord_nodes = create_chord_nodes(education_dictionary)
    print(chord_nodes)
    print(len(chord_nodes))
    # Δημιουργεί το δίκτυο με τα ChordNodes
    create_nodes_network(chord_nodes)




