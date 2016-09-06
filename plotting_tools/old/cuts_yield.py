from ROOT import TFile
from numpy import genfromtxt

files = []
trees = []
names = []
cross_sections = []
eff_files = []
generators = []
luminosity = 1000.


files.append(TFile("ntuple_used/tt_semilep_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("$t\\bar{t}$ single-lep")
cross_sections.append(750.*0.45)
eff_files.append( genfromtxt("ntuple_used/tt_semilep_ILD/analyzers.CheckParticles.CheckParticles_1/events.txt",skip_header=1,delimiter='\t', dtype=None) )
generators.append("Madgraph")

files.append(TFile("ntuple_used/tt_dilep_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("$t\\bar{t}$ di-lep")
cross_sections.append(750.*0.09)
eff_files.append( genfromtxt("ntuple_used/tt_dilep_ILD/analyzers.CheckParticles.CheckParticles_1/events.txt",skip_header=1,delimiter='\t', dtype=None) )
generators.append("Pythia8")

files.append(TFile("ntuple_used/tt_allhad_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("$t\\bar{t}$ all-had")
cross_sections.append(750.*0.46)
eff_files.append( genfromtxt("ntuple_used/tt_allhad_ILD/analyzers.CheckParticles.CheckParticles_1/events.txt",skip_header=1,delimiter='\t', dtype=None) )
generators.append("Pythia8")

files.append(TFile("ntuple_used/hz_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("hz")
cross_sections.append(130.)
eff_files.append( genfromtxt("ntuple_used/hz_ILD/analyzers.CheckParticles.CheckParticles_1/events.txt",skip_header=1,delimiter='\t', dtype=None) )
generators.append("Pythia8")

files.append(TFile("ntuple_used/zz_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("zz")
cross_sections.append(500.)
eff_files.append( genfromtxt("ntuple_used/zz_ILD/analyzers.CheckParticles.CheckParticles_1/events.txt",skip_header=1,delimiter='\t', dtype=None) )
generators.append("Pythia8")

files.append(TFile("ntuple_used/ww_ILD/tree.TreeTTSemilep.TreeTTSemilep_1/tree.root","OPEN"))
trees.append(files[-1].Get("events"))
names.append("ww")
cross_sections.append(5000.)
eff_files.append( genfromtxt("ntuple_used/ww_ILD/analyzers.CheckParticles.CheckParticles_1/events.txt",skip_header=1,delimiter='\t', dtype=None) )
generators.append("Pythia8")


cuts = []

cuts.append("four_jets_mass > 150")
cuts.append("four_jets_mass < 270")

cuts.append("min_jets_mass > 10")
cuts.append("min_jets_mass < 90")

cuts.append("second_min_jets_mass > 20")
cuts.append("second_min_jets_mass < 100")

cuts.append("lep1_e < 100")

cuts.append("missing_rec_e > 20")
cuts.append("missing_rec_e < 150")

cuts.append("n_rec_charged >= 20")
# cuts.append("n_rec_charged >= 10")
cuts.append("chi2_top_constrainer <= 40")

cuts.append("success == 1")

##############2
# cuts.append("four_jets_mass > 180")
# cuts.append("four_jets_mass < 270")
#
# cuts.append("min_jets_mass > 15")
# cuts.append("min_jets_mass < 80")
#
# cuts.append("jet3_logbtag > 3")


#############3
# cuts.append("four_jets_mass > 180")
# cuts.append("four_jets_mass < 270")
#
# cuts.append("min_jets_mass > 15")
# cuts.append("min_jets_mass < 80")
# #
# # cuts.append("jet3_logbtag > 3")
#
# cuts.append("missing_rec_e > 20")
# cuts.append("missing_rec_e < 150")
# cuts.append("success == 1")

################ PERCENTAGE #######################
results = []
cumulative_cuts = []
for i, cut in enumerate(cuts):
    if i == 0:
        cumulative_cuts.append(cut)
    else:
        cumulative_cuts.append( cumulative_cuts[i-1] + " && " +  cut)



for cumulative_cut in cumulative_cuts:
    results.append( [] )
    for i, tree in enumerate(trees):
        eff = eff_files[i][3][3]
        results[-1].append( eff * float( tree.GetEntries(cumulative_cut) ) /  tree.GetEntries() )


# formatting the latex_code
lines = []

begin_line = "\\begin{table}\n"
starting_line = "\\begin{tabular}{c"
first_line_string_list = ["cut"]
generator_line_string_list = ["Generator"]
for name, generator in zip(names, generators):
    starting_line += "|c"
    first_line_string_list.append(name + " [\%]")
    generator_line_string_list.append(generator)
starting_line += "}\n"
first_line = " & ".join(first_line_string_list)
first_line += "\\\\ \n"
generator_line = " & ".join(generator_line_string_list)
generator_line += "\\\\ \n"


lines += [begin_line, starting_line, first_line, generator_line]


aux_string_list = ["Generated events"]
for eff_file in eff_files:
    print eff_file[0][1]
    print reduce(lambda x, y: x + " " + y, eff_file[0][1].split()[:-1])

    print eff_file[0][1].split()[-1]
    aux_string_list.append(eff_file[0][1].split()[-1])
lines.append(" & ".join(aux_string_list) + "\\\\ \n"

# lines.append("None")
# for tree in trees:
#     lines[-1] += " & {:.3f}".format(1.)
# lines[-1] += "\\\\ \n"

for j, counter_line in enumerate(eff_files[0]):
    aux_line_string_list = []
    aux_line_string_list.append( reduce(lambda x, y: x + " " + y, counter_line[1].split()[:-1]).replace("&&", "and") )
    for eff_file in eff_files:
        aux_line_string_list.append("{:.3f}".format( eff_file[j][3] ))
    lines.append(" & ".join(aux_line_string_list) + "\\\\ \n")

for i, cut in enumerate(cuts):
    lines.append(cut.replace("_", "\_"))
    for result in results[i]:
            lines[-1] += " & {:.3f}".format(result)
    lines[-1] += "\\\\ \n"

ending_line = "\end{tabular} \n"
lines.append(ending_line)

lines.append("\end{table}\n")

#saving file
with open('yields.txt', 'w+') as f:
    for line in lines:
        f.write(line)
    f.write("\n \n \n")


############ EVENTS #################

results = []
cumulative_cuts = []
for i, cut in enumerate(cuts):
    if i == 0:
        cumulative_cuts.append(cut)
    else:
        cumulative_cuts.append( cumulative_cuts[i-1] + " && " +  cut)



for cumulative_cut in cumulative_cuts:
    results.append( [] )
    for tree in trees:
        results[-1].append( tree.GetEntries(cumulative_cut) )

lines = []

begin_line = "\\begin{table}\n"
starting_line = "\\begin{tabular}{c"
first_line = "cut"
generator_line = "Generator"
for i, name in enumerate(names):
    starting_line += "|c"
    first_line += " & " + name
    generator_line += " & " + generators[i]
starting_line += "}\n"
first_line += "\\\\ \n"
generator_line += "\\\\ \n"

lines += [begin_line, starting_line, first_line, generator_line]

for j, counter_line in enumerate(eff_files[0]):
    lines.append( counter_line[1][1:25].replace("&&", "and") )
    for i, eff_file in enumerate(eff_files):
        lines[-1] += " & {}".format( int(eff_file[j][1][37:]) )
    lines[-1] += "\\\\ \n"

# lines.append("None")
# for tree in trees:
#     lines[-1] += " & {}".format(tree.GetEntries())
# lines[-1] += "\\\\ \n"

for i, cut in enumerate(cuts):
    lines.append(cut.replace("_", "\_"))
    for result in results[i]:
            lines[-1] += " & {}".format(result)
    lines[-1] += "\\\\ \n"

ending_line = "\end{tabular} \n"
lines.append(ending_line)
lines.append("\end{table}\n")

#saving file
with open('yields.txt', 'a+') as f:
    for line in lines:
        f.write(line)
    f.write("\n \n \n")




############ NORMALIZED  EVENTS #################

results = []
cumulative_cuts = []
for i, cut in enumerate(cuts):
    if i == 0:
        cumulative_cuts.append(cut)
    else:
        cumulative_cuts.append( cumulative_cuts[i-1] + " && " +  cut)



for cumulative_cut in cumulative_cuts:
    results.append( [] )
    for i, tree in enumerate(trees):
        eff = eff_files[i][3][3]
        results[-1].append( eff*cross_sections[i]*luminosity*float( tree.GetEntries(cumulative_cut) ) /  tree.GetEntries() )

lines = []

begin_line = "\\begin{table}\n"
starting_line = "\\begin{tabular}{c"
first_line = "cut"
generator_line = "Generator"
for i, name in enumerate(names):
    starting_line += "|c"
    first_line += " & " + name
    generator_line += " & " + generators[i]
starting_line += "}\n"
first_line += "\\\\ \n"
generator_line += "\\\\ \n"

lines += [begin_line, starting_line, first_line, generator_line]

lines.append( "Generated events" )
for i, eff_file in enumerate(eff_files):
    lines[-1] += " & {}".format( int(eff_file[0][1][37:]) )
lines[-1] += "\\\\ \n"


for j, counter_line in enumerate(eff_files[0]):
    lines.append( counter_line[1][1:25].replace("&&", "and") )
    for i, eff_file in enumerate(eff_files):
        lines[-1] += " & {}".format( int(eff_file[j][3]*cross_sections[i]*luminosity) )
    lines[-1] += "\\\\ \n"



# lines.append("None")
# for i, tree in enumerate(trees):
#     eff = eff_files[i][3][3]
#     lines[-1] += " & {:d}".format(int(eff*cross_sections[i]*luminosity))
# lines[-1] += "\\\\ \n"

for i, cut in enumerate(cuts):
    lines.append(cut.replace("_", "\_"))
    for result in results[i]:
            lines[-1] += " & {:d}".format(int(result))
    lines[-1] += "\\\\ \n"

ending_line = "\end{tabular} \n"
lines.append(ending_line)
lines.append("\end{table}\n")

#saving file
with open('yields.txt', 'a+') as f:
    for line in lines:
        f.write(line)
    f.write("\n \n \n")


# signal = 0.
# signal_gen = 0.
# background = 0.
# s2n_ratio = signal/background
# purity = background/(signal + background)
# efficiency = signal/signal_gen
