from ROOT import TROOT, TStyle, gStyle

def TopMassStyle():

    gStyle.SetPadTickX(1);
    gStyle.SetPadTickY(1);
    gStyle.SetHistLineWidth(3);
    gStyle.SetMarkerStyle(1);

    gStyle.SetTextSize(0.065);

    gStyle.SetOptFit(1111);
    gStyle.SetTitleSize(.05,"X");#.055
    gStyle.SetTitleOffset(1.1,"X");#1.2,0.9
    gStyle.SetLabelSize(.05,"X");

    gStyle.SetTitleSize(.05,"Y");#.055
    gStyle.SetTitleOffset(1.1,"Y");
    gStyle.SetLabelSize(.05,"Y");

    gStyle.SetPadLeftMargin(.16);
    gStyle.SetPadBottomMargin(.12);

    gStyle.SetTitleSize(.05,"Z");
    gStyle.SetTitleOffset(1.8,"Z");
    gStyle.SetLabelSize(0.06,"Z");

    gStyle.SetLegendTextSize(0.04);

    gStyle.SetOptStat(112210);

    gStyle.SetPadLeftMargin(.12);
    gStyle.SetPadRightMargin(.02);
    gStyle.SetPadBottomMargin(.12);
    gStyle.SetPadTopMargin(.07);
    gStyle.SetPadGridX(1);
    gStyle.SetPadGridY(1);
    # gStyle.SetPadTickX(1);
    # gStyle.SetPadTickY(1);
