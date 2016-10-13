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

parser.add_option('--xtitle', type='string', action='store',
                  dest='xtitle',
                  default = 'AK8 SD jet mass (GeV)',
                  help='x axis title of hist')

parser.add_option('--allMC', action='store_true',
                  default=True,
                  dest='allMC',
                  help='Do you want to plot all MC? (or just ttjets)')

parser.add_option('--rebinNum', type='float', action='store',
                  dest='rebinNum',
                  default = 10,
                  help='number to rebin the histograms by')

parser.add_option('--minval', type='float', action='store',
                  dest='minval',
                  default = 40.,
                  help='Minval for the x axis of plot')

parser.add_option('--maxval', type='float', action='store',
                  dest='maxval',
                  default = 150.,
                  help='Maxval for the x axis of plot')

parser.add_option('--Type2', action='store_true',
                  default=True,
                  dest='Type2',
                  help='Do you want to apply selection for type 2 tops as described in AN-16-215 ?')


(options, args) = parser.parse_args(sys.argv)
argv = []



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
lumi = 12300. # pb-1

kfactorW = 1.21
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

for istage in xrange(11) : 
    httbar = ttbarfile.Get(options.hist + str(istage))
    httbar.Sumw2()
    httbar.Scale( xs_ttbar / nev_ttbar * lumi ) 
    httbar.SetFillColor(ROOT.kGreen + 2)


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

    httbar.Rebin(options.rebinNum)
    hdata.Rebin(options.rebinNum)

    hstack = ROOT.THStack("bkgs", "")
    if options.allMC :
        hstack.Add( hwjets )
    hstack.Add( httbar )


    c1 = ROOT.TCanvas("c" + str(istage), "c" + str(istage) )
    max1 = hdata.GetMaximum()
    max2 = hstack.GetMaximum()
    hdata.SetMaximum(   max (max1,max2) * 1.618 )
    hdata.Draw("e")
    hdata.GetXaxis().SetRangeUser( options.minval , options.maxval )
    hstack.Draw("hist same")
    hstack.GetXaxis().SetRangeUser( options.minval , options.maxval )
    hstack.SetMaximum(   max (max1,max2) * 1.618 )
    hdata.Draw("e same")

    hdata.GetYaxis().SetTitleOffset(1.2)
    hdata.SetXTitle(options.xtitle)
    hdata.SetYTitle("Events")
    hdata.BufferEmpty(1)
    hdata.GetXaxis().SetTitleSize(0.057)
    hdata.GetYaxis().SetTitleSize(0.057)

    CMS_lumi.CMS_lumi(c1, iPeriod, iPos)

    leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.AddEntry( hdata, 'Data', 'p')
    leg.AddEntry( httbar, 't#bar{t}', 'f')
    if options.allMC :
        leg.AddEntry( hwjets, 'W+jets', 'f')
        #leg.AddEntry( hst, 'ST', 'f')
    leg.Draw()
    
    c1.Update()
    c1.Draw()
    c1.Print("plot_" + options.hist + str(istage) + ".pdf", "pdf")
    c1.Print("plot_" + options.hist + str(istage) + ".png", "png")
    objs.append( [hdata, httbar, c1, hstack, leg] )
    if options.allMC :
        objs.append( [hdata, httbar, hwjets, c1, hstack, leg] )
        #objs.append( [hdata, httbar, hwjets, hst, c1, hstack, leg] )
