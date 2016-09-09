import numpy as np
from ROOT import TEllipse, TCanvas, TGraph, TLegend
from plotting_tools.CovarianceMatrix2DContourPlot import CovarianceMatrix2DContourPlot
from plotting_tools.TopMassStyle import TopMassStyle

class CovarianceMatrixPlotWithExternalPoints(CovarianceMatrix2DContourPlot):
    """

    TODO: extend the class to plot more than one covariance_matrix!
    TODO: raise exceptions in the init code instead of printing some erros message!
    """

    def __init__(self, name, fit_parameters, covariance_matrix, args, filename, percentage = False):
        """ """
        super(CovarianceMatrixPlotWithExternalPoints, self).__init__(name,
                                                                     fit_parameters,
                                                                     covariance_matrix,
                                                                     args)

        self.percentage = percentage
        if self.percentage == True:
            self.ellipse_dimension *= 100.
            fit_parameters *= 100.
            
        self.LoadExternalPoints(filename)

    def LoadExternalPoints(self, filename):
        self.external_points = TGraph()
        with open(filename) as f:
            for i, line in enumerate(f):
                data = line.split()
                self.external_points.SetPoint(i, float( data[0] ), float( data[1] ) )

    def PrepareDraw(self, title = '', ellipse_legend_title = '', external_points_legend_title = '', xtitle = '', ytitle = ''):

        if self.percentage == True:
            self.xtitle = xtitle + " (%)"
            self.ytitle = ytitle + " (%)"

        super(CovarianceMatrixPlotWithExternalPoints, self).PrepareDraw(title,
                                                                        ellipse_legend_title,
                                                                        xtitle,
                                                                        ytitle)

        self.external_points_legend_title = external_points_legend_title
        self.external_points.SetNameTitle(self.name, self.title)
        self.external_points.SetMarkerSize(0.4)
        self.external_points.SetMarkerStyle(20)

        self.external_points.GetXaxis().SetTitle(self.xtitle)
        self.external_points.GetYaxis().SetTitle(self.ytitle)

        self.legend.AddEntry(self.external_points, self.external_points_legend_title, "p")

    def Draw(self):
        TopMassStyle()

        self.canvas = TCanvas("canvas_" + self.name, self.title, 800, 600)
        self.canvas.cd()
        self.canvas.SetGrid()

        self.graph_axis.Draw("AP")
        self.external_points.Draw("same P")
        self.ellipse.Draw("same")
        self.legend.Draw("same")
