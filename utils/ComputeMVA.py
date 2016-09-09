from ROOT import TTree, TFile, TH1D, TCanvas, gDirectory, TGraph, TLegend, kFALSE
from plotting_tools.TopMassStyle import TopMassStyle
import numpy

class ComputeMVA(object):
    """Perform a multivariate analysis based on a simple algorithm.

    This MVA algorithm, thanks to its simplicity, provides you with
    a quite fast MVA which doesn't suffer of overtraining.

    The algorithm needs a background and a signal tree, and a list of variables
    that are going to be used in the computation.

    Basically the program calculates, for each event (both signal and background),
    the normalized number of background events that have all the values of the
    varaibles larger or equal than the event (that is the number of background events that look like signal more than the considered event). This is the generalization of the p-value in a given number of dimensions, wrt to the background
    distribution.
    This variable is the discriminating variable between signal and background,
    and can be transformed in a flat variable for bg and a variable peaked at 0 for signal.

    You can find a few examples in the __main__ part.
    """

    def __init__(self, variables_list, background_tree_training, signal_tree_training, n_max = 1e10, verbosity = 0):
        self.variables_list = variables_list
        self.background_tree_training = background_tree_training
        self.signal_tree_training = signal_tree_training
        self.n_max = n_max
        self.verbosity = verbosity

        if self.verbosity >=1:
            print "### INIT ###"
            print
            print "background entries", self.background_tree_training.GetEntries()
            print "signal entries", self.signal_tree_training.GetEntries()
            print

        self.variables_signs = []

        def get_mean(tree, variable):
            tree.Draw(variable + ">>" + variable)
            h = gDirectory.Get(variable)
            return h.GetMean()

        if self.verbosity >=1:
            print
            print "deciding sign looking at the means"
            print

        for variable in self.variables_list:
            mean_background = get_mean(self.background_tree_training, variable)
            mean_signal = get_mean(self.signal_tree_training, variable)

            if mean_background <= mean_signal:
                self.variables_signs.append(1)
            else:
                self.variables_signs.append(-1)

            if self.verbosity >=1:
                print variable
                print "mean_background", mean_background
                print "mean_signal", mean_signal
                print "sign", self.variables_signs[-1]

        self.background_histograms = []
        self.signal_histograms = []
        self.graphs = []
        self.canvases = []
        self.legendes = []

        TopMassStyle()

    def ComputePvalue(self, point):

        string_list = []
        for variable, variable_sign, point_component in zip(self.variables_list, self.variables_signs, point):
            if variable_sign == 1:
                sign = ">="
            elif variable_sign == -1:
                sign = "<="
            string_list.append(variable + sign + str(point_component))

        join_cuts = " && "
        cut_string = join_cuts.join(string_list)

        if self.verbosity >=2:
            print
            print "final cut_string"
            print cut_string
            print

        pvalue = float( self.background_tree_training.GetEntries(cut_string) )\
                      / self.background_tree_training.GetEntries()

        if self.verbosity >=1:
            print pvalue
        return pvalue

    def Training(self):

        self.discriminating_tree = TTree("discriminating_tree", "discriminating_tree")
        self.event_type = numpy.zeros(1, dtype=int, )
        self.discriminating_tree.Branch('event_type', self.event_type, 'event_type/I')

        self.value = numpy.zeros(1, dtype=float, )
        self.discriminating_tree.Branch('value', self.value, 'value/D')


        for i, event in enumerate(self.signal_tree_training):
            if i > self.n_max:
                continue

            self.event_type[0] = 1
            signal_values = []
            for variable in self.variables_list:
                signal_values.append( getattr(event, variable) )
            self.value[0] = self.ComputePvalue(signal_values)
            self.discriminating_tree.Fill()

        for i, event in enumerate(self.background_tree_training):
            if i > self.n_max:
                continue
            self.event_type[0] = 0
            background_values = []
            for variable in self.variables_list:
                background_values.append( getattr(event, variable) )
            self.value[0] = self.ComputePvalue(background_values)
            self.discriminating_tree.Fill()

    def Transform(self):

        self.transformed_discriminating_tree = TTree("transformed_discriminating_tree", "transformed_discriminating_tree")
        self.transformed_event_type = numpy.zeros(1, dtype=int, )
    	self.transformed_discriminating_tree.Branch('event_type', self.transformed_event_type, 'event_type/I')
        self.transformed_value = numpy.zeros(1, dtype=float, )
        self.transformed_discriminating_tree.Branch('value',self.transformed_value, 'value/D')

        for i, event in enumerate(self.discriminating_tree):
            if i > self.n_max:
                continue

            if getattr(event, "event_type") == 1:
                self.transformed_event_type[0] = 1
            else:
                self.transformed_event_type[0] = 0

            cut_string = "event_type == 0 && " + "value <= {}".format(getattr(event, "value"))
            self.transformed_value[0] = float( self.discriminating_tree.GetEntries(cut_string) ) / self.discriminating_tree.GetEntries("event_type == 0")
            self.transformed_discriminating_tree.Fill()

    def RocCurve(self, tree, name, title, n_points = 100):

        graph = TGraph()
        graph.SetNameTitle("g_roc_" + name, "ROC curve " + title)

        cuts = numpy.linspace(0, 20, n_points)

        for i, cut_value in enumerate(cuts):
            cut_string = "value <= {cv}".format(cv=10**(-cut_value))

            eff_signal = float( tree.GetEntries("event_type == 1 && " + cut_string) ) / tree.GetEntries("event_type == 1")
            eff_bg = float( tree.GetEntries("event_type == 0 && " + cut_string) ) / tree.GetEntries("event_type == 0")
            graph.SetPoint(i, eff_signal, 1. - eff_bg)

        graph.GetXaxis().SetTitle("Signal efficiency")
        graph.GetYaxis().SetTitle("1 - Background efficiency")
        graph.SetMarkerStyle(3)
        graph.SetMarkerColor(2)
        canvas = TCanvas("canvas_roc_" + name, "Canvas ROC " + title, 800, 600)
        canvas.SetGrid()
        canvas.cd()
        graph.Draw("alp")

        self.graphs.append( graph )
        self.canvases.append(canvas)

    def Draw(self, tree, name, title, xtitle, n_bin = 100):

        h_background = TH1D("h_background_" + name, title, n_bin, 0. , 1.001)
        tree.Project("h_background_" + name, "value", "event_type == 0")
        h_background.SetLineColor(2)
        h_background.SetStats(kFALSE)

        h_signal = TH1D("h_signal_" + name, title, n_bin, 0. , 1.001)
        tree.Project("h_signal_" + name, "value", "event_type == 1")
        h_signal.SetLineColor(4)
        h_signal.SetStats(kFALSE)

        h_signal.GetXaxis().SetTitle(xtitle)
        h_signal.GetYaxis().SetTitle("Normalized entries / {:3.2f} ".format(h_signal.GetBinWidth(1)) )


        h_background.Scale(1./h_background.Integral())
        h_signal.Scale(1./h_signal.Integral())

        legend = TLegend(0.7,0.6,0.9,0.8)
        legend.AddEntry(h_background, "background", "l")
        legend.AddEntry(h_signal, "signal", "l")

        canvas = TCanvas("canvas_" + name, title, 800, 600)
        canvas.SetGrid()
        canvas.cd()
        h_signal.Draw()
        h_background.Draw("same")
        legend.Draw("same")

        self.background_histograms.append( h_background )
        self.signal_histograms.append( h_signal )
        self.legendes.append( legend )
        self.canvases.append( canvas )

    def DrawRawVariables(self):

        self.raw_variables_canvases = []
        self.raw_var_background_histo = []
        self.raw_var_signal_histo = []
        self.raw_var_legendes = []

        for variable in self.variables_list:
            raw_variable_canvas = TCanvas("c_" + variable, variable, 800, 600)
            raw_variable_canvas.cd()
            raw_variable_canvas.SetGrid()

            self.raw_variables_canvases.append(raw_variable_canvas)

            h_background = TH1D("h_background_" + variable, variable, 30, 0. , 15)
            self.background_tree_training.Project("h_background_" + variable, variable)
            h_background.SetLineColor(2)
            h_background.SetStats(kFALSE)

            h_signal = TH1D("h_signal_" + variable, variable, 30, 0. , 15)
            self.signal_tree_training.Project("h_signal_" + variable, variable)
            h_signal.SetLineColor(4)
            h_signal.SetStats(kFALSE)

            h_signal.GetXaxis().SetTitle(variable)
            h_signal.GetYaxis().SetTitle("Normalized entries / {:3.2f} ".format(h_signal.GetBinWidth(1)) )

            h_background.Scale(1./h_background.Integral())
            h_signal.Scale(1./h_signal.Integral())

            legend = TLegend(0.7,0.6,0.9,0.8)
            legend.AddEntry(h_background, "background", "l")
            legend.AddEntry(h_signal, "signal", "l")

            h_signal.Draw()
            h_background.Draw("same")
            legend.Draw("same")

            self.raw_var_background_histo.append( h_background )
            self.raw_var_signal_histo.append( h_signal )
            self.raw_var_legendes.append( legend )

    def Perform(self):
        self.Training()
        self.Draw(self.discriminating_tree, "before_transf", "Separation of the two classes before transforming", "combined variable", 100)
        #self.RocCurve(self.discriminating_tree, "before_transf", "before transforming")
        self.Transform()
        self.Draw(self.transformed_discriminating_tree, "after_transf", "Separation of the two classes after transforming", "combined variable", 100)
        self.RocCurve(self.transformed_discriminating_tree, "after_transf", "")

if __name__ == '__main__':

    # analysis = "tt"
    analysis = "b-tag"

    if analysis == "tt":
        tt_file = TFile("../08_ttbar_analysis/05_two_detector_signal_test/ntuple/tt_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN")
        zz_file = TFile("../08_ttbar_analysis/05_two_detector_signal_test/ntuple/ww_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN")

        tt_tree = tt_file.Get("events")
        zz_tree = zz_file.Get("events")

        variables = ["four_jets_mass", "min_jets_mass", "second_min_jets_mass", "lep1_e", "missing_rec_e"]

        aux_file = TFile("./aux_tree.root", "RECREATE")
        my_mva = ComputeMVA(zz_tree.CopyTree(""), tt_tree.CopyTree(""), variables)

        my_mva.Perform()

    elif analysis == "b-tag":
        my_file = TFile("../02_b_tagging/18_without_beampipe_simple_ILD/ntuple/qq_ILD_spIP/analyzers.ZqqIPJetsTreeProducer.ZqqIPJetsTreeProducer_1/tree.root","OPEN")

        my_tree = my_file.Get("events")

        variables = ["jet_logbtag", "jet_m_inv_signif_larger3", "jet_n_signif_larger3", "jet_angle_wrt_jet_dir_larger3"]

        aux_file = TFile("./aux_tree.root", "RECREATE")
        my_mva = ComputeMVA(my_tree.CopyTree("quark_type <= 4"), my_tree.CopyTree("quark_type == 5"), variables)

        my_mva.Perform()
