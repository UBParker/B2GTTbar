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
                  default=True,
                  dest='allMC',
                  help='Do you want to plot all MC? (or just ttjets)')

parser.add_option('--rebinNum', type='float', action='store',
                  dest='rebinNum',
                  default = 10,
                  help='number to rebin the histograms by')

parser.add_option('--nstages', type='int', action='store',
                  dest='nstages',
                  default = 13,
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

(options, args) = parser.parse_args(sys.argv)
argv = []


def ScalettMC(httbar__, hdata__ , hMC__, intMin, intMax ) :
    # Find the tt scale factor
    sf = 0.
    scalefactortt = 0.

    intMinbin = hMC__.FindBin(intMin)
    intMaxbin = hMC__.FindBin(intMax)

    if (hdata__.Integral() > 0.) and (hMC__.Integral() > 0.) and options.ttSF: 
        diff = float(hdata__.Integral(intMinbin, intMaxbin))- float(  hMC__.Integral(intMinbin, intMaxbin)  )
        sf = abs(    diff/ float(  httbar__.Integral(intMinbin, intMaxbin)     ) +1.       )     
    if not options.ttSF: 
        sf = 1.

    scalefactortt = sf 
    if options.ttSF and options.verbose: print "tt SCALE FACTOR APPLIED : {0:2.2f} based on integral of range ({1},{2})".format(scalefactortt, intMin, intMax)

    if httbar__.Integral() > 0 : 
        httbar__.Scale( scalefactortt ) 
    else :
        print "tt bin  empty when using scalettMC() "
        httbar__.Scale( 0.)

    return httbar__ 

# Define histograms and arrays for storing and calculating SF, JMR, JMS
ptBs =  array.array('d', [200., 300., 400., 500., 600., 800.])
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
hDataEff = ROOT.TH1F("hDataEff", " ; ; ", nptBs, ptBs)
hMCEff = ROOT.TH1F("hMCEff", " ; ; ", nptBs, ptBs)


nMCpre = array.array('d', [0., 0., 0., 0., 0.])
nDatapre = array.array('d', [0., 0., 0., 0., 0.])
nMCupre = array.array('d', [0., 0., 0., 0., 0.])
nDataupre = array.array('d', [0., 0., 0., 0., 0.])

MCmeans = array.array('d', [0., 0., 0., 0., 0.])
MCsigmas = array.array('d', [0., 0., 0., 0., 0.])
Datameans = array.array('d', [0., 0., 0., 0., 0.])
Datasigmas = array.array('d', [0., 0., 0., 0., 0.])

nMCpost = array.array('d', [0., 0., 0., 0., 0.])
nDatapost = array.array('d', [0., 0., 0., 0., 0.])
nMCupost = array.array('d', [0., 0., 0., 0., 0.])
nDataupost = array.array('d', [0., 0., 0., 0., 0.])



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
                          [39.    ,   150. ], # AK8MSDSJ0Pt200To300Hist
                          [39.    ,   150. ], # AK8MSDSJ0Pt300To400Hist
                          [39.    ,   150. ], # AK8MSDSJ0Pt400To500Hist
                          [39.    ,   150. ], # AK8MSDSJ0Pt500To600Hist                                                                        
                 ]

else:
    xAxisrange = [        [140.0  ,   250. ], # AK8MSDHist
                          [ 39.0  ,   150. ], # AK8MSDSJ0Hist
                          [0.     ,  1000. ], # AK8PtHist
                          [-2.5   ,    2.5 ], # AK8EtaHist
                          [0.0    ,    1.0 ], # AK8Tau21Hist
                          [0.0    ,    1.0 ], # AK8Tau32Hist
                          [140.0  ,   250. ], # AK8MHist
                          [0.0    ,   600. ], # LeptonPtHist
                          [2.5    ,  -2.5  ], # LeptonEtaHist
                          [0.     ,   300. ], # METPtHist
                          [0.     ,   700. ], # HTLepHist
                          [0.     ,   300. ], # Iso2DHist
                          [0.     ,     1. ], # AK4BdiscHist
                          [39.    ,   150. ], # AK8MSDSJ0Pt200To300Hist
                          [39.    ,   150. ], # AK8MSDSJ0Pt300To400Hist
                          [39.    ,   150. ], # AK8MSDSJ0Pt400To500Hist
                          [39.    ,   150. ], # AK8MSDSJ0Pt500To600Hist
                 ]


Histos = [  "AK8MSDHist", #0
         "AK8MSDSJ0Hist", #1
             "AK8PtHist", #2
            "AK8EtaHist", #3
          "AK8Tau21Hist", #4
          "AK8Tau32Hist", #5
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
"AK8MSDSJ0Pt500To600Hist"  #16    
    ]

# TO-DO : Add all below histo names to Histos and HistoTitle
'''
            self.AK8MPt200To300Hist
            self.AK8MSDPt200To300Hist
            self.AK8MSDSJ0Pt200To300Hist
            self.AK8MPt300To400Hist
            self.AK8MSDPt300To400Hist
            self.AK8MSDSJ0Pt300To400Hist
            self.AK8MPt400To500Hist
            self.AK8MSDPt400To500Hist
            self.AK8MPt500To600Hist
            self.AK8MSDPt500To600Hist
            self.AK8MSDSJ0Pt500To600Hist
            self.AK8MPt600To800Hist
            self.AK8MSDPt600To800Hist
            self.AK8MSDSJ0Pt600To800Hist

'''

HistoTitle =            [           "AK8 Jet SD Mass (GeV)",
                             "Leading Subjet SD Mass (GeV)",
                                                "AK8 Jet P_{T} (GeV)",
                                                 "AK8 Jet #eta", 
                                            "AK8 Jet #tau_{21}",
                                            "AK8 Jet #tau_{32}",
                                                 "AK8 Jet Mass (GeV)",
                                                 "Lepton P_{T} (GeV)",
                                                  "Lepton #eta",
                                                "Missing P_{T} (GeV)",
                                 "Lepton P_{T} + Missing P_{T} (GeV)",
               "Lepton 2D isolation (#Delta R vs p_{T}^{REL} )",
                                                 "CSVv2 B Disc",
                             "(200<P_{t}<300) Leading Subjet SD Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(300<P_{t}<400) Leading Subjet SD Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(400<P_{t}<500) Leading Subjet SD Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(500<P_{t}<600) Leading Subjet SD Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
                             "(600<P_{t}<800) Leading Subjet SD Mass (GeV)", # TO-DO : move pt label elsewhere on canvas
]


iHisto = Histos.index(options.hist) 
if options.verbose : print "Histo name in options was {0}, index number {1:0.0f}, entry in Histos(index) is {2}".format(options.hist, iHisto, Histos[iHisto] )

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)

CMS_lumi.lumi_13TeV = "12.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref


# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref




xs_ttbar = 831.
nev_ttbar = 92925926.
lumi = 12900. # pb-1

kfactorW = 1. #1.21
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
    27529599., #100To200   1 / 642 failed      CORRECT
    4963240.,  #200To400  # fix this: update to new numbers after crab report
    1963464.,  #400To600 
    3722395.,  #600To800
    6314257.,  #800To1200 
    5215198.,  #1200To2500 12 / 54 failed  (total = 6817172)
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

nev_st = [                                      # fix this :add event counts from crab report
   2990400.,     #ST t-channel top  1/41 incomplete
   1682400.,     #ST t-channel antitop  
    998400.,     #ST tW top     
    985000.,     #ST tW antitop                         
   1000000.,     #ST s-channel  
    ]



if options.Type2 :
    print "Type 2 selection"
    ttbarfile = ROOT.TFile('ttjets_outfile_type2.root')
    datafile = ROOT.TFile('data_BCD_outfile_type2.root')
else :
    print "Type 1 selection"
    ttbarfile = ROOT.TFile('ttjets_outfile_type1.root')
    datafile = ROOT.TFile('data_BCD_outfile_type1.root')

if options.allMC :
    if options.Type2 :
        wjetsfiles = [
            ROOT.TFile('wjets1_outfile_type2.root'),
            ROOT.TFile('wjets2_outfile_type2.root'),
            ROOT.TFile('wjets3_outfile_type2.root'),
            ROOT.TFile('wjets4_outfile_type2.root'),
            ROOT.TFile('wjets5_outfile_type2.root'),
            ROOT.TFile('wjets6_outfile_type2.root'),
            ROOT.TFile('wjets7_outfile_type2.root'),
            ]
    else :
        wjetsfiles = [
            ROOT.TFile('wjets1_outfile_type1.root'),
            ROOT.TFile('wjets2_outfile_type1.root'),
            ROOT.TFile('wjets3_outfile_type1.root'),
            ROOT.TFile('wjets4_outfile_type1.root'),
            ROOT.TFile('wjets5_outfile_type1.root'),
            ROOT.TFile('wjets6_outfile_type1.root'),
            ROOT.TFile('wjets7_outfile_type1.root'),
            ]

    wjets_colors = [   
        ROOT.kWhite,ROOT.kRed - 9, ROOT.kRed - 7, ROOT.kRed - 4, ROOT.kRed, ROOT.kRed +1, ROOT.kRed +2   ]

    if options.Type2 :
        stfiles = [
                ROOT.TFile('st1_outfile_type2.root'),
                ROOT.TFile('st2_outfile_type2.root'),
                ROOT.TFile('st3_outfile_type2.root'),
                ROOT.TFile('st4_outfile_type2.root'),
                ROOT.TFile('st5_outfile_type2.root') ]
    else:        
        stfiles = [
                ROOT.TFile('st1_outfile_type1.root'),
                ROOT.TFile('st2_outfile_type1.root'),
                ROOT.TFile('st3_outfile_type1.root'),
                ROOT.TFile('st4_outfile_type1.root'),
                ROOT.TFile('st5_outfile_type1.root'),
            ]

    st_colors = [  ROOT.kWhite,ROOT.kCyan - 9, ROOT.kCyan - 7, ROOT.kCyan - 4, ROOT.kCyan  ]
    
objs = []

for istage in xrange(options.nstages) : 

    # Get and scale the stored histos
 
    hdata = datafile.Get(options.hist + str(istage))
    hdata.SetMarkerStyle(20)


    hwjets_list = []
    hst_list = []
    if options.allMC :
        # W + Jets MC Stack
        hwjets = None
        hwjets_stack = ROOT.THStack("hwjets_stack", "hwjets_stack")

        for iwjet in xrange(len(wjetsfiles)) :
            htemp = wjetsfiles[iwjet].Get(options.hist + str(istage))
            htemp.Scale( ( kfactorW * xs_wjets[iwjet] ) / nev_wjets[iwjet] * lumi )
            hwjets_list.append( htemp )
            htemp.SetFillColor( wjets_colors[iwjet] )
            if iwjet == 0 :
                hwjets = htemp.Clone('hwjets')
            else :
                hwjets.Add( htemp )
            hwjets_stack.Add( htemp )
        #hwjets_stack.Draw("hist")
        hwjets.SetFillColor( ROOT.kRed )
        hwjets.Rebin(options.rebinNum)
        
        # ST stack (t-channel top, t-channel antitop, tW top, tW antitop, s-channel)
        hst = None
        hst_stack = ROOT.THStack("hst_stack", "hst_stack")
        for ist in xrange(len(stfiles)) :
            htemp = stfiles[ist].Get(options.hist + str(istage))
            htemp.Scale( xs_st[ist] / nev_st[ist] * lumi )
            hst_list.append( htemp )
            htemp.SetFillColor( st_colors[ist] )
            if ist == 0 :
                hst = htemp.Clone('hst')
            else :
                hst.Add( htemp )
            hst_stack.Add( htemp )
        #hwjets_stack.Draw("hist")

        hst.SetFillColor( ROOT.kCyan )
        hst.Rebin(options.rebinNum)
        

    httbar = ttbarfile.Get(options.hist + str(istage))
    httbar.Sumw2()
    ttKfactor = 1. # 0.94 # TO-DO - Check with Christine on origin of this and updating to 80x
    httbar.Scale(ttKfactor * xs_ttbar / nev_ttbar * lumi )
    httbar.SetFillColor(ROOT.kGreen + 2)
    httbar.Rebin(options.rebinNum)

    hdata.Rebin(options.rebinNum)

    mchist = httbar.Clone()
    if options.allMC : 
        mchist.Add( hwjets )
        mchist.Add( hst )

    #Scale ttbar MC by ratio of integrals of data MC
    httbar = ScalettMC(httbar, hdata, mchist ,  xAxisrange[iHisto][0] , xAxisrange[iHisto][1] ) 

    hstack = ROOT.THStack("bkgs", "")
    if options.allMC :
        hstack.Add( hwjets )
        hstack.Add( hst )
    hstack.Add( httbar )
   
    # Fitting Preparation 
    ## Only fit the histos of SD jet mass in later stages of selection
    if (iHisto <2 or iHisto > 12 ) and istage >= (options.nstages-2) : 
        theIndex = iHisto - 13

        if options.Type2 :
            if iHisto == 1 or iHisto > 12 : continue # Don't fit SD subjet mass for type 2
            minFit = 55.
            maxFit = 115.

        else :
            if iHisto == 0 : continue # Don't fit AK8 jet mass for type 1 
            minFit = 55.
            maxFit = 115.


        if options.verbose : print "Fitting range for {0} ,istage {1}, is from {2:2.2f} to {3:2.2f} GeV".format(options.hist, istage, minFit, maxFit)

        fitter_data = ROOT.TF1("fitter_data", "gaus", minFit, maxFit)

        if options.fixFit and istage ==(options.nstages - 1) :
            
            data_meanval = Datameans[theIndex]                                          
            data_sigmaval = Datasigmas[theIndex] 

            fitter_data.FixParameter(1, data_meanval)
            fitter_data.FixParameter(2, data_sigmaval)
        
        fitter_data.SetLineColor(1)
        fitter_data.SetLineWidth(2)
        fitter_data.SetLineStyle(2)

        if options.fixFit :
            hdata.Fit(fitter_data,'B' )
        else :
            hdata.Fit(fitter_data,'R' )


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

        if options.fixFit and istage == (options.nstages -1):
            mc_meanval = MCmeans[theIndex]
            mc_sigmaval = MCsigmas[theIndex]
            fitter_mc.FixParameter(1, mc_meanval)
            fitter_mc.FixParameter(2, mc_sigmaval)

        fitter_mc = ROOT.TF1("fitter_mc", "gaus", minFit, maxFit)
        fitter_mc.SetLineColor(4)
        fitter_mc.SetLineWidth(2)
        fitter_mc.SetLineStyle(4)

        if options.fixFit :
            mchist.Fit("fitter_mc",'B' )
        else :
            mchist.Fit("fitter_mc",'R' )
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

        if iHisto > 12 :
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
            if istage == (options.nstages-1)  :
                nMCpost[theIndex] = mchist.Integral(bminmc , bmaxmc  ) #/ binSizeMC
                nDatapost[theIndex] = hdata.Integral(bmindata, bmaxdata  ) #/ binSizeData
                nMCupost[theIndex] =  math.sqrt( nMCpost[theIndex] )  #mchist.IntegralError(bminmc , bmaxmc  ) / binSizeMC
                nDataupost[theIndex] = math.sqrt(nDatapost[theIndex] )#hdata.IntegralError(bmindata, bmaxdata  ) / binSizeData

            # compute the jet mass resolution
            jmr = 0.
            jmr_uncert = 0.
            jmrel_uncert = 0.
            jmrel = 0.
            jmrmu = 0.
            jmrmu_uncert = 0.
            if mean_mc > 0. : 
                jmr = mean_data / mean_mc
                jmr_uncert = jmr * math.sqrt( (emean_data/mean_data)**2 + (emean_mc/mean_mc)**2 )

            # compute the jet mass scale
            jms = 0.
            jms_uncert = 0.
            jms_mu = 0.
            jms_mu_uncert = 0.
            jms_el = 0.
            jms_el_uncert = 0.
            if width_mc > 0. :
                jms = width_data / width_mc
                jms_uncert = jms * math.sqrt( (ewidth_data/width_data)**2 + (ewidth_mc/width_mc)**2 )

            ibin = hpeak.GetXaxis().FindBin(pt)
            hpeak.SetBinContent(ibin, jmr ) 
            hwidth.SetBinContent(ibin, jms )
            hpeak.SetBinError(ibin, jmr_uncert)   
            hwidth.SetBinError(ibin, jms_uncert)


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
            if istage == (options.nstages -1) :
                ibin = hNpassDataPost.GetXaxis().FindBin(pt)
                hNpassDataPost.SetBinContent(ibin, nDatapost[theIndex])
                hNpassMCPost.SetBinContent(ibin, nMCpost[theIndex])
                hNpassDataPost.SetBinError(ibin, nDataupost[theIndex])
                hNpassMCPost.SetBinError(ibin, nMCupost[theIndex])

                for ipt in xrange(0, len(ptBs)-1 ) :
                    datapost = nDatapost[ipt] 
                    datapre  = nDatapre[ipt] 
                    pt = ptBs[ipt]
                    ptToFill = float(pt)
                    if pt > 800. :
                        ptToFill = 799.
                    bot = -1.
                    if float(nMCpre[ipt]) > 0.001 :
                        bot = ( float(nMCpost[ipt]) / float(nMCpre[ipt]) )
                    if (nDatapre[ipt] > 0.001 and nMCpre[ipt] > 0.001 and pt >= 201. and float(datapre) > 0.001 and  bot > 0.001) :
                        print "bot {} datapre {} datapost {}".format(bot, datapre, datapost)
                        SF =  ( float(datapost) / float(datapre) ) / bot
                        SF_sd = SF * math.sqrt(   (- float(datapost) + float(datapre) ) / ( float(datapost) * float(datapre) )  + (-float(nMCpost[ipt]) + float(nMCpre[ipt])) / (float(nMCpost[ipt]) * float(nMCpre[ipt]))  )
                        print "............................................"
                        print "             SCALE FACTOR                   "
                        print "............................................"
                        print "pt Bin lower bound in GeV :  " + str(pt)
                        print "Preliminary W tagging SF from subjet w : " + str(SF)
                        print "Data efficiency for this  bin {0:5.3}".format(  float(datapost) / float(datapre) )
                        print "MC efficiency for this  bin" + str(float(nMCpost[ipt]) / float(nMCpre[ipt]))
                        print "standard deviation : " + str(SF_sd)
                        print "............................................"
                        ibin = hscale.GetXaxis().FindBin(ptToFill)
                        hscale.SetBinContent(ibin, SF )
                        hscale.SetBinError(ibin, SF_sd)
                    else :
                        ibin = hscale.GetXaxis().FindBin(ptToFill)
                        hscale.SetBinContent(ibin, 0.0 )

        print "Integrals of fitted mass peak for W subjet of high Pt top:"


        print "##################  DATA  #############################"

        print "N pass post W tag Data pt 200-300 : " + str( nDatapost[0])
        print "N pass pre W tag Data pt 200-300 : " + str(nDatapre[0])

        print "N pass post W tag Data pt 300-400 : " + str(nDatapost[1])
        print "N pass pre W tag Data pt 300-400 : " + str(nDatapre[1])

        print "N pass post W tag Data pt 400-500 : " + str(nDatapost[2])
        print "N pass pre W tag Data pt 400-500 : " + str(nDatapre[2])

        print "N pass post W tag Data pt 500-600 : " + str(nDatapost[3])
        print "N pass pre W tag Data pt 500-600 : " + str(nDatapre[3])

        print "N pass post W tag Data pt 600-800 : " + str(nDatapost[4])
        print "N pass pre W tag Data pt 600-800 : " + str(nDatapre[4])

        print "##################   MC   #############################"

        print "N pass post W tag MC pt 200-300 : " + str( nMCpost[0])
        print "N pass pre W tag MC pt 200-300 : " + str(nMCpre[0])

        print "N pass post W tag MC pt 300-400 : " + str(nMCpost[1])
        print "N pass pre W tag MC pt 300-400 : " + str(nMCpre[1])

        print "N pass post W tag MC pt 400-500 : " + str(nMCpost[2])
        print "N pass pre W tag MC pt 400-500 : " + str(nMCpre[2])

        print "N pass post W tag MC pt 500-600 : " + str(nMCpost[3])
        print "N pass pre W tag MC pt 500-600 : " + str(nMCpre[3])

        print "N pass post W tag MC pt 600-800 : " + str(nMCpost[4])
        print "N pass pre W tag MC pt 600-800 : " + str(nMCpre[4])

        print "###############################################"

    

    # TO-DO : Add Ratios to plots
    c1 = ROOT.TCanvas("c" + str(istage), "c" + str(istage) )
    CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
    max1 = hdata.GetMaximum()
    max2 = httbar.GetMaximum()
    hdata.Draw("e")
    hdata.GetXaxis().SetRangeUser( xAxisrange[iHisto][0] , xAxisrange[iHisto][1] )
    if options.verbose : print "Setting X axis range to ({0}  ,  {1})".format(xAxisrange[iHisto][0] , xAxisrange[iHisto][1] )
    hstack.Draw("hist same")
    hstack.GetXaxis().SetRangeUser(  xAxisrange[iHisto][0] , xAxisrange[iHisto][1] )
    hstack.SetMaximum(   max2 * 1.318 )
    ## Only fit the histos of SD jet mass in later stages of selection
    if (iHisto <2 or iHisto > 12 ) and istage >= (options.nstages -2) : 
        fitter_mc.Draw("same")
        fitter_data.Draw("same")
        #fitter_mc.SetMaximum(   max (max1,max2) * 1.618 )
        #fitter_data.SetMaximum(   max (max1,max2) * 1.618 )
    #hdata.SetMaximum(   max (max1,max2) * 1.618 )
    hdata.Draw("e same")

    hdata.GetYaxis().SetTitleOffset(1.2)
    hdata.SetXTitle(HistoTitle[iHisto]+" , Stage "+str(istage))
    hdata.SetYTitle("Events")
    hdata.BufferEmpty(1)
    hdata.GetXaxis().SetTitleSize(0.04)
    hdata.GetYaxis().SetTitleSize(0.05)



    leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.045)
    leg.AddEntry( hdata, 'Data', 'p')
    leg.AddEntry( httbar, 't#bar{t}', 'f')
    if options.allMC :
        leg.AddEntry( hwjets, 'W+jets', 'f')
        leg.AddEntry( hst, 'ST', 'f')
    leg.Draw()
    #ROOT.gStyle.SetOptStat(000000)
    c1.Update()
    c1.Draw()

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
    CorrIs = "_NoCorr"
    if options.allMC and options.ttSF : CorrIs = "_ttSF"

    c1.Print("plot_" + options.hist + str(istage) + typeIs + MCs + CorrIs + ".pdf", "pdf")
    c1.Print("plot_" + options.hist + str(istage) + typeIs + MCs + CorrIs + ".png", "png")
    #c1.Print("plot_" + options.hist + str(istage) + MCs + ".root", "root")
    objs.append( [hdata, httbar, c1, hstack, leg] )
    if options.allMC :
        objs.append( [hdata, httbar, hwjets, c1, hstack, leg] )
        #objs.append( [hdata, httbar, hwjets, hst, c1, hstack, leg] )
