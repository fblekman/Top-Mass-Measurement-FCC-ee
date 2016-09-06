from DistributionPlotter import DistributionPlotter
from cebefo_style import cebefo_style
from ROOT import TFile

cebefo_style()

save = False
detector = "ILD"
dir_fig = "fig/tt_check/"
save_root_file_name = "tt_check_{}.root".format(detector)

files = []
names = []
trees = []

files.append(TFile("ntuple/tt_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("tt_semilep_ILD")



distributions = []

# selection = "lep1_e > 0 && success == 1 && abs(mc_lepton_pdgid) != 15"
selection = ""

lep1_res_var = "lep1_e - mc_lepton_e"
lep1_res = DistributionPlotter(lep1_res_var, "", "lep1_res_{}".format(detector), 200, -2, 2, "lep1_res @{}".format(detector), "lep1_res [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    lep1_res.add_entry(tree, names[i] + "_lep1_res", names[i])
distributions.append(lep1_res)

neutrino_res_var = "missing_rec_e - mc_neutrino_e"
neutrino_res = DistributionPlotter(neutrino_res_var, "", "neutrino_res_{}".format(detector), 200, -0, 100, "neutrino_res @{}".format(detector), "neutrino_res [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    neutrino_res.add_entry(tree, names[i] + "_neutrino_res", names[i])
distributions.append(neutrino_res)

neutrino_mc_res_var = "missing_sim_e - mc_neutrino_e"
neutrino_mc_res = DistributionPlotter(neutrino_mc_res_var, "", "neutrino_mc_res_{}".format(detector), 200, -0, 100, "neutrino_mc_res @{}".format(detector), "neutrino_mc_res [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    neutrino_mc_res.add_entry(tree, names[i] + "_neutrino_mc_res", names[i])
distributions.append(neutrino_mc_res)

missing_mass_tc_var = "missingMassRec - missing_rec_m"
missing_mass_tc = DistributionPlotter(missing_mass_tc_var, "success == 1", "missing_mass_tc_{}".format(detector), 2000, -5, 5, "missing_mass_tc @{}".format(detector), "missing_mass_tc [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    missing_mass_tc.add_entry(tree, names[i] + "_missing_mass_tc", names[i])
distributions.append(missing_mass_tc)

if save == True:
    save_file = TFile(dir_fig + save_root_file_name, "RECREATE")
    save_file.cd()
    for distribution in distributions:
        distribution.save_pdf(dir_fig)
        distribution.write()
