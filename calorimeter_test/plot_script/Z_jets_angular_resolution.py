from ROOT import TH1D, TCanvas, TF1, TFile, TTree, TLegend, TGraph, kFALSE
from math import sqrt
import numpy
from cebefo_style import cebefo_style

cebefo_style()

variable = "delta_alpha_gen_rec_jet"
title = "Zed jets angular resolution"
xtitle = "#Delta#alpha_{rec, gen}"

# variable = "zed_gen_stable_m"
# title = "Zed invariant mass with stable gen particles"
# xtitle = "zed mass [GeV]"


template = "ntuple_new/qq_ILD{}/analyzers.ZqqIPJetsWithMCTreeProducer.ZqqIPJetsWithMCTreeProducer_1/tree.root"
formats = [
    "",
    "_20res",
    "_0res",
    "_0res_ecal_hcal"
]
legend_names = [
    "hcal 50%",
    "hcal 20%",
    "hcal 0%",
    "hcal and ecal 0%"
]
file_names = [template.format(x) for x in formats]
files = [TFile.Open(file_name) for file_name in file_names]
trees = [tree_file.Get("events") for tree_file in files]

canvas = TCanvas("c_" + variable, title, 800, 600)
canvas.SetGrid()
legend = TLegend(0.7,0.6,0.9,0.8)
legend.SetFillStyle(0)
legend.SetBorderSize(0)

histogram_list = []
for tree, form, legend_name in zip(trees, formats, legend_names):
    histogram = TH1D("h" + form, title, 25, 0, 0.1)
    histogram.SetStats(kFALSE)
    histogram.GetYaxis().SetTitle("Entries/ {:.3f}".format(histogram.GetBinWidth(1)))
    histogram.GetXaxis().SetTitle(xtitle)
    tree.Project(histogram.GetName(), variable)
    histogram.SetLineColor(len(histogram_list) + 2)
    legend.AddEntry(histogram, legend_name +
                               " RMS: {:.3f}".format(histogram.GetRMS()), "l")
    canvas.cd()
    histogram.Draw("same")
    histogram_list.append(histogram)
    histogram_list[0].SetMaximum(1.1*histogram.GetMaximum())

legend.Draw("same")
