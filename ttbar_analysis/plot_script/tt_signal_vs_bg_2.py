from DistributionPlotter import DistributionPlotter
from cebefo_style import cebefo_style
from ROOT import TFile
from numpy import genfromtxt


cebefo_style()

save = False
detector = "ILD"
dir_fig = "fig/"
save_root_file_name = "signal_vs_bg_{}.root".format(detector)

luminosity = 1000.

files = []
trees = []

cuts = []

# cuts.append("four_jets_mass > 180")
# cuts.append("four_jets_mass < 270")
#
# cuts.append("min_jets_mass > 15")
# cuts.append("min_jets_mass < 80")
# #
# # cuts.append("jet3_logbtag > 3")
#
# cuts.append("missing_rec_e > 20")
# cuts.append("missing_rec_e < 150")
# cuts.append("success == 1")
#
# cuts.append("min_jets_mass > 20")
# cuts.append("min_jets_mass < 100")
#
# cuts.append("lep1_e < 100")
#

# cuts.append("missing_rec_e < 150")
#
# cuts.append("n_rec >= 40")
# cuts.append("n_rec_charged >= 20")
# cuts.append("n_rec_charged >= 10")
# cuts.append("chi2_top_constrainer <= 40")


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
cuts.append("chi2_top_constrainer <= 40")

cuts.append("success == 1")


cumulative_cuts = []
for i, cut in enumerate(cuts):
    if i == 0:
        cumulative_cuts.append(cut)
    else:
        cumulative_cuts.append( cumulative_cuts[i-1] + " && " +  cut)



class DataSet:
    def __init__(self, name, legend_name, cross_section, luminosity, efficiency = True):
        self.file = TFile("ntuple_used/{}_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root".format(name),"OPEN")
        self.tree = self.file.Get("events")
        self.name = name
        self.legend_name = legend_name
        self.cross_section = cross_section
        self.luminosity = luminosity

        if efficiency == True:
            eff_filename = "ntuple_used/{}_ILD/analyzers.CheckParticles.CheckParticles_1/events.txt".format(name)
            eff_file = genfromtxt(eff_filename,skip_header=1,delimiter='\t', dtype=None)
            self.efficiency = float( eff_file[3][3])
        else:
            self.efficiency = 1.

        self.n_event = self.cross_section * self.luminosity * self.efficiency

names = [
    ["hz", "HZ inclusive", 130.],
    ["zz", "ZZ inclusive", 500.],
    ["tt_dilep", "t #bar{t} di-lepton", 750.*0.09],
    ["tt_allhad", "t #bar{t} all-hadronic", 750.*0.46],
    ["ww", "WW inclusive", 5000.],
    ["tt_semilep", "t #bar{t} single-lepton", 750.*0.45 ],
]

data_sets = []

for name in names:
    new_data_set = DataSet(name[0], name[1], name[2], luminosity, True)
    data_sets.append( new_data_set )

distributions = []
selection = cumulative_cuts[-1]
# selection = ""
print "selection: ", selection
############KINEMATIC VARIABLES #####################################

# mc_lepton_pdgid = DistributionPlotter("mc_lepton_pdgid", selection, "mc_lepton_pdgid_{}".format(detector), 200, -150, 20, "mc_lepton_pdgid @{}".format(detector), "mc_lepton_pdgid [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     mc_lepton_pdgid.add_entry(data_set.tree, data_set.name + "_mc_lepton_pdgid", data_set.legend_name, data_set.n_event)
# distributions.append(mc_lepton_pdgid)


#
four_jets_mass = DistributionPlotter("four_jets_mass", selection, "four_jets_mass_{}".format(detector), 48, 0, 340, "Hadronic Mass @{}".format(detector), "hadronic mass [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
for data_set in data_sets:
    four_jets_mass.add_entry(data_set.tree, data_set.name + "_four_jets_mass", data_set.legend_name, data_set.n_event)
distributions.append(four_jets_mass)

# lep1_e = DistributionPlotter("lep1_e", selection, "lep1_e_{}".format(detector), 50, 0, 160, "lep1_e @{}".format(detector), "lep1_e [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     lep1_e.add_entry(data_set.tree, data_set.name + "_lep1_e", data_set.legend_name, data_set.n_event)
# distributions.append(lep1_e)
#
# min_jets_mass = DistributionPlotter("min_jets_mass", selection, "min_jets_mass_{}".format(detector), 50, 0, 140, "min_jets_mass @{}".format(detector), "min_jets_mass [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     min_jets_mass.add_entry(data_set.tree, data_set.name + "_min_jets_mass", data_set.legend_name, data_set.n_event)
# distributions.append(min_jets_mass)
#
second_min_jets_mass = DistributionPlotter("second_min_jets_mass", selection, "second_min_jets_mass_{}".format(detector), 50, 0, 140, "second_min_jets_mass @{}".format(detector), "second_min_jets_mass [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
for data_set in data_sets:
    second_min_jets_mass.add_entry(data_set.tree, data_set.name + "_second_min_jets_mass", data_set.legend_name, data_set.n_event)
distributions.append(second_min_jets_mass)

# max_b_tag = DistributionPlotter("jet4_logbtag", selection, "max_b_tag_{}".format(detector), 80, 0, 150, "max_b_tag @{}".format(detector), "max_b_tag [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     max_b_tag.add_entry(data_set.tree, data_set.name + "_max_b_tag", data_set.legend_name, data_set.n_event)
# distributions.append(max_b_tag)
#
# second_max_b_tag = DistributionPlotter("jet3_logbtag", selection, "second_max_b_tag_{}".format(detector), 500, 0, 500, "second_max_b_tag @{}".format(detector), "second_max_b_tag [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     second_max_b_tag.add_entry(data_set.tree, data_set.name + "_second_max_b_tag", data_set.legend_name, data_set.n_event)
# distributions.append(second_max_b_tag)
#
# sum_max_b_tag = DistributionPlotter("jet4_logbtag + jet3_logbtag", selection, "sum_max_b_tag_{}".format(detector), 80, 0, 150, "sum_max_b_tag @{}".format(detector), "sum_max_b_tag [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     sum_max_b_tag.add_entry(data_set.tree, data_set.name + "_sum_max_b_tag", data_set.legend_name, data_set.n_event)
# distributions.append(sum_max_b_tag)
#
missing_rec_e = DistributionPlotter("missing_rec_e", selection, "missing_rec_e_{}".format(detector), 80, -10, 300, "missing_rec_e @{}".format(detector), "missing_rec_e [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
for data_set in data_sets:
    missing_rec_e.add_entry(data_set.tree, data_set.name + "_missing_rec_e", data_set.legend_name, data_set.n_event)
distributions.append(missing_rec_e)

# missing_sim_e = DistributionPlotter("missing_sim_e", selection, "missing_sim_e_{}".format(detector), 80, 0, 250, "missing_sim_e @{}".format(detector), "missing_sim_e [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     missing_sim_e.add_entry(data_set.tree, data_set.name + "_missing_sim_e", data_set.legend_name, data_set.n_event)
# distributions.append(missing_sim_e)

# total_rec_m = DistributionPlotter("total_rec_m", selection, "total_rec_m_{}".format(detector), 80, 0, 350, "total_rec_m @{}".format(detector), "total_rec_m [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     total_rec_m.add_entry(data_set.tree, data_set.name + "_total_rec_m", data_set.legend_name, data_set.n_event)
# distributions.append(total_rec_m)







############TOP CONSTRAINER#######################
# chi2_algorithm = DistributionPlotter("chi2_algorithm", selection, "chi2_algorithm_{}".format(detector), 80, 0, 10000, "chi2_algorithm @{}".format(detector), "chi2_algorithm", "", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     chi2_algorithm.add_entry(data_set.tree, data_set.name + "_chi2_algorithm", data_set.legend_name, data_set.n_event)
# distributions.append(chi2_algorithm)
#
tophadRec = DistributionPlotter("tophadRec", selection, "tophadRec_{}".format(detector), 24, 0, 350, "Mass of the hadronic decayed top @{}".format(detector), "m_{top, hadronic} [GeV]", "GeV", norm = False, logy = False, stack = True, set_title = False)
for data_set in data_sets:
    tophadRec.add_entry(data_set.tree, data_set.name + "_tophadRec", data_set.legend_name)
distributions.append(tophadRec)
#
# whadRec = DistributionPlotter("whadRec", selection, "whadRec_{}".format(detector), 80, 0, 150, "whadRec @{}".format(detector), "whadRec [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     whadRec.add_entry(data_set.tree, data_set.name + "_whadRec", data_set.legend_name, data_set.n_event)
# distributions.append(whadRec)
#
# toplepRec = DistributionPlotter("toplepRec", selection, "toplepRec_{}".format(detector), 150, 0, 250, "toplepRec @{}".format(detector), "toplepRec [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     toplepRec.add_entry(data_set.tree, data_set.name + "_toplepRec", data_set.legend_name, data_set.n_event)
# distributions.append(toplepRec)
#
# wlepRec = DistributionPlotter("wlepRec", selection, "wlepRec_{}".format(detector), 150, -150, 180, "wlepRec @{}".format(detector), "wlepRec [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     wlepRec.add_entry(data_set.tree, data_set.name + "_wlepRec", data_set.legend_name, data_set.n_event)
# distributions.append(wlepRec)
#
# missingMassRec = DistributionPlotter("missingMassRec", selection, "missingMassRec_{}".format(detector), 100, -150, 200, "missingMassRec @{}".format(detector), "missingMassRec [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     missingMassRec.add_entry(data_set.tree, data_set.name + "_missingMassRec", data_set.legend_name, data_set.n_event)
# distributions.append(missingMassRec)
#
# missingMassFit = DistributionPlotter("missingMassFit", selection, "missingMassFit_{}".format(detector), 100, -150, 100, "missingMassFit @{}".format(detector), "missingMassFit [GeV]", "GeV", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     missingMassFit.add_entry(data_set.tree, data_set.name + "_missingMassFit", data_set.legend_name, data_set.n_event)
# distributions.append(missingMassFit)
#
# chi2_tophadRec = DistributionPlotter("chi2_tophadRec", selection, "chi2_tophadRec_{}".format(detector), 80, 0, 50, "chi2_tophadRec @{}".format(detector), "chi2_tophadRec", "", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     chi2_tophadRec.add_entry(data_set.tree, data_set.name + "_chi2_tophadRec", data_set.legend_name, data_set.n_event)
# distributions.append(chi2_tophadRec)
#
# chi2_whadRec = DistributionPlotter("chi2_whadRec", selection, "chi2_whadRec_{}".format(detector), 80, 0, 50, "chi2_whadRec @{}".format(detector), "chi2_whadRec", "", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     chi2_whadRec.add_entry(data_set.tree, data_set.name + "_chi2_whadRec", data_set.legend_name, data_set.n_event)
# distributions.append(chi2_whadRec)
#
# chi2_toplepRec = DistributionPlotter("chi2_toplepRec", selection, "chi2_toplepRec_{}".format(detector), 150, 0, 50, "chi2_toplepRec @{}".format(detector), "chi2_toplepRec", "", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     chi2_toplepRec.add_entry(data_set.tree, data_set.name + "_chi2_toplepRec", data_set.legend_name, data_set.n_event)
# distributions.append(chi2_toplepRec)
#
# chi2_wlepRec = DistributionPlotter("chi2_wlepRec", selection, "chi2_wlepRec_{}".format(detector), 80, 0, 50, "chi2_wlepRec @{}".format(detector), "chi2_wlepRec", "", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     chi2_wlepRec.add_entry(data_set.tree, data_set.name + "_chi2_wlepRec", data_set.legend_name, data_set.n_event)
# distributions.append(wlepRec)


chi2_top_constrainer = DistributionPlotter("chi2_top_constrainer", selection, "chi2_top_constrainer_{}".format(detector), 10, 0, 40, "#chi^{}-like variable from the kineamtic constraint @{}".format("{2}", detector), "#chi^{}-like variable".format("{2}"), "", norm = False, logy = True, stack = True, set_title = True)
for data_set in data_sets:
    chi2_top_constrainer.add_entry(data_set.tree, data_set.name + "_chi2_top_constrainer", data_set.legend_name, data_set.n_event)
distributions.append(chi2_top_constrainer)








######################### NUMBER OF PARTICLES ########################
# n_rec = DistributionPlotter("n_rec", selection, "n_rec_{}".format(detector), 141, 0, 140, "n_rec @{}".format(detector), "n_rec", "", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     n_rec.add_entry(data_set.tree, data_set.name + "_n_rec", data_set.legend_name, data_set.n_event)
# distributions.append(n_rec)

# n_rec_charged = DistributionPlotter("n_rec_charged", selection, "n_rec_charged_{}".format(detector), 86, 0, 85, "n_rec_charged @{}".format(detector), "n_rec_charged", "", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     n_rec_charged.add_entry(data_set.tree, data_set.name + "_n_rec_charged", data_set.legend_name, data_set.n_event)
# distributions.append(n_rec_charged)

# n_rec_neutral = DistributionPlotter("n_rec_neutral", selection, "n_rec_neutral_{}".format(detector), 16, 0, 15, "n_rec_neutral @{}".format(detector), "n_rec_neutral", "", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     n_rec_neutral.add_entry(data_set.tree, data_set.name + "_n_rec_neutral", data_set.legend_name, data_set.n_event)
# distributions.append(n_rec_neutral)
#
# n_rec_photon = DistributionPlotter("n_rec_photon", selection, "n_rec_photon_rec_{}".format(detector), 51, 0, 50, "n_rec_photon @{}".format(detector), "n_rec_photon", "", norm = False, logy = True, stack = True, set_title = True)
# for data_set in data_sets:
#     n_rec_photon.add_entry(data_set.tree, data_set.name + "_n_rec_photon", data_set.legend_name, data_set.n_event)
# distributions.append(n_rec_photon)






############# SAVING #########################

if save == True:
    save_file = TFile(dir_fig + save_root_file_name, "RECREATE")
    save_file.cd()
    for distribution in distributions:
        distribution.save_pdf(dir_fig)
        distribution.write()
