# Copyright (c) 2020 N.J. Pritchard
# Released under Apache 2.0 License
# Tested with 64-bit Python 3.8
from Block import *


class MerkleDAG(object):

    def __init__(self):
        self.parents = []
        self.siblings = []
        self.children = []
        self.data = Block()
        self.hasOutgoing = False

    def print(self):
        self.data.print()
        for i in self.children:
            i.print()

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
