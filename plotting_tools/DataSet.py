class DataSet(object):
    """Store data sample with methods to obtain the rescaled number of events,
    and the fraction that passes a given cut.

    TODO: add methods to obtain directly the number of events expected after rescaling
    with a given cut.
    """

    def __init__(self, tree, name, legend_name, cross_section, luminosity, generator = None, efficiency = None):
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

        self.n_gen_with_eff = self.tree.GetEntries()
        self.n_gen = int( float(self.n_gen_with_eff) / self.efficiency )

        self.n_event_with_eff = int( self.cross_section * self.luminosity * self.efficiency )
        self.n_event = int( self.cross_section * self.luminosity )

    def cut_efficiency(self, cut):
        """Fraction of events passing a given cut"""
        return float(self.tree.GetEntries(cut) ) / self.n_gen_with_eff
