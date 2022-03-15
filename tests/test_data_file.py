import unittest
from pyroofiller.data_management import DataFile
import ROOT
import numpy as np

def make_test_root_files():
    fname = "testing_file_1.root"
    testing_file = ROOT.TFile(fname, "RECREATE")
    tree = ROOT.TTree("test", "test")

    x = np.array([1,2,3,3,4,5,6,7,8,9,10], dtype=np.float32)
    y = np.array([1,1,1,1,1,1,1,1,1,1,1], dtype=np.float32)
    tree.Branch("x", x, "x[{}]/F".format(len(x)))
    tree.Branch("y", y, "y[{}]/F".format(len(y)))
    tree.Fill()
    testing_file.Write()
    testing_file.Close()

    fname = "testing_file_2.root"
    testing_file = ROOT.TFile(fname, "RECREATE")
    tree = ROOT.TTree("test", "test")
    x = np.array([5,6,7,8,9,10], dtype=np.float32)
    y = np.array([2,2,2,2,2,2], dtype=np.float32)
    tree.Branch("x", x, "x[{}]/F".format(len(x)))
    tree.Branch("y", y, "y[{}]/F".format(len(arr)))
    tree.Fill()
    testing_file.Write()
    testing_file.Close()

class TestDataFile(unittest.TestCase):

    def test_data_reading(self):
        df = DataFile("testing_file_1.root", ""


if __name__ == "__main__":
    make_test_root_files()
    unittest.main()
