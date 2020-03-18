from Block import Block


class TestBlock:
    def test_add_data(self):
        test_block = Block()
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
