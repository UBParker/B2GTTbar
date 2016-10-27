#! /usr/bin/env python


##
##   Scale factor , JMR, JMS Plotter
##                                         UNDER CONSTRUCTION
##
##
##	     \\
##	     ||
##	\\___//
import sys
import math
import array as array
import CMS_lumi, tdrstyle
import ROOT
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--verbose', action='store_true',
                  default=False,
                  dest='verbose',
                  help='Do you want to print values of key variables?')

parser.add_option('--Type2', action='store_true',
                  default=False,
                  dest='Type2',
                  help='Do you want to apply selection for type 2 tops as described in AN-16-215 ?')

parser.add_option('--histo', type='string', action='store',
                  dest='histo',
                  default = '',
                  help='Hist string: hpeak, hwidth, hscale')

(options, args) = parser.parse_args(sys.argv)
argv = []


# Define histograms and arrays for storing and calculating SF, JMR, JMS
ptBs =  array.array('d', [200., 300., 400., 500., 800.])
nptBs = len(ptBs) - 1

if options.Type2 : stageBs = array.array('d',  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
else : stageBs = array.array('d',  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

nstageBs = len(stageBs) - 1


histYTitle =[
                "#frac{Data}{MC} Scale Factor ",
                "Jet Mass Resolution",
                "Jet Mass Scale",
                "Events Passing Selection Stage",
]

histXTitle =[
                "Pt of SD subjet 0 (GeV)",
                "Pt of SD subjet 0 (GeV)",
                "Pt of SD subjet 0 (GeV)",
                "Pt of SD subjet 0 (GeV)",
                "Stage of selection", #  semileptonic ttbar selection for W jets from RunSemiLepTTbar.py
]

histList = [
                ROOT.TH1F("hScale",   " ; ;   ", nptBs, ptBs)
                ROOT.TH1F("hWidth",   " ; ;   ", nptBs, ptBs)
                ROOT.TH1F("hPeak",    " ; ;   ", nptBs, ptBs)
                ROOT.TH1F("hCountSF", " ; ;   ", nptBs, ptBs)
                ROOT.TH1F("hCountAll", " ; ;  ", nstageBs, stageBs )
]

# Open input root files
histName = options.histo
if histName.find("hpeak" or "hwidth" or "hscale") == -1 : 
    print "Not using plotstackoutput"
	filesIn = [ ] #TODO : input filesin list input files

else :           
	filesIn = [
		        ROOT.TFile('plotstackOutfile_AK8MSDSJ0Pt200To300Hist.root'),
		        ROOT.TFile('plotstackOutfile_AK8MSDSJ0Pt300To400Hist.root'),
		        ROOT.TFile('plotstackOutfile_AK8MSDSJ0Pt400To500Hist.root'),
		        ROOT.TFile('plotstackOutfile_AK8MSDSJ0Pt500To800Hist.root'),
		  ]



for ifile, fileIs in enumerate(filesIn) :
    fileIs.Get(options.histo)
'''
h_list = []
h = None
h_stack = ROOT.TH1f("h_stack", "h_stack")

for iwjet in xrange(len(wjetsfiles)) :
    htemp = wjetsfiles[iwjet].Get(options.hist + str(istage))
    htemp.Scale( ( kfactorW * ttSFfromAllHad * xs_wjets[iwjet] ) / nev_wjets[iwjet] * lumi )
    h_list.append( htemp )
    htemp.SetFillColor( wjets_colors[iwjet] )
    if iwjet == 0 :
        h = htemp.Clone('h')
    else :
        h.Add( htemp )
    h_stack.Add( htemp )

            ibin = hpeak.GetXaxis().FindBin(pt)
            hpeak.SetBinContent(ibin, jmr ) 
            hwidth.SetBinContent(ibin, jms )
            hpeak.SetBinError(ibin, jmr_uncert)  


get
hscale
hpeak
hwidth

        self.AK8PuppiSDPtoverPuppiPtvsPuppiPttHist = []
        self.AK8SDPtovergenPtvsGenPttHist = []


'''
#h.Rebin(options.rebinNum)
        
for ihist, hist in enumerate(histList) :
 
    # Remove all extra info from canvas (stat box etc..)
    ROOT.gStyle.SetOptStat(000000)

    #Set multiple of maximum to scale y axis by
    SetMaxYto = 1.618

    c1 = ROOT.TCanvas("c" + str(istage), "c" + str(istage) ) #,1,1,745,701)
    #gStyle.SetOptFit(1)
    #gStyle.SetOptStat(0)
    c1.SetHighLightColor(2)
    c1.Range(0,0,1,1)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetBorderSize(2)
    c1.SetTickx(1)
    c1.SetTicky(1)
    c1.SetLeftMargin(0.14)
    c1.SetRightMargin(0.04)
    c1.SetTopMargin(0.08)
    c1.SetBottomMargin(0.15)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)

      
    pad1 = ROOT.TPad("pad1", "pad1",0,0,1,1)
    pad1.Draw()
    pad1.cd()
    pad1.SetFillColor(0)
    pad1.SetBorderMode(0)
    pad1.SetBorderSize(2)
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad1.SetLeftMargin(0.14)
    pad1.SetRightMargin(0.04)
    pad1.SetTopMargin(0.12)
    pad1.SetBottomMargin(0.02)
    pad1.SetFrameFillStyle(0)
    pad1.SetFrameBorderMode(0)
    pad1.SetFrameFillStyle(0)
    pad1.SetFrameBorderMode(0)


    hist.GetXaxis().SetRangeUser(  200. , 800. )
    hist.SetMaximum(SetMaxYto * hist.GetMaximum() )
    hist.SetMinimum(0.000 )
    hist.GetYaxis().SetTitle(histYTitle[ihist])
    hist.GetYaxis().SetTitleSize(0.065)
    hist.GetYaxis().SetTitleOffset(0.9) ## 0.7)
    hist.GetYaxis().SetLabelSize(0.06)
    ## hist.SetMarkerStyle(20)
    ## hist.SetMarkerSize(0.8)
    hist.SetLineColor(1)
    hist.SetFillColor(1)
    hist.SetFillStyle(0)
    hist.SetLineWidth(2)
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(0.8)

    hist.GetXaxis().SetNdivisions(506)
    hist.GetXaxis().SetLabelFont(42)
    hist.GetXaxis().SetLabelSize(0)
    hist.GetXaxis().SetTitleSize(0.0475)
    hist.GetXaxis().SetTickLength(0.045)
    hist.GetXaxis().SetTitleOffset(1.15)
    hist.GetXaxis().SetTitleFont(42)
    hist.GetYaxis().SetTitle("Events")
    hist.GetYaxis().SetNdivisions(506)
    hist.GetYaxis().SetLabelFont(42)
    hist.GetYaxis().SetLabelSize(0.06375)
    hist.GetYaxis().SetTitleSize(0.07125)
    hist.GetYaxis().SetTitleOffset(0.9)
    hist.GetYaxis().SetTitleFont(42)
    hist.GetZaxis().SetLabelFont(42)
    hist.GetZaxis().SetLabelSize(0.0425)
    hist.GetZaxis().SetTitleSize(0.0475)
    hist.GetZaxis().SetTitleFont(42)
    hist.SetXTitle( histXTitle[ihist] +" , Stage "+str(istage))

    hist.Draw("e x0")


    if options.verbose : 
        print "Setting X axis range to ({0}  ,  {1})".format(xAxisrange[iHisto][0] , xAxisrange[iHisto][1] )
        print "Setting Y axis range to ({0}  ,  {1})".format(0. ,SetMaxYto * hist.GetMaximum() )

    words = ROOT.TLatex(0.14,0.916,"#font[62]{CMS} #font[52]{Preliminary}")
    words.SetNDC()
    words.SetTextFont(42)
    words.SetTextSize(0.0725)
    words.SetLineWidth(2)
    words.Draw()
    words1 = ROOT.TLatex(0.9,0.916,"12.9 fb^{-1} (13 TeV)")
    words1.SetNDC()
    words1.SetTextAlign(31)
    words1.SetTextFont(42)
    words1.SetTextSize(0.0725)
    words1.SetLineWidth(2)
    words1.Draw()
    words2 = ROOT.TLatex(0.181,0.82225,"")
    words2.SetNDC()
    words2.SetTextAlign(13)
    words2.SetTextFont(42)
    words2.SetTextSize(0.045)
    words2.SetLineWidth(2)
    words2.Draw()


    c1.cd()

    c1.Print("plot_" + options.hist + str(istage) + typeIs + MCs + CorrIs + ".pdf", "pdf")
    c1.Print("plot_" + options.hist + str(istage) + typeIs + MCs + CorrIs + ".png", "png")
