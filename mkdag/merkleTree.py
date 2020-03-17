# Copyright (c) 2020 N.J. Pritchard
# Released under Apache 2.0 License
# Tested with 64-bit Python 3.8

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import json


class Block(object):
    def __init__(self):
        self.data = {}
        self.digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        self.hash = None

    def add_data(self, key, value):
        self.data[key] = ''.join([str(elem) for elem in value]).encode()
        # TODO: This is yucky come up with something better
        self.digest.update(self.data[key])
        self.generate_hash()

    def get_data(self):
        return self.data

    def generate_hash(self):
        self.hash = self.digest.finalize()
        self.digest = hashes.Hash(hashes.SHA256(), backend=default_backend())

    def print(self):
        for element in self.data:
            print(str(element) + " " + str(self.data.get(element)))
        print(self.hash)


class Tree:

    def __init__(self):
        self.left = None
        self.right = None
        self.data = Block()

    def update_left(self, left):
        self.left = left

    def update_right(self, right):
        self.right = right

    def print(self):
        self.data.print()
        if type(self.left) == Tree:
            self.left.print()
        if type(self.right) == Tree:
            self.right.print()


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
mytree.data.add_data('txList', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
mytree.data.add_data('rxList', ['yummy'])
mytree.print()

