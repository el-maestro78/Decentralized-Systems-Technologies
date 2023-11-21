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


def create_education_dictionary(csv_file):
    education_dict = {}

    with open(csv_file, 'r', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            education = row['Education']
            surname = row['Surname']
            awards = row['#Awards']

            # If the education key is not in the dictionary, add it with a list containing the first tuple
            if education not in education_dict:
                education_dict[education] = [(surname, awards)]
            else:
                # Else append the tuple to the existing list
                education_dict[education].append((surname, awards))
    
    # Drop from dictionary scientists with empty education key
    education_dict.pop("[]")

    return education_dict

def create_chord_nodes(education_dict):
    chord_nodes = {}

    for education, values in education_dict.items():
        # Concatenate surname and awards for the value
        value = ''.join([f"{surname}_{awards} " for surname, awards in values])
        # Create an instance of ChordNode and call create_key on that instance
        node = ChordNode(None)
        node_id = node.create_key(education)
        node.node_id = node_id
        node.data = value
        chord_nodes[node_id] = node

    return chord_nodes
    '''
    startNode = list(chord_nodes.items())[0]

    for key, value in chord_nodes.items():
        print(value)
        value.join(startNode)
        startNode = value
    
    startNode = list(chord_nodes.items())[0]

    for item in chord_nodes.items():
        item.join(startNode)
        print(item)
        startNode = item
    '''

if __name__ == '__main__':

    # Example usage:
    csv_file_path = './computer_scientists_data.csv'
    education_dictionary = create_education_dictionary(csv_file_path)
    chord_nodes = create_chord_nodes(education_dictionary)
    
    print(len(chord_nodes))
    Node0 = chord_nodes.get("['University of Bristol']")
    Node1 = chord_nodes.get("['Technical University of Berlin']")
    print(Node0)
    print(Node1)
    print(Node0.node_id)
    print(Node0.data)
    print(Node0.find_successor("['University of Bristol']"))




