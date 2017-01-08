from numpy import genfromtxt
from ROOT import TFile
from plotting_tools import DistributionPlotter, TopMassStyle, DataSet
from ttbarDataDictionaries import legend_names, cross_sections, generators

def save_distributions(save_root_file_name, distributions):
    save_file = TFile(save_root_file_name, "RECREATE")
    save_file.cd()
    for distribution in distributions:
        # distribution.save_pdf(dir_fig)
        distribution.write()

if __name__ == "__main__":
    TopMassStyle.TopMassStyle()

    save = False
    detector = "ILD"
    dir_fig = "fig/"
    save_root_file_name = "01_fig/discriminating_variables_{}.root".format(detector)

    luminosity = 1000.
    filename_template = "ntuple/{}/heppy.analyzers.tree.TreeTTSemilep.TreeTTSemilep_1/tree.root"

    sample_names = [
        'hz',
        'tt_semilep',
        'ww',
        'tt_dilep',
        'tt_allhad',
        'zz',
        ]
    filenames = []
    files = []
    trees = []
    datasets = []
    distributions = []

    for sample_name in sample_names:
        aux_filename = filename_template.format(sample_name)
        aux_file = TFile.Open(aux_filename)
        aux_tree = aux_file.Get("events")
        aux_dataset = DataSet.DataSet(aux_tree, sample_name, legend_names[sample_name], cross_sections[sample_name], luminosity, generators[sample_name])

        filenames.append(aux_filename)
        files.append(aux_file)
        trees.append(aux_tree)
        datasets.append(aux_dataset)

    #lepton
    lep1_e = DistributionPlotter.DistributionPlotter("lep1_e",
                                         "",
                                         "lep1_e_{}".format(detector),
                                         48, 0, 150,
                                         "Lepton Energy @{}".format(detector),
                                         "Lepton Energy [GeV]", "GeV",
                                         norm=True,
                                         logy=False,
                                         stack=False,
                                         set_title=True)
    lep1_e.add_dataset_list(datasets)
    distributions.append(lep1_e)

    lep1_iso_e = DistributionPlotter.DistributionPlotter("lep1_iso_e",
                                     "",
                                     "lep1_iso_e_{}".format(detector),
                                     48, 0, 20.,
                                     "Lepton Iso E @{}".format(detector),
                                     "Lepton Iso E [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    lep1_iso_e.add_dataset_list(datasets)
    distributions.append(lep1_iso_e)

    lep1_iso_num = DistributionPlotter.DistributionPlotter("lep1_iso_num",
                                     "",
                                     "lep1_iso_num_{}".format(detector),
                                     15, 0, 15.,
                                     "Lepton Iso Num @{}".format(detector),
                                     "Lepton Iso Num", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    lep1_iso_num.add_dataset_list(datasets)
    distributions.append(lep1_iso_num)

    lep1_iso_pt_wrt_lepton = DistributionPlotter.DistributionPlotter("lep1_iso_pt_wrt_lepton",
                                     "",
                                     "lep1_iso_pt_wrt_lepton_{}".format(detector),
                                     48, 0, 4.,
                                     "Lepton Iso Pt wrt Lepton @{}".format(detector),
                                     "Lepton Iso Pt wrt Lepton [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    lep1_iso_pt_wrt_lepton.add_dataset_list(datasets)
    distributions.append(lep1_iso_pt_wrt_lepton)

    max_jet_e = DistributionPlotter.DistributionPlotter("max_jet_e",
                                         "",
                                         "max_jet_e_{}".format(detector),
                                         48, 0, 180,
                                         "Max Jet Energy @{}".format(detector),
                                         "Max Jet Energy [GeV]", "GeV",
                                         norm=True,
                                         logy=False,
                                         stack=False,
                                         set_title=True)
    max_jet_e.add_dataset_list(datasets)
    distributions.append(max_jet_e)

    min_jet_e = DistributionPlotter.DistributionPlotter("min_jet_e",
                                         "",
                                         "min_jet_e_{}".format(detector),
                                         48, 0, 80,
                                         "Min Jet Energy @{}".format(detector),
                                         "Min Jet Energy [GeV]", "GeV",
                                         norm=True,
                                         logy=False,
                                         stack=False,
                                         set_title=True)
    min_jet_e.add_dataset_list(datasets)
    distributions.append(min_jet_e)

    #######JETS MASS#########
    four_jets_mass = DistributionPlotter.DistributionPlotter("four_jets_mass",
                                         "",
                                         "four_jets_mass_{}".format(detector),
                                         48, 0, 340,
                                         "Hadronic Mass @{}".format(detector),
                                         "hadronic mass [GeV]", "GeV",
                                         norm=True,
                                         logy=False,
                                         stack=False,
                                         set_title=True)
    four_jets_mass.add_dataset_list(datasets)
    distributions.append(four_jets_mass)

    min_jets_mass = DistributionPlotter.DistributionPlotter("min_jets_mass",
                                         "",
                                         "min_jets_mass_{}".format(detector),
                                         48, 0, 120,
                                         "Min Jets Mass @{}".format(detector),
                                         "Min Jets mass [GeV]", "GeV",
                                         norm=True,
                                         logy=False,
                                         stack=False,
                                         set_title=True)
    min_jets_mass.add_dataset_list(datasets)
    distributions.append(min_jets_mass)

    second_min_jets_mass = DistributionPlotter.DistributionPlotter("second_min_jets_mass",
                                         "",
                                         "second_min_jets_mass_{}".format(detector),
                                         48, 0, 150,
                                         "Second Min Jets Mass @{}".format(detector),
                                         "Second Min Jets mass [GeV]", "GeV",
                                         norm=True,
                                         logy=False,
                                         stack=False,
                                         set_title=True)
    second_min_jets_mass.add_dataset_list(datasets)
    distributions.append(second_min_jets_mass)

    max_jets_mass = DistributionPlotter.DistributionPlotter("max_jets_mass",
                                         "",
                                         "max_jets_mass_{}".format(detector),
                                         48, 0, 220,
                                         "Max Jets Mass @{}".format(detector),
                                         "Max Jets mass [GeV]", "GeV",
                                         norm=True,
                                         logy=False,
                                         stack=False,
                                         set_title=True)
    max_jets_mass.add_dataset_list(datasets)
    distributions.append(max_jets_mass)

    ############JETS ANGLE#############
    min_jets_angle = DistributionPlotter.DistributionPlotter("min_jets_angle",
                                     "",
                                     "min_jets_angle_{}".format(detector),
                                     48, 0, 2,
                                     "Min Jets Angle @{}".format(detector),
                                     "Min Jets Angle", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    min_jets_angle.add_dataset_list(datasets)
    distributions.append(min_jets_angle)

    second_min_jets_angle = DistributionPlotter.DistributionPlotter("second_min_jets_angle",
                                     "",
                                     "second_min_jets_angle_{}".format(detector),
                                     48, 0, 2,
                                     "Second Min Jets Angle @{}".format(detector),
                                     "Second Min Jets Angle", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    second_min_jets_angle.add_dataset_list(datasets)
    distributions.append(second_min_jets_angle)

    max_jets_angle = DistributionPlotter.DistributionPlotter("max_jets_angle",
                                     "",
                                     "max_jets_angle_{}".format(detector),
                                     48, 0, 3.14,
                                     "Max Jets Angle @{}".format(detector),
                                     "Max Jets Angle", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    max_jets_angle.add_dataset_list(datasets)
    distributions.append(max_jets_angle)

    ###########JETS LEPTON ANGLE#######
    min_jets_lepton_angle = DistributionPlotter.DistributionPlotter("min_jets_lepton_angle",
                                     "",
                                     "min_jets_lepton_angle_{}".format(detector),
                                     48, 0, 3.14,
                                     "Min Jets lepton Angle @{}".format(detector),
                                     "Min Jets lepton Angle", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    min_jets_lepton_angle.add_dataset_list(datasets)
    distributions.append(min_jets_lepton_angle)

    second_min_jets_lepton_angle = DistributionPlotter.DistributionPlotter("second_min_jets_lepton_angle",
                                     "",
                                     "second_min_jets_lepton_angle_{}".format(detector),
                                     48, 0, 3.14,
                                     "Second Min Jets Lepton Angle @{}".format(detector),
                                     "Second Min Jets Lepton Angle", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    second_min_jets_lepton_angle.add_dataset_list(datasets)
    distributions.append(second_min_jets_lepton_angle)

    max_jets_lepton_angle = DistributionPlotter.DistributionPlotter("max_jets_lepton_angle",
                                     "",
                                     "max_jets_lepton_angle_{}".format(detector),
                                     48, 1.5, 3.14,
                                     "Max Jets Lepton Angle @{}".format(detector),
                                     "Max Jets Lepton Angle", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    max_jets_lepton_angle.add_dataset_list(datasets)
    distributions.append(max_jets_lepton_angle)


    ###########lepton pt wrt Jet
    lep_pt_wrt_closest_jet = DistributionPlotter.DistributionPlotter("lep_pt_wrt_closest_jet",
                                     "",
                                     "lep_pt_wrt_closest_jet_{}".format(detector),
                                     48, 0, 80.,
                                     "Lepton Pt wrt closest jet @{}".format(detector),
                                     "Lepton Pt wrt closest jet [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    lep_pt_wrt_closest_jet.add_dataset_list(datasets)
    distributions.append(lep_pt_wrt_closest_jet)

    lep_pt_wrt_second_closest_jet = DistributionPlotter.DistributionPlotter("lep_pt_wrt_second_closest_jet",
                                     "",
                                     "lep_pt_wrt_second_closest_jet_{}".format(detector),
                                     48, 0, 100.,
                                     "Lepton Pt wrt second closest jet @{}".format(detector),
                                     "Lepton Pt wrt second closest jet [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    lep_pt_wrt_second_closest_jet.add_dataset_list(datasets)
    distributions.append(lep_pt_wrt_second_closest_jet)

    lep_pt_wrt_farthest_jet = DistributionPlotter.DistributionPlotter("lep_pt_wrt_farthest_jet",
                                     "",
                                     "lep_pt_wrt_farthest_jet_{}".format(detector),
                                     48, 0, 80.,
                                     "Lepton Pt wrt farthestt jet @{}".format(detector),
                                     "Lepton Pt wrt farthestt jet [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    lep_pt_wrt_farthest_jet.add_dataset_list(datasets)
    distributions.append(lep_pt_wrt_farthest_jet)

    #other
    total_rec_mass = DistributionPlotter.DistributionPlotter("total_rec_mass",
                                     "",
                                     "total_rec_mass_{}".format(detector),
                                     48, 0, 350.,
                                     "Total Rec Mass @{}".format(detector),
                                     "Total Rec Mass [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    total_rec_mass.add_dataset_list(datasets)
    distributions.append(total_rec_mass)

    jets_vecp_over_sump = DistributionPlotter.DistributionPlotter("jets_vecp_over_sump",
                                     "",
                                     "jets_vecp_over_sump_{}".format(detector),
                                     48, 0, 1.,
                                     "Jets VecP over SumP @{}".format(detector),
                                     "Jets VecP over SumP", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    jets_vecp_over_sump.add_dataset_list(datasets)
    distributions.append(jets_vecp_over_sump)

    jets_sumpt = DistributionPlotter.DistributionPlotter("jets_sumpt",
                                     "",
                                     "jets_sumpt_{}".format(detector),
                                     48, 0, 350.,
                                     "Jets Sum Pt @{}".format(detector),
                                     "Jets Sum Pt [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    jets_sumpt.add_dataset_list(datasets)
    distributions.append(jets_sumpt)

    sphericity_jets = DistributionPlotter.DistributionPlotter("sphericity_jets",
                                     "",
                                     "sphericity_jets_{}".format(detector),
                                     48, 0, 1,
                                     "Sphericity jets @{}".format(detector),
                                     "Sphericity jets", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    sphericity_jets.add_dataset_list(datasets)
    distributions.append(sphericity_jets)

    planarity_jets = DistributionPlotter.DistributionPlotter("planarity_jets",
                                     "",
                                     "planarity_jets_{}".format(detector),
                                     48, 0, 0.5,
                                     "Planarity jets @{}".format(detector),
                                     "Planarity jets", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    planarity_jets.add_dataset_list(datasets)
    distributions.append(planarity_jets)

    aplanarity_jets = DistributionPlotter.DistributionPlotter("aplanarity_jets",
                                     "",
                                     "aplanarity_jets_{}".format(detector),
                                     48, 0, 0.5,
                                     "Aplanarity jets @{}".format(detector),
                                     "Aplanarity jets", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    aplanarity_jets.add_dataset_list(datasets)
    distributions.append(aplanarity_jets)

    sphericity_axis_jets = DistributionPlotter.DistributionPlotter("sphericity_axis_jets",
                                     "",
                                     "sphericity_axis_jets_{}".format(detector),
                                     48, -1, 1,
                                     "Sphericity axis jets @{}".format(detector),
                                     "Sphericity axis jets", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    sphericity_axis_jets.add_dataset_list(datasets)
    distributions.append(sphericity_axis_jets)



    n_rec_charged = DistributionPlotter.DistributionPlotter("n_rec_charged",
                                     "",
                                     "n_rec_charged_{}".format(detector),
                                     48, 0, 100,
                                     "N rec charged @{}".format(detector),
                                     "N rec charged", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    n_rec_charged.add_dataset_list(datasets)
    distributions.append(n_rec_charged)

    e_rec_charged = DistributionPlotter.DistributionPlotter("e_rec_charged",
                                     "",
                                     "e_rec_charged_{}".format(detector),
                                     48, 0, 350,
                                     "E rec charged @{}".format(detector),
                                     "E rec charged [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    e_rec_charged.add_dataset_list(datasets)
    distributions.append(e_rec_charged)

    missing_rec_e = DistributionPlotter.DistributionPlotter("missing_rec_e",
                                     "",
                                     "missing_rec_e_{}".format(detector),
                                     48, -30, 200,
                                     "Missin energy reco @{}".format(detector),
                                     "Missin energy reco [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    missing_rec_e.add_dataset_list(datasets)
    distributions.append(missing_rec_e)

    missing_rec_m = DistributionPlotter.DistributionPlotter("missing_rec_m",
                                     "",
                                     "missing_rec_m_{}".format(detector),
                                     48, -30, 120,
                                     "Missin mass reco @{}".format(detector),
                                     "Missin mass reco [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    missing_rec_m.add_dataset_list(datasets)
    distributions.append(missing_rec_m)

    whadRec = DistributionPlotter.DistributionPlotter("whadRec",
                                     "",
                                     "whadRec_{}".format(detector),
                                     48, 40, 150,
                                     "W had rec @{}".format(detector),
                                     "W had rec [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    whadRec.add_dataset_list(datasets)
    distributions.append(whadRec)

    wlepRec = DistributionPlotter.DistributionPlotter("wlepRec",
                                     "",
                                     "wlepRec_{}".format(detector),
                                     48, 40, 120,
                                     "W lep rec @{}".format(detector),
                                     "W lep rec [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    wlepRec.add_dataset_list(datasets)
    distributions.append(wlepRec)

    tophadRec = DistributionPlotter.DistributionPlotter("tophadRec",
                                     "",
                                     "tophadRec_{}".format(detector),
                                     48, 120, 220,
                                     "Top had rec @{}".format(detector),
                                     "Top had rec [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    tophadRec.add_dataset_list(datasets)
    distributions.append(tophadRec)

    toplepRec = DistributionPlotter.DistributionPlotter("toplepRec",
                                     "",
                                     "toplepRec_{}".format(detector),
                                     48, 120, 250,
                                     "W lep rec @{}".format(detector),
                                     "W lep rec [GeV]", "GeV",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    toplepRec.add_dataset_list(datasets)
    distributions.append(toplepRec)

    chi2_whadRec = DistributionPlotter.DistributionPlotter("chi2_whadRec",
                                     "",
                                     "chi2_whadRec_{}".format(detector),
                                     48, 0, 30,
                                     "chi2 W had rec @{}".format(detector),
                                     "chi2 W had rec", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    chi2_whadRec.add_dataset_list(datasets)
    distributions.append(chi2_whadRec)

    chi2_wlepRec = DistributionPlotter.DistributionPlotter("chi2_wlepRec",
                                     "",
                                     "chi2_wlepRec_{}".format(detector),
                                     48, 0, 30,
                                     "chi2 W lep rec @{}".format(detector),
                                     "chi2 W lep rec", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    chi2_wlepRec.add_dataset_list(datasets)
    distributions.append(chi2_wlepRec)

    chi2_tophadRec = DistributionPlotter.DistributionPlotter("chi2_tophadRec",
                                     "",
                                     "chi2_tophadRec_{}".format(detector),
                                     48, 0, 30,
                                     "chi2 Top had rec @{}".format(detector),
                                     "chi2 Top had rec", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    chi2_tophadRec.add_dataset_list(datasets)
    distributions.append(chi2_tophadRec)

    chi2_toplepRec = DistributionPlotter.DistributionPlotter("chi2_toplepRec",
                                     "",
                                     "chi2_toplepRec_{}".format(detector),
                                     48, 0, 30,
                                     "chi2 W lep rec @{}".format(detector),
                                     "chi2 W lep rec", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    chi2_toplepRec.add_dataset_list(datasets)
    distributions.append(chi2_toplepRec)

    # chi2_algorithm = DistributionPlotter.DistributionPlotter("chi2_algorithm",
    #                                  "",
    #                                  "chi2_algorithm_{}".format(detector),
    #                                  48, 0, 1500,
    #                                  "chi2 algorithm @{}".format(detector),
    #                                  "chi2 algorithm", "",
    #                                  norm=True,
    #                                  logy=False,
    #                                  stack=False,
    #                                  set_title=True)
    # chi2_algorithm.add_dataset_list(datasets)
    # distributions.append(chi2_algorithm)

    chi2_top_constrainer = DistributionPlotter.DistributionPlotter("chi2_top_constrainer",
                                     "",
                                     "chi2_top_constrainer_{}".format(detector),
                                     48, 0, 50,
                                     "chi2 top constrainer @{}".format(detector),
                                     "chi2 top constrainer", "",
                                     norm=True,
                                     logy=False,
                                     stack=False,
                                     set_title=True)
    chi2_top_constrainer.add_dataset_list(datasets)
    distributions.append(chi2_top_constrainer)
