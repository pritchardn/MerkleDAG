# Copyright (c) 2020 N.J. Pritchard
import networkx as nx
import json
import hashlib


def convert_data(content):
    """
    Handles arbitrary data for insertion into a MerkleDAG
    :param content: Only primitives, bytes and byte-arrays are currently supported
    :return: JSON serialised string representation of content
    """
    ctype = type(content)
    if ctype == bytes:
        return json.dumps(content.decode(), sort_keys=True)
    elif ctype == bytearray:
        return json.dumps(bytes(content).decode(), sort_keys=True)
    elif ctype == complex:
        return None
    else:
        return json.dumps(content, sort_keys=True)


class MerkleDAG(object):
    """
    A basic implementation of a MerkleDAG

    # TODO: Remove edge
    # TODO: Remove node
    """

    def __init__(self):
        self.new_node_name = 0
        self.graph = nx.DiGraph()

    def __generate_hash__(self, node):
        """
        For a provided node in the class' graph, generates its corresponding data-hash as is.
        This collects the data-hashes of all descendants
        :param node: The candidate node
        :return: None
        """
        # Start with my data
        data = self.graph.nodes[node]["data"]

        #  Append all descendent nodes' hashes
        for elem in nx.descendants(self.graph, node):  # TODO: Check if deterministic
            if not self.graph.nodes[elem]["dataHash"] is None:
                data += self.graph.nodes[elem]["dataHash"]
        self.graph.nodes[node]["dataHash"] = hashlib.sha3_256(data.encode('utf-8')).hexdigest()

    def add_node(self, content) -> int:
        """
        Adds a node to the MerkleDAG.

        Sets the new node as changed, increments the global node label and returns the new nodes name.
        :param content:
        :return: -1 if data is unsupported, int otherwise (node's label).
        """
        data = convert_data(content)
        if data is None:
            return -1
        self.graph.add_node(self.new_node_name,
                            data=data,
                            dataHash=None,
                            changed=True,
                            name=self.new_node_name)
        self.graph.nodes[self.new_node_name]["changed"] = True
        self.new_node_name += 1
        return self.new_node_name - 1

    def add_edge(self, u: int, v: int) -> bool:
        """
        Adds an edge to the MerkleDAG u -> v.

        Also sets both nodes to changed.
        :param u: The outgoing node
        :param v: The incoming node
        :return: False upon failure, True otherwise
        """
        if not self.graph.has_node(u) or not self.graph.has_node(v):
            print("Nodes do not exist yet, need to be created with content first")
            return False
        else:
            self.graph.add_edge(u, v)
            self.graph.nodes[u]["changed"] = True
            self.graph.nodes[v]["changed"] = True
            return True

    def commit_graph(self) -> bool:
        """
        Updates the hash-values for all changed nodes in the graph.

        Additionally checks if the graph is a DAG, and sets all nodes to un-changed
        :return:  False upon failure, True otherwise.
        """
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
