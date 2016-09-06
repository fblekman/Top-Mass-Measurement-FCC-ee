import numpy as np
from ROOT import TEllipse, TCanvas, TGraph, TLegend

def covarianceMatrixEllipse(covarianceMatrix, probability=0.683):

    k = np.sqrt(-2*np.log(1-probability))


    secondDerivativeMatrix = np.linalg.inv(covarianceMatrix)

    eigenvals, eigenvecs = np.linalg.eig(secondDerivativeMatrix)
    lambd = np.sqrt(eigenvals)
    angle = np.rad2deg(np.arctan(eigenvecs[1,0]/eigenvecs[0,0]))

    ellipse = TEllipse(0,0,k/lambd[0],k/lambd[1],0.,360.,angle)
    ellipse.SetFillStyle(0)
    ellipse.SetLineColor(2)
    ellipse.SetLineWidth(4)

    scale = max(k/lambd[0],k/lambd[1])


    return ellipse, scale

def combineCova(cova1,cova2):
    inv1 = np.linalg.inv(cova1)
    inv2 = np.linalg.inv(cova2)
    aux = inv1+inv2
    aux2 = np.linalg.inv(aux)
    return aux2
