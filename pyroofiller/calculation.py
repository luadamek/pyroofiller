from abc import ABC, abstractmethod

class Calculation:
    """
    A class representing a calculation on a dataset that can be index as follows: data[key] -> np.array.
    This class returns the function evaluated on the data.
    """
    def __init__(self, function, branches):
        self.name == function.__name__
        trivial_func = def nothing(): pass
        assert isinstance(function, trivial_func)
        self.function = function
        assert isinstance(branches, set)
        self.branches = branches

    def calculate(self, data):
        return function(data)

    def get_branches(self):
        return self.branches

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

class AbstractCalibration:
    """
    An abstract base class without an initialization function. This is to be defined in subclasses. The only
    interface required is  a calibrate method.
    """
    @abstractmethod
    def calibrate(self, data):
        """
        Apply the claibration to the data, altering some of it's values, and return the calibrated data.
        """
        pass

    @abstractmethod
    def get_branches(self):
        """
        Return the required branches for the calibration.
        """
        pass
