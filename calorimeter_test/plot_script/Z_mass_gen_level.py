from ROOT import TH1D, TCanvas, TF1, TFile, TTree, TLegend, TGraph
from math import sqrt
import numpy
from QuarksDistroPlotter import QuarksDistroPlotter
from cebefo_style import cebefo_style

cebefo_style()


variable = "zed_gen_stable_m"
title = "Zed invariant mass with gen particles"
xtitle = "zed mass [GeV]"


file_name = "ntuple/qq_ILD_cut_genlevel/analyzers.TreeZqqGenLevel.TreeZqqGenLevel_1/tree.root"
root_file = TFile.Open(file_name)
tree = root_file.Get("events")

legend_names = [
    "#theta_{every} > 100 mrad, p_{charged} > 100 MeV",
    "+ E_{photons} > 100 MeV, E_{n hadrons} > 0.5 GeV",
    "+ E_{photons} > 100 MeV, E_{n hadrons} > 1 GeV",
    "+ E_{photons} > 500 MeV, E_{n hadrons} > 1 GeV",
]

variables = [
    "sum_particles_with_cut_m",
    "sum_p4_low_thresholds_m",
    "sum_p4_low_ecal_high_hcal_thresholds_m",
    "sum_p4_high_thresholds_m",
]

canvas = TCanvas("c_zed_mass", title, 800, 600)
canvas.SetGrid()
legend = TLegend(0.7, 0.6, 0.9, 0.8)

histogram_list = []
for variable, legend_name in zip(variables, legend_names):
    histogram = TH1D("h" + variable, title, 16, 84, 92)
    histogram.GetYaxis().SetTitle("Entries/ {:3.1f} GeV".format(histogram.GetBinWidth(1)))
    histogram.GetXaxis().SetTitle(xtitle)
    tree.Project(histogram.GetName(), variable)
    histogram.SetLineColor(len(histogram_list) + 2)
    legend.AddEntry(histogram, legend_name, "l")
    canvas.cd()
    histogram.Draw("same")
    histogram_list.append(histogram)
    # histogram_list[0].SetMaximum(1.2*histogram.GetMaximum())

legend.Draw("same")
