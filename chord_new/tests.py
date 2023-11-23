from dht import DHT, Node
from random import randint

# Create a DHT with k=4
d = DHT(3)

# Number of nodes to add 
u = 5

# Add u nodes to the DHT
d.join(d._startNode)

# Generate unique random IDs for nodes
existing_ids = {d._startNode.ID}
nodes = [Node(randint(0, 128)) for _ in range(u)]
for node in nodes:
    while node.ID in existing_ids:
        node.ID = randint(0, 128)
    existing_ids.add(node.ID)
    d.join(node)

# Update finger tables after all nodes have joined
d.updateAllFingerTables()
d.printFingerTables()

'''
# Remove the third node from the network
print("===============REMOVING NODE===============")
print(f"Removing node {nodes[2].ID}.")
d.leave(nodes[2])
nodes.pop(2)

# Update finger tables after all nodes have joined
d.updateAllFingerTables()
d.printFingerTables()
'''
# Store data in the DHT with string keys and multiple values
data_to_store = {'University of Patras': [('Alexiou', 3), ('Tsichlas', 2)], 'Harvard University': [('Vergos', 1)]}
for key, values in data_to_store.items():
    chosen_node = nodes[randint(0, u - 1)]

    while len(chosen_node.data) != 0:
        chosen_node = nodes[randint(0, u - 1)]

    # At this point, chosen_node is a node without a key-value pair
    chosen_node.data = {key: values}

# Print the stored data for each node
print("===================DATA===================")
for node in [d._startNode] + nodes:
    print(f"Data stored at Node {node.ID}: {node.data}")

# Lookup specific keys in all nodes
print("==================LOOKUP==================")
key_to_lookup = 'University of Patras'
awards_threshold = 3
key_found = False

for node in [d._startNode] + nodes:
    values = d.lookup(node, key_to_lookup)
    if values is not None:
        for value in values:
            if value[1] >= awards_threshold:
                print(f"{value[0]} studied at {key_to_lookup} and has earned {value[1]} awards.")
        key_found = True
        
if not key_found:
    print(f"The key {key_to_lookup} is not present in any node.")
