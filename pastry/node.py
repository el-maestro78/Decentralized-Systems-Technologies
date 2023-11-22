import pandas as pd
import numpy as np
df = pd.read_csv('computer_scientists_data.csv')
nodes_num = 16


class Node:
    # f"""Pastry Node no {str(nodeId)}"""
    nodeId_cnt = 1
    # surname = ''
    # awards = 0
    # education = []

    def __init__(self):
        self.nodeId = Node.nodeId_cnt
        Node.nodeId_cnt += 1


# for i in range(0, nodes_num):
#     n = Node()
#     print(n.nodeId)
