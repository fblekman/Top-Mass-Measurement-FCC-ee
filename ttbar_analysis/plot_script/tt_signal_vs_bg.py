from DistributionPlotter import DistributionPlotter
from cebefo_style import cebefo_style
from ROOT import TFile

cebefo_style()

save = False
detector = "ILD"
dir_fig = "fig/"
save_root_file_name = "signal_vs_bg_{}.root".format(detector)

luminosity = 1000.

files = []
trees = []
names = []
legend_names = []
cross_sections = []

files.append(TFile("ntuple/tt_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("tt_semilep")
legend_names.append("t #bar{t} single-lepton")
cross_sections.append(750.*0.45)

files.append(TFile("ntuple/ttlep_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("tt_dilep")
legend_names.append("t #bar{t} di-lepton")
cross_sections.append(750.*0.09)

files.append(TFile("ntuple/tthad_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("tt_allhad")
legend_names.append("t #bar{t} all-hadronic")
cross_sections.append(750.*0.46)

files.append(TFile("ntuple/hz_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("hz")
legend_names.append("HZ inclusive")
cross_sections.append(130.)

files.append(TFile("ntuple/zz_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("zz")
legend_names.append("ZZ inclusive")
cross_sections.append(500.)

files.append(TFile("ntuple/ww_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("ww")
legend_names.append("WW inclusive")
cross_sections.append(5000.)

distributions = []


# selection = "lep1_e > 0 && success == 1 && abs(mc_lepton_pdgid) != 15"
selection = ""

four_jets_mass = DistributionPlotter("four_jets_mass", selection, "four_jets_mass_{}".format(detector), 80, 0, 350, "four_jets_mass @{}".format(detector), "four_jets_mass [GeV]", "GeV", norm = False, logy = False, stack = True, set_title = True)
for i, tree in enumerate(trees):
    four_jets_mass.add_entry(tree, names[i] + "_four_jets_mass", legend_names[i], luminosity*cross_sections[i])
distributions.append(four_jets_mass)

lep1_e = DistributionPlotter("lep1_e", selection, "lep1_e_{}".format(detector), 80, 0, 160, "lep1_e @{}".format(detector), "lep1_e [GeV]", "GeV", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    lep1_e.add_entry(tree, names[i] + "_lep1_e", legend_names[i])
distributions.append(lep1_e)

min_jets_mass = DistributionPlotter("min_jets_mass", selection, "min_jets_mass_{}".format(detector), 80, 0, 140, "min_jets_mass @{}".format(detector), "min_jets_mass [GeV]", "GeV", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    min_jets_mass.add_entry(tree, names[i] + "_min_jets_mass", legend_names[i])
distributions.append(min_jets_mass)

second_min_jets_mass = DistributionPlotter("second_min_jets_mass", selection, "second_min_jets_mass_{}".format(detector), 80, 0, 140, "second_min_jets_mass @{}".format(detector), "second_min_jets_mass [GeV]", "GeV", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    second_min_jets_mass.add_entry(tree, names[i] + "_second_min_jets_mass", legend_names[i])
distributions.append(second_min_jets_mass)

max_b_tag = DistributionPlotter("jet4_logbtag", selection, "max_b_tag_{}".format(detector), 80, 0, 150, "max_b_tag @{}".format(detector), "max_b_tag [GeV]", "GeV", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    max_b_tag.add_entry(tree, names[i] + "_max_b_tag", legend_names[i])
distributions.append(max_b_tag)

second_max_b_tag = DistributionPlotter("jet3_logbtag", selection, "second_max_b_tag_{}".format(detector), 80, 0, 500, "second_max_b_tag @{}".format(detector), "second_max_b_tag [GeV]", "GeV", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    second_max_b_tag.add_entry(tree, names[i] + "_second_max_b_tag", legend_names[i])
distributions.append(second_max_b_tag)

sum_max_b_tag = DistributionPlotter("jet4_logbtag + jet3_logbtag", selection, "sum_max_b_tag_{}".format(detector), 80, 0, 150, "sum_max_b_tag @{}".format(detector), "sum_max_b_tag [GeV]", "GeV", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    sum_max_b_tag.add_entry(tree, names[i] + "sum_max_b_tag", legend_names[i])
distributions.append(sum_max_b_tag)

missing_rec_e = DistributionPlotter("missing_rec_e", selection, "missing_rec_e_{}".format(detector), 80, -10, 300, "missing_rec_e @{}".format(detector), "missing_rec_e [GeV]", "GeV", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    missing_rec_e.add_entry(tree, names[i] + "_missing_rec_e", legend_names[i])
distributions.append(missing_rec_e)

missing_sim_e = DistributionPlotter("missing_sim_e", selection, "missing_sim_e_{}".format(detector), 80, 0, 250, "missing_sim_e @{}".format(detector), "missing_sim_e [GeV]", "GeV", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    missing_sim_e.add_entry(tree, names[i] + "_missing_sim_e", legend_names[i])
distributions.append(missing_sim_e)

tophadRec = DistributionPlotter("tophadRec", selection, "tophadRec_{}".format(detector), 80, 80, 300, "tophadRec @{}".format(detector), "tophadRec [GeV]", "GeV", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    tophadRec.add_entry(tree, names[i] + "_tophadRec", legend_names[i])
distributions.append(tophadRec)

whadRec = DistributionPlotter("whadRec", selection, "whadRec_{}".format(detector), 80, 0, 150, "whadRec @{}".format(detector), "whadRec [GeV]", "GeV", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    whadRec.add_entry(tree, names[i] + "_whadRec", legend_names[i])
distributions.append(whadRec)

toplepRec = DistributionPlotter("toplepRec", selection, "toplepRec_{}".format(detector), 150, 0, 250, "toplepRec @{}".format(detector), "toplepRec [GeV]", "GeV", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    toplepRec.add_entry(tree, names[i] + "_toplepRec", legend_names[i])
distributions.append(toplepRec)

wlepRec = DistributionPlotter("wlepRec", selection, "wlepRec_{}".format(detector), 80, 0, 180, "wlepRec @{}".format(detector), "wlepRec [GeV]", "GeV", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    wlepRec.add_entry(tree, names[i] + "_wlepRec", legend_names[i])
distributions.append(wlepRec)

chi2 = DistributionPlotter("chi2", "success==0", "chi2_{}".format(detector), 80, 0, 1000, "chi2 @{}".format(detector), "chi2", "", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    chi2.add_entry(tree, names[i] + "_chi2", legend_names[i])
distributions.append(chi2)

n_rec = DistributionPlotter("n_rec", "", "n_rec_{}".format(detector), 1000, 0, 150, "n_rec @{}".format(detector), "n_rec", "", norm = False, logy = False, stack = False, set_title = True)
for i, tree in enumerate(trees):
    n_rec.add_entry(tree, names[i] + "_n_rec", legend_names[i])
distributions.append(n_rec)

# n_rec_charged = DistributionPlotter("n_rec_charged", "", "n_rec_charged_{}".format(detector), 1000, 0, 150, "n_rec_charged @{}".format(detector), "n_rec_charged", "", norm = False, logy = False, stack = False, set_title = True)
# for i, tree in enumerate(trees):
#     n_rec_charged.add_entry(tree, names[i] + "_n_rec_charged", legend_names[i])
# distributions.append(n_rec_charged)
#
# n_rec_neutral = DistributionPlotter("n_rec_neutral", "", "n_rec_neutral_{}".format(detector), 1000, 0, 150, "n_rec_neutral @{}".format(detector), "n_rec_neutral", "", norm = False, logy = False, stack = False, set_title = True)
# for i, tree in enumerate(trees):
#     n_rec_neutral.add_entry(tree, names[i] + "_n_rec_neutral", legend_names[i])
# distributions.append(n_rec_neutral)
#
# n_rec_photon = DistributionPlotter("n_rec_photon", "", "n_rec_photon_rec_{}".format(detector), 1000, 0, 150, "n_rec_photon @{}".format(detector), "n_rec_photon", "", norm = False, logy = False, stack = False, set_title = True)
# for i, tree in enumerate(trees):
#     n_rec_photon.add_entry(tree, names[i] + "_n_rec_photon", legend_names[i])
# distributions.append(n_rec_photon)

if save == True:
    save_file = TFile(dir_fig + save_root_file_name, "RECREATE")
    save_file.cd()
    for distribution in distributions:
        distribution.save_pdf(dir_fig)
        distribution.write()
