


def HistogramFiller:
    def __init__(self, datafilesets):
        self.datafilesets = datafilesets
        self.branches = set()
        self.calculations = set()
        self.tobject_fills = []

    def add_calculation(calculation):
        self.calculations.add(calculation)
        self.branches.update(calculation.branches)

    def book_tobject_fill(self, fill):
        self.tobject_fills.append(fill)
        self.calculations.update(fill.calculations)
        for f in fill.calculations:
            self.branches.update(f.branches) #update the branches needed for the calculation

    def write_objects(self, output_file, split = None, nsplits = None):
        if not ( (split is None and nsplits is None) or (split is not None and nsplits is not None) ):
             raise ValueError("You need to specify both split and nsplits.")

        outfile = ROOT.TFile(output_file, "RECREATE")

        for datafileset in datafilesets:
            channel = datafiles.channel
            dataframes = datafileset.get_data(self.branches, split = split, nsplits = nsplits)

            for c in self.calibrations:
                dataframes = [c.calibrate(df) for df in dataframes] #calibrate the dataframes

            for df in dataframes:
                evaluations = {c.name : c.calculate(df) for c in self.calculations}
                for objfill in self.tobject_fills:
                    objfill.fill(evaluations)

            #write to the output file
            objects = [objfill.get_object() for objfill in self.tobject_fills]

            outfile.cd()
            outfile.mkdir(channel)
            outfile.cd(channel)
            for obj in objects:
                obj.SetName(h.GetName() + "_{}".format(channel))
                obj.Write()

            #reset the fills for the next batch
            for objfill in sel.tobject_fills:
                objfill.reset() #set the histogram to empty again, and ready for the next histogram fill
