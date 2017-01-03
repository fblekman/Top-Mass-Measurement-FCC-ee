from ROOT import TH1D, TCanvas, TF1, TFile, TTree, TLegend, TGraph, kFALSE
from math import sqrt
import numpy
from QuarksDistroPlotter import QuarksDistroPlotter
from cebefo_style import cebefo_style

cebefo_style()

variable = "rec_zed_m"
title = "Zed invariant mass"
xtitle = "zed mass [GeV]"

# variable = "zed_gen_stable_m"
# title = "Zed invariant mass with stable gen particles"
# xtitle = "zed mass [GeV]"


template = "ntuple_new/qq_ILD{}/analyzers.ZqqIPEventsTreeProducer.ZqqIPEventsTreeProducer_1/tree.root"
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
    histogram = TH1D("h" + form, title, 18, 80, 95)
    histogram.SetStats(kFALSE)
    histogram.GetYaxis().SetTitle("Entries/ {:3.1f} GeV".format(histogram.GetBinWidth(1)))
    histogram.GetXaxis().SetTitle(xtitle)
    tree.Project(histogram.GetName(), variable)
    histogram.SetLineColor(len(histogram_list) + 2)
    histogram.Fit("gaus", "0", "", 88, 96)
    histogram.Fit("gaus", "0", "", histogram.GetFunction("gaus").GetParameter(1)-2*histogram.GetFunction("gaus").GetParameter(2), 96)
    histogram.Fit("gaus", "0", "", histogram.GetFunction("gaus").GetParameter(1)-2*histogram.GetFunction("gaus").GetParameter(2), 96)
    legend.AddEntry(histogram, legend_name +
                            #    " RMS: {:.2f}".format(histogram.GetRMS()),
                               " #sigma: {:.3f}".format(histogram.GetFunction("gaus").GetParameter(2))
                            #    +  " #chi^{2}: " + "{:2.1f}".format(histogram.GetFunction("gaus").GetChisquare()),
                               ,"l")
    canvas.cd()
    histogram.Draw("same")
    histogram.GetFunction("gaus").SetLineColor(len(histogram_list) + 2)
    histogram.GetFunction("gaus").Draw("same")
    histogram_list.append(histogram)
    histogram_list[0].SetMaximum(1.1*histogram.GetMaximum())

legend.Draw("same")
