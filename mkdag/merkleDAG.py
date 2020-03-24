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
