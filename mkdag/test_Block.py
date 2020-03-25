from Node import Node, block_compare


class TestBlock:
    def test_add_data(self):
        test_block = Node()
        test_block.add_data(0)
        assert test_block.get_data()['data'] == '0'
        test_block.add_data(1)
        assert test_block.get_data()['data'] == '1'
        test_block.add_data([0, 1, 2])
        assert test_block.get_data()['data'] == "[0, 1, 2]"
        test_block.add_data(0, "test")
        assert test_block.get_data()["test"] == '0'
        test_block.add_data("ABCDEFG", "txList")
        assert test_block.get_data()["txList"] == "'ABCDEFG'"
        test_block.add_data(True, "boolTest")
        assert test_block.get_data()["boolTest"] == "True"
        test_block.add_data(None, "nullTest")
        assert test_block.get_data()["nullTest"] == "None"

    def test_generate_hash(self):
        assert True


class TestComparison:
    x = Node()
    y = Node()
    z = Node()
    x.add_data("help")
    y.add_data("help")
    z.add_data("helP")
    x.generate_hash()
    y.generate_hash()
    z.generate_hash()

    def test_block_compare(self):
        assert block_compare(self.x, self.y)
        assert block_compare(self.y, self.x)
        assert not block_compare(self.x, self.z)
        assert not block_compare(self.z, self.x)
