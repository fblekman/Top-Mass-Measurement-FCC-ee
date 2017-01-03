from ROOT import TH1D, TCanvas, TF1, TFile, TTree, TLegend, TGraph
from math import sqrt
import numpy
from QuarksDistroPlotter import QuarksDistroPlotter
from cebefo_style import cebefo_style

cebefo_style()

save = True
detector = "CMS"
dir_fig = "fig/jets/"

my_file = TFile("ntuple/outdir_ALEPH/qq/analyzers.ZqqIPJetsWithMCTreeProducer.ZqqIPJetsWithMCTreeProducer_1/tree.root","OPEN")
my_tree = my_file.Get("events")

qdp_mc_quark_delta_alpha_wrt_nearest_gen_jet = QuarksDistroPlotter(my_tree, "mc_quark_delta_alpha_wrt_nearest_gen_jet", "", "mc_quark_delta_alpha_wrt_nearest_gen_jet_{}".format(detector), 200, 0., 1.5, "delta_alpha between gen_quark and gen_jet @{}".format(detector), "delta_alpha(gen_quark, gen_jet) [rad]", "[rad]", norm = True, logy = True, set_title = True)

qdp_mc_quark_delta_alpha_wrt_nearest_rec_jet = QuarksDistroPlotter(my_tree, "mc_quark_delta_alpha_wrt_nearest_rec_jet", "", "mc_quark_delta_alpha_wrt_nearest_rec_jet_{}".format(detector), 200, 0., 1.5, "delta_alpha between gen_quark and rec_jet @{}".format(detector), "delta_alpha(gen_quark, rec_jet) [rad]", "[rad]", norm = True, logy = True, set_title = True)

qdp_delta_alpha_gen_rec_jet = QuarksDistroPlotter(my_tree, "delta_alpha_gen_rec_jet", "", "delta_alpha_gen_rec_jet_{}".format(detector), 200, 0., 1.5, "delta_alpha between gen_jet and rec_jet @{}".format(detector), "delta_alpha(gen_jet, rec_jet) [rad]", "[rad]", norm = True, logy = True, set_title = True)



qdp_mc_quark_deltaE_wrt_nearest_gen_jet = QuarksDistroPlotter(my_tree, "mc_quark_nearest_gen_jet_e - mc_quark_e", "", "mc_quark_deltaE_wrt_nearest_gen_jet_{}".format(detector), 100, -20., 20., "deltaE between gen_jet and gen_quark @{}".format(detector), "E_{gen_jet} - E_{gen_quark} [GeV]", "[GeV]", norm = True, logy = False, set_title = True)

qdp_mc_quark_deltaE_wrt_nearest_rec_jet = QuarksDistroPlotter(my_tree, "mc_quark_nearest_rec_jet_e - mc_quark_e", "", "mc_quark_deltaE_wrt_nearest_rec_jet_{}".format(detector), 100, -20., 20., "deltaE between rec_jet and gen_quark @{}".format(detector), "E_{rec_jet} - E_{gen_quark} [GeV]", "[GeV]", norm = True, logy = False, set_title = True)

qdp_deltaE_gen_rec_jet = QuarksDistroPlotter(my_tree, "mc_quark_nearest_rec_jet_e - mc_quark_nearest_gen_jet_e", "", "deltaE_gen_rec_jet_{}".format(detector), 100, -20., 20., "deltaE between rec_jet and gen_jet @{}".format(detector), "E_{rec_jet} - E_{gen_jet} [GeV]", "[GeV]", norm = True, logy = False, set_title = True)

qdps = [qdp_mc_quark_delta_alpha_wrt_nearest_gen_jet, qdp_mc_quark_delta_alpha_wrt_nearest_rec_jet, qdp_delta_alpha_gen_rec_jet,
    qdp_mc_quark_deltaE_wrt_nearest_gen_jet, qdp_mc_quark_deltaE_wrt_nearest_rec_jet, qdp_deltaE_gen_rec_jet]

if save == True:
    save_file = TFile("fig/jets/delta_alpha_gen_rec_jet_{}.root".format(detector), "RECREATE")
    save_file.cd()
for qdp in qdps:
    qdp.draw()
    if save == True:
        qdp.save_pdf(dir_fig)
        qdp.write()
