names = [
    ["hz", "HZ inclusive", 130., "Pythia8"],
    ["zz", "ZZ inclusive", 500., "Pythia8"],
    ["tt_dilep", "t #bar{t} di-lepton", 750.*0.09, "Pythia8"],
    ["tt_allhad", "t #bar{t} all-hadronic", 750.*0.46, "Pythia8"],
    ["ww", "WW inclusive", 5000., "Pythia8"],
    ["tt_semilep", "t #bar{t} single-lepton", 750.*0.45, "Madgraph"],
]

legend_names = {x[0]: x[1] for x in names}
print "legend_names =", legend_names
cross_sections = {x[0]: x[2] for x in names}
print "cross_sections =", cross_sections
generators = {x[0]: x[3] for x in names}
print "generators =", generators

data_set_names = [
                  "hz",
                  "zz",
                  "tt_dilep",
                  "tt_allhad",
                  "ww",
                  "tt_semilep",
                 ]
