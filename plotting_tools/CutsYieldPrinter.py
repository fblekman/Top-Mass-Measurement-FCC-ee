from ROOT import TFile
from numpy import genfromtxt

class CutsYieldPrinter(object):
    """Generate LaTeX code for a table with the yields of a list of cut on a list of dataset.

    It integrates with the DataSet Class.
    The class contains a lot of methods to generate the various lines of the table code;
    these are of course very customizable.

    TODO: print table method?
    """

    def __init__(self, dataset_list, cut_list, caption = None):
        """ Constructor with a list of DataSet objects, a list of cut (string format),
        and possibly a caption."""
        self.lines = []
        self.dataset_list = dataset_list
        self.cut_list = cut_list
        self.caption = caption

        self.cumulative_cuts = []
        for i, cut in enumerate(self.cut_list):
            aux_cumulative_cut = " && ".join(self.cut_list[:i+1])
            self.cumulative_cuts.append( aux_cumulative_cut )

    def JoinValuesForLine(self, values_list):
        return " & ".join(values_list)

    def AddBeginning(self):
        begin_table_line = "\\begin{table}\n"
        self.lines.append(begin_table_line)

        begin_tabular_line = "\\begin{tabular}{c"
        begin_tabular_line += "|c" * len(self.dataset_list)
        begin_tabular_line += "}\n"
        self.lines.append(begin_tabular_line)

    def AddDataSetLine(self):
        name_line_string_list = ["Dataset"]
        for dataset in self.dataset_list:
            name_line_string_list.append(dataset.name)
        name_line = self.JoinValuesForLine(name_line_string_list)
        name_line += "\\\\ \n"

    def AddGeneratorsLine(self):
        generator_line_string_list = ["Generator"]
        for dataset in self.dataset_list:
            generator_line_string_list.append(dataset.generator)
        generator_line = self.JoinValuesForLine(generator_line_string_list)
        generator_line += "\\\\ \n"
        self.lines.append(generator_line)

    def AddGeneratedEvents(self):
        generated_events_line_string_list = ["Generated events"]
        for dataset in self.dataset_list:
            generated_events_line_string_list.append(str(dataset.n_gen))
        generated_events_line = self.JoinValuesForLine(generated_events_line_string_list)
        generated_events_line += "\\\\ \n"
        self.lines.append(generated_events_line)

    def ComputeYields(self):
        self.yields = []
        for cumulative_cut in self.cumulative_cuts:
            aux_yields_list = []
            for dataset in self.dataset_list:
                aux_yields_list.append(str( int( dataset.cut_efficiency(cumulative_cut) * dataset.n_gen_with_eff ) ) )
            self.yields.append(aux_yields_list)

    def WriteYields(self):
        for cut, cut_yield in zip(self.cut_list, self.yields):
            aux_line = cut + " & "
            aux_line += self.JoinValuesForLine(cut_yield)
            aux_line += "\\\\ \n"
            self.lines.append(aux_line)

    def AddEnd(self):
        end_tabular_line = "\end{tabular} \n"
        self.lines.append(end_tabular_line)

        if self.caption != None:
            caption_line = "\caption{" + self.caption + "}\n"
            self.lines.append(caption_line)

        end_table_line = "\end{table} \n"
        self.lines.append(end_table_line)
        self.lines.append("\n" * 3)

    def SaveFile(self, filename):
        with open(filename, 'w+') as f:
            for line in self.lines:
                f.write(line)

    def WriteTable(self, filename):
        self.AddBeginning()
        self.AddDataSetLine()
        self.AddGeneratorsLine()
        self.AddGeneratedEvents()

        self.ComputeYields()
        self.WriteYields()
        self.AddEnd()

        self.SaveFile(filename)
