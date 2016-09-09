import numpy as np
from ROOT import TEllipse, TCanvas, TGraph, TLegend

class CovarianceMatrix2DContourPlot(object):
    """

    TODO: extend the class to plot more than one covariance_matrix!
    TODO: raise exceptions in the init code instead of printing some erros message!
    """

    def __init__(self, name, mean, covariance_matrix, args = dict(sigma = 1)):
        """ """
        self.name = name
        self.mean = mean
        self.covariance_matrix = covariance_matrix
        self.args = args

        if len(self.args) != 1:
            print "args length different than 1"
            return

        if 'sigma' in self.args:
            self.sigma = self.args['sigma']
            self.k = self.sigma
        elif 'probability' in self.args:
            self.probability = self.args['probability']
            if self.probability > 1 or self.probability < 0:
                print "probability must be between 0 and 1!"
                return
            self.k = np.sqrt(-2 * np.log(1 - self.probability))
        else:
            print "neither 'sigma' nor 'probability' in args"
            return

        self.second_derivative_matrix = np.linalg.inv(self.covariance_matrix)

        self.eigenvals, self.eigenvecs = np.linalg.eig(self.second_derivative_matrix)
        self.lambd = np.sqrt(self.eigenvals)
        self.angle = np.rad2deg(np.arctan(self.eigenvecs[1,0]/self.eigenvecs[0,0]))

        self.ellipse = TEllipse(self.mean[0],
                                self.mean[1],
                                self.k/self.lambd[0],
                                self.k/self.lambd[1],
                                0.,
                                360.,
                                self.angle)
        self.ellipse.SetFillStyle(0)
        self.ellipse.SetLineColor(2)
        self.ellipse.SetLineWidth(4)

        self.scale = max(self.k/self.lambd[0], self.k/self.lambd[1])

    def Draw(self):

        self.canvas = TCanvas("canvas_" + self.name, self.name, 800, 600)

        self.x_axis = np.array([-self.scale * 2.1, self.scale * 2.1, 0., 0., 0., 0.])
        self.y_axis = np.array([0., 0., 0., -self.scale * 2.1, 0., self.scale * 2.1])
        self.axis = TGraph(6, x, y)
        self.axis.SetNameTitle("axis_" + self.name, self.name)

        self.ellipse.SetFillStyle(3001)
        self.ellipse.SetFillColor(2)
        self.ellipse.SetLineColor(2)
        self.ellipse.SetLineWidth(4)

        self.legend = TLegend(0.7407705, 0.6983945, 0.9911717, 0.928899)
        self.legend.AddEntry(self.ellipse, "FCC-ee 1 #sigma ", "f")

        self.canvas.cd()
        self.canvas.SetGrid()

        self.axis.Draw("AP")
        self.ellipse.Draw("same")
        self.legend.Draw("same")


    def LoadExternalPoints(self):

        external_points = TGraph()
        external_points.SetNameTitle()

        with open(fileName) as f:
            for i, line in enumerate(f):
                data = line.split()
                external_points.SetPoint(i, data[0], data[1])

        external_points.GetXaxis().SetLimits(-6, 6)
        external_points.GetYaxis().SetRangeUser(-6, 10)
        external_points.GetXaxis().SetTitle("#Delta g_{L} / g_{L} (%)")
        external_points.GetYaxis().SetTitle("#Delta g_{R} / g_{R} (%)")
        external_points.SetTitle("Expected relative precision on the Zt_{L}t_{L} and Zt_{R}t_{R} couplings at FCC-ee")
        external_points.SetMarkerSize(0.4)
        external_points.SetMarkerStyle(20)

        self.legend.AddEntry(external_points, "4DCHM f #leq 1.5 TeV", "p")
