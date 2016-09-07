from ROOT import TFile, TCanvas, TH1D
from TopMassStyle import TopMassStyle

class PlotVariable:
    """Plot the distribution of a variable for different data samples.

    Previous class wrt to DistributionPlotter, probably can be replaced.
    TODO: replace this class.
    """

    def __init__(self, variable, cut, name, nbin, xmin, xmax, title, xtitle, ytitle_unity_measure, norm = False, logy = False, set_title = True):

        self.variable = variable
        self.cut = cut
        self.name = name
        self.nbin = nbin
        self.xmin = xmin
        self.xmax = xmax
        self.title = title
        self.xtitle = xtitle
        self.ytitle_unity_measure = ytitle_unity_measure
        self.norm = norm
        self.logy = logy
        self.set_title = set_title

        # canvas
        self.canvas = TCanvas("canvas_" + self.name, self.title, 800, 600)
        self.canvas.SetGrid()
        if logy == True:
            self.canvas.SetLogy()

    def add_entry(self, tree, name, n_events = None):

        self.histogram = TH1D("h_" + name, self.variable + " {" + self.cut + "}", self.nbin, self.xmin, self.xmax)
        tree.Project("h_" + name, self.variable, self.cut)
        if self.norm == True:
            self.histogram.Scale(1./self.histogram.Integral())
            self.histogram.GetYaxis().SetTitle("Normalized entries / {:3.2f} ".format(self.histogram.GetBinWidth(1)) + self.ytitle_unity_measure)
        else:
            self.histogram.GetYaxis().SetTitle("Entries / {:3.2f} ".format(self.histogram.GetBinWidth(1)) + self.ytitle_unity_measure)

        if n_events != None:
            self.histogram.Scale( float(n_events) / self.histogram.Integral())

        self.histogram.GetXaxis().SetTitle(self.xtitle)

        self.canvas.cd()
        self.histogram.Draw("same")

        self.canvas.Update()

    def save_pdf(self, dir_name):
        self.canvas.Print(dir_name + self.name + ".pdf", "pdf")

    def write(self):
        self.canvas.Write()

TopMassStyle()

save = False
detector = "ILD"
dir_fig = "fig/"
save_root_file_name = "top_constrainer_variables_{}.root".format(detector)


tt_file = TFile("ntuple/tt_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN")
tt_tree = tt_file.Get("events")

selection = "success == 1"

detector = "ILD"

distributions = []

tophadRec = PlotVariable("tophadRec", selection, "tophadRec_{}".format(detector), 80, 100, 250, "tophadRec @{}".format(detector), "tophadRec [GeV]", "GeV", norm = False, logy = False, set_title = True)
tophadRec.add_entry(tt_tree, "tophadRec")
distributions.append(tophadRec)

whadRec = PlotVariable("whadRec", selection, "whadRec_{}".format(detector), 80, 40, 150, "whadRec @{}".format(detector), "whadRec [GeV]", "GeV", norm = False, logy = False, set_title = True)
whadRec.add_entry(tt_tree, "whadRec")
distributions.append(whadRec)

toplepRec = PlotVariable("toplepRec", selection, "toplepRec_{}".format(detector), 80, 80, 250, "toplepRec @{}".format(detector), "toplepRec [GeV]", "GeV", norm = False, logy = False, set_title = True)
toplepRec.add_entry(tt_tree, "toplepRec")
distributions.append(toplepRec)

wlepRec = PlotVariable("wlepRec", selection, "wlepRec_{}".format(detector), 80, 40, 200, "wlepRec @{}".format(detector), "wlepRec [GeV]", "GeV", norm = False, logy = False, set_title = True)
wlepRec.add_entry(tt_tree, "wlepRec")
distributions.append(wlepRec)

with open('top_constrainer_variables.txt', 'w+') as f:

    for distribution in distributions:
        f.write(distribution.name + "\n")
        f.write("Mean = " + "{:.3f}".format(distribution.histogram.GetMean()) + " +- " + "{:.3f}".format(distribution.histogram.GetMeanError()) + "\n")
        f.write("RMS = " + "{:.3f}".format(distribution.histogram.GetRMS()) + " +- " + "{:.3f}".format(distribution.histogram.GetRMSError()) + "\n")

    f.write("\n\n\n")

    for distribution in distributions:
        f.write(distribution.variable + "_m = {:.2f}".format(distribution.histogram.GetMean()) + ",\n")
        f.write(distribution.variable + "_w = {:.2f}".format(distribution.histogram.GetRMS()) + ",\n")


if save == True:
    save_file = TFile(dir_fig + save_root_file_name, "RECREATE")
    save_file.cd()
    for distribution in distributions:
        distribution.save_pdf(dir_fig)
        distribution.write()
