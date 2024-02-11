from node import Node
from network import Network
from random import sample
from time import perf_counter_ns
# Χρησιμοποιούμε την συηνάρτηση perf_counter_ns() της βιβλιοθήκης time, για να μετρήσουμε τον χρόνο εισαγωγής/εύρεσης.
# Η συνάρτηση, μετρράει σε nanoseconds τον χρόνο που πέρασε.
# Στην αρχή κάθε εισαγωγής, μετράμε τον χρόνο έναρξης σε μια μεταβλητή start,
# και μόλις ολοκληρωθεί η εισαγωγή, κρατάμε τον χρόνο σε μια άλλη μετβλητή end
# Η διάρκεια τότε, θα είναι start-end.
start = end = time1 = time2 = 0


m_user = int(input('m: '))
Node.m = m_user
Node.r_size = 2 ** m_user
print(f'Το δίκτυο έχει χωρητικότητα {Node.r_size}')
num_nodes = int(input('Κόμβοι: '))
while num_nodes > 2 ** m_user:
    print(f'Δε μπορείς να εισάγεις πάνω από {Node.r_size} κόμβους')
    num_nodes = int(input('Κόμβοι: '))

start = perf_counter_ns()
# Γεννήτρια x τυχαίων/unique id από 0 έως το μέγιστο επιτρεπτό
node_ids = sample(range(Node.r_size), num_nodes)

# Κατασκευή του δικτύου
s_network = Network(m_user, node_ids)

# Κατασκευή των κόμβων που θα εισαχθούν στο δίκτυο
for node_id in node_ids: 
    node = Node(node_id, m_user)
    s_network.nodes.append(node)

# Προσθήκη των κόμβων στο δίκτυο
for node in s_network.nodes:
    node.join(s_network.first_node)
    print(f'Κόμβος {node.node_id} προστέθηκε στο δίκτυο')
end = perf_counter_ns()
# time1: χρόνος κατασκευής κόμβων
time1=end-start

# Προσθήκη δεδομένων στους κόμβους του δικτύου
n_data = int(input(f'Δεδομένα: '))
while n_data > 2 ** m_user:
    print(f'Δε μπορείς να εισάγεις πάνω από {Node.r_size} δεδομένα')
    n_data = int(input('Δεδομένα: '))

start = perf_counter_ns()
s_network.add_data(n_data)

s_network.update_fingers_tables()
end = perf_counter_ns()
# time2 : χρόνος προσθήκης δεδομένων και ενημέρωσης fingers table
time2 = end-start

s_network.visualize_chord()

print("\nΤο δίκτυο κατασκευάστηκε σε: ", (time1+time2)/1000000, " milliseconds (ή ",(time1+time2)/pow(10,9), " seconds).\n")

while True:
    print("1 -> Προσθήκη κόμβου\n2 -> Αφαίρεση κόμβου\n3 -> Αναζήτηση δεδομένων\n4 -> Πληροφορίες κόμβων\n5 -> Προβολή γράφου\n6 -> Σταθεροποίηση\n0 -> Τερματισμός")
    choice = int(input('# -> '))
    if choice == 1: 
        node_id = int(input('ID Κόμβου: '))
        if node_id in node_ids:
            print('Υπάρχει ήδη κόμβος με αυτό το ID!')
        elif len(s_network.nodes) > Node.r_size - 1:
            print('Δεν μπορούν να προστεθούν άλλοι κόμβοι')
        elif node_id > s_network.r_size:
            print(f'Το ID πρέπει να είναι από 0 έως {s_network.r_size}!')
        else:
            start = perf_counter_ns()
            s_network.add_node(node_id)
            node_ids.append(node_id)
            end = perf_counter_ns()
            print("Ο κόμβος προστέθηκε σε: ", (end-start)/1000000, " milliseconds.")
    elif choice == 2: 
        node_id = int(input('ID Κόμβου: '))
        if node_id not in node_ids:
            print('Δεν υπάρχει κόμβος με αυτό το ID!')
        else:
            start = perf_counter_ns()
            node_ids.remove(node_id)
            s_network.remove_node(node_id)
            end = perf_counter_ns()
            print("Ο κόμβος αφαιρέθηκε σε: ", (end-start)/1000000, " milliseconds.")
    elif choice == 3: 
        query = input('Πανεπιστήμιο: ')
        num_awards = int(input('# Βραβεία: '))
        start = perf_counter_ns()
        s_network.lookup(query, num_awards)
        end = perf_counter_ns()
        print("Η αναζήτηση ολοκληρώθηκε σε: ", (end-start)/1000000, " milliseconds.")
    elif choice == 4: 
        s_network.print_network()
    elif choice == 5:
        s_network.visualize_chord()
    elif choice == 6:
        s_network.update_fingers_tables()
    elif choice == 0: break
    else: 
        choice = int(input('# -> '))
        
