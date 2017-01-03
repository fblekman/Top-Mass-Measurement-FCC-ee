from ROOT import TH1D, TCanvas, TF1, TFile, TTree, TLegend, TGraph
from math import sqrt
import numpy
from QuarksDistroPlotter import QuarksDistroPlotter
from cebefo_style import cebefo_style

cebefo_style()
save = False
dir_fig = "fig/tracks/with_no_cut/"


detector = "ILD"
mode = ""
mode_save = "_sp_IP"


my_file = TFile("ntuple/qq_ILD_spIP/analyzers.ZqqIPTrackTreeProducer.ZqqIPTrackTreeProducer_2/tree.root","OPEN")
my_tree = my_file.Get("events")

# ip mc
# impact_parameter_mc_zoom = QuarksDistroPlotter(my_tree, "ip", "", "ip_mc_zoom_{}".format(detector)+mode_save, 200, -1e-15, 1e-15, "IP_{} @{}".format("{mc}", detector) + mode, "IP_{mc} [m]", "m", norm = False, logy = True, set_title = True)
#
# # ip mc
# impact_parameter_mc = QuarksDistroPlotter(my_tree, "ip", "", "ip_mc_{}".format(detector)+mode_save, 200, -0.8e-3, 0.8e-3, "IP_{} @{}".format("{mc}", detector) + mode, "IP_{mc} [m]", "m", norm = False, logy = True, set_title = True)

# ip smeared
impact_parameter_smeared = QuarksDistroPlotter(my_tree, "ip_smeared", "", "ip_smeared_{}".format(detector)+mode_save, 150, -2e-3, 4e-3, "IP_{} @{}".format("{smeared}", detector) + mode, "IP_{smeared} [m]", "m", norm = True, logy = True, set_title = True)

# # track resolution
# track_resolution = QuarksDistroPlotter(my_tree, "sigma", "", "sigma_{}".format(detector)+mode_save, 200, 0, 1e-3, "#sigma @{}".format(detector) + mode, "#sigma [m]", "[m]", norm = True, logy = True, set_title = True)
#
# # track energy
# energy = QuarksDistroPlotter(my_tree, "track_e", "", "energy_{}".format(detector)+mode_save, 200, 0, 30, "Track energy [GeV] @{}".format(detector) + mode, "Track energy [GeV]", "[GeV]", norm = True, logy = False, set_title = True)

# # track significance mc
# track_significance_mc = QuarksDistroPlotter(my_tree, "ip/sigma", "", "ip_divide_sigma_{}".format(detector)+mode_save, 200, -5, 1000, "Ratio IP_{} / #sigma @{}".format("{mc}", detector) + mode, "IP_{mc} / #sigma", "", norm = False, logy = True, set_title = True)

# track significance smeared
# track_significance = QuarksDistroPlotter(my_tree, "signif", "", "track_significance_{}".format(detector)+mode_save, 200, -10, 10, "Track significance @{}".format(detector) + mode, "Track significance", "", norm = False, logy = False, set_title = True)

# track Significance
track_significance_logy = QuarksDistroPlotter(my_tree, "signif", "", "track_significance_logy_{}".format(detector)+mode_save, 200, -10, 50, "Track significance @{}".format(detector) + mode, "Track significance", "", norm = True, logy = True, set_title = True)

# track probability
track_probability = QuarksDistroPlotter(my_tree, "track_probability", "", "track_probability_{}".format(detector)+mode_save, 201, -1, 1, "Track probability @{}".format(detector) + mode, "Track probability", "", norm = True, logy = True, set_title = True)

# # d_j
# d_j = QuarksDistroPlotter(my_tree, "d_j", "", "d_j_{}".format(detector)+mode_save, 200, 0, 1e-1, "d_j @{}".format(detector) + mode, "d_j [m]", "[m]", norm = False, logy = True, set_title = True)
#
# # d_j_signif
# d_j_signif = QuarksDistroPlotter(my_tree, "d_j_signif", "", "d_j_signif_{}".format(detector)+mode_save, 200, -11, 1000, "Significance of the distance of min approach to jet dir @{}".format(detector) + mode, "D_{j} significance", "", norm = False, logy = True, set_title = True)
#
# # s_j_wrt_pr_vtx
# s_j_wrt_pr_vtx = QuarksDistroPlotter(my_tree, "s_j_wrt_pr_vtx", "", "s_j_wrt_pr_vtx_{}".format(detector)+mode_save, 200, -5e-3, 2e-1, "s_j_wrt_pr_vtx @{}".format(detector) + mode, "s_j_wrt_pr_vtx [m]", "[m]", norm = False, logy = True, set_title = True)


qdps = [
    # impact_parameter_mc_zoom,
    # impact_parameter_mc,
    impact_parameter_smeared,
    # track_resolution,
    # energy,
    # track_significance_mc,
    # track_significance,
    track_significance_logy,
    track_probability,
    # d_j,
    # d_j_signif,
    # s_j_wrt_pr_vtx
    ]

if save == True:
    save_file = TFile("fig/tracks/with_no_cut/sp_IP/track_with_no_cut_{}.root".format(detector)+mode_save, "RECREATE")
    save_file.cd()
for qdp in qdps:
    qdp.draw()
    if save == True:
        qdp.save_pdf(dir_fig)
        qdp.write()
