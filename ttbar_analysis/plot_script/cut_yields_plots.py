from numpy import genfromtxt
from ROOT import TFile
from plotting_tools.DataSet import DataSet
from plotting_tools.CutsYieldPrinter import CutsYieldPrinter
from plotting_tools.DistributionPlotter import DistributionPlotter
from GetTreeAndEfficiency import *

detector = "ILD"
luminosity = 1000.

# name, legend-name, cross section, generator
names = [
    ["hz", "HZ inclusive", 130., "Pythia8"],
    ["zz", "ZZ inclusive", 500., "Pythia8"],
    ["tt_dilep", "t #bar{t} di-lepton", 750.*0.09, "Pythia8"],
    ["tt_allhad", "t #bar{t} all-hadronic", 750.*0.46, "Pythia8"],
    ["ww", "WW inclusive", 5000., "Pythia8"],
    ["tt_semilep", "t #bar{t} single-lepton", 750.*0.45, "Madgraph"],
]

root_files = []
trees = []
efficiencies = []
data_sets = []

for name in names:
    print name
    aux_file, aux_tree = get_tree(name[0])
    aux_efficiency = get_efficiency(name[0])
    root_files.append(aux_file)
    trees.append(aux_tree)
    efficiencies.append(aux_efficiency)
    new_data_set = DataSet(aux_tree, name[0], name[1], name[2], luminosity, name[3], aux_efficiency)
    data_sets.append( new_data_set )

# cut yields
cuts = []
cuts.append("four_jets_mass > 150")
cuts.append("four_jets_mass < 270")
cuts.append("min_jets_mass > 10")
cuts.append("min_jets_mass < 90")
cuts.append("second_min_jets_mass > 20")
cuts.append("second_min_jets_mass < 100")
cuts.append("lep1_e < 100")
cuts.append("missing_rec_e > 20")
cuts.append("missing_rec_e < 150")
cuts.append("n_rec_charged >= 20")
cuts.append("n_rec_charged >= 10")
cuts.append("chi2_top_constrainer <= 40")
cuts.append("success == 1")

aux_caption = "Selection cuts yields"
ttbar_yields_printer = CutsYieldPrinter(data_sets, cuts, aux_caption)

output_filename = "txt/selection_cut_yields.txt"
ttbar_yields_printer.WriteTable(output_filename)


# distribution plot
distributions = []
selection = " && ".join(cuts)

four_jets_mass = DistributionPlotter("four_jets_mass",
                                     "",
                                     "four_jets_mass_{}".format(detector),
                                     48, 0, 340,
                                     "Hadronic Mass @{}".format(detector),
                                     "hadronic mass [GeV]", "GeV",
                                     norm = False,
                                     logy = True,
                                     stack = True,
                                     set_title = True)
for data_set in data_sets:
    four_jets_mass.add_entry(data_set.tree, data_set.name + "_four_jets_mass", data_set.legend_name, data_set.n_event)
distributions.append(four_jets_mass)

min_jets_mass = DistributionPlotter("min_jets_mass",
                                     "",
                                     "min_jets_mass_{}".format(detector),
                                     48, 0, 340,
                                     "Min Jets Mass @{}".format(detector),
                                     "Min Jets mass [GeV]", "GeV",
                                     norm = True,
                                     logy = False,
                                     stack = False,
                                     set_title = True)
for data_set in data_sets:
    min_jets_mass.add_entry(data_set.tree, data_set.name + "_min_jets_mass", data_set.legend_name, data_set.n_event)
distributions.append(min_jets_mass)

chi2_top_constrainer = DistributionPlotter("chi2_top_constrainer",
                                           selection,
                                           "chi2_top_constrainer_{}".format(detector),
                                           48, 0, 40,
                                           "#chi^{} top constrainer @{}".format("{2}", "detector"),
                                           "#chi^{} top constrainer".format("{2}"), "",
                                           norm = False,
                                           logy = True,
                                           stack = True,
                                           set_title = True)
for data_set in data_sets:
    chi2_top_constrainer.add_entry(data_set.tree, data_set.name + "_chi2_top_constrainer", data_set.legend_name, data_set.n_event)
distributions.append(chi2_top_constrainer)
