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
        self.dataset_list = dataset_list
        self.cut_list = cut_list
        self.caption = caption

        self.cumulative_cuts = []
        for i, cut in enumerate(self.cut_list):
            aux_cumulative_cut = " && ".join(self.cut_list[:i+1])
            self.cumulative_cuts.append( aux_cumulative_cut )

        self.table_list = []
        self.FillTable()

    def BeginningLatex(self):
        begginning_latex_lines = []
        begin_table_line = "\\begin{table}\n"
        begginning_latex_lines.append(begin_table_line)

        begin_tabular_line = "\\begin{tabular}{c"
        begin_tabular_line += "|c" * len(self.dataset_list)
        begin_tabular_line += "}\n"
        begginning_latex_lines.append(begin_tabular_line)

        return begginning_latex_lines

    def AddDataSetLine(self):
        name_line_string_list = ["Dataset"]
        for dataset in self.dataset_list:
            name_line_string_list.append(dataset.name)
        self.table_list.append(name_line_string_list)

    def AddGeneratorsLine(self):
        generator_line_string_list = ["Generator"]
        for dataset in self.dataset_list:
            generator_line_string_list.append(dataset.generator)
        self.table_list.append(generator_line_string_list)

    def AddGeneratedEvents(self):
        generated_events_line_string_list = ["Generated events"]
        for dataset in self.dataset_list:
            generated_events_line_string_list.append(str(dataset.n_gen))
        self.table_list.append(generated_events_line_string_list)

    def ComputeYields(self):
        self.yields = []
        for cumulative_cut in self.cumulative_cuts:
            aux_yields_list = []
            for dataset in self.dataset_list:
                aux_yields_list.append(str( int( dataset.cut_efficiency(cumulative_cut) * dataset.n_gen_with_eff ) ) )
            self.yields.append(aux_yields_list)

    def WriteYields(self):
        for cut, cut_yield in zip(self.cut_list, self.yields):
            self.table_list.append([cut] + cut_yield)

    def EndLatex(self):
        ending_latex_lines = []
        end_tabular_line = "\end{tabular} \n"
        ending_latex_lines.append(end_tabular_line)

        if self.caption != None:
            caption_line = "\caption{" + self.caption + "}\n"
            ending_latex_lines.append(caption_line)

        end_table_line = "\end{table} \n"
        ending_latex_lines.append(end_table_line)

        return ending_latex_lines

    def FillTable(self):
        self.AddDataSetLine()
        self.AddGeneratorsLine()
        self.AddGeneratedEvents()

        self.ComputeYields()
        self.WriteYields()

    def PrintTable(self):
        for table_raw in self.table_list:
            aux_line_string = "\t".join(table_raw)
            print aux_line_string
        print "\n" * 3

    def WriteTable(self, filename):
        with open(filename, 'w+') as f:
            for table_raw in self.table_list:
                aux_line_string = "\t".join(table_raw)
                aux_line_string += "\n"
                f.write(aux_line_string)
            f.write("\n" * 3)

    def PrintLatex(self):
        for line in self.BeginningLatex():
            print line
        for table_raw in self.table_list:
            aux_line_string = " & ".join(table_raw)
            aux_line_string += "\\\\"
            print aux_line_string
        for line in self.EndLatex():
            print line
        print "\n" * 3

    def WriteLatex(self, filename):
        with open(filename, 'w+') as f:
            for line in self.BeginningLatex():
                f.write(line)
            for table_raw in self.table_list:
                aux_line_string = " & ".join(table_raw)
                aux_line_string += "\\\\ \n"
                f.write(aux_line_string)
            for line in self.EndLatex():
                f.write(line)
            f.write("\n" * 3)
