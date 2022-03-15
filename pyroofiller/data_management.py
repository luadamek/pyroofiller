
import uproot as ur

class DataFile:
    def __init__(self, filename, treename):
        self.filename = filename
        self.treename = treename
        self.nentries = ur.open(filename)[treename].num_entries #get the number of entries

    def get_data(self, branches, start=None, stop=None):
        return ur.open(self.filename)[self.treename].arrays(branches, entry_start=start, entry_stop=stop, library="np")

import glob

class DataFileSet:
    def __init__(self, filewcards, treename):
        self.treename = treename

        if not type(filewcards) == list:
            self.filewcards = [filewcards]
        else:
            self.filewcards = filewcards

        self.datafiles = []
        for filewcard in self.filewcards:
            files = glob.glob(filewcard)
            for f in files:
                self.datafiles.append(DataFile(f, self.treename))

        self.nentries = sum([d.nentries for d in self.datafiles])

        self.file_edges = [0]
        for d in self.datafiles:
            self.file_edges.append(d.nentries + self.file_edges[-1])

    def get_intersecting_files(self, start=None, stop=None):
        indices = []
        start_and_stop = []
        if start is None: start = 0
        if stop is None: stop = self.nentries

        assert start >= 0
        assert stop <= self.nentries
        assert start <= stop

        for i in range(0, len(self.file_edges) - 1):
            low = self.file_edges[i]
            high = self.file_edges[i+1]

            if (start < high and stop >= high) or (start <= low and stop > low):
                indices.append(i)
                start_and_stop.append((0, high - low))

                if start > low and start < high:
                    last_entry = start_and_stop[-1]
                    start_and_stop[-1] = (start - low, last_entry[-1])

                if stop > low and stop < high:
                    last_entry = start_and_stop[-1]
                    start_and_stop[-1] = (last_entry[0], stop - low)


        files_to_use = [self.datafiles[i] for i in indices]
        return files_to_use, start_and_stop

    def get_start_and_stop(self, split=0, nsplits=1):
        if split is None:
            split = 0
        if nsplits is None:
            nsplits = 1

        assert split < nsplits
        step = self.nentries // nsplits
        start = step * split
        stop = step * (split + 1)
        if split == nsplits - 1:
            stop = self.nentries
        return (start, stop)

    def get_data(self, branches, split=None, nsplits=None):
        start, stop = self.get_start_and_stop(split=split, nsplits=nsplits)
        files, start_and_stop = self.get_intersecting_files(start=start, stop=stop)
        dataframes = []
        for f, (start, stop) in zip(files, start_and_stop):
            dataframes.append(f.get_data(branches, start=start, stop=stop))
        return dataframes




