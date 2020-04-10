from merkleDAG import MerkleDAG, convert_data


def add_nodes(graph):
    graph.add_node("Normal")
    graph.add_node(123)
    graph.add_node(1.23)
    graph.add_node(complex(1.0, 1.0))
    graph.add_node(b"Potato")
    graph.add_node(bytearray("potato", 'utf-8'))


def add_edges(graph):
    add_nodes(graph)  # Guaranteed to hold six nodes now
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(0, 3)


class TestMerkleDAG:
    x = MerkleDAG()
    y = MerkleDAG()
    z = MerkleDAG()

    def reset_class_instances(self):
        self.x.__init__()
        self.y.__init__()
        self.z.__init__()

    def test_add_node(self):
        self.reset_class_instances()
        assert self.x.add_node("Normal") is not None
        assert self.x.add_node(123) is not None
        assert self.x.add_node(1.23) is not None
        assert self.x.add_node(complex(1.0, 1.0)) is not None
        assert self.x.add_node(b"Potato") is not None
        assert self.x.add_node(bytearray("potato", 'utf-8')) is not None
        assert self.x.add_node([1, 2, 3]) is None
        assert self.x.add_node(["fd", "sd", 3]) is None
        assert len(self.x.graph.nodes) == 6

    def test_add_edge(self):
        self.reset_class_instances()
        add_nodes(self.x)
        assert self.x.add_edge(0, 1)
        assert not self.x.add_edge(-1, 0)
        assert not self.x.add_edge(5, 6)
        assert not self.x.add_edge(7, 8)
        assert self.x.add_edge(1, 0)  # Naughty, back edge, no longer DAG

    def test_commit_graph(self):
        self.reset_class_instances()
        add_nodes(self.x)
        add_nodes(self.y)
        add_edges(self.x)
        add_edges(self.y)
        assert self.x.commit_graph()
        self.y.add_edge(1, 0)
        assert not self.y.commit_graph()
        self.x.add_edge(0, 4)
        oldhash = self.x.graph.nodes[0]["dataHash"]
        assert self.x.commit_graph()
        assert oldhash != self.x.graph.nodes[0]["dataHash"]


def test_convert_data():
    assert convert_data("Normal") is not None
    assert convert_data(123) is not None
    assert convert_data(1.23) is not None
    assert convert_data(complex(1.0, 1.0)) is not None
    assert convert_data(b"Potato") is not None
    assert convert_data(bytearray("potato", 'utf-8')) is not None
    assert convert_data([1, 2, 3]) is None
    assert convert_data(["fd", "sd", 3]) is None
