# Copyright (c) 2020 N.J. Pritchard
# Released under Apache 2.0 License
# Tested with 64-bit Python 3.8
import networkx as nx
import matplotlib.pyplot as plt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

#  TODO: Checking DAG constraints


class Dag2(object):

    def __init__(self):
        self.new_node_name = 0
        self.graph = nx.DiGraph()
        self.hash_algorithm = hashes.SHA256()
        self.digest = None

    def __generatehash__(self, node):
        self.digest = hashes.Hash(self.hash_algorithm, backend=default_backend())
        self.digest.update(self.graph.nodes[node]["data"])
        new_hash = self.digest.finalize()
        self.digest = None
        self.graph.nodes[node]["dataHash"] = new_hash

    def add_node(self, content):
        self.graph.add_node(self.new_node_name,
                            data=content.encode(encoding="utf-8"),
                            dataHash=None,
                            changed=True,
                            name=self.new_node_name)
        self.new_node_name += 1
        return self.new_node_name - 1

    def add_edge(self, u: int, v: int):
        if not self.graph.has_node(u) or not self.graph.has_node(v):
            print("Nodes do not exist yet, need to be created with content first")
        else:
            self.graph.add_edge(u, v)
            self.graph.nodes[u]["changed"] = True
            self.graph.nodes[v]["changed"] = True

    def commit_graph(self):
        if not nx.is_directed_acyclic_graph(self.graph):
            print("Not a DAG, reconsider")
        else:
            for node in self.graph.nodes:  # Will result in a lot of repated work. Okay for initial implementation
                if self.graph.nodes[node]["changed"]:
                    for parent in self.graph.predecessors(node):
                        self.graph.nodes[parent]["changed"] = True
        #  TODO: Go for the DFS Implementation

test = Dag2()
x = test.add_node("Potato")
y = test.add_node("Tomato")
test.add_edge(x, y)
test.commit_graph()
nx.draw(test.graph)
plt.show()

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
