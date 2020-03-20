from merkleTree import MerkleTree, compare_mktree


class TestMerkleTree:
    def test_add_data(self):
        mTree = MerkleTree()
        mTree.add_data(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
        assert True


class TestCompareMKTree:
    x = MerkleTree()
    y = MerkleTree()
    z = MerkleTree()
    w = MerkleTree()
    a = MerkleTree()
    b = MerkleTree()
    x.add_data([1, 2, 3, 4])
    y.add_data([1, 2, 3, 4])
    z.add_data([2, 3, 4, 5])
    w.add_data([1, 2, 3, 6])
    a.add_data(['1', '2', '3', '4'])
    b.add_data(['1', '2', '3', '4', '5'])

    def test_compare_mktree(self):
        assert compare_mktree(self.x, self.y)
        assert not compare_mktree(self.x, self.z)
        assert not compare_mktree(self.x, self.w)
        assert not compare_mktree(self.x, self.a)
        assert not compare_mktree(self.a, self.b)
        assert not compare_mktree(self.b, self.a)
