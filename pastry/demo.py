# Βεβαιωθείτε ότι έχετε εγκαταστήσει τα πακέτα networkx και matplotlib για την λειτουργία του Network.
# Οι εντολές για την εγκατάσταση των πακέτων στο cmd των Windows είναι:
# pip install networkx
# pip install matplotlib

from network import Network
from node import Node
from random import sample
from hash import hash_function
from time import perf_counter_ns
# Χρησιμοποιούμε την συηνάρτηση perf_counter_ns() της βιβλιοθήκης time, για να μετρήσουμε τον χρόνο εισαγωγής/εύρεσης.
# Η συνάρτηση, μετρράει σε nanoseconds τον χρόνο που πέρασε.
# Στην αρχή κάθε εισαγωγής, μετράμε τον χρόνο έναρξης σε μια μεταβλητή start,
# και μόλις ολοκληρωθεί η εισαγωγή, κρατάμε τον χρόνο σε μια άλλη μετβλητή end
# Η διάρκεια τότε, θα είναι start-end.
start = end = 0


m_user = int(input("Παράμετρoς m: "))
Node.m = m_user
Node.r_size = 2**m_user
print(f"Το δίκτυο έχει χωρητικότητα για {Node.r_size} κόμβους")
num_nodes = int(input("Πλήθος κόμβων: "))
while num_nodes > 2**m_user:
    print("Μη έγκυρο πλήθος κόμβων")
    num_nodes = int(input("Πλήθος κόμβων: "))

# Γεννήτρια x τυχαίων/unique id από 0 έως το μέγιστο επιτρεπτό.
# Χωρίζονται σε εκατοντάδες για να υπάρχουν κοινά prefix.
rand_ints = sample(range(100*Node.m), num_nodes)
node_ids = []
for num in rand_ints:
    node_id = hash_function(str(num))
    node_ids.append(node_id)
# Κατασκευή του δικτύου
s_network = Network(m_user, node_ids)

# Κατασκευή των κόμβων που θα εισαχθούν στο δίκτυο
for node_id in node_ids:
    # node_id = hash_function(str(node_id))
    node = Node(str(node_id), m_user)
    s_network.nodes.append(node)

# Προσθήκη των κόμβων στο δίκτυο
for node in s_network.nodes:
    for new in s_network.nodes:
        if node != new:
            node.join(new)
    print(f"Κόμβος {node.node_id} προστέθηκε στο δίκτυο")

# Προσθήκη δεδομένων στους κόμβους του δικτύου
n_data = int(input(f"Πλήθος δεδομένων: "))
while n_data > 2**m_user:
    print("Μη έγκυρο πλήθος δεδομένων")
    n_data = int(input("Πλήθος δεδομένων: "))

s_network.add_data(n_data)

# DEBUG
# s_network.update_routing_tables()
# for node in s_network.nodes:
#     node.print_routing_table_and_leaf_set()

s_network.visualize_pastry()
# s_network.visualize_connections()

while True:
    print("1 -> Προσθήκη κόμβου")
    print("2 -> Αφαίρεση κόμβου")
    print("3 -> Αναζήτηση δεδομένων")
    print("4 -> Πληροφορίες κόμβων")
    print("5 -> Προβολή γράφου")
    print("6 -> Προβολή συνδέσεων")
    print("0 -> Τερματισμός")
    choice = int(input("# -> "))
    if choice == 1:
        node_id = int(input("ID Κόμβου: "))
        if node_id in node_ids:
            print("Υπάρχει ήδη κόμβος με αυτό το ID!")
        elif node_id > s_network.r_size:
            print(f"Το ID πρέπει να είναι από 0 έως {s_network.r_size}!")
        else:
            start = perf_counter_ns()
            node_id = str(node_id)
            s_network.add_node(str(hash_function(node_id, s_network.m)))
            s_network.node_ids.append(node_id)
            end = perf_counter_ns()
            print("Ο κόμβος προστέθηκε σε: ", (end-start)/1000000, " milliseconds.")
    elif choice == 2:
        node_id = int(input("ID Κόμβου: "))
        if node_id not in node_ids:
            print("Δεν υπάρχει κόμβος με αυτό το ID!")
        else:
            start = perf_counter_ns()
            node_ids.remove(node_id)
            node_id = str(node_id)
            for n in s_network.nodes:
                if n.node_id == node_id:
                    s_network.nodes.remove(n)
                    s_network.remove_node(n)
                    end = perf_counter_ns()
                    print("Ο κόμβος αφαιρέθηκε σε: ", (end-start)/1000000, " milliseconds.")
                    break
    elif choice == 3:
        query = input("Πανεπιστήμιο: ")
        num_awards = int(input("# Βραβεία: "))
        start = perf_counter_ns()
        s_network.lookup(query, num_awards)
        end = perf_counter_ns()
        print("Η αναζήτηση ολοκληρώθηκε σε: ", (end-start)/1000000, " milliseconds.")
    elif choice == 4:
        s_network.print_network()
    elif choice == 5:
        s_network.visualize_pastry()
    elif choice == 6:
        s_network.visualize_connections()
    elif choice == 0: break
    else: 
        choice = int(input('# -> '))
