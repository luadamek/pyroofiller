from abc import ABC, abstractmethod

class AbstractTObjectFill:

    @abstractmethod
    def fill(self):
        pass

    @abstractmethod
    def get_object(self):
        pass

    @property
    @abstractmethod
    def calculations(self):
        pass

    @abstractmethod
    def reset(self):
        pass

from caluclation import Calculation
def trivial_weights(data):
    key = data.keys()[0]
    return np.ones(len(data[key]))
calc_trivial_weights = Calculation(trivial_weights, {})

class TH1DFill:
    def __init__(self, histogram_name, variable, selections = {}, weight_calculation = trivial_weights, bins = 1, range_low = 0.000001, range_high=1. - 0.00001,  xlabel ="", ylabel = ""):
        self.variable = variable
        self.selections = self.selections
        self.weight_calculation = weight_calculation

        self.bin_edges = np.linspace(range_low, range_high, bins+1)
        bins_array = array('d',bin_edges)

        self.tobject = ROOT.TH1D(histogram_name + channel, histogram_name + channel, len(bins_array)-1, bins_array)
        self.tobject.GetXaxis().SetTitle(xlabel)
        self.tobject.GetYaxis().SetTitle(ylabel)

    def fill(self, evaluations):
        var = evaluations[self.variable]
        weights = evaluations[self.weight_calculation]
        selection = np.logical_and([evaluations[el] for el in self.selections])

        var = var[selection]
        weights = weights[selection]
        vals, edges = np.histogram(var, bins=self.bin_edges, weights=weights)
        vals_sq, edges = np.histogram(var, bins=self.bin_edges, weights=weights**2)

        for i in range(1, self.tobject.GetNbinsX() + 1):
            self.tobject.SetBinContent(i, vals[i])
            self.tobject.SetBinError(i, vals_sq[i] ** 0.5)
            self.tobject.SetEntries(np.sum(weights))



    @property
    def calculations(self):
        return {variable} + self.selections + {self.weight_calculation}

    def get_object(self):
        return self.tobject

    def reset(self):
        self.tobject.Reset()
