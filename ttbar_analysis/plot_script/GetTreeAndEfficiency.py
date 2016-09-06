from ROOT import TFile
from numpy import genfromtxt

def get_efficiency(name):
    eff_filename = "ntuple/{}_ILD/analyzers.CheckParticles.CheckParticles_1/events.txt".format(name)
    eff_file = genfromtxt(eff_filename,skip_header=1,delimiter='\t', dtype=None)
    return float( eff_file[3][3])

def get_tree(name):
    aux_file = TFile("ntuple/{}_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root".format(name),"OPEN")
    return aux_file, aux_file.Get("events")
