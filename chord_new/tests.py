from dht import DHT, Node
from random import randint

# Create a DHT with k=4
d = DHT(4)

# Add three nodes to the DHT
d.join(d._startNode)
nodes = [Node(randint(0, 128)) for _ in range(8)]


for node in nodes:
    d.join(node)

# Update finger tables after all nodes have joined
d.updateAllFingerTables()
d.printFingerTables()

# Print the stored data for each node
for node in [d._startNode] + nodes:
    print(f"Data stored at Node {node.ID}: {node.data}")

# Remove the third node from the network
d.leave(nodes[2])
nodes.pop(2)

# Update finger tables after all nodes have joined
d.updateAllFingerTables()
d.printFingerTables()

# Store data in the DHT with string keys
data_to_store = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
for key, value in data_to_store.items():
    chosen_node = nodes[randint(0, 6)]
    d.store(chosen_node, key, value)

# Print the stored data for each node
for node in [d._startNode] + nodes:
    print(f"Data stored at Node {node.ID}: {node.data}")

# Lookup specific keys in all nodes
keys_to_lookup = ['key1', 'key2', 'key3']

for key in keys_to_lookup:
    for node in [d._startNode] + nodes:
        value = d.lookup(node, key)
        if value is not None:
            break
    else:
        print(f"The key {key} is not present in any node")