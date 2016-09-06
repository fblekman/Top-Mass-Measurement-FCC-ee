from DistributionPlotter import DistributionPlotter
from cebefo_style import cebefo_style
from ROOT import TFile

cebefo_style()

save = False
detector = "CMS"
dir_fig = "fig/kinematic_variables/"
save_root_file_name = "kinematic_variables_{}.root".format(detector)

files = []
names = []
trees = []

files.append(TFile("ntuple/tt_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("tt_semilep_ILD")

files.append(TFile("ntuple/tt_CMS/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("tt_semilep_CMS")


distributions = []

# selection = "lep1_e > 0 && success == 1 && abs(mc_lepton_pdgid) != 15"
selection = ""

four_jets_mass = DistributionPlotter("four_jets_mass", selection, "four_jets_mass_{}".format(detector), 200, 0, 400, "four_jets_mass @{}".format(detector), "four_jets_mass [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    four_jets_mass.add_entry(tree, names[i] + "_four_jets_mass", names[i])
distributions.append(four_jets_mass)

lep1_e = DistributionPlotter("lep1_e", selection, "lep1_e_{}".format(detector), 200, 0, 160, "lep1_e @{}".format(detector), "lep1_e [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    lep1_e.add_entry(tree, names[i] + "_lep1_e", names[i])
distributions.append(lep1_e)

min_jets_mass = DistributionPlotter("min_jets_mass", selection, "min_jets_mass_{}".format(detector), 200, 0, 150, "min_jets_mass @{}".format(detector), "min_jets_mass [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    min_jets_mass.add_entry(tree, names[i] + "_min_jets_mass", names[i])
distributions.append(min_jets_mass)

second_min_jets_mass = DistributionPlotter("second_min_jets_mass", selection, "second_min_jets_mass_{}".format(detector), 200, 0, 150, "second_min_jets_mass @{}".format(detector), "second_min_jets_mass [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    second_min_jets_mass.add_entry(tree, names[i] + "_second_min_jets_mass", names[i])
distributions.append(second_min_jets_mass)

missing_rec_e = DistributionPlotter("missing_rec_e", selection, "missing_rec_e_{}".format(detector), 200, -50, 300, "missing_rec_e @{}".format(detector), "missing_rec_e [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    missing_rec_e.add_entry(tree, names[i] + "_missing_rec_e", names[i])
distributions.append(missing_rec_e)

missing_sim_e = DistributionPlotter("missing_sim_e", selection, "missing_sim_e_{}".format(detector), 200, -50, 300, "missing_sim_e @{}".format(detector), "missing_sim_e [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    missing_sim_e.add_entry(tree, names[i] + "_missing_sim_e", names[i])
distributions.append(missing_sim_e)

tophadRec = DistributionPlotter("tophadRec", selection, "tophadRec_{}".format(detector), 80, 100, 250, "tophadRec @{}".format(detector), "tophadRec [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    tophadRec.add_entry(tree, names[i] + "_tophadRec", names[i])
distributions.append(tophadRec)

whadRec = DistributionPlotter("whadRec", selection, "whadRec_{}".format(detector), 80, 40, 120, "whadRec @{}".format(detector), "whadRec [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    whadRec.add_entry(tree, names[i] + "_whadRec", names[i])
distributions.append(whadRec)

toplepRec = DistributionPlotter("toplepRec", selection, "toplepRec_{}".format(detector), 80, 100, 350, "toplepRec @{}".format(detector), "toplepRec [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    toplepRec.add_entry(tree, names[i] + "_toplepRec", names[i])
distributions.append(toplepRec)

wlepRec = DistributionPlotter("wlepRec", selection, "wlepRec_{}".format(detector), 80, 40, 180, "wlepRec @{}".format(detector), "wlepRec [GeV]", "GeV", norm = False, logy = False, set_title = False)
for i, tree in enumerate(trees):
    wlepRec.add_entry(tree, names[i] + "_wlepRec", names[i])
distributions.append(wlepRec)

if save == True:
    save_file = TFile(dir_fig + save_root_file_name, "RECREATE")
    save_file.cd()
    for distribution in distributions:
        distribution.save_pdf(dir_fig)
        distribution.write()
