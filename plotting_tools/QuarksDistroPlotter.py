from ROOT import TH1D, TCanvas, TFile, TTree, TLegend, kFALSE
from plotting_tools.TopMassStyle import TopMassStyle

class QuarksDistroPlotter(object):

    def __init__(self, tree, variable, cut, name, nbin, xmin, xmax, title, xtitle, ytitle_unity_measure, norm = True, logy = False, set_title = True):

        TopMassStyle()

        # tree
        self.tree = tree
        self.name = name

        # histograms
        if set_title == False:
            self.h_uu = TH1D("h_uu_" + name, variable + " {" + cut + "}", nbin, xmin, xmax)
            self.h_cc = TH1D("h_cc_" + name, variable + " {" + cut + "}", nbin, xmin, xmax)
            self.h_bb = TH1D("h_bb_" + name, variable + " {" + cut + "}", nbin, xmin, xmax)
        elif set_title == True:
            self.h_uu = TH1D("h_uu_" + name, title, nbin, xmin, xmax)
            self.h_cc = TH1D("h_cc_" + name, title, nbin, xmin, xmax)
            self.h_bb = TH1D("h_bb_" + name, title, nbin, xmin, xmax)

        self.tree.Project(self.h_uu.GetName(), variable, "quark_type <= 3" + cut)
        self.h_uu.SetLineColor(2)
        self.h_uu.SetStats(kFALSE)
        self.tree.Project(self.h_cc.GetName(), variable, "quark_type == 4" + cut)
        self.h_cc.SetLineColor(3)
        self.h_cc.SetStats(kFALSE)
        self.tree.Project(self.h_bb.GetName(), variable, "quark_type == 5" + cut)
        self.h_bb.SetLineColor(4)
        self.h_bb.SetStats(kFALSE)
        self.h_bb.GetXaxis().SetTitle(xtitle)


        # normalization
        if norm == True:
            self.h_uu.Scale(1./self.h_uu.Integral())
            self.h_cc.Scale(1./self.h_cc.Integral())
            self.h_bb.Scale(1./self.h_bb.Integral())
            self.h_bb.GetYaxis().SetTitle("Normalized entries / {:3.2f} ".format(self.h_bb.GetBinWidth(1)) + ytitle_unity_measure)
        else:
            self.h_bb.GetYaxis().SetTitle("Entries / {:3.2f} ".format(self.h_bb.GetBinWidth(1)) + ytitle_unity_measure)

        # legend
        self.leg = TLegend(0.7,0.6,0.9,0.8)
        self.leg.AddEntry(self.h_uu,"u, d, s jets","l")
        self.leg.AddEntry(self.h_cc,"c jets","l")
        self.leg.AddEntry(self.h_bb,"b jets","l")

        # canvas
        self.c_qq = TCanvas("c_qq_" + name, title, 800, 600)

        self.c_qq.SetGrid()
        if logy == True:
            self.c_qq.SetLogy()

    def draw(self):
        self.c_qq.cd()
        self.h_bb.Draw()
        self.h_cc.Draw("same")
        self.h_uu.Draw("same")
        self.leg.Draw("same")

        maxs = [self.h_uu.GetBinContent(self.h_uu.GetMaximumBin()),
                self.h_cc.GetBinContent(self.h_cc.GetMaximumBin()),
                self.h_bb.GetBinContent(self.h_bb.GetMaximumBin()) ]
        self.h_bb.SetMaximum(1.2*max(maxs))

        self.c_qq.Update()

    def save_pdf(self,dir_name):
        self.c_qq.Print(dir_name + self.name + ".pdf", "pdf")

    def write(self):
        self.c_qq.Write()
