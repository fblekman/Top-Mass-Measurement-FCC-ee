from ROOT import TH1D, TCanvas, TF1, TFile, TTree, TLegend, TGraph
from math import sqrt
import numpy
from QuarksDistroPlotter import QuarksDistroPlotter
from cebefo_style import cebefo_style

cebefo_style()

save = False
dir_fig = "fig/jets/"


detector = "ILD"
mode = ""
mode_save = "_sp_IP"


my_file = TFile("ntuple/qq_ILD_spIP/analyzers.ZqqIPJetsTreeProducer.ZqqIPJetsTreeProducer_1/tree.root","OPEN")
my_tree = my_file.Get("events")

qdp_btag = QuarksDistroPlotter(my_tree, "jet_btag", "", "btag_{}".format(detector)+mode_save, 100, 0., 1.01, "b-tag (jet probability) @{}".format(detector)  + mode, "b-tag", "", norm = True, logy = True, set_title = True)

qdp_logbtag = QuarksDistroPlotter(my_tree, "jet_logbtag", "", "logbtag_{}".format(detector)+mode_save, 100, 0, 600, "- log(b-tag) (jet probability) @{}".format(detector)  + mode, "- log(b-tag)", "", norm = True, logy = True, set_title = True)

qdp_log10btag = QuarksDistroPlotter(my_tree, "jet_log10btag", "", "log10btag_{}".format(detector)+mode_save, 100, -200, 0, "log_{}(b-tag) (jet probability) @{}".format("{10}", detector)  + mode, "log_{10}(b-tag)", "", norm = True, logy = True, set_title = True)

qdp_m_inv_signif_larger3 = QuarksDistroPlotter(my_tree, "jet_m_inv_signif_larger3", "", "m_inv_signif_larger3_{}".format(detector)+mode_save, 200, 0, 6, "Invariant mass of the tracks with significance > 3 @{}".format(detector)  + mode, "M_{inv}(tracks, significance > 3) [GeV]", "GeV", norm = True, logy = True, set_title = True)

qdp_n_larger3 = QuarksDistroPlotter(my_tree, "jet_n_signif_larger3", "", "n_larger3_{}".format(detector)+mode_save, 12, -0.001, 12, "Number of tracks with significance > 3 @{}".format(detector)  + mode, "n(tracks, significance > 3)", "", norm = True, logy = True, set_title = True)

qdp_angle_larger3 = QuarksDistroPlotter(my_tree, "jet_angle_wrt_jet_dir_larger3", "", "angle_larger3_{}".format(detector)+mode_save, 100, 0, 1, "Angle between jet direction and the tracks with significance > 3 @{}".format(detector)  + mode, "#Delta alpha (jet direction, tracks with s > 3)" , "", norm = True, logy = True, set_title = True)

# qdp_m_inv_charged = QuarksDistroPlotter(my_tree, "jet_m_inv_charged", "", "m_inv_charged_{}".format(detector)+mode_save, 200, 0, 10, "m inv charged @{}".format(detector)  + mode, "m inv charged [GeV]", "GeV", norm = False, logy = True, set_title = True)
#
# qdp_n_charged = QuarksDistroPlotter(my_tree, "jet_n_charged", "", "n_charged_{}".format(detector)+mode_save, 200, 0., 15, "n charged @{}".format(detector)  + mode, "n charged", "", norm = False, logy = True, set_title = True)
#
# qdp_angle_charged = QuarksDistroPlotter(my_tree, "jet_angle_wrt_jet_dir_charged", "", "angle_charged_{}".format(detector)+mode_save, 200, 0, 2, "angle charged @{}".format(detector)  + mode, "angle charged" , "", norm = False, logy = True, set_title = True)

qdps = [qdp_btag,
    qdp_logbtag,
    qdp_log10btag,
    qdp_m_inv_signif_larger3,
    qdp_n_larger3,
    qdp_angle_larger3,
    # qdp_m_inv_charged,
    # qdp_n_charged,
    # qdp_angle_charged
    ]

if save == True:
    save_file = TFile("fig/jets/b_tag_{}.root".format(detector)+mode_save, "RECREATE")
    save_file.cd()
for qdp in qdps:
    qdp.draw()
    if save == True:
        qdp.save_pdf(dir_fig)
        qdp.write()
