# Copyright (c) 2020 N.J. Pritchard
# Released under Apache 2.0 License
# Tested with 64-bit Python 3.8
import networkx as nx
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


def convert_data(content):
    ctype = type(content)
    if ctype == list:
        print("Currently unsupported")
        return None
    elif ctype == bytes:
        return content
    elif ctype == bytearray:
        return bytes(content)
    else:
        return bytes(repr(content), 'utf-8')


class MerkleDAG(object):
    # TODO: Remove edge
    # TODO: Remove node
    # TODO: convert to hashlib

    def __init__(self):
        self.new_node_name = 0
        self.graph = nx.DiGraph()
        self.hash_algorithm = hashes.SHA256()
        self.digest = None

    def __generate_hash__(self, node):
        self.digest = hashes.Hash(self.hash_algorithm, backend=default_backend())
        # Start with my data
        data = self.graph.nodes[node]["data"]

        #  Append all descendent nodes' hashes
        for elem in nx.descendants(self.graph, node):  # TODO: Check if deterministic
            if not self.graph.nodes[elem]["dataHash"] is None:
                data += self.graph.nodes[elem]["dataHash"]

        self.digest.update(data)
        self.graph.nodes[node]["dataHash"] = self.digest.finalize()
        self.digest = None

    def add_node(self, content):
        data = convert_data(content)
        if data is None:
            return None
        self.graph.add_node(self.new_node_name,
                            data=convert_data(content),
                            dataHash=None,
                            changed=True,
                            name=self.new_node_name)
        self.graph.nodes[self.new_node_name]["changed"] = True
        self.new_node_name += 1
        return self.new_node_name - 1

    def add_edge(self, u: int, v: int):
        if not self.graph.has_node(u) or not self.graph.has_node(v):
            print("Nodes do not exist yet, need to be created with content first")
            return False
        else:
            self.graph.add_edge(u, v)
            self.graph.nodes[u]["changed"] = True
            self.graph.nodes[v]["changed"] = True
            return True

    def commit_graph(self):
        if not nx.is_directed_acyclic_graph(self.graph):
            print("Not a DAG, reconsider")
            return False
        # TODO: Check for orphan nodes
        # Find reverse topological sort of graph
        ordering = list(reversed(list(nx.topological_sort(self.graph))))
        # Mark all nodes that will need updating
        for elem in ordering:
            if self.graph.nodes[elem]["changed"]:
                ancs = nx.ancestors(self.graph, elem)
                for anc in ancs:
                    self.graph.nodes[anc]["changed"] = True
            # Hash content including children (since this is in reverse topo ordering we can do so safely)
            self.__generate_hash__(elem)
            self.graph.nodes[elem]["changed"] = False
        return True

# test.commit_graph()
# nx.draw(test.graph)
# plt.show()
