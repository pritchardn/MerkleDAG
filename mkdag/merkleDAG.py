# Copyright (c) 2020 N.J. Pritchard
# Released under Apache 2.0 License
# Tested with 64-bit Python 3.8
from Node import *


#  TODO: Checking DAG constraints


class MerkleDAG(object):

    def __init__(self):
        self.parents = []
        self.children = []
        self.child_hashes = []
        self.data = Node()

    def print(self):
        self.data.print()
        for i in self.children:
            i.print()

    def get_hash(self):
        return self.data.hash

    def add_child(self, child):
        if type(child) == MerkleDAG:
            if child not in self.children:
                self.children.append(child)
                child.add_parent(self)

    def add_parent(self, parent):
        if type(parent) == MerkleDAG:
            if parent not in self.parents:
                self.parents.append(parent)
                parent.add_child(self)

    def add_data(self, data, key="data"):  # Will directly hash data and pass this value to parents
        self.data.add_data(data, key)
        self.data.generate_hash()

    def update_hashes(self):
        self.child_hashes = []
        for child in self.children:
            self.child_hashes.append(child.get_hash())
        self.add_data(self.child_hashes, "children")

    def are_siblings(self, candidate):
        if type(candidate) == MerkleDAG:
            if not self.parents:
                if not candidate.parents:  # Two roots is possible
                    return True
                else:  # Edge case of comparing root to child
                    return False
            # I know this is O(n^2) but it is accurate and deterministic
            for parent in self.parents:
                if parent not in candidate.parents:
                    return False
            return True
