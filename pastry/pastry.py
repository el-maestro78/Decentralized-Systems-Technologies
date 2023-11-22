import node as Node
import hashlib


def hash_func(node):
    hs = hashlib.md5(b'node')
    return hs.hexdigest()


def lookup(node):
    pass


def insert(node, data):
    pass


def delete(node):
    pass


class Data:
    def __init__(self, nodeId, surname, awards, education):
        self.surname = surname
        self.awards = awards
        self.education = education


