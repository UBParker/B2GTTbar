#! /usr/bin/env python


## _________                _____.__                            __  .__               
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____  
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \ 
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/ 
import sys
import math
import array as array
import CMS_lumi, tdrstyle
import ROOT
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--hist', type='string', action='store',
                  dest='hist',
                  default = '',
                  help='Hist string')

parser.add_option('--allMC', action='store_true',
                  default=False,
                  dest='allMC',
                  help='Do you want to plot all MC? (or just ttjets)')

parser.add_option('--includeQCD', action='store_true',
                  default=False,
                  dest='includeQCD',
                  help='Do you want to add QCD MC? (or just ttjets, W+Jets and ST)')

parser.add_option('--rebinNum', type='float', action='store',
                  dest='rebinNum',
                  default = 20,
                  help='number to rebin the histograms by')

parser.add_option('--nstages', type='int', action='store',
                  dest='nstages',
                  default = 16,
                  help='number of stages of selection (sum of nstages from lept and had selections)')

parser.add_option('--Type2', action='store_true',
                  default=False,
                  dest='Type2',
                  help='Do you want to apply selection for type 2 tops as described in AN-16-215 ?')

parser.add_option('--ttSF', action='store_true',
                  default=False,
                  dest='ttSF',
                  help='Apply a ttbar scaling computed using ScalettMC?')

parser.add_option('--fixFit', action='store_true',
                  default=False,
                  dest='fixFit',
                  help='Do you want to constrain the gaussian fit?')

parser.add_option('--verbose', action='store_true',
                  default=False,
                  dest='verbose',
                  help='Do you want to print values of key variables?')

parser.add_option('--noData', action='store_true',
                  default=False,
                  dest='noData',
                  help='Plot only MC (for testing purposes)?')

(options, args) = parser.parse_args(sys.argv)
argv = []


def ScalettMC(httbar__, hdata__ , hMC__, intMin, intMax ) :
    # Find the tt scale factor
    if not options.ttSF: 
        sf = 1.
        return httbar__
    sf = 0.
    scalefactortt = 0.

    intMinbin = hMC__.FindBin(intMin)
    intMaxbin = hMC__.FindBin(intMax)

    if (hdata__.Integral() > 0.) and (hMC__.Integral() > 0.) and options.ttSF: 
        diff = float(hdata__.Integral(intMinbin, intMaxbin))- float(  hMC__.Integral(intMinbin, intMaxbin)  )
        sf = abs(    diff/ float(  httbar__.Integral(intMinbin, intMaxbin)     ) +1.       )     


    scalefactortt = sf 
    if options.ttSF and options.verbose: print "tt SCALE FACTOR APPLIED : {0:2.2f} based on integral of range ({1},{2})".format(scalefactortt, intMin, intMax)

    if httbar__.Integral() > 0 : 
        httbar__.Scale( scalefactortt ) 
    else :
        print "tt bin  empty when using scalettMC() "
        httbar__.Scale( 0.)

    return httbar__ 


if options.noData : print "WARNING : noData option is ON so the data wil not be plotted !!! "

# Open output root file to store SF, JMR, JMS 

fileout = "plotstackoutfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_" + options.hist + ".root"

fout = ROOT.TFile( fileout, "RECREATE") 

fout.cd()



# Define histograms and arrays for storing and calculating SF, JMR, JMS
ptBs =  array.array('d', [200., 300., 400., 500., 800.])
nptBs = len(ptBs) - 1


hpeak = ROOT.TH1F("hpeak", " ;p_{T} of SD subjet 0 (GeV); JMS ",  nptBs, ptBs)  ##frac{Mean Mass_{data}}{Mean Mass_{MC}}
hwidth = ROOT.TH1F("hwidth", " ;p_{T} of SD subjet 0 (GeV); JMR ", nptBs, ptBs) ##frac{#sigma_{data}}{#sigma_{MC}}

hNpassDataPre = ROOT.TH1F("hNpassDataPre", " ;;  ", nptBs, ptBs) 
hNpassMCPre = ROOT.TH1F("hNpassMCPre", " ;;  ", nptBs, ptBs) 
hmeanDataPre = ROOT.TH1F("hmeanDataPre", " ;;  ", nptBs, ptBs) 
hmeanMCPre = ROOT.TH1F("hmeanMCPre", " ;;  ", nptBs, ptBs) 
hsigmaDataPre = ROOT.TH1F("hsigmaDataPre", " ;;  ", nptBs, ptBs) 
hsigmaMCPre = ROOT.TH1F("hsigmaMCPre", " ;;  ", nptBs, ptBs) 

hNpassDataPost = ROOT.TH1F("hNpassDataPost", " ;;  ", nptBs, ptBs) 
hNpassMCPost = ROOT.TH1F("hNpassMCPost", " ;;  ", nptBs, ptBs) 
hscale = ROOT.TH1F("hscale", " ; ;  ", nptBs, ptBs)
hdataEff = ROOT.TH1F("hdataEff", " ; ; ", nptBs, ptBs)
hMCEff = ROOT.TH1F("hMCEff", " ; ; ", nptBs, ptBs)


nMCpre = array.array('d', [0., 0., 0., 0.])
nDatapre = array.array('d', [0., 0., 0., 0.])
nMCupre = array.array('d', [0., 0., 0., 0.])
nDataupre = array.array('d', [0., 0., 0., 0.])

MCmeans = array.array('d', [0., 0., 0., 0.])
MCsigmas = array.array('d', [0., 0., 0., 0.])
Datameans = array.array('d', [0., 0., 0., 0.])
Datasigmas = array.array('d', [0., 0., 0., 0.])

nMCpost = array.array('d', [0., 0., 0., 0.])
nDatapost = array.array('d', [0., 0., 0., 0.])
nMCupost = array.array('d', [0., 0., 0., 0.])
nDataupost = array.array('d', [0., 0., 0., 0.])



# Set X axis range based on histo name

if options.Type2:
    xAxisrange = [        [39.0   ,   150. ], # AK8MSDHist
                          [0.     ,   100. ], # AK8MSDSJ0Hist
                          [200.   ,   800. ], # AK8PtHist
                          [-2.5   ,    2.5 ], # AK8EtaHist
                          [0.0    ,    1.0 ], # AK8Tau21Hist
                          [0.0    ,    1.0 ], # AK8Tau32Hist
                          [39.0   ,   150. ], # AK8MHist
                          [0.0    ,   600. ], # LeptonPtHist
                          [2.5    ,  -2.5  ], # LeptonEtaHist
                          [0.     ,   300. ], # METPtHist
                          [0.     ,   700. ], # HTLepHist
                          [0.     ,   300. ], # Iso2DHist  
                          [0.     ,     1. ], # AK4BdiscHist
                          [45.    ,   151. ], # AK8MSDSJ0Pt200To300Hist
                          [45.    ,   151. ], # AK8MSDSJ0Pt300To400Hist
                          [45.    ,   151. ], # AK8MSDSJ0Pt400To500Hist
                          [45.    ,   151. ], # AK8MSDSJ0Pt500To800Hist   
                          [0.     ,  1000. ], # AK8PtHist
                          [0.     ,  1000. ], # AK8SDPtHist
                          [0.     ,  1000. ], # AK8PuppiSDPtHist
                          [0.     ,  1000. ], # AK8PuppiPtHist  
                          [0.    ,   300.   ], # AK8MPt200To300Hist
                          [0.    ,   300.   ], # AK8MPt300To400Hist
                          [0.    ,   300.   ], # AK8MPt400To500Hist
                          [0.    ,   300.   ], # AK8MPt500To800Hist
                          [0.    ,   300.   ], # AK8MSDPt200To300Hist
                          [0.    ,   300.   ], # AK8MSDPt300To400Hist
                          [0.    ,   300.   ], # AK8MSDPt400To500Hist
                          [0.    ,   300.   ], # AK8MSDPt500To800Hist                                                                   
                 ]

else:
    xAxisrange = [        [  0.0  ,   300. ], # AK8MSDHist
                          [ 39.0  ,   150. ], # AK8MSDSJ0Hist
                          [0.     ,  1000. ], # AK8PtHist
                          [-2.5   ,    2.5 ], # AK8EtaHist
                          [0.0    ,    1.0 ], # AK8Tau21Hist
                          [0.0    ,    1.0 ], # AK8Tau32Hist
                          [  0.0  ,   300. ], # AK8MHist
                          [0.0    ,   600. ], # LeptonPtHist
                          [2.5    ,  -2.5  ], # LeptonEtaHist
                          [0.     ,   1000. ], # METPtHist
                          [0.     ,   700. ], # HTLepHist
                          [0.     ,   300. ], # Iso2DHist
                          [0.     ,     1. ], # AK4BdiscHist
                          [45.    ,   151. ], # AK8MSDSJ0Pt200To300Hist
                          [45.    ,   151. ], # AK8MSDSJ0Pt300To400Hist
                          [45.    ,   151. ], # AK8MSDSJ0Pt400To500Hist
                          [45.    ,   151. ], # AK8MSDSJ0Pt500To800Hist
                          [0.     ,  1000. ], # AK8HTHist
                          [0.     ,  1000. ], # AK8SDPtHist
                          [0.     ,  1000. ], # AK8PuppiSDPtHist
                          [0.     ,  1000. ], # AK8PuppiPtHist
                          [0.    ,   300.   ], # AK8MPt200To300Hist
                          [0.    ,   300.   ], # AK8MPt300To400Hist
                          [0.    ,   300.   ], # AK8MPt400To500Hist
                          [0.    ,   300.   ], # AK8MPt500To800Hist
                          [0.    ,   300.   ], # AK8MSDPt200To300Hist
                          [0.    ,   300.   ], # AK8MSDPt300To400Hist
                          [0.    ,   300.   ], # AK8MSDPt400To500Hist
                          [0.    ,   300.   ], # AK8MSDPt500To800Hist
                          [0.0    ,    1.0 ], # AK8Tau32Hist

                 ]


Histos = [  "AK8MSDHist", #0
         "AK8MSDSJ0Hist", #1
             "AK8PtHist", #2
            "AK8EtaHist", #3
     "AK8puppitau21Hist", #4
     "AK8puppitau32Hist", #5
              "AK8MHist", #6
          "LeptonPtHist", #7
         "LeptonEtaHist", #8
             "METPtHist", #9
             "HTLepHist", #10
             "Iso2DHist", #11
          "AK4BdiscHist", #12
"AK8MSDSJ0Pt200To300Hist", #13
"AK8MSDSJ0Pt300To400Hist", #14
"AK8MSDSJ0Pt400To500Hist", #15
"AK8MSDSJ0Pt500To800Hist", #16  
"AK8HTHist",               #17 
"AK8SDPtHist",             #18 
"AK8PuppiSDPtHist",        #19 
"AK8PuppiPtHist",          #20 
"AK8MPt200To300Hist", #21
"AK8MPt300To400Hist", #22
"AK8MPt400To500Hist", #23
"AK8MPt500To800Hist", #24 
"AK8MSDPt200To300Hist", #25
"AK8MSDPt300To400Hist", #26
"AK8MSDPt400To500Hist", #27
"AK8MSDPt500To800Hist", #28 
"AK8Tau32Hist",         #29
    ]

# TO-DO : Add all below histo names to Histos and HistoTitle
'''

'''

HistoTitle =            [           "AK8 Jet SD Mass (GeV)",
                             "Leading Subjet SD Mass (GeV)",
                                                "AK8 Jet P_{T} (GeV)",
                                                 "AK8 Jet #eta", 
                                            "AK8 puppi Jet #tau_{21}",
                                            "AK8 puppi Jet #tau_{32}",
                                                 "AK8 Jet Mass (GeV)",
                                                 "Lepton P_{T} (GeV)",
                                                  "Lepton #eta",
                                                "Missing P_{T} (GeV)",
                                 "Lepton P_{T} + Missing P_{T} (GeV)",
               "Lepton 2D isolation (#Delta R vs p_{T}^{REL} )",
                                                 "CSVv2 B Disc",
                             "(200<P_{t}<300) Subjet 0 SD Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(300<P_{t}<400) Subjet 0 SD Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(400<P_{t}<500) Subjet 0 SD Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(500<P_{t}<800) Subjet 0 SD Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                                                "AK8 Jet H_{T} (GeV)",
                                                "AK8 SD Jet P_{T} (GeV)",
                                                "AK8 PUPPI SD Jet P_{T} (GeV)",
                                                "AK8 PUPPI Jet P_{T} (GeV)",
                             "(200<P_{t}<300)  AK8 Jet Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(300<P_{t}<400)  AK8 Jet Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(400<P_{t}<500)  AK8 Jet Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(500<P_{t}<800)  AK8 Jet Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(200<P_{t}<300)  AK8 SD Jet Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(300<P_{t}<400)  AK8 SD Jet Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(400<P_{t}<500)  AK8 SD Jet Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(500<P_{t}<800)  AK8 SD Jet Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                                            "AK8 Jet #tau_{32}",
]


iHisto = Histos.index(options.hist) 
if options.verbose : print "Histo name in options was {0}, index number {1:0.0f}, entry in Histos(index) is {2}".format(options.hist, iHisto, Histos[iHisto] )


#set the tdr style
tdrstyle.setTDRStyle()

xs_ttbar = 831.76
nev_ttbar = 92925926.
lumi = 12900. # pb-1

kfactorW = 1.21
kfactortt = 1. #0.94
ttSFfromAllHad = 1. #0.89*0.89

xs_wjets = [
    1629.87,  #1345.,     #100To200  
    435.6,    #359.7,     #200To400  
    59.27,    #48.91,     #400To600  
    14.58,    #12.05,     #600To800  
    6.656,    #5.501,     #800To1200 
    1.608,    #1.329,     #1200To2500
    0.039,    #0.03216,   #2500ToInf 
    ]

nev_wjets = [
    27529599., #100To200   1 / 642 failed      CORRECT
    4963240.,  #200To400  # fix this: update to new numbers BEFORE crab report
    1963464.,  #400To600 
    3722395.,  #600To800
    6314257.,  #800To1200 
    5215198.,  #1200To2500
    253561.,   #2500ToInf 
    ]
# fix this : get new event yeilds
xs_st = [
    136.02*0.322,     #ST t-channel top  
    80.95*0.322 ,     #ST t-channel antitop   
    71.7/2.,     #ST tW top                       xsec given for top + antitop https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_Wt
    71.7/2.,     #ST tW antitop                         
    47.13,     #ST s-channel            fix this: NOT SURE https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_s_channel_cross_secti Thea used  47.13 but website says 10.32
    ]

nev_st = [                                     
   2990400.,     #ST t-channel top  1/41 incomplete
   1682400.,     #ST t-channel antitop  
    998400.,     #ST tW top     
    985000.,     #ST tW antitop                         
   1000000.,     #ST s-channel  
    ]


xs_QCD = [
    7475.,
    587.1,
    167.,
    28.25,
    8.195,
    0.7346,
    0.102,
    0.00644,
    0.000163, 
    ] 

nev_QCD = [
    2482816., 
    1998648.,  
    1377400., 
    395328., 
    299967.,  
    38848.,  
    39975.,  
    39990.,  
    39988.,  
    ]


if options.noData : 
    print "WARNING : noData option is ON so the data wil not be plotted !!! "
else :
    if options.Type2 :
        print "Type 2 selection"
        datafile = ROOT.TFile('data_BCD_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root')
    else :
        print "Type 1 selection"
        datafile = ROOT.TFile('data_BCD_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root')

if options.Type2 :
    print "Type 2 selection"
    ttbarfile = ROOT.TFile('ttjets_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root')
else :
    print "Type 1 selection"
    ttbarfile = ROOT.TFile('ttjets_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root')



if options.allMC :
    if options.Type2 :
        wjetsfiles = [
            ROOT.TFile('wjets1_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
            ROOT.TFile('wjets2_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
            ROOT.TFile('wjets3_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
            ROOT.TFile('wjets4_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
            ROOT.TFile('wjets5_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
            ROOT.TFile('wjets6_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
            ROOT.TFile('wjets7_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
            ]
    else :
        wjetsfiles = [
            ROOT.TFile('wjets1_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
            ROOT.TFile('wjets2_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
            ROOT.TFile('wjets3_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
            ROOT.TFile('wjets4_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
            ROOT.TFile('wjets5_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
            ROOT.TFile('wjets6_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
            ROOT.TFile('wjets7_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
            ]

    wjets_colors = [   
        ROOT.kWhite,ROOT.kRed - 9, ROOT.kRed - 7, ROOT.kRed - 4, ROOT.kRed, ROOT.kRed +1, ROOT.kRed +2   ]

    if options.Type2 :
        stfiles = [
                ROOT.TFile('st1_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
                ROOT.TFile('st2_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
                ROOT.TFile('st3_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
                ROOT.TFile('st4_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
                ROOT.TFile('st5_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root') ]
    else:        
        stfiles = [
                ROOT.TFile('st1_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
                ROOT.TFile('st2_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
                ROOT.TFile('st3_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
                ROOT.TFile('st4_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
                ROOT.TFile('st5_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
            ]

    st_colors = [  ROOT.kWhite,ROOT.kCyan - 9, ROOT.kCyan - 7, ROOT.kCyan - 4, ROOT.kCyan  ]
 
    if options.Type2 :
        QCDfiles = [
                ROOT.TFile('QCD1_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
                ROOT.TFile('QCD2_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
                ROOT.TFile('QCD3_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
                ROOT.TFile('QCD4_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
                ROOT.TFile('QCD5_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
                ROOT.TFile('QCD6_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
                ROOT.TFile('QCD7_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
                ROOT.TFile('QCD8_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root'),
                ROOT.TFile('QCD9_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type2.root') ]
    else:        
        QCDfiles = [
                ROOT.TFile('QCD1_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
                ROOT.TFile('QCD2_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
                ROOT.TFile('QCD3_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
                ROOT.TFile('QCD4_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
                ROOT.TFile('QCD5_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
                ROOT.TFile('QCD6_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
                ROOT.TFile('QCD7_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
                ROOT.TFile('QCD8_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root'),
                ROOT.TFile('QCD9_outfile_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_type1.root') ]

    QCD_colors = [  ROOT.kWhite,ROOT.kYellow - 9, ROOT.kYellow - 8, ROOT.kYellow - 7,  ROOT.kYellow - 6,  ROOT.kYellow - 5, ROOT.kYellow - 4, ROOT.kYellow ,  ROOT.kYellow + 1 ]

   
objs = []



for istage in xrange(options.nstages) : 
    # Store the int number to rbin by
    rebinNum = int(options.rebinNum)


    # Get and scale the stored histos
    if options.noData : 
        print "WARNING : noData option is ON !!! "
        #hdata = ttbarfile.Get(options.hist + str(istage))
    else :
        hdata = datafile.Get(options.hist + str(istage))
        hdata.SetMarkerStyle(20)

    hwjets_list = []
    hst_list = []
    hQCD_list = []

    if options.allMC :
        # W + Jets MC Stack
        hwjets = None
        hwjets_stack = ROOT.THStack("hwjets_stack", "hwjets_stack")

        for iwjet in xrange(len(wjetsfiles)) :
            htemp = wjetsfiles[iwjet].Get(options.hist + str(istage))
            htemp.Scale( ( kfactorW * ttSFfromAllHad * xs_wjets[iwjet] ) / nev_wjets[iwjet] * lumi )
            hwjets_list.append( htemp )
            htemp.SetFillColor( wjets_colors[iwjet] )
            if iwjet == 0 :
                hwjets = htemp.Clone('hwjets')
            else :
                if options.verbose : print "Adding w+jets histos" 
                hwjets.Add( htemp )
            hwjets_stack.Add( htemp )
        #hwjets_stack.Draw("hist")
        hwjets.SetFillColor( ROOT.kRed )
        if iHisto != 11: hwjets.Rebin(rebinNum)
        
        # ST stack (t-channel top, t-channel antitop, tW top, tW antitop, s-channel)
        hst = None
        hst_stack = ROOT.THStack("hst_stack", "hst_stack")

        for ist in xrange(len(stfiles)) :
            htemp = stfiles[ist].Get(options.hist + str(istage))
            htemp.Scale(ttSFfromAllHad * xs_st[ist] / nev_st[ist] * lumi )
            hst_list.append( htemp )
            htemp.SetFillColor( st_colors[ist] )
            if ist == 0 :
                hst = htemp.Clone('hst')
            else :
                if options.verbose : print "Adding ST histos" 
                hst.Add( htemp )
            hst_stack.Add( htemp )
        hst.SetFillColor( ROOT.kCyan)
        if iHisto != 11:        hst.Rebin(rebinNum)
        #hwjets_stack.Draw("hist")

        if options.includeQCD :

            hQCD = None
            hQCD_stack = ROOT.THStack("hQCD_stack","hQCD_stack")
            for iQCD in xrange(len(QCDfiles)):
                if options.verbose : print "About to Get QCD histo" 
                htemp = QCDfiles[iQCD].Get(options.hist + str(istage))
                if options.verbose : print "About to scale QCD histo" 
                htemp.Scale(ttSFfromAllHad * xs_QCD[iQCD] / nev_QCD[iQCD] * lumi )
                if options.verbose : print "About to append QCD histo" 
                hQCD_list.append( htemp )
                htemp.SetFillColor( QCD_colors[iQCD] )
                if iQCD == 0 :
                    hQCD = htemp.Clone('hQCD')
                else :
                    if options.verbose : print "About to ADD QCD histos" 
                    hQCD.Add( htemp )
                    if options.verbose : print "Adding QCD histos" 
                hQCD_stack.Add( htemp )
            hQCD.Sumw2()
            hQCD.SetFillColor( ROOT.kYellow )
            if iHisto != 11:  hQCD.Rebin(rebinNum)
        

    httbar = ttbarfile.Get(options.hist + str(istage))
    httbar.Sumw2()
    httbar.Scale(kfactortt *ttSFfromAllHad * (xs_ttbar / nev_ttbar) * lumi   )
    httbar.SetFillColor(ROOT.kGreen + 2)
    if iHisto != 11:    httbar.Rebin(rebinNum)

    if not options.noData and  iHisto != 11:
        hdata.Rebin(rebinNum)

    mchist = httbar.Clone()
    if options.allMC : 
        if options.verbose : print "About to ADD hwjets to httbar histo" 
        mchist.Add( hwjets )
        mchist.Add( hst )
        #if options.includeQCD :
        #    mchist.Add( hQCD )

    #if not options.noData and iHisto != 11:
        #Scale ttbar MC by ratio of integrals of data MC
        #httbar = ScalettMC(httbar, hdata, mchist ,  xAxisrange[iHisto][0] , xAxisrange[iHisto][1] ) 

    if iHisto != 11:
        hstack = ROOT.THStack("bkgs", "")
        if options.allMC :
            hstack.Add( hwjets )
            hstack.Add( hst )
            if options.includeQCD :
                hstack.Add( hQCD )
        hstack.Add( httbar )
   
    theIndex = None 
    # Fitting Preparation 
    ## Only fit the histos of SD jet mass in later stages of selection
    if (iHisto <17 and iHisto > 12 ) and istage >= (options.nstages-2) : 
        theIndex = iHisto - 13
        
        if options.Type2 :
            if iHisto > 12 : continue # Don't fit SD subjet mass for type 2
            minFitMC = 65.
            maxFitMC = 105.

            minFitData = 65.
            maxFitData = 105.

        else :
            #if iHisto == 0 : continue # Don't fit AK8 jet mass for type 1 
            minFitMC = 55.
            maxFitMC = 115.

            minFitData = 55.
            maxFitData = 115.

    if not options.noData and (  (iHisto <17 and iHisto > 12 )  and istage >= (options.nstages-2) ) :

        if options.verbose : print "Fitting range for {0} ,istage {1}, is from {2:2.2f} to {3:2.2f} GeV for data and {2:2.2f} to {3:2.2f} GeV for MC".format(options.hist, istage, minFitData, maxFitData,  minFitMC, maxFitMC)
 
        if minFitData !=  minFitMC or maxFitData != maxFitMC : print "USING DIFFERENT FIT RANGES FOR DATA AND MC"

        fitter_data = ROOT.TF1("fitter_data", "gaus", minFitData, maxFitData)

        if options.fixFit and istage ==(options.nstages - 1) and Datameans[theIndex] != 0. :
            
            data_meanval = Datameans[theIndex]                                          
            data_sigmaval = Datasigmas[theIndex] 

            fitter_data.FixParameter(1, data_meanval)
            fitter_data.FixParameter(2, data_sigmaval)
        if options.fixFit  :
            fitter_data.SetParLimits(1,76.,86.)
        fitter_data.SetLineColor(1)
        fitter_data.SetLineWidth(2)
        fitter_data.SetLineStyle(2)
   
        tempCloneData = hdata.Clone()
        tempCloneData.SetName("tempCloneData")

        if options.fixFit and istage == (options.nstages -1):
            tempCloneData.Fit(fitter_data,'B' )
        else :
            tempCloneData.Fit(fitter_data,'R' )


        amp_data    = fitter_data.GetParameter(0);
        eamp_data   = fitter_data.GetParError(0); 
        mean_data   = fitter_data.GetParameter(1);
        emean_data  = fitter_data.GetParError(1); 
        width_data  = fitter_data.GetParameter(2);
        ewidth_data = fitter_data.GetParError(2); 

        print 'Combined: amp_data {0:6.3}, eamp_data {1:6.3}, mean_data {2:6.3},emean_data {3:6.3}, width_data {4:6.3}, ewidth_data {5:6.3}  '.format(amp_data , eamp_data , mean_data, emean_data,  width_data, ewidth_data   ) 


        if options.fixFit and istage == (options.nstages -2) :
            Datameans[theIndex] = mean_data
            Datasigmas[theIndex] = width_data
            if options.verbose : print "The mean of the gaussian fit to data is {0:3.3f} +/- {1:3.3f} with fit range ({2}, {3} ) ".format(mean_data , width_data , minFitData, maxFitData )

    if (iHisto <17 and iHisto > 12 )  and istage >= (options.nstages-2) : 
        fitter_mc = ROOT.TF1("fitter_mc", "gaus", minFitMC, maxFitMC)
        fitter_mc.SetLineColor(4)
        fitter_mc.SetLineWidth(2)
        fitter_mc.SetLineStyle(4)

        if options.fixFit and istage == (options.nstages -1) and MCmeans[theIndex] != 0. :
            mc_meanval = MCmeans[theIndex]
            mc_sigmaval = MCsigmas[theIndex]
            fitter_mc.FixParameter(1, mc_meanval)
            fitter_mc.FixParameter(2, mc_sigmaval)
        if options.fixFit  :
            fitter_mc.SetParLimits(1,76.,86.)

        tempCloneMC = mchist.Clone()
        tempCloneMC.SetName("tempCloneMC")

        if options.fixFit and istage ==(options.nstages - 1):
            tempCloneMC.Fit(fitter_mc,'B' )
        else :
            tempCloneMC.Fit(fitter_mc,'R' )

        amp_mc    = fitter_mc.GetParameter(0);
        eamp_mc   = fitter_mc.GetParError(0); 
        mean_mc   = fitter_mc.GetParameter(1);
        emean_mc  = fitter_mc.GetParError(1); 
        width_mc  = fitter_mc.GetParameter(2);
        ewidth_mc = fitter_mc.GetParError(2); 
              
        print 'MC : amp_mc {0:6.3}, eamp_mc {1:6.3}, mean_mc {2:6.3},emean_mc {3:6.3}, width_mc {4:6.3}, ewidth_mc {5:6.3}  '.format(amp_mc , eamp_mc , emean_mc, emean_mc,  width_mc, ewidth_mc   ) 

        if options.fixFit and istage == (options.nstages -2) :
            MCmeans[theIndex] = mean_mc
            MCsigmas[theIndex] = width_mc
            if options.verbose : print "The mean of the gaussian fit to mchist MC is {0:3.3f} +/- {1:3.3f} with fit range ({2}, {3} ) ".format(mean_mc, width_mc, minFitMC, maxFitMC )

    if (iHisto <17 and iHisto > 12 ) and not options.noData and theIndex != None :
        # define pt of SD subjet 0 for this histo
        ptIs = [250., 350.,450.,550.,700.]           
        pt = ptIs[theIndex]

        jmr = 1.0
        jmr_uncert = jmr
        jms = 1.0
        jms_uncert = jms
        
        binSizeData = hdata.GetBinWidth(0)
        binSizeMC = mchist.GetBinWidth(0) 

        if options.verbose : print "Bin size in data {0:1.2f} and MC  {1:1.2f}".format(binSizeData, binSizeMC )
        mclow = 0. 
        mchigh = 0.

        datalow = 0.
        datahigh = 0.
       
        mclow = MCmeans[theIndex] - MCsigmas[theIndex] 
        mchigh = MCmeans[theIndex] + MCsigmas[theIndex] 

        datalow = Datameans[theIndex] - Datasigmas[theIndex] 
        datahigh = Datameans[theIndex] + Datasigmas[theIndex]

        mcAxis = mchist.GetXaxis()
        dataAxis = hdata.GetXaxis()

        bminmc = mcAxis.FindBin(mclow)
        bmaxmc = mcAxis.FindBin(mchigh)

        bmindata = hdata.FindBin(datalow)
        bmaxdata = hdata.FindBin(datahigh)

        if istage == (options.nstages-2)  :
            nMCpre[theIndex] = mchist.Integral(bminmc , bmaxmc  ) #/ binSizeMC
            nDatapre[theIndex] = hdata.Integral(bmindata, bmaxdata  ) #/ binSizeData
            nMCupre[theIndex] =  math.sqrt( nMCpre[theIndex] )   #mchist.IntegralError(bminmc , bmaxmc  ) / binSizeMC
            nDataupre[theIndex] = math.sqrt(nDatapre[theIndex] ) #hdata.IntegralError(bmindata, bmaxdata  ) / binSizeData
            if options.verbose : 
                print "Integral +/- 1 sigma from peak BEFORE tau21 cut is : "
                print "MC : {}".format(nMCpre[theIndex])
                print "Data : {}".format(nDatapre[theIndex])

        if istage == (options.nstages-1)  :
            nMCpost[theIndex] = mchist.Integral(bminmc , bmaxmc  ) #/ binSizeMC
            nDatapost[theIndex] = hdata.Integral(bmindata, bmaxdata  ) #/ binSizeData
            nMCupost[theIndex] =  math.sqrt( nMCpost[theIndex] )  #mchist.IntegralError(bminmc , bmaxmc  ) / binSizeMC
            nDataupost[theIndex] = math.sqrt(nDatapost[theIndex] )#hdata.IntegralError(bmindata, bmaxdata  ) / binSizeData
            if options.verbose : 
                print "Integral +/- 1 sigma from peak BEFORE tau21 cut is : "
                print "MC : {}".format(nMCpost[theIndex])
                print "Data : {}".format(nDatapost[theIndex])

        # compute the jet mass resolution
        jmr = 0.
        jmr_uncert = 0.
        jmrel_uncert = 0.
        jmrel = 0.
        jmrmu = 0.
        jmrmu_uncert = 0.
        if mean_mc > 0. and mean_data > 0. : 
            jmr = mean_data / mean_mc
            jmr_uncert = jmr * math.sqrt( (emean_data/mean_data)**2 + (emean_mc/mean_mc)**2 )

        # compute the jet mass scale
        jms = 0.
        jms_uncert = 0.
        jms_mu = 0.
        jms_mu_uncert = 0.
        jms_el = 0.
        jms_el_uncert = 0.
        if width_mc > 0. and width_data > 0. :
            jms = width_data / width_mc
            jms_uncert = jms * math.sqrt( (ewidth_data/width_data)**2 + (ewidth_mc/width_mc)**2 )

        if hpeak != None :    
            peakAxis = hpeak.GetXaxis()
            ibin = peakAxis.FindBin(pt)
            hpeak.SetBinContent(ibin, jmr ) 
            hwidth.SetBinContent(ibin, jms )
            hpeak.SetBinError(ibin, jmr_uncert)   
            hwidth.SetBinError(ibin, jms_uncert)
            #else: print "hpeak is ZERO, unable to fill it or hwidth"

        if istage == (options.nstages -2) :
            ibin = hNpassDataPre.GetXaxis().FindBin(pt)
            hNpassDataPre.SetBinContent(ibin, nDatapre[theIndex])
            hNpassMCPre.SetBinContent(ibin, nMCpre[theIndex])
            hNpassDataPre.SetBinError(ibin, nDataupre[theIndex])
            hNpassMCPre.SetBinError(ibin, nMCupre[theIndex])
            hmeanDataPre.SetBinContent(ibin, Datameans[theIndex]) 
            hmeanMCPre.SetBinContent(ibin, MCmeans[theIndex] )
            hsigmaDataPre.SetBinContent(ibin, Datasigmas[theIndex])
            hsigmaMCPre.SetBinContent(ibin,  MCsigmas[theIndex] )
        if hNpassDataPost == None: print "WARNING: hNpassDataPost is empty, not setting bin content"
        if istage == (options.nstages -1)  and hNpassDataPost != None:
            ibin = hNpassDataPost.GetXaxis().FindBin(pt)
            hNpassDataPost.SetBinContent(ibin, nDatapost[theIndex])
            hNpassMCPost.SetBinContent(ibin, nMCpost[theIndex])
            hNpassDataPost.SetBinError(ibin, nDataupost[theIndex])
            hNpassMCPost.SetBinError(ibin, nMCupost[theIndex])
            datapost = nDatapost[theIndex] 
            datapre  = nDatapre[theIndex] 
            pt = ptBs[theIndex]
            ptToFill = float(pt)
            if pt > 800. :
                ptToFill = 799.
            bot = -1.
            if float(nMCpre[theIndex]) > 0.001 :
                bot = ( float(nMCpost[theIndex]) / float(nMCpre[theIndex]) )
            if (nDatapre[theIndex] > 0.001 and nMCpre[theIndex] > 0.001 and pt >= 201. and float(datapre) > 0.001 and  bot > 0.001) :
                print "bot {} datapre {} datapost {}".format(bot, datapre, datapost)
                SF =  ( float(datapost) / float(datapre) ) / bot
                SF_sd = SF * math.sqrt(   (- float(datapost) + float(datapre) ) / ( float(datapost) * float(datapre) )  + (-float(nMCpost[theIndex]) + float(nMCpre[theIndex])) / (float(nMCpost[theIndex]) * float(nMCpre[theIndex]))  )
                print "............................................"
                print "             SCALE FACTOR                   "
                print "............................................"
                print "pt Bin lower bound in GeV :  " + str(pt)
                print "Preliminary W tagging SF from subjet w : " + str(SF)
                print "Data efficiency for this  bin {0:5.3}".format(  float(datapost) / float(datapre) )
                print "MC efficiency for this  bin" + str(float(nMCpost[theIndex]) / float(nMCpre[theIndex]))
                print "standard deviation : " + str(SF_sd)
                print "............................................"
                ibin = hscale.GetXaxis().FindBin(ptToFill)
                hscale.SetBinContent(ibin, SF )
                hscale.SetBinError(ibin, SF_sd)
            else :
                ibin = hscale.GetXaxis().FindBin(ptToFill)
                hscale.SetBinContent(ibin, 0.0 )

        print "Integrals of fitted mass peak for W subjet of high Pt top:"
        thePtbins  = ["200-300", "300-400", "400-500", "500-600", "600-800"]

        print "##################  DATA  #############################"

        print "N pass post W tag MC pt {} : {}".format( thePtbins[theIndex], str( nDatapost[theIndex]  ) )
        print "N pass pre W tag MC pt {} : {}".format(  thePtbins[theIndex], str( nDatapre[theIndex]   ) )


        print "##################   MC   #############################"

        print "N pass post W tag MC pt {} : {}".format( thePtbins[theIndex], str( nMCpost[theIndex])  )
        print "N pass pre W tag MC pt {} : {}".format(  thePtbins[theIndex], str( nMCpre[theIndex])   )

        print "###############################################"

        fout.cd()
        fout.Write()
        fout.Close()



    ROOT.gStyle.SetOptStat(000000)
    #Set multiple of maximum to scale y axis by
    y_max_scale = 1.618 +1.

    c1 = ROOT.TCanvas("c" + str(istage), "c" + str(istage),1,1,745,701)
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
    if iHisto == 11:
        if not options.noData:
            '''
            hdata.GetXaxis().SetRangeUser(  xAxisrange[iHisto][0] , xAxisrange[iHisto][1] )
            hdata.SetMaximum(y_max_scale * hdata.GetMaximum() )
            hdata.SetMinimum(0.0001 )
            hdata.GetYaxis().SetTitle("Events")
            hdata.GetYaxis().SetTitleSize(0.065)
            hdata.GetYaxis().SetTitleOffset(0.9) ## 0.7)
            hdata.GetYaxis().SetLabelSize(0.06)
            ## hdata.SetMarkerStyle(20)
            ## hdata.SetMarkerSize(0.8)
            '''
            hdata.SetLineColor(1)
            hdata.SetFillColor(1)
            hdata.SetFillStyle(0)
            hdata.SetLineWidth(2)
            hdata.SetMarkerStyle(20)
            hdata.SetMarkerSize(0.8)
        mchist.SetLineColor(4)
        mchist.SetFillColor(4)
        mchist.SetFillStyle(0)
        mchist.SetLineWidth(2)
        mchist.SetMarkerStyle(20)
        mchist.SetMarkerSize(0.8)

        mchist.Draw()
        hdata.Draw("e0 same")

    if iHisto != 11:      
        pad1 = ROOT.TPad("pad1", "pad1",0,0.3333333,1,1)
        pad1.Draw()
        pad1.cd()
        ## pad1.Range(-0.1792683,-2.983224,1.10122,146.183)
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

        if options.noData:
            httbar.GetXaxis().SetRangeUser(  xAxisrange[iHisto][0] , xAxisrange[iHisto][1] )
            httbar.SetMaximum(y_max_scale * httbar.GetMaximum() )
            httbar.SetXTitle(HistoTitle[iHisto]+" , Stage "+str(istage))
        if not options.noData:
            hdata.GetXaxis().SetRangeUser(  xAxisrange[iHisto][0] , xAxisrange[iHisto][1] )
            hdata.SetMaximum(y_max_scale * hdata.GetMaximum() )
            hdata.SetMinimum(0.0001 )
            hdata.GetYaxis().SetTitle("Events")
            hdata.GetYaxis().SetTitleSize(0.065)
            hdata.GetYaxis().SetTitleOffset(0.9) ## 0.7)
            hdata.GetYaxis().SetLabelSize(0.06)
            ## hdata.SetMarkerStyle(20)
            ## hdata.SetMarkerSize(0.8)
            hdata.SetLineColor(1)
            hdata.SetFillColor(1)
            hdata.SetFillStyle(0)
            hdata.SetLineWidth(2)
            hdata.SetMarkerStyle(20)
            hdata.SetMarkerSize(0.8)

            hdata.GetXaxis().SetNdivisions(506)
            hdata.GetXaxis().SetLabelFont(42)
            hdata.GetXaxis().SetLabelSize(0)
            hdata.GetXaxis().SetTitleSize(0.0475)
            hdata.GetXaxis().SetTickLength(0.045)
            hdata.GetXaxis().SetTitleOffset(1.15)
            hdata.GetXaxis().SetTitleFont(42)
            hdata.GetYaxis().SetTitle("Events")
            hdata.GetYaxis().SetNdivisions(506)
            hdata.GetYaxis().SetLabelFont(42)
            hdata.GetYaxis().SetLabelSize(0.06375)
            hdata.GetYaxis().SetTitleSize(0.07125)
            hdata.GetYaxis().SetTitleOffset(0.9)
            hdata.GetYaxis().SetTitleFont(42)
            hdata.GetZaxis().SetLabelFont(42)
            hdata.GetZaxis().SetLabelSize(0.0425)
            hdata.GetZaxis().SetTitleSize(0.0475)
            hdata.GetZaxis().SetTitleFont(42)
            hdata.SetXTitle(HistoTitle[iHisto]+" , Stage "+str(istage))


        if options.noData:
            httbar.Draw("e x0")
        if not options.noData:
            hdata.Draw("e x0")


        hstack.Draw("hist same")



        ## Only fit the histos of SD jet mass in later stages of selection
        if (iHisto <17 and iHisto > 12 )  and istage >= (options.nstages-2) : 
            tempCloneMC.Draw("axis same")
            fitter_mc.Draw("same")
            if not options.noData:
                tempCloneData.Draw("axis same")
                fitter_data.Draw("same")

        if options.noData:
            httbar.Draw("e same x0")
        if not options.noData:
            hdata.Draw("e same x0")


        if options.verbose : 
            print "Setting X axis range to ({0}  ,  {1})".format(xAxisrange[iHisto][0] , xAxisrange[iHisto][1] )
            if not options.noData:
                print "Setting Y axis range to ({0}  ,  {1})".format(0. ,y_max_scale * hdata.GetMaximum() )
    if iHisto != 11:
        words = ROOT.TLatex(0.14,0.916,"#font[62]{CMS} #font[52]{Preliminary}")
        words.SetNDC()
        words.SetTextFont(42)
        words.SetTextSize(0.0825)
        words.SetLineWidth(2)
        words.Draw()
        words1 = ROOT.TLatex(0.9,0.916,"12.9 fb^{-1} (13 TeV)")
        words1.SetNDC()
        words1.SetTextAlign(31)
        words1.SetTextFont(42)
        words1.SetTextSize(0.0825)
        words1.SetLineWidth(2)
        words1.Draw()
        words2 = ROOT.TLatex(0.181,0.82225,"")
        words2.SetNDC()
        words2.SetTextAlign(13)
        words2.SetTextFont(42)
        words2.SetTextSize(0.045)
        words2.SetLineWidth(2)
        words2.Draw()

        leg = ROOT.TLegend(0.63,0.5,0.78,0.8)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)
        leg.SetTextSize(0.036)

        leg.AddEntry( httbar, 't#bar{t} (80X Powheg + Pythia 8 )', 'f')
        if options.allMC :
            leg.AddEntry( hst, 'Single Top', 'f')
            leg.AddEntry( hwjets, 'W+jets', 'f')
            if options.includeQCD :
                leg.AddEntry( hQCD, 'QCD', 'f')
        if not options.noData:
            leg.AddEntry( hdata, 'Data', 'p')
        leg.Draw()

    ROOT.gPad.RedrawAxis()

    if iHisto != 11:
        pad1.Modified()
        c1.cd()
        if not options.noData:
            pad2 = ROOT.TPad("pad2", "pad2",0,0,1,0.3333333)
            pad2.Draw()
            pad2.cd()
            ## pad2.Range(-0.1792683,-1.370091,1.10122,1.899)
            pad2.SetFillColor(0)
            pad2.SetBorderMode(0)
            pad2.SetBorderSize(2)
            pad2.SetTickx(1)
            pad2.SetTicky(1)
            pad2.SetLeftMargin(0.14)
            pad2.SetRightMargin(0.04)
            pad2.SetTopMargin(0)
            pad2.SetBottomMargin(0.45)
            pad2.SetFrameFillStyle(0)
            pad2.SetFrameBorderMode(0)
            pad2.SetFrameFillStyle(0)
            pad2.SetFrameBorderMode(0)

            hRatio = hdata.Clone()
            hRatio.SetName('hRatio')
            hRatio.Sumw2()
            hRatio.SetStats(0)
            hRatio.Divide(mchist)


            hRatio.GetYaxis().SetRangeUser(0.01,1.99)
            ## hRatio.GetYaxis().SetTitle("Data / Bkgd")
            ## hRatio.GetYaxis().SetTitleOffset(0.3)
            ## hRatio.GetYaxis().SetTitleSize(0.17)
            ## hRatio.GetYaxis().SetNdivisions(205)
            ## hRatio.GetYaxis().SetLabelSize(0.11)
            ## hRatio.GetXaxis().SetLabelSize(0.11)
            ## hRatio.GetXaxis().SetTitleSize(0.17)
            hRatio.GetXaxis().SetTitle(  HistoTitle[iHisto]+" , Stage "+str(istage)  )

            hRatio.SetStats(0)
            hRatio.SetFillColor(1)
            hRatio.SetFillStyle(0)
            hRatio.SetLineWidth(2)
            hRatio.SetLineColor(1)
            hRatio.SetMarkerStyle(20)
            hRatio.SetMarkerSize(0.8)
            hRatio.GetXaxis().SetNdivisions(506)
            hRatio.GetXaxis().SetLabelFont(42)
            hRatio.GetXaxis().SetLabelOffset(0.015)
            hRatio.GetXaxis().SetLabelSize(0.1275)
            hRatio.GetXaxis().SetTitleSize(0.1425)
            hRatio.GetXaxis().SetTickLength(0.09)
            hRatio.GetXaxis().SetTitleOffset(1.15)
            hRatio.GetXaxis().SetTitleFont(42)
            hRatio.GetYaxis().SetTitle("#frac{Data}{MC}")
            #hRatio.GetYaxis().CenterTitle(true)
            hRatio.GetYaxis().SetNdivisions(304)
            hRatio.GetYaxis().SetLabelFont(42)
            hRatio.GetYaxis().SetLabelSize(0.1275)
            hRatio.GetYaxis().SetTitleSize(0.1425)
            hRatio.GetYaxis().SetTickLength(0.045)
            hRatio.GetYaxis().SetTitleOffset(0.45)
            hRatio.GetYaxis().SetTitleFont(42)
            hRatio.GetZaxis().SetLabelFont(42)
            hRatio.GetZaxis().SetLabelSize(0.0425)
            hRatio.GetZaxis().SetTitleSize(0.0475)
            hRatio.GetZaxis().SetTitleFont(42)

            hRatio.Draw("lepe0")

            lineup = ROOT.TF1("lineup", "1.5", -7000, 7000)
            lineup.SetLineColor(1)
            lineup.SetLineStyle(2)
            lineup.SetLineWidth(2)
            lineup.Draw("same")
            hRatio.Draw("e same x0")

            line = ROOT.TF1("line", "1", -7000, 7000)
            line.SetLineColor(1)
            line.SetLineStyle(1)
            line.SetLineWidth(3)
            line.Draw("same")
            hRatio.Draw("e same x0")

            lined = ROOT.TF1("lined", "0.5", -7000, 7000)
            lined.SetLineColor(1)
            lined.SetLineStyle(2)
            lined.SetLineWidth(2)
            lined.Draw("same")
            hRatio.Draw("e same x0")
            ROOT.gPad.RedrawAxis()
             
            pad2.Modified()
            c1.cd()
            c1.Modified()

            c1.cd()
            c1.SetSelected(c1)     


    if options.allMC :    MCs = "_MCIsttbarWjetsST"
    else             :    MCs = "_MCIsttbar"

    if options.Type2 : typeIs = "_type2Tops"
    else             : typeIs = "_type1Tops" 

    '''
    NOTE : Corrections applied beyond the standard MC scaling and weighting by semileptEvent weight are listed below:

 
    CorrIs = ["_NoCorr",     # 
                             # (negative weights corrected for now but must scale to account for them)


                "_ttSF",     # tt MC is scaled by ratio of integrals of tt to data


           "_PuppiCorr",     # Puppi corrections from Thea]

    ''' 
    CorrIs = "_PUreweight_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD"
    if options.allMC and options.ttSF : 
        CorrIs = "_PUreweight_ttSF_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD_"
    if options.allMC and options.includeQCD : CorrIs = "_PUreweight_QCD_mu45Trig_ak8pt500_METPt50_HTlep150_AK4pt30_tau32AFTERmSD"

    c1.Print("./plots_Oct28th/" + options.hist + str(istage) + typeIs + MCs + CorrIs + ".pdf", "pdf")
    #c1.Print("./plots_Oct25/" + options.hist + str(istage) + typeIs + MCs + CorrIs + ".png", "png")
    #c1.Print("plot_" + options.hist + str(istage) + MCs + ".root", "root")
    if not options.noData and not iHisto ==11 :  
        objs.append( [hdata, httbar, c1, hstack, leg] )
        if options.allMC :
            #objs.append( [hdata, httbar, hwjets, c1, hstack, leg] )
            objs.append( [hdata, httbar, hwjets, hst, c1, hstack, leg] )
