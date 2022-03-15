# Handle the creation of ROOT objects in a distributed manner

# class Calculation
# __init__(self, function):
# self.__name__ == function.__name__
# calculate(self, data) -> 
# return self.function(data)

# abstract object Calibration
# takes the data and modifies it before doing any selections or variable calculations
# abstractmethod calibrate(self, data) -> returns data
# abstractmethod get_name(self, data) -> returns a name

# abstract object TObjectFill
# do not implement init -> this depends on the kind of tobject to be filled
#
# @abstractmethod
# get_filled_object(self, data) -> TObject to be written to root file
#
# @property
# @abstractmethod
# object_name(self): (to implement)

# class TProfileFill
# implement __init__(slef, ... args ...)
# implement object_name(self)
# implement get_filled_object(self, data)

# ... repeat for TH1D, TH2D, TH3D, TProfile, TTree, etc ...

# concrete class:
# def __init__(self, [DataFileChannels]):
#     #set up the data file channels
# def book_histogram_fill(self, histogram_fill):

# class DataFile
# def __init__(self, filename):
#     the name and files
#
#def get_start_stop(self, n_splits, this_split):
#    ... get the sart and stop given n_splits and the requested this_split ...
#
# def get_data(self, branches, n_splits, this_split):
#     get the data given the branch names branches i.e. it gets the number of entries in the file, reads from 0 to n

# class DataFileChannel
# def __init__(self, channel_name, files)
#     self.datafiles = [DataFile(f) for f in files]
#     self.channel_name = channel_name
# def get_data(self, n_splits, this_split)
#     return [get_data(el, n_splits, this_split) for el in self.datafiles]


