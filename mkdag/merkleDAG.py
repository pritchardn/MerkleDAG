# Copyright (c) 2020 N.J. Pritchard
# Released under Apache 2.0 License
# Tested with 64-bit Python 3.8
from Block import *


#  TODO: Checking DAG constraints


class MerkleDAG(object):

    def __init__(self):
        self.parents = []
        self.siblings = []
        self.children = []
        self.child_hashes = []
        self.data = Block()
        self.hasOutgoing = False

    def print(self):
        self.data.print()
        for i in self.children:
            i.print()

    def get_hash(self):
        return self.data.hash

    def add_child(self, child):
        self.hasOutgoing = True
        if type(child) == MerkleDAG:
            if child not in self.children:
                self.children.append(child)
                child.add_parent(self)

    def add_sibling(self, sibling):
        if type(sibling) == MerkleDAG:
            if sibling not in self.siblings:
                self.siblings.append(sibling)
                sibling.add_sibling(self)

    def add_parent(self, parent):
        if type(parent) == MerkleDAG:
            if parent not in self.parents:
                self.parents.append(parent)
                parent.add_child(self)

    def add_data(self, data, key="data"):  # Will directly hash data and pass this value to parents
        self.data.add_data(data, key)
        self.data.generate_hash()
        for parent in self.parents:
            parent.update_hashes()

    def update_hashes(self):
        self.child_hashes = []
        for child in self.children:
            self.child_hashes.append(child.get_hash())
        self.add_data(self.child_hashes, "children")
