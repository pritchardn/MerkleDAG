# Copyright (c) 2020 N.J. Pritchard
# Released under Apache 2.0 License
# Tested with 64-bit Python 3.8
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class Node(object):
    def __init__(self):
        self.data = {}
        self.data_serial = None
        self.digest = None
        self.hash_algorithm = hashes.SHA256()
        self.hash = None
        self.changed = False

    def is_empty(self):
        return self.data == {}

    def add_data(self, value, key="data"):
        new_value = repr(value)
        if key in self.data.keys():
            if new_value != self.data.get(key):
                self.changed = True
                self.data[key] = new_value
        else:
            self.changed = True
            self.data[key] = new_value

    def get_data(self):
        return self.data

    def generate_hash(self):
        if self.changed:
            self.digest = hashes.Hash(self.hash_algorithm, backend=default_backend())
            self.data_serial = repr(self.data)  # json.dumps(self.data, sort_keys=True)
            self.digest.update(self.data_serial.encode(encoding="utf-8"))
            self.hash = self.digest.finalize()
            self.digest = None
            self.changed = False

    def print(self):
        for element in self.data:
            print(str(element) + " " + str(self.data.get(element)))
        print(self.hash)


def block_compare(x: Node, y: Node):  # type hints added in Python 3.8
    if x.hash != y.hash:
        return False
    else:
        return True
