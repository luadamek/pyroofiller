import unittest
from pyroofiller.data_management import DataFileSet
import numpy as np
import uproot as ur

x1 = np.array([1,2,3,3,4,5,6,7,8,9,10], dtype=np.float32)
y1 = np.array([1,1,1,1,1,1,1,1,1,1,1], dtype=np.float32)

x2 = np.array([5,6,7,8,9,10], dtype=np.float32)
y2 = np.array([2,2,2,2,2,2], dtype=np.float32)

x3 = np.array([8,8,8,8,8,8], dtype=np.float32)
y3 = np.array([3,3,3,3,3,3], dtype=np.float32)

xs = [x1,x2,x3]
ys = [y1,y2,y3]

treename = "test"
def make_test_root_files():
    fname = "testing_file_1.root"
    with ur.recreate(fname, compression = None) as fout:
        fout[treename] = {"x": x1, "y": y1}

    fname = "testing_file_2.root"
    with ur.recreate(fname, compression = None) as fout:
        fout[treename] = {"x": x2, "y": y2}

    fname = "testing_file_3.root"
    with ur.recreate(fname, compression = None) as fout:
        fout[treename] = {"x": x3, "y": y3}

class TestDataFile(unittest.TestCase):
    def test_number_of_entries(self):
        self.assertEqual(datafiles.nentries, len(x1) + len(x2) + len(x3))

    def test_start_stop(self):
        self.assertEqual(datafiles.get_start_and_stop(), (0, len(x1) + len(x2) + len(x3)))
        self.assertEqual(datafiles.get_start_and_stop(0, 2), (0, (len(x1) + len(x2) + len(x3))//2))
        self.assertEqual(datafiles.get_start_and_stop(1, 2), ((len(x1) + len(x2) + len(x3))//2, len(x1) + len(x2) + len(x3)))

    def test_get_all_intersecting_files(self):
        files, start_stop = datafiles.get_intersecting_files()
        self.assertTrue(all([files[i].filename == filenames[i] for i in range(0, len(filenames))]))
        self.assertTrue(all([start_stop[i] == (0, len(xs[i])) for i in range(0, len(xs))]))

    def subset_intersecting_files_one_from_all(self):
        files, start_stop = datafiles.get_intersecting_files(start=0, stop=len(x1))
        self.assertEqual(len(files), 1)
        self.assertEqual(len(start_stop), 1)
        self.assertEqual(start_stop[0], (0, len(x1)))

    def test_subset_intersecting_files_two_from_all(self):
        files, start_stop = datafiles.get_intersecting_files(start=0, stop=len(x1) + 5)
        self.assertEqual(len(files), 2)
        self.assertEqual(len(start_stop), 2)
        self.assertEqual(start_stop[0], (0, len(x1)))
        self.assertEqual(start_stop[1], (0, 5))

    def test_subset_intersecting_files_three_from_all(self):
        files, start_stop = datafiles.get_intersecting_files(start=0, stop=len(x1) + len(x2) + 1)
        self.assertEqual(len(files), 3)
        self.assertEqual(len(start_stop), 3)
        self.assertEqual(start_stop[0], (0, len(x1)))
        self.assertEqual(start_stop[1], (0, len(x2)))
        self.assertEqual(start_stop[2], (0, 1))

    def test_retrieve_all_data(self):
        data = datafiles.get_data(["x", "y"])
        for el, x, y in zip(data, [x1,x2,x3], [y1,y2,y3]):
            self.assertTrue(np.all(x == el["x"]))
            self.assertTrue(np.all(y == el["y"]))



if __name__ == "__main__":
    make_test_root_files()
    filenames = ["testing_file_{}.root".format(i) for i in range(1, 4)]
    datafiles = DataFileSet(filenames, "test")
    unittest.main()
