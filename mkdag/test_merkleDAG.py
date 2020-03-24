from merkleDAG import MerkleDAG


class TestMerkleDAG:
    x = MerkleDAG()
    y = MerkleDAG()
    z = MerkleDAG()

    def reset_class_instances(self):
        self.x = MerkleDAG()
        self.y = MerkleDAG()
        self.z = MerkleDAG()

    def test_get_hash(self):
        assert self.x.get_hash() is None
        self.x.add_data(['A', 'B', 'C'])
        assert self.x.get_hash() is not None

    def test_add_child(self):
        self.x.add_child(self.y)
        self.y.add_child(self.z)
        assert self.x.parents == []
        assert self.x in self.y.parents
        assert self.y in self.z.parents
        self.reset_class_instances()

    def test_add_parent(self):
        self.z.add_parent(self.x)
        self.z.add_parent(self.y)
        self.y.add_parent(self.x)
        assert self.x.parents == []
        assert self.x in self.y.parents
        assert self.x in self.z.parents and self.y in self.z.parents
        self.reset_class_instances()

    def test_update_hashes(self):
        self.x.add_data(['A', 'B', 'C'])
        old_hash = self.x.get_hash()
        self.x.add_child(self.y)
        assert old_hash == self.x.get_hash()

        old_hash = self.x.get_hash()
        self.y.add_data(['D', 'E', 'F'])
        self.x.update_hashes()
        assert old_hash != self.x.get_hash()

        old_hash = self.z.get_hash()
        self.z.add_child(self.y)
        self.z.update_hashes()
        assert old_hash != self.z.get_hash()
        self.reset_class_instances()
