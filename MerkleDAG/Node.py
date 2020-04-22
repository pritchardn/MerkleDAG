# Copyright (c) 2020 N.J. Pritchard
import enum
import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class HashAlg(enum.Enum):
    SHA256 = 1
    SHA3_256 = 2
    MD5 = 3


class Node(object):
    """
    Our own implemenetation of a data-node as a precursor to a block structure.
    Abstracts away hash generation

    TODO: Change to Hashlib
    """

    def __init__(self):
        self.data = {}
        self.data_serial = None
        self.digest = None
        self.hash_algorithm = hashes.SHA256()
        self.hashtype = HashAlg.SHA256
        self.hash = None
        self.changed = False

    @property
    def is_empty(self):
        return self.data == {}

    def add_data(self, value, key="data"):
        """
        Adds data values blindly
        :param value: The data
        :param key: The internal dictionary key which can be specified if non-default behaviour is needed
        """
        self.data[key] = value
        self.changed = True

    def get_data(self):
        return self.data

    def change_hashalg(self, alg: HashAlg):
        """
        Changes the choice of internal hash function from a set of enum
        :param alg: A HashAlg enum
        """
        if alg != self.hashtype and type(alg) == HashAlg:
            self.hashtype = alg
            self.changed = True
            if alg == HashAlg.SHA256:
                self.hash_algorithm = hashes.SHA256()
            elif alg == HashAlg.SHA3_256:
                self.hash_algorithm = hashes.SHA3_256()
            elif alg == HashAlg.MD5:
                self.hash_algorithm = hashes.MD5()

    def generate_hash(self):
        """
        Hashes the current data
        """
        if self.changed:
            self.digest = hashes.Hash(self.hash_algorithm, backend=default_backend())
            self.data_serial = json.dumps(self.data, sort_keys=True)
            self.digest.update(self.data_serial.encode(encoding="utf-8"))
            self.hash = str(self.digest.finalize())
            self.digest = None
            self.changed = False

    def print(self):
        for element in self.data:
            print(str(element) + " " + str(self.data.get(element)))
        print(self.hash)


def node_compare(x: Node, y: Node):
    """
    Compares two nodes by hash
    :param x: The first node
    :param y: The second node
    :return: True if matching, false otherwise
    """
    if type(x) != Node or type(y) != Node:
        raise TypeError("Need to compare Nodes")
    if x.hash != y.hash:
        return False
    else:
        return True
