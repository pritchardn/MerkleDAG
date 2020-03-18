# Copyright (c) 2020 N.J. Pritchard
# Released under Apache 2.0 License
# Tested with 64-bit Python 3.8

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import json


class Block(object):
    def __init__(self):
        self.data = {}
        self.data_serial = None
        self.digest = None
        self.hash_algorithm = hashes.SHA256()
        self.hash = None

    def add_data(self, value, key="data"):
        self.data[key] = repr(value)

    def get_data(self):
        return self.data

    def generate_hash(self):
        self.digest = hashes.Hash(self.hash_algorithm, backend=default_backend())
        self.data_serial = repr(self.data)  # json.dumps(self.data, sort_keys=True)
        self.digest.update(self.data_serial.encode(encoding="utf-8"))
        self.hash = self.digest.finalize()
        self.digest = None

    def print(self):
        for element in self.data:
            print(str(element) + " " + str(self.data.get(element)))
        print(self.hash)


class Tree:

    def __init__(self):
        self.left = None
        self.right = None
        self.data = Block()

    def print(self):
        self.data.print()
        if type(self.left) == Tree:
            self.left.print()
        if type(self.right) == Tree:
            self.right.print()

    def _add_data(self, data):
        print(data)
        self.data.add_data(data)
        if len(data) > 1:
            self.left = Tree()
            self.data.add_data(self.left._add_data(data[:len(data)//2]), "left")
            self.right = Tree()
            self.data.add_data(self.right._add_data(data[len(data)//2:]), "right")
        self.data.generate_hash()
        return self.data.hash

    def add_data(self, data):  # Assumes data is list
        print(data)
        if len(data) % 2 != 0:
            data += data[-1]  # Pad with final element
        self._add_data(data)


def recurse(elements):
    print(elements)
    if len(elements) > 1:
        recurse(elements[:len(elements)//2])
        recurse(elements[len(elements)//2:])


def ascii_tree(elements):
    if len(elements) % 2 != 0:
        elements += elements[-1]  # Pad with final element to make even
    recurse(elements)


# ascii_tree(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])

mytree = Tree()
mytree.add_data(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
mytree.data.generate_hash()
mytree.print()
