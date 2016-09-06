from ROOT import TH1D, THStack, TCanvas, TFile, TTree, TLegend, kFALSE
from plotting_tools.TopMassStyle import TopMassStyle

class DistributionPlotter:
    """
    #TODO: add entry method also directly with dataset class
    #TODO: check correct rescaling of data set with cuts
    """
    
    def __init__(self, variable, cut, name, nbin, xmin, xmax, title, xtitle, ytitle_unity_measure, norm = False, logy = False, stack = False, set_title = True):

        TopMassStyle()

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
        self.stack = stack
        self.set_title = set_title

        self.dataset = [[], []]
        self.histograms = []

        # legend
        self.leg = TLegend(0.7,0.6,0.9,0.8)

        # canvas
        self.canvas = TCanvas("canvas_" + self.name, self.title, 800, 600)
        self.canvas.SetGrid()
        if logy == True:
            self.canvas.SetLogy()

        if self.stack == False:
            self.maxs_histograms = []
        else:
            self.h_stack = THStack("h_stack_" + self.name, self.title)

    def add_entry(self, tree, name, legend_title, n_events = None):
        self.dataset[0].append(tree)
        self.dataset[1].append(name)

        histogram = TH1D("h_" + name, self.variable + " {" + self.cut + "}", self.nbin, self.xmin, self.xmax)
        self.dataset[0][-1].Project("h_" + name, self.variable, self.cut)

        histogram_aux = TH1D("h_aux_" + name, self.variable + " {" + self.cut + "}", self.nbin, self.xmin, self.xmax)
        self.dataset[0][-1].Project("h_aux_" + name, self.variable)


        # print "before", histogram.GetName(), histogram.GetEntries(), histogram.Integral()


        if n_events != None:
            if histogram.Integral() != 0:
                # print "n_events", n_events
                # print "histogram.Integral()", histogram.Integral()
                # print "histogram_aux.Integral()", histogram_aux.Integral()
                histogram.Scale( float(n_events) / float(histogram_aux.Integral() ) )

        # print "after", histogram.GetName(), histogram.GetEntries(), histogram.Integral()

        if self.norm == True:
            if histogram.Integral() != 0:
                histogram.Scale(1./histogram.Integral())
            else:
                print
                print "histogram " + histogram.GetName()
                print "imposible to normalize, integral = 0"
                print

            histogram.GetYaxis().SetTitle("Normalized entries / {:3.2f} ".format(histogram.GetBinWidth(1)) + self.ytitle_unity_measure)
        else:
            histogram.GetYaxis().SetTitle("Entries / {:3.2f} ".format(histogram.GetBinWidth(1)) + self.ytitle_unity_measure)


        histogram.GetXaxis().SetTitle(self.xtitle)
        i = len(self.dataset[0])
        histogram.SetStats(kFALSE)
        self.histograms.append( histogram )

        self.canvas.cd()
        if self.stack == False:
            histogram.SetLineColor(i+1)
            self.leg.AddEntry(histogram, legend_title, "l")
            histogram.Draw("same")
            self.maxs_histograms.append(histogram.GetBinContent(histogram.GetMaximumBin()) )
            self.histograms[0].SetMaximum( 1.2*max(self.maxs_histograms))
        else:
            histogram.SetLineStyle(1)
            histogram.SetLineWidth(1)
            histogram.SetFillColor(i+1)
            histogram.SetFillStyle(3000 + i)
            self.leg.AddEntry(histogram, legend_title, "f")
            self.h_stack.Add(histogram)
            self.h_stack.Draw()

            self.h_stack.GetXaxis().SetTitle(self.xtitle)
            if self.norm == True:
                self.h_stack.GetYaxis().SetTitle("Normalized entries / {:3.2f} ".format(histogram.GetBinWidth(1)) + self.ytitle_unity_measure)
            else:
                self.h_stack.GetYaxis().SetTitle("Entries / {:3.2f} ".format(histogram.GetBinWidth(1)) + self.ytitle_unity_measure)
                self.h_stack.SetMinimum(1)


        self.leg.Draw("same")
        self.canvas.Update()



    def save_pdf(self, dir_name):
        self.canvas.Print(dir_name + self.name + ".pdf", "pdf")

    def write(self):
        self.canvas.Write()
