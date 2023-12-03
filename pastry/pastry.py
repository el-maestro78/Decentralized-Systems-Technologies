from Pastry_node import Node as node
import hashlib
from csv_to_dict import create_education_dictionary


def hash_func(node):
    """
Calculate the longest common prefix (LCP) between the current node's identifier and the destination key.
Use the LCP to determine the next hop in the routing table.
Forward the message to the node with the closest identifier in terms of the LCP.
"""
    hs = hashlib.md5(b'node')
    return hs.hexdigest()


def lookup(node):
    pass


def insert(node, data):
    pass


def delete(node):
    pass





