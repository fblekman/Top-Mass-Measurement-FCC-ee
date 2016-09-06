from ROOT import TH1D, TCanvas, TF1, TFile, TTree, TLegend, TGraph
from math import sqrt
import numpy
from cebefo_style import cebefo_style

cebefo_style()
save = True

detector = "ALEPH"
mode = "simple_ip"

my_file = TFile("ntuple/outdir_sp/qq/analyzers.ZqqIPJetsTreeProducer.ZqqIPJetsTreeProducer_1/tree.root","OPEN")
my_tree = my_file.Get("events")

# quality check
total_uu = my_tree.GetEntries("quark_type <= 3")
total_cc = my_tree.GetEntries("quark_type == 4")
total_bb = my_tree.GetEntries("quark_type == 5")

total_events = my_tree.GetEntries()

print "uu entries", total_uu
print "cc entries", total_cc
print "bb entries", total_bb
print "total entries", total_events

# graphs
g_roc = TGraph()
g_roc.SetNameTitle("g_roc","ROC curve for b-jets @{}".format(detector) + " " + mode)

g_roc_b_eff_c_eff = TGraph()
g_roc_b_eff_c_eff.SetNameTitle("g_roc_b_eff_c_eff","Roc curve b-jet vs c-jet efficiency @{}".format(detector) + " " + mode)


g_uu_eff = TGraph()
g_uu_eff.SetNameTitle("g_uu_eff","Flavor efficiency tagging @{}".format(detector) + " " + mode)


g_cc_eff = TGraph()
g_cc_eff.SetNameTitle("g_cc_eff","Flavor efficiency tagging @{}".format(detector) + " " + mode)


g_bb_eff = TGraph()
g_bb_eff.SetNameTitle("g_bb_eff","Flavor efficiency tagging @{}".format(detector) + " " + mode)



g_bb_pur = TGraph()
g_bb_pur.SetNameTitle("g_bb_pur","Flavor efficiency tagging @{}".format(detector) + " " + mode)



leg_eff = TLegend(0.2,0.6,0.6,0.8)
leg_eff.AddEntry(g_uu_eff,"u, d, s jets efficiency","p")
leg_eff.AddEntry(g_cc_eff,"c jets efficiency","p")
leg_eff.AddEntry(g_bb_eff,"b jets efficiency","p")
leg_eff.AddEntry(g_bb_pur,"b jets purity","p")


# canvases
c_roc = TCanvas("c_roc_{}_".format(detector) + mode, "ROC curve for b jets @{}".format(detector), 800, 600)
c_roc_b_eff_c_eff = TCanvas("c_roc_b_eff_c_eff_{}_".format(detector) + mode, "Product efficiency x purity for b-jets @{}".format(detector), 800, 600)
c_eff = TCanvas("c_eff_{}_".format(detector) + mode, "Jets b-tagging efficiency @{}".format(detector), 800, 600)

canvases = [c_roc, c_roc_b_eff_c_eff, c_eff]

# starting fill graphs
n_points = 200
cut_max = -200

cuts = numpy.linspace(cut_max,0,n_points)

for i, cut_value in enumerate(cuts):

    cut_string = "jet_log10btag < {cv}".format(cv=cut_value)

    n_uu = float(my_tree.GetEntries(cut_string + "&& quark_type <= 3"))
    n_cc = float(my_tree.GetEntries(cut_string + "&& quark_type == 4"))
    n_bb = float(my_tree.GetEntries(cut_string + "&& quark_type == 5"))

    uu_eff = n_uu/total_uu
    cc_eff = n_cc/total_cc
    bb_eff = n_bb/total_bb

    bb_pur = (n_bb) / (n_uu + n_cc + n_bb)

    g_roc.SetPoint(i, bb_eff, bb_pur)
    g_roc_b_eff_c_eff.SetPoint(i, bb_eff, cc_eff)
    g_uu_eff.SetPoint(i, cut_value, uu_eff)
    g_cc_eff.SetPoint(i, cut_value, cc_eff)
    g_bb_eff.SetPoint(i, cut_value, bb_eff)
    g_bb_pur.SetPoint(i, cut_value, bb_pur)

c_roc.cd()
c_roc.SetGrid()
g_roc.Draw("alp")
g_roc.GetXaxis().SetTitle("b-jet efficiency")
g_roc.GetYaxis().SetTitle("b-jet purity")
g_roc.SetMarkerStyle(3)
g_roc.SetMarkerColor(2)

c_roc_b_eff_c_eff.cd()
c_roc_b_eff_c_eff.SetGrid()
g_roc_b_eff_c_eff.Draw("alp")
g_roc_b_eff_c_eff.SetMarkerStyle(3)
g_roc_b_eff_c_eff.SetMarkerColor(4)
g_roc_b_eff_c_eff.GetXaxis().SetTitle("b-jet efficiency")
g_roc_b_eff_c_eff.GetYaxis().SetTitle("c-jet efficiency")

c_eff.cd()
c_eff.SetGrid()
g_uu_eff.GetXaxis().SetRangeUser(cut_max, 1)
g_uu_eff.Draw("ap")
g_cc_eff.Draw("p same")
g_bb_eff.Draw("p same")
g_bb_pur.Draw("p same")
leg_eff.Draw("same")

g_uu_eff.GetXaxis().SetTitle("log_{10} b-tag cut")
g_uu_eff.SetMarkerStyle(20)
g_uu_eff.SetMarkerColor(2)
g_cc_eff.SetMarkerStyle(21)
g_cc_eff.SetMarkerColor(3)
g_bb_eff.SetMarkerStyle(22)
g_bb_eff.SetMarkerColor(4)
g_bb_pur.SetMarkerStyle(5)
g_bb_pur.SetMarkerColor(6)

if save == True:
    save_file = TFile("fig/roc/roc_curves_" + mode + "_{}.root".format(detector), "RECREATE")
    save_file.cd()
for canvas in canvases:
    canvas.Update()
    if save == True:
        canvas.Write()
        canvas.Print("fig/roc/" + canvas.GetName() + ".pdf", "pdf")
