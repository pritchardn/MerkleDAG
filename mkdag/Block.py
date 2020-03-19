# Copyright (c) 2020 N.J. Pritchard
# Released under Apache 2.0 License
# Tested with 64-bit Python 3.8
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class Block(object):
    def __init__(self):
        self.data = {}
        self.data_serial = None
        self.digest = None
        self.hash_algorithm = hashes.SHA256()
        self.hash = None

    def add_data(self, value, key="data"):
        self.data[key] = repr(value)

    def get_data(self):
        return self.data

    def generate_hash(self):
        self.digest = hashes.Hash(self.hash_algorithm, backend=default_backend())
        self.data_serial = repr(self.data)  # json.dumps(self.data, sort_keys=True)
        self.digest.update(self.data_serial.encode(encoding="utf-8"))
        self.hash = self.digest.finalize()
        self.digest = None

    def print(self):
        for element in self.data:
            print(str(element) + " " + str(self.data.get(element)))
        print(self.hash)


def block_compare(x: Block, y: Block):  # type hints added in Python 3.8
    if x.hash != y.hash:
        return False
    else:
        return True
