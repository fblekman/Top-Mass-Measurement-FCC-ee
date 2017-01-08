class DataSet(object):
    """Store data sample with methods to obtain the rescaled number of events,
    and the fraction that passes a given cut.
    """

    def __init__(self, tree, name, legend_name, cross_section, luminosity, generator=None, efficiency=None):

        self.tree = tree
        self.name = name
        self.legend_name = legend_name
        self.cross_section = cross_section
        self.luminosity = luminosity
        self.generator = generator

        if efficiency == None:
            self.efficiency = 1.
        else:
            self.efficiency = efficiency

        self.n_entries = self.tree.GetEntries()

    def cut_efficiency(self, cut):
        """Fraction of events passing a given cut"""
        return float(self.tree.GetEntries(cut)) / self.n_entries

    def n_generated_with_eff(self, cut = ""):
        return self.tree.GetEntries(cut)

    def n_generated(self, cut = ""):
        return int(float(self.tree.GetEntries(cut)) / self.efficiency)

    def n_expected_with_eff(self, cut = ""):
        return int(self.cut_efficiency(cut) * self.cross_section * self.luminosity * self.efficiency)

    def n_expected(self, cut = ""):
        return int(self.cut_efficiency(cut) * self.cross_section * self.luminosity)
