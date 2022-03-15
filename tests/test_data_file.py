import unittest
from pyroofiller.data_management import DataFile
import numpy as np
import uproot as ur

def make_test_root_files():
    fname = "testing_file_1.root"
    with ur.recreate(fname, compression = None) as fout:
        x = np.array([1,2,3,3,4,5,6,7,8,9,10], dtype=np.float32)
        y = np.array([1,1,1,1,1,1,1,1,1,1,1], dtype=np.float32)
        fout["test"] = {"x": x, "y": y}

    fname = "testing_file_2.root"
    with ur.recreate(fname, compression = None) as fout:
        x = np.array([5,6,7,8,9,10], dtype=np.float32)
        y = np.array([2,2,2,2,2,2], dtype=np.float32)
        fout["test"] = {"x": x, "y": y}

class TestDataFile(unittest.TestCase):

    def test_data_reading_one_branch(self):
        dataf = DataFile("testing_file_1.root", "test")
        branches = ["x"]
        dataframe = dataf.get_data(branches)
        self.assertEqual(len(dataframe["x"]), 11)
        self.assertIn("x", dataframe)
        self.assertNotIn("y", dataframe)
        self.assertTrue( np.all(np.array([1,2,3,3,4,5,6,7,8,9,10], dtype=np.float32) == dataframe["x"]))

    def test_data_reading_two_branches(self):
        dataf = DataFile("testing_file_1.root", "test")
        branches = ["x", "y"]
        dataframe = dataf.get_data(branches)
        self.assertEqual(len(dataframe["x"]), 11)
        self.assertEqual(len(dataframe["y"]), 11)
        self.assertIn("x", dataframe)
        self.assertIn("y", dataframe)
        self.assertTrue( np.all(np.array([1,2,3,3,4,5,6,7,8,9,10], dtype=np.float32) == dataframe["x"]))
        self.assertTrue( np.all(np.array([1,1,1,1,1,1,1,1,1,1,1], dtype=np.float32) == dataframe["y"]))

    def test_data_reading_subset(self):
        dataf = DataFile("testing_file_1.root", "test")
        branches = ["x", "y"]
        dataframe = dataf.get_data(branches, start=2, stop=10)
        self.assertEqual(len(dataframe["x"]), 8)
        self.assertEqual(len(dataframe["y"]), 8)
        self.assertIn("x", dataframe)
        self.assertIn("y", dataframe)
        self.assertTrue( np.all(np.array([3,3,4,5,6,7,8,9], dtype=np.float32) == dataframe["x"]))
        self.assertTrue( np.all(np.array([1,1,1,1,1,1,1,1], dtype=np.float32) == dataframe["y"]))


if __name__ == "__main__":
    make_test_root_files()
    unittest.main()
