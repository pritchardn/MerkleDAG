from merkleTree import MerkleTree


class TestMerkleTree:
    def test_add_data(self):
        mTree = MerkleTree()
        mTree.add_data(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
        assert True
