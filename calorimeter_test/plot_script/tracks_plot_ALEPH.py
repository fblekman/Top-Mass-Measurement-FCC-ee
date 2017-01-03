from ROOT import TH1D, TCanvas, TF1, TFile, TTree, TLegend, TGraph
from math import sqrt
import numpy
from QuarksDistroPlotter import QuarksDistroPlotter
from cebefo_style import cebefo_style

cebefo_style()
save = False
dir_fig = "fig/tracks/with_no_cut/"


detector = "ALEPH"
mode = " cpx IP"
mode_save = "_cpx_IP"


my_file = TFile("ntuple/outdir_cpx/qq/analyzers.ZqqIPTrackTreeProducer.ZqqIPTrackTreeProducer_2/tree.root","OPEN")
my_tree = my_file.Get("events")

impact_parameter_real = QuarksDistroPlotter(my_tree, "ip/sigma", "", "ip_divide_sigma_{}".format(detector), 200, -5, 5, "Ratio IP_{} / #sigma @{}".format("{mc}", detector), "IP_{mc} / #sigma", "", norm = True, logy = True, set_title = True)

track_significance = QuarksDistroPlotter(my_tree, "signif", "", "track_significance_{}".format(detector), 200, -10, 10, "Track significance @{}".format(detector), "Track significance", "", norm = True, logy = False, set_title = True)

track_significance_no_norm = QuarksDistroPlotter(my_tree, "signif", "", "track_significance_no_norm_{}".format(detector), 200, -10, 10, "Track significance @{}".format(detector), "Track significance", "", norm = False, logy = False, set_title = True)

track_resolution = QuarksDistroPlotter(my_tree, "sigma", "", "sigma_{}".format(detector), 200, 0, 1e-4, "#sigma @{}".format("{mc}", detector), "#sigma", "", norm = True, logy = True, set_title = True)

track_significance_logy = QuarksDistroPlotter(my_tree, "signif", "", "track_significance_logy_{}".format(detector), 200, -10, 10, "Track significance @{}".format(detector), "Track significance", "", norm = True, logy = True, set_title = True)

track_probability = QuarksDistroPlotter(my_tree, "track_probability", "", "track_probability_{}".format(detector), 201, -1, 1, "Track probability @{}".format(detector), "Track probability", "", norm = True, logy = True, set_title = True)

d_j_signif = QuarksDistroPlotter(my_tree, "d_j_signif", "", "d_j_signif_{}".format(detector), 200, -10, 10, "Significance of the distance of min approach to jet dir @{}".format(detector), "D_{j} significance", "", norm = True, logy = True, set_title = True)


# signif fit
h_signif = TH1D("h_signif_{}".format(detector), "Negative significance tracks @{}".format(detector), 200, 0, 20)
h_signif.GetXaxis().SetTitle("- track significance")
h_signif.GetYaxis().SetTitle("Entries / {:3.2f} ".format(h_signif.GetBinWidth(1)))
my_tree.Project("h_signif_{}".format(detector), "-signif", "signif < 0")

c_signif = TCanvas("c_signif_{}".format(detector), "c_signif", 800, 600)
c_signif.cd()
c_signif.SetLogy()

f_dist = TF1("f_dist","[0]*abs(x)*exp((-1)*(x^2)/(2*[1]^2) )", 0, 15)
f_dist.SetParameters(100., 1.)
h_signif.Fit(f_dist, "L", "", 0, 3)

h_signif.Draw()

# signif fit
h_signif_light_quarks = TH1D("h_signif_light_quarks_{}".format(detector), "Significance of u, d, s quarks tracks @{}".format(detector), 200, -5, 5)
h_signif_light_quarks.GetXaxis().SetTitle("track significance")
h_signif_light_quarks.GetYaxis().SetTitle("Entries / {:3.2f} ".format(h_signif_light_quarks.GetBinWidth(1)))
my_tree.Project("h_signif_light_quarks_{}".format(detector), "signif", "quark_type <= 3")

c_signif_light_quarks = TCanvas("c_signif_light_quarks_{}".format(detector), "c_signif_light_quarks", 800, 600)
c_signif_light_quarks.cd()

f_dist_light_quarks = TF1("f_dist_light_quarks","[0]*abs(x)*exp((-1)*(x^2)/(2*[1]^2) )", -5, 5)
f_dist_light_quarks.SetParameters(100., 1.)
h_signif_light_quarks.Fit(f_dist_light_quarks, "L", "", -5, 5)

h_signif_light_quarks.Draw()


qdps = [impact_parameter_real, track_significance, track_significance_no_norm, track_resolution, track_significance_logy, track_probability, d_j_signif]

if save == True:
    save_file = TFile("fig/tracks/with_cut/track_significance_{}.root".format(detector), "RECREATE")
    save_file.cd()
for qdp in qdps:
    qdp.draw()
    if save == True:
        qdp.save_pdf(dir_fig)
        qdp.write()

if save == True:
    c_signif.Write()
    c_signif_light_quarks.Write()
    c_signif.Print(dir_fig + c_signif.GetName() + ".pdf", "pdf")
    c_signif_light_quarks.Print(dir_fig + c_signif_light_quarks.GetName() + ".pdf", "pdf")
