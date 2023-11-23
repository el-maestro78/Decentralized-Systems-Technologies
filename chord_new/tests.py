from dht import DHT, Node
from random import randint

# Create a DHT with k=4
d = DHT(4)

# Add three nodes to the DHT
d.join(d._startNode)
nodes = [Node(randint(0, 128)) for _ in range(12)]

for node in nodes:
    d.join(node)

# Update finger tables after all nodes have joined
d.updateAllFingerTables()
d.printFingerTables()

# Print the stored data for each node
for node in [d._startNode] + nodes:
    print(f"Data stored at Node {node.ID}: {node.data}")

# Remove the third node from the network
print(f"Removing node {nodes[2].ID}")
d.leave(nodes[2])
nodes.pop(2)

# Update finger tables after all nodes have joined
d.updateAllFingerTables()
d.printFingerTables()

# Store data in the DHT with string keys and multiple values
data_to_store = {'University of Patras': [('Alexiou', 3), ('Tsichlas', 2)],
                 'Harvard University': [('Vergos', 1)]}
for key, values in data_to_store.items():
    chosen_node = nodes[randint(3, 7)]
    for value in values:
        d.store(chosen_node, key, value)

# Print the stored data for each node
for node in [d._startNode] + nodes:
    print(f"Data stored at Node {node.ID}: {node.data}")

# Lookup specific keys in all nodes
key_to_lookup = 'University of Patras'
awards_threshold = 2

for node in [d._startNode] + nodes:
    values = d.lookup(node, key_to_lookup)
    if values is not None:
        for value in values:
            if value[1] > awards_threshold:
                print(f"{value[0]} studied at {key} and has earned {value[1]} awards.")
        break
else:
    print(f"The key {key} is not present in any node.")
