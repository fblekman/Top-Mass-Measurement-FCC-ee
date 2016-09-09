from ROOT import TTree, TFile
from utils.ComputeMVA import ComputeMVA

analysis = "b-tag"

if analysis == "tt":
    tt_file = TFile("../08_ttbar_analysis/05_two_detector_signal_test/ntuple/tt_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN")
    zz_file = TFile("../08_ttbar_analysis/05_two_detector_signal_test/ntuple/ww_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN")

    tt_tree = tt_file.Get("events")
    zz_tree = zz_file.Get("events")

    variables = ["four_jets_mass", "min_jets_mass", "second_min_jets_mass", "lep1_e", "missing_rec_e"]

    aux_file = TFile("./aux_tree.root", "RECREATE")
    my_mva = ComputeMVA(variables, zz_tree.CopyTree(""), tt_tree.CopyTree(""))

    my_mva.Perform()

elif analysis == "b-tag":
    my_file = TFile("./b-tagging_ntuple/qq_ILD_spIP/analyzers.ZqqIPJetsTreeProducer.ZqqIPJetsTreeProducer_1/tree.root","OPEN")
    my_tree = my_file.Get("events")

    variables = ["jet_logbtag", "jet_m_inv_signif_larger3", "jet_n_signif_larger3", "jet_angle_wrt_jet_dir_larger3"]

    aux_file = TFile("./aux_tree.root", "RECREATE")
    my_mva = ComputeMVA(variables, my_tree.CopyTree("quark_type <= 4"), my_tree.CopyTree("quark_type == 5"))

    my_mva.Perform()
