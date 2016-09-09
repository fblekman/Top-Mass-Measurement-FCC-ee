import numpy as np
from ROOT import TEllipse, TCanvas, TGraph, TLegend
from plotting_tools.TopMassStyle import TopMassStyle

class CovarianceMatrix2DContourPlot(object):
    """

    TODO: extend the class to plot more than one covariance_matrix!
    TODO: raise exceptions in the init code instead of printing some erros message!
    """

    def __init__(self, name, fit_parameters, covariance_matrix, args = dict(sigma = 1)):
        """ """
        self.name = name
        self.fit_parameters = fit_parameters
        self.covariance_matrix = covariance_matrix
        self.args = args

        if len(self.args) != 1:
            print "args length different than 1"
            return

        if 'sigma' in self.args:
            self.sigma = self.args['sigma']
            self.ellipse_dimension = self.sigma
        elif 'probability' in self.args:
            self.probability = self.args['probability']
            if self.probability > 1 or self.probability < 0:
                print "probability must be between 0 and 1!"
                return
            self.ellipse_dimension = np.sqrt(-2 * np.log(1 - self.probability))
        else:
            print "neither 'sigma' nor 'probability' in args"
            return

    def DefineEllipse(self):
        self.second_derivative_matrix = np.linalg.inv(self.covariance_matrix)

        self.eigenvals, self.eigenvecs = np.linalg.eig(self.second_derivative_matrix)
        self.lambd = np.sqrt(self.eigenvals)
        self.angle = np.rad2deg(np.arctan(self.eigenvecs[1,0]/self.eigenvecs[0,0]))

        self.ellipse = TEllipse(self.fit_parameters[0, 0],
                                self.fit_parameters[0, 1],
                                self.ellipse_dimension/self.lambd[0],
                                self.ellipse_dimension/self.lambd[1],
                                0.,
                                360.,
                                self.angle)
        self.ellipse.SetFillStyle(0)
        self.ellipse.SetLineColor(2)
        self.ellipse.SetLineWidth(4)

        self.graph_axis_range = max(self.ellipse_dimension/self.lambd[0], self.ellipse_dimension/self.lambd[1])

    def PrepareDraw(self, title = '', legend_title = '', xtitle = '', ytitle = ''):
        self.title = title
        self.legend_title = legend_title
        self.xtitle = xtitle
        self.ytitle = ytitle

        self.x_axis = np.array([-self.graph_axis_range * 2.1,
                                self.graph_axis_range * 2.1,
                                self.fit_parameters[0, 0],
                                self.fit_parameters[0, 0],
                                self.fit_parameters[0, 0],
                                self.fit_parameters[0, 0]])
        self.y_axis = np.array([self.fit_parameters[0, 1],
                                self.fit_parameters[0, 1],
                                self.fit_parameters[0, 1],
                                -self.graph_axis_range * 2.1,
                                self.fit_parameters[0, 1],
                                self.graph_axis_range * 2.1])
        self.graph_axis = TGraph(6, self.x_axis, self.y_axis)
        self.graph_axis.SetNameTitle("axis_" + self.name, self.title)
        self.graph_axis.GetXaxis().SetTitle(xtitle)
        self.graph_axis.GetYaxis().SetTitle(ytitle)
        self.graph_axis.GetXaxis().SetRangeUser(self.fit_parameters[0, 0] - self.graph_axis_range * 2.,
                                          self.fit_parameters[0, 0] + self.graph_axis_range * 2.)

        self.graph_axis.GetYaxis().SetRangeUser(self.fit_parameters[0, 1] - self.graph_axis_range * 2.,
                                          self.fit_parameters[0, 1] + self.graph_axis_range * 2.)

        self.ellipse.SetFillStyle(3001)
        self.ellipse.SetFillColor(2)
        self.ellipse.SetLineColor(2)
        self.ellipse.SetLineWidth(4)

        self.legend = TLegend(0.7407705, 0.6983945, 0.9911717, 0.928899)
        key, value = self.args.items()[0]
        if key == 'sigma':
            aux_legend_string = self.legend_title + " " + str(value) + ' #sigma'
        else:
            aux_legend_string = self.legend_title + " C.L. " + str(int(100 * value)) + '%'
        self.legend.AddEntry(self.ellipse, aux_legend_string, "f")

    def Draw(self):
        TopMassStyle()

        self.canvas = TCanvas("canvas_" + self.name, self.title, 800, 600)
        self.canvas.cd()
        self.canvas.SetGrid()

        self.graph_axis.Draw("AP")
        self.ellipse.Draw("same")
        self.legend.Draw("same")
