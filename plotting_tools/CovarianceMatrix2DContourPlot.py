import numpy as np
from ROOT import TEllipse, TCanvas, TGraph, TLegend

class CovarianceMatrix2DContourPlot(object):
    """

    TODO: extend the class to plot more than one covariance_matrix!
    TODO: raise exceptions in the init code instead of printing some erros message!
    """

    def __init__(self, mean, covariance_matrix, args = dict(sigma = 1)):
        """ """
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

        self.secondDerivativeMatrix = np.linalg.inv(self.covarianceMatrix)

        self.eigenvals, self.eigenvecs = np.linalg.eig(self.secondDerivativeMatrix)
        self.lambd = np.sqrt(self.eigenvals)
        self.angle = np.rad2deg(np.arctan(self.eigenvecs[1,0]/self.eigenvecs[0,0]))

        self.ellipse = TEllipse(self.mean[0], self.mean[1], self.k/self.lambd[0], self.k/self.lambd[1], 0., 360., self.angle)
        self.ellipse.SetFillStyle(0)
        self.ellipse.SetLineColor(2)
        self.ellipse.SetLineWidth(4)

        self.scale = max(self.k/self.lambd[0], self.k/self.lambd[1])

    def draw(self):
        
