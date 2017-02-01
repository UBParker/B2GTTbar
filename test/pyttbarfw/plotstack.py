#! /usr/bin/env python


## _________                _____.__                            __  .__               
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____  
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \ 
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/ 
import sys
import math
import json
import array as array
from optparse import OptionParser
from utils.APlot import APlot
from utils.CutList import *

parser = OptionParser()

parser.add_option('--hist', type='string', action='store',
                  dest='hist',
                  default = '',
                  help='Hist string')


parser.add_option('--highmass', action='store_true',
                  dest='highmass',
                  default = False,
                  help='High mass?')

parser.add_option('--el', action='store_true',
                  dest='el',
                  default = False,
                  help='plot only electrons?')
                  
parser.add_option('--mu', action='store_true',
                  dest='mu',
                  default = False,
                  help='plot only muons?')   
                                 
parser.add_option('--fixFit', action='store_true',
                  dest='fixFit',
                  default = False,
                  help='Fix the fit of the tau21 cut distribution to the value from the mass cut ?') 
                  
(options, args) = parser.parse_args(sys.argv)
argv = []

import ROOT
ROOT.gStyle.SetOptStat(000000)

       
        
xs_ttbar = 831.
nev_ttbar = 92925926.

lumi = 36220. # pb-1
expectedRunsHist = None
expectedRunsList = None
if (options.hist.find("RunNumberHist")!= -1)  : 
    
    ### Plot lumis that should be present. json production described here https://docs.google.com/document/d/1aTeTVIi9eb-aup37dbUL8cWDPCJrn_sRYrZcjFhd4tI/edit?usp=sharing
    if options.el : expectedRuns = json.loads(open('./CertandsingleEl.json').read())
    elif options.mu : expectedRuns = json.loads(open('./CertandSingleMu.json').read()) 
    elif not (options.mu or options.el) : expectedRuns = None #    json.loads(open('./singleMuEl2016B-H.json').read())
    expectedRunsList = []
    expectedRunsHist = ROOT.TH1F("expectedRunsHist" , "Run Number for lepton ", 286591, 0, 286591)
    runNumber = None
    for run in expectedRuns :
       runNumber = float(run)
       if runNumber != None :
           print("Run number is : {}".format(runNumber))
           expectedRunsList.append(runNumber)
           expectedRunsHist.Fill(runNumber)
           expectedRunsHist.SetMarkerStyle(30)
           expectedRunsHist.SetMarkerColor(6)
           expectedRunsHist.Rebin(10)
           
xs_wjets = [
    1345.,     #100To200  
    359.7,     #200To400  
    48.91,     #400To600  
    12.05,     #600To800  
    5.501,     #800To1200 
    1.329,     #1200To2500
    0.03216,   #2500ToInf 
    ]

nev_wjets = [
    10231928., #100To200   10 / 214 failed
    4963240.,  #200To400 
    1963464.,  #400To600 
    3722395.,  #600To800
    1540477.,  #800To1200 
    246737.,   #1200To2500 12 / 54 failed  (total = 6817172)
    253561.,   #2500ToInf 
    ]
xs_qcd = [
    27990000., # 100To200
    1712000.,  # 200To300
    347700.,   # 300To500
    32100.,    # 500To700
    6831.,     # 700To1000
    1207.,     # 1000To1500
    119.9,     # 1500To2000
    25.24,     # 2000ToInf 
    ]

nev_qcd = [
    82073090., # 100To200  
    18523829., # 200To300  
    16830696., # 300To500  
    19199088., # 500To700  
    15621634., # 700To1000 
    4980387.,  # 1000To1500
    3846616.,  # 1500To2000
    1960245.   # 2000ToInf 
    ]

xs_singletop = [
    136.02 * 0.322,#singletop_tchanneltop_outfile.root
    80.95 * 0.322, #singletop_tchannel_outfile.root
    35.6,          #singletop_tW_outfile.root
    35.6,          #singletop_tWantitop_outfile.root
    3.36           #singletop_schannel_outfile.root    
    ]
nev_singletop = [
    32808300.,
    19825855.,
    998400.,
    985000.,
    1000000.
    ]


    
instring = ''
endstring1 = ''
endstring2 = 'Commit0529f0f' #'Commit8651dac' # plotstack_Commite39827c
endstrings = endstring2

#   ____  _    _ _______ _____  _    _ _______   _____   ____   ____ _______ 
#  / __ \| |  | |__   __|  __ \| |  | |__   __| |  __ \ / __ \ / __ \__   __|
# | |  | | |  | |  | |  | |__) | |  | |  | |    | |__) | |  | | |  | | | |   
# | |  | | |  | |  | |  |  ___/| |  | |  | |    |  _  /| |  | | |  | | | |   
# | |__| | |__| |  | |  | |    | |__| |  | |    | | \ \| |__| | |__| | | |   
#  \____/ \____/   |_|  |_|     \____/   |_|    |_|  \_\\____/ \____/  |_|   


theOutfile = ROOT.TFile( "./plotstack_"+ str(endstring2)+ '/plotstack_outfile_'+ str(options.hist)+'_' +str(endstrings)+ '.root' , "RECREATE") 

theOutfile.cd()
 
 

if options.highmass :
    instring = '_highmass'
else: endstrings = ''
ttbarfile = ROOT.TFile('ttbar' + instring + '_outfile'+ endstrings +'.root')

if  options.el :  datafile = ROOT.TFile('singleel' + instring + '_outfile'+ endstring1 +'.root')
if options.mu :  datafile = ROOT.TFile('singlemu' + instring + '_outfile'+ endstring1 +'.root')
if not (options.el or options.mu):
    datafile = ROOT.TFile('singleel' + instring + '_outfile'+ endstring1 +'.root')
    datafile1 = ROOT.TFile('singlemu' + instring + '_outfile'+ endstring1 +'.root')


wjetsfiles = [
    ROOT.TFile('wjets100to200' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('wjets200to400' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('wjets400to600' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('wjets600to800' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('wjets800to1200' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('wjets1200to2500' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('wjets2500toinf' + instring + '_outfile'+ endstrings +'.root'),
    ]

wjets_colors = [ 
    ROOT.kWhite,ROOT.kRed - 9, ROOT.kRed - 7, ROOT.kRed - 4, ROOT.kRed, ROOT.kRed +1, ROOT.kRed +2   ]

qcdfiles = [
    ROOT.TFile('qcd100' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('qcd200' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('qcd300' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('qcd500' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('qcd700' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('qcd1000' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('qcd1500' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('qcd2000' + instring + '_outfile'+ endstrings +'.root'),
    ]

singletopfiles = [
    ROOT.TFile('singletop_tchanneltop' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('singletop_tchannel' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('singletop_tW' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('singletop_tWantitop' + instring + '_outfile'+ endstrings +'.root'),
    ROOT.TFile('singletop_schannel' + instring + '_outfile'+ endstrings +'.root'),
    ]
    
objs = []

### Set the maximum y axis increment with respect to the maximum y axis value
y_max_scale = 4.9


lepName0 = 'Electron'
lepName1 = 'Muon'
lep = None 
lepTag = None
cutTag = None

histName0 = options.hist 
    
    
rangenum = 14
if options.highmass: rangenum = 18 #14

### Runs in stage 0 data selection
actualRunsList = [] 
  
for istage in range(rangenum) : 

    
    histName = None
    histName1 = None
    
    if options.el : 
        histName = options.hist + lepName0 + str(istage)
        lep = str(lepName0)
        lepTag = 'Electron Data'
    if options.mu : 
        histName = options.hist + lepName1 + str(istage)
        lep = str(lepName1)
        lepTag = 'Muon Data'

    if not (options.el or options.mu): 
        histName = options.hist + lepName0 + str(istage)
        histName1 = options.hist + lepName1 + str(istage)
        lepTag = 'Electron and Muon Data'
        lep = 'Lepton'
    #print("mc file is {}".format(ttbarfile))
    httbar = ttbarfile.Get(histName)
    #print ("Extracting histo titled {}".format(histName))
    if not (options.el or options.mu): 
        httbar1 = ttbarfile.Get(histName1)
        httbar1.Sumw2()
        httbar.Add(httbar1)
    httbar.Sumw2()
    httbar.Scale( xs_ttbar / nev_ttbar* lumi ) 
    httbar.SetFillColor(ROOT.kGreen + 2)

    ROOT.gStyle.SetOptStat(000000)
    hdata = datafile.Get(histName)
    if not (options.el or options.mu):
        hdata1 = datafile1.Get(histName1)
        hdata1.Sumw2()
        hdata1.GetXaxis().SetTitle("")#Electron and Muon Data at Stage, {}".format( str(istage)))

        hdata.Add(hdata1)
    print ("Extracting histo titled {}".format(histName))
    hdata.Sumw2()    
    hdata.SetMarkerStyle(20)
   
    hdata.SetTitle("")#Electron and Muon Data at Stage, {}".format( str(istage)))
    #hdata.GetYaxis().SetTitle("Events")
    hdata.GetXaxis().SetTitle("")#Histogram name {}".format(options.hist + str(istage)))
   
    if options.hist == "RunNumberHist" and istage == 0:
        nbinsis = hdata.GetNbinsX()
        for i in range(nbinsis):
            binn = hdata.GetBinContent(i) 
            if binn > 0.:
                runnum = hdata.GetBinLowEdge(i)
                actualRunsList.append(runnum)

    hwjets_list = []
    hwjets = None
    hwjets_stack = ROOT.THStack("hwjets_stack", "hwjets_stack")

    for iwjet in range(len(wjetsfiles)) :
        htemp = wjetsfiles[iwjet].Get(histName)
        if not (options.el or options.mu): 
            htemp1 = wjetsfiles[iwjet].Get(histName1)
            htemp1.Sumw2()
            htemp.Add(htemp1)        
        htemp.Scale( xs_wjets[iwjet] / nev_wjets[iwjet] * lumi )
        hwjets_list.append( htemp )
        htemp.SetFillColor( wjets_colors[iwjet] )
        if iwjet == 0 :
            hwjets = htemp.Clone('hwjets')
        else :
            hwjets.Add( htemp )
        hwjets_stack.Add( htemp )
    #hwjets_stack.Draw("hist")


    hwjets.SetFillColor( ROOT.kRed )


    hqcd_list = []
    hqcd = None
    hqcd_stack = ROOT.THStack("hqcd_stack", "hqcd_stack")

    for iqcd in range(len(qcdfiles)) :
        htemp = qcdfiles[iqcd].Get(histName)
        if not (options.el or options.mu): 
            htemp1 = qcdfiles[iqcd].Get(histName1)
            htemp1.Sumw2()
            htemp.Add(htemp1)  
        htemp.Scale( xs_qcd[iqcd] / nev_qcd[iqcd] * lumi )
        hqcd_list.append( htemp )
        #htemp.SetFillColor( qcd_colors[iqcd] )
        if iqcd == 0 :
            hqcd = htemp.Clone('hqcd')
        else :
            hqcd.Add( htemp )
        hqcd_stack.Add( htemp )
    #hqcd_stack.Draw("hist")
    hqcd.SetFillColor( ROOT.kYellow )
    
    hsingletop_list = []
    hsingletop = None
    hsingletop_stack = ROOT.THStack("hsingletop_stack", "hsingletop_stack")

    for isingletop in range(len(singletopfiles)) :
        htemp = singletopfiles[isingletop].Get(histName)
        if not (options.el or options.mu):
            htemp1 = singletopfiles[isingletop].Get(histName1)
            htemp1.Sumw2()
            htemp.Add(htemp1)  
        htemp.Scale( xs_singletop[isingletop] / nev_singletop[isingletop] * lumi )
        hsingletop_list.append( htemp )
        #htemp.SetFillColor( singletop_colors[isingletop] )
        if isingletop == 0 :
            hsingletop = htemp.Clone('hsingletop')
        else :
            hsingletop.Add( htemp )
        hsingletop_stack.Add( htemp )
    #hsingletop_stack.Draw("hist")


    hsingletop.SetFillColor( ROOT.kMagenta )
               
           
    hqcd.Rebin(10)
    hsingletop.Rebin(10)
    hwjets.Rebin(10)
    httbar.Rebin(10)
    if options.hist != "RunNumberHist" :
        hdata.Rebin(10)
    hdata2 = hdata.Clone('hdata2')
    
    hstack = ROOT.THStack("bkgs", "")
    hstack.Add( hqcd )
    hstack.Add( hsingletop )
    hstack.Add( hwjets )
    hstack.Add( httbar )

    hmc = hqcd.Clone('hmc')
    hmc.Add(hsingletop )
    hmc.Add( hwjets )
    hmc.Add( httbar )
    hmc2 = hmc.Clone('hmc2')


    if options.highmass:    
        cutTag = CutsPerStage_Type1[str(istage)][1]    
    else: cutTag =  CutsPerStage_Type2[str(istage)][1]
    
    zplot = APlot(istage , y_max_scale, hdata, hdata2, hmc,hmc2 , hstack, httbar, hwjets, hsingletop, hqcd, str(histName0), lumi/1000., lepTag, cutTag, options.fixFit, expectedRunsHist)
        
    theCanvas = zplot.GetPlotCanvas()
    
    theCanvas.Print("./plotstack_"+ str(endstring2)+ "/" + histName0 + lep + str(istage)  + instring + endstrings+".pdf", "pdf")
    theCanvas.Print("./plotstack_"+ str(endstring2)+ "/" + histName0 + lep + str(istage)  + instring + endstrings+".png", "png")

    theOutfile.cd()
                    
    objs.append( [hdata, httbar, hwjets, theCanvas, hstack, expectedRunsList, actualRunsList ] )

    theOutfile.Close()
    
missingRunsList = []

if expectedRunsList != None :
    for i in expectedRunsList :
        if i not in actualRunsList : 
            missingRunsList.append(i)
            print("PROBLEM!!!: Run {} is in the expected list but not in stage 0 RunNumberHist".format(i))
            

    print("Sanity check: Actual runs {}".format(actualRunsList))

    print("    ")
    print("    ")

    print("Expected runs {}".format(expectedRunsList))

    print("    ")
    print("    ")

    print("MISSING runs {}".format(missingRunsList))

    print("    ")
    print("    ")


    print( "Philosophy is written in this grand book")  
    print("      *     the universe   *        .       .")
    print(" which stands continually open to our gaze.  ")
    print("       *         *           .       ^   ") #-0-
    print("          .                .  *       - )-  ")
    print("The book wont be understood until one learns")
    print("       .      *       *       .       *     ")
    print("    to comprehend |                         ")
    print(" *          .    -O- the language    ")
    print(".                 |               *    -0- ")
    print("       *  o     .    '       *      .        o")
    print("      in which it is composed.    |     .  *")
    print("   *             *              -O-          .")
    print("         .             *         |     ,")
    print("                .           o")
    print("        .---.               ---Galileo Galilei  ")
    print("  =   _/__~0_\_     .  *            o       '")
    print(" = = (_________)             .")
    print("                 .                        *")
    print("       *               - ) -       *")
