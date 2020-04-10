from merkleDAG import MerkleDAG


class TestMerkleDAG:
    x = MerkleDAG()
    y = MerkleDAG()
    z = MerkleDAG()

    def reset_class_instances(self):
        self.x.__init__()
        self.y.__init__()
        self.z.__init__()

    def test_add_node(self):
        self.x.add_node("Normal")
        self.x.add_node(123)
        self.x.add_node([1, 2, 3])
        self.x.add_node(["fd", "sd", 3])

    def test_add_edge(self):
        assert False

    def test_commit_graph(self):
        assert False
