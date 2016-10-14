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


def ScalettMC(httbar__, hdata__ , hstT__ , hwjetsT__, intMin, intMax ) :
    # Find the tt scale factor
    sf = 0.
    scalefactortt = 0.

    hMC__ = httbar__.Clone()
    hMC__.SetDirectory(0)
    if options.allMC:
        hMC__.Add(hstT__)
        hMC__.Add(hwjetsT__)

    intMinbin = hMC__.FindBin(intMin)
    intMaxbin = hMC__.FindBin(intMax)

    if (hdata__.Integral() > 0.) and (hMC__.Integral() > 0.) and options.ttSF: 
        diff = float(hdata__.Integral(intMinbin, intMaxbin))- float(  hMC__.Integral(intMinbin, intMaxbin)  )
        sf = abs(    diff/ float(  httbar__.Integral(intMinbin, intMaxbin)     +1.  )        )     
    if not options.ttSF: 
        sf = 1.

    scalefactortt = sf 
    if options.ttSF and options.vebose: print "tt SCALE FACTOR APPLIED : {0:2.2f}".format(scalefactortt)

    if httbar__.Integral() > 0 : 
        httbar__.Scale( scalefactortt ) 
    else :
        print "tt bin  empty when using scalettMC() "
        httbar__.Scale( 0.)

    return httbar__ 



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
                          [0.     ,   400. ], # HTLepHist
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
                          [0.     ,   400. ], # HTLepHist
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


import ROOT
#ROOT.gStyle.SetTitleOffset(0.5, "Y")


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
    26304033., #100To200   10 / 214 failed      # fix this: update to new numbers after crab report
    4963240.,  #200To400 
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
    3279200.,     #ST t-channel top  
    1682400.,     #ST t-channel antitop   
    998400.,     #ST tW top                        https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_Wt
    985000.,     #ST tW antitop                         
    985000.,     #ST s-channel  
    ]

ROOT.gStyle.SetOptStat(000000)

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
    #wjets_colors = [  ROOT.kBlack,ROOT.kMagenta, ROOT.kYellow, ROOT.kGreen, ROOT.kRed, ROOT.kBlue, ROOT.kOrange   ]

    '''
    stfiles = [
        ROOT.TFile('wjets100to200_outfile.root'),
        ROOT.TFile('wjets200to400_outfile.root'),
        ROOT.TFile('wjets400to600_outfile.root'),
        ROOT.TFile('wjets600to800_outfile.root'),
        ROOT.TFile('wjets800to1200_outfile.root')
        ]

    st_colors = [  ROOT.kWhite,ROOT.kCyan - 9, ROOT.kCyan - 7, ROOT.kCyan - 4, ROOT.kCyan  ]
    '''
objs = []

for istage in xrange(13) : 

    # Get and scale the stored histos
 
    hdata = datafile.Get(options.hist + str(istage))
    hdata.SetMarkerStyle(20)


    hwjets_list = []
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
        '''
        # ST stack (t-channel top, t-channel antitop, tW top, tW antitop, s-channel)
        hst = None
        hst_stack = ROOT.THStack("hst_stack", "hst_stack")
        # working here ???
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
        '''

    httbar = ttbarfile.Get(options.hist + str(istage))
    httbar.Sumw2()
    httbar.Scale( xs_ttbar / nev_ttbar * lumi )
    if options.allMC : 
        #httbar = ScalettMC(httbar, hdata, hst , hwjets,  xAxisrange[iHisto][0] , xAxisrange[iHisto][1] ) 
        if options.verbose : print "Apply another scaling after adding ST "
    httbar.SetFillColor(ROOT.kGreen + 2)


    httbar.Rebin(options.rebinNum)
    hdata.Rebin(options.rebinNum)

    mchist = httbar.Clone()
    if options.allMC : 
        mchist.Add( hwjets )
        #mchist.Add( hst )

    hstack = ROOT.THStack("bkgs", "")
    if options.allMC :
        hstack.Add( hwjets )
    hstack.Add( httbar )
   
    # Fitting Preparation 
    ## Only fit the histos of SD jet mass in later stages of selection
    if (iHisto <2 or iHisto > 12 ) and istage > 7 : 

        if options.Type2 :
            if iHisto == 1 : continue # Don't fit SD subjet mass for type 2
            minFit = 55.
            maxFit = 115.

        else :
            if iHisto == 0 : continue # Don't fit AK8 jet mass for type 1 
            minFit = 55.
            maxFit = 115.


        if options.verbose : print "Fitting range is from {0:2.2f} to {1:2.2f} GeV".format(minFit, maxFit)

        fitter_data = ROOT.TF1("fitter_data", "gaus", minFit, maxFit)

        ''' # TO-DO : finish adding constraints on the gaussian fitting
        if options.fixFit :
            data_meanval = Datameans[iHisto]
            data_sigmaval = Datasigmas[iHisto] 

            fitter_data.FixParameter(1, data_meanval)
            fitter_data.FixParameter(2, data_sigmaval)
        '''
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

        ''' TO-DO : save these values at stage max-1 to use for fixing the fit at final selection stage
        if options.pre :
            Datameans[ipt] = mean_data
            Datasigmas[ipt] = width_data
        if ipt <=6:
            mc_meanval = MCmeans[ipt]
            mc_sigmaval = MCsigmas[ipt]


        if options.fixFit :
            fitter_mc.FixParameter(1, mc_meanval)
            fitter_mc.FixParameter(2, mc_sigmaval)
        '''

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
        '''
        if options.pre and ipt <=3 :
            MCmeans[ipt] = mean_mc
            MCsigmas[ipt] = width_mc
        '''



        # TO-DO : finish adding gaussian fitting




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
    #hstack.SetMaximum(   max (max1,max2) * 1.618 )
    ## Only fit the histos of SD jet mass in later stages of selection
    if (iHisto <2 or iHisto > 12 ) and istage > 7 : 
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
        #leg.AddEntry( hst, 'ST', 'f')
    leg.Draw()
    
    c1.Update()
    c1.Draw()

    if options.allMC :    MCs = "_MCIsttbarWjets" # update when adding ST
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
