import pandas as pd
import numpy as np
import math

df = pd.read_csv('computer_scientists_data.csv')


class Node:
    """Pastry Node"""
    nodes_cnt = 0

    def __init__(self, node_id, nodes_num=16):
        self.node_id = node_id
        self.predecessor = self
        self.successor = self
        self.routing_table = [[None] * nodes_num for _ in range(int(math.sqrt(nodes_num)))]
        self.data = {}
        Node.nodes_cnt += 1

    def __str__(self):
        return str(self.node_id)


n = Node('fjfj')
print(n.routing_table)
