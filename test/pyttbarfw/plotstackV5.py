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


class plotstack() : 
    '''
    This class uses as input the output histograms from the RunSemiLepTTbar class.
    It combines and scales the input hists and plots them in proper CMS PubCom format using the APlot class.
    '''
    def __init__(self,  argv) :
                    
        parser = OptionParser()

        parser.add_option('--hist', type='string', action='store',
                          dest='hist',
                          default = '',
                          help='Hist string')

        parser.add_option('--highmass', action='store_true',
                          dest='highmass',
                          default = True,
                          help='High mass?')

        parser.add_option('--el', action='store_true',
                          dest='el',
                          default = False,
                          help='plot only electrons?')
                          
        parser.add_option('--mu', action='store_true',
                          dest='mu',
                          default = False,
                          help='plot only muons?')  
                           
        parser.add_option('--otherttbar', action='store_true',
                          dest='otherttbar',
                          default = True,
                          help='plot ttbarTuneCUETP8M2T4?')   

        parser.add_option('--fixFit', action='store_true',
                          dest='fixFit',
                          default = False,
                          help='Fix the fit of the tau21 cut distribution to the value from the mass cut ?') 
                          
        (options, args) = parser.parse_args(sys.argv)
        argv = []

        import ROOT
        ROOT.gStyle.SetOptStat(000000)
        
        type1 = False
        type2 = False
        if options.highmass:
            type1 = True
        else: type2 = True  
        
        isMu = False
        isEl = False
        isBoth = True # False
        
        if options.mu: isMu = True
        elif options.el: isEl = True
        else: isBoth = True

        isTopmass = False
        isWmass = False
        if (options.hist.find("AK8")== -1 ) :
            print("Not fitting this histo since AK8 wasn't found.")
        else:
            if type1:
                if (options.hist.find("SDSJ")== -1 ) :
                    isTopmass = True
                else :
                    isWmass = True
            if type2:
                if (options.hist.find("MPt")== -1 ) and (options.hist.find("SD")== -1 ) :
                    print("Not fitting this histo since MPt and SD werent found.")
                else:   
                    isWmass = True                
        xs_ttbar = 831.
        nev_ttbar = 92925926. 
        self.otherttbar = False
        tune = 'CUETP8M1'
        
        if options.otherttbar == True :
            self.otherttbar = True
            nev_ttbar = 70452080.
            tune = 'CUETP8M2T4'

        lumi = 35860. #36494. # pb-1
        expectedRunsHist = None
        expectedRunsList = None
        if (options.hist.find("RunNumberHist")!= -1)  : 
            
            ### Plot lumis that should be present. json production described here https://docs.google.com/document/d/1aTeTVIi9eb-aup37dbUL8cWDPCJrn_sRYrZcjFhd4tI/edit?usp=sharing

            if options.el : expectedRuns = json.loads(open('/uscms_data/d3/aparker/B2GAll/CMSSW_8_0_22/src/Analysis/B2GTTbar/test/ProcessedLumis/singleEl2016B-H.json').read())
            elif options.mu : expectedRuns = json.loads(open('/uscms_data/d3/aparker/B2GAll/CMSSW_8_0_22/src/Analysis/B2GTTbar/test/ProcessedLumis/singleMu2016B-H.json').read()) 
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
                                        1345.,     #100To200  W + jets
                                        1.329,     #1200To2500
                                        359.7,     #200To400  
                                        0.03216,   #2500ToInf
                                        48.91,     #400To600  
                                        12.05,     #600To800  
                                        5.501     #800To1200 
            ]

        nev_wjets = [
                                    78403814.,# WJetsToLNu_HT-100To200_All 10235198 + 28550829 + 39617787
                                     6797731.,# 1200To2500_All 244532 + 6553199
                                    39680891.,# 200To400_All  4950373 + 14815928 + 19914590
                                     2637821.,# 2500ToInf 253561 + 2384260
                                     7759701.,# 400To600_All 1963464 + 5796237
                                    18425597.,# 600To800  14819287 + 3606310
                                     7352465., # 800To1200_  1544513 + 5807952
            ]
        xs_qcd = [
                                   645.528, # MuEnriched 470-600
                                   645.528 # MuEnriched 470-600
            ]

        nev_qcd = [
                                        3851524., # 470-600 MuEnriched
                                        5663755.,  # 470-600 MuEnriched ext1
       
            ]

        xs_singletop = [
                                        3.36 , # ST_schannel
                                        80.95*0.322, # ST t channel antitop
                                        136.02*0.322, # ST t channel top
                                        35.6 ,  #singletop_tWantitop
                                        35.6 ,  #singletop_tWantitop ext1
                                        35.6 ,  #singletop_tW top
                                        35.6 ,  #singletop_tW top ext1
                                   
            ]
        nev_singletop = [
                                    1000000., # ST_schannel
                                    35038862., # ST t channel antitop
                                    67240808., # ST t channel top
                                      998276.,#ST_tW_antitop
                                      6846954., #ST_tW_antitop ext1
                                      992024., # ST tW top
                                      6733210., # ST tW top ext1
            ]


            
        instring = ''
        '''
        if options.highmass: endstring1 = '3526d13'# 'f271a16'
        else: endstring1 = '3526d13' # '186b8ea'

         # #'5db659f' #'605c442'
        endstring2 = 'Commit' + endstring1  # plotstack_Commite39827c
        endstring3 = 'Commit' + endstring1  # plotstack_Commite39827c

        endstrings = endstring2
        '''
        if options.highmass: endstring1 = 'June1' #'tau3208top110to250Matchedtry3'#'tau3208top110to250Matchedtry2' 
        else: endstring1 = 'tau3208' # '186b8ea'

         # #'5db659f' #'605c442'
        endstring2 = None 
        if  options.highmass: endstring2 = '_' + endstring1 
        else: endstring2 = '_outfile_' + endstring1  # plotstack_Commite39827c
        endstring3 = '_' + endstring1  # plotstack_Commite39827c

        endstrings = endstring2
        
        
        
        lepName0 = 'Electron'
        lepName1 = 'Muon'
        lep = None
        if isEl : 
            lep = str(lepName0)
            print("Data is Electrons!")
        if isMu : 
            lep = str(lepName1)
            print("Data is Muons!")
        if isBoth: 
            print("Data is for Electrons and Muons!")
            lep = 'Lepton'
        #   ____  _    _ _______ _____  _    _ _______   _____   ____   ____ _______ 
        #  / __ \| |  | |__   __|  __ \| |  | |__   __| |  __ \ / __ \ / __ \__   __|
        # | |  | | |  | |  | |  | |__) | |  | |  | |    | |__) | |  | | |  | | | |   
        # | |  | | |  | |  | |  |  ___/| |  | |  | |    |  _  /| |  | | |  | | | |   
        # | |__| | |__| |  | |  | |    | |__| |  | |    | | \ \| |__| | |__| | | |   
        #  \____/ \____/   |_|  |_|     \____/   |_|    |_|  \_\\____/ \____/  |_|   


        theOutfile = ROOT.TFile( "./plotstack"+ str(endstring2)+ '/plotstack_outfile_'+ str(options.hist)+'_' +lep+ str(endstrings)+ '.root' , "RECREATE") 

        theOutfile.cd()
        
        self.ptBs =  array.array('d', [200., 300., 400., 500., 800., 900., 1000.,1100.])
        self.nptBs = len(self.ptBs) - 1


        hpeak = ROOT.TH1F("hpeak", " ;p_{T} of AK8 SD jet (GeV); JMS ",  self.nptBs, self.ptBs) 
        hwidth = ROOT.TH1F("hwidth", " ;p_{T}  of AK8 SD jet  (GeV); JMR ", self.nptBs, self.ptBs)
        hNpassDataPre  = ROOT.TH1F("hNpassDataPre", " ;p_{T} of AK8 SD jet  (GeV); Integral(mean+- sigma) pre tag ", self.nptBs, self.ptBs)
        hNpassDataPost  = ROOT.TH1F("hNpassDataPost", " ;p_{T} of AK8 SD jet (GeV); # Integral(mean+- sigma) post tag ", self.nptBs, self.ptBs)
        hNpassMCPre  = ROOT.TH1F("hNpassMCPre", " ;p_{T} of AK8 SD jet (GeV); # Integral(mean+- sigma) pre tag ", self.nptBs, self.ptBs)
        hNpassMCPost  = ROOT.TH1F("hNpassMCPost", " ;p_{T} of AK8 SD jet  (GeV); # Integral(mean+- sigma) post tag ", self.nptBs, self.ptBs)
        hSFs  = ROOT.TH1F("hSFs", " ;p_{T} of SD subjet 0 (GeV); # data/mc [Integral(mean+- sigma) post/pre ", self.nptBs, self.ptBs)

        fitValues = [ ["Datamean", "Datasigma", "MCmean", "MCsigma"],[0.,0.,0.,0.],[0.,0.,0.,0.] ]
        fitDiffs = [ ["DataLowerBound", "DataHigherBound", "MCLowerBound", "MCHigherBound"],[0.,0.,0.,0.],[0.,0.,0.,0.] ]
        passPretagUncert = []
        passPretag = []

        highmass = False
        if options.highmass :
            instring = '_highmass'
            highmass = True
        else: endstring2 = ''
        
        #ttbarfile = ROOT.TFile('ttbar' + instring + '_outfile'+ endstring3 +'.root') #ttbarTuneCUETP8M2T4 or ttbarTuneCUETP8M1 currently the latter
        if not options.otherttbar :
            print('Opening file ttbarTTuneCUETP8M1' + instring +  endstring3 +'.root')
            ttbarfile = ROOT.TFile('ttbarTTuneCUETP8M1' + instring +  endstring3 +'.root') #ttbarTuneCUETP8M2T4 or ttbarTuneCUETP8M1 currently the latter
        if options.otherttbar : 
            self.otherttbar = options.otherttbar
            print('Opening file ttbarTTuneCUETP8M2T4' + instring +  endstring3 +'.root')

            ttbarfile = ROOT.TFile('ttbarTTuneCUETP8M2T4' + instring +  endstring3 +'.root')
        datafile = None
        datafile1 = None
        if isEl :  
            if highmass:
                datafile = ROOT.TFile('singleel' + instring +  endstring3 +'.root')
            else:
                datafile = ROOT.TFile('singleel' + instring +  endstring3 +'.root')
            print('Opening file singleel' + instring +  endstring3 +'.root')
        if isMu :  
            if highmass:
                datafile = ROOT.TFile('singlemu' + instring +  endstring3 +'.root')
            else:
                datafile = ROOT.TFile('singlemu' + instring +  endstring3 +'.root')            
            print('Opening file singlemu' + instring +  endstring3 +'.root')
        if isBoth:
            if  highmass:
                datafile = ROOT.TFile('singleel' + instring +  endstring3 +'.root')
                print('Opening file singleel' + instring +  endstring3 +'.root')
            else:
                datafile = ROOT.TFile('singleel' + instring +  endstring3 +'.root')  
                print('Opening file singleel' + instring +  endstring3 +'.root')          
            if options.highmass:
                datafile1 = ROOT.TFile('singlemu' + instring +  endstring3 +'.root')
                print('Opening file singlemu' + instring +  endstring3 +'.root')
            else:
                datafile1 = ROOT.TFile('singlemu' + instring +  endstring3 +'.root')
                print('Opening file singlemu' + instring +  endstring3 +'.root')
                
        wjetsfiles = [
            ROOT.TFile('WJetsToLNu_HT-100To200' + instring +  endstring2 +'.root'),
            ROOT.TFile('WJetsToLNu_HT-200To400' + instring +  endstring2 +'.root'),
            ROOT.TFile('WJetsToLNu_HT-400To600' + instring +  endstring2 +'.root'),
            ROOT.TFile('WJetsToLNu_HT-600To800' + instring +  endstring2 +'.root'),
            ROOT.TFile('WJetsToLNu_HT-800To1200' + instring +  endstring2 +'.root'),
            ROOT.TFile('WJetsToLNu_HT-1200To2500' + instring +  endstring2 +'.root'),
            ROOT.TFile('WJetsToLNu_HT-2500ToInf' + instring +  endstring2 +'.root'),
            ]


        wjets_colors = [ 
            ROOT.kWhite,ROOT.kRed - 9, ROOT.kRed - 7, ROOT.kRed - 4, ROOT.kRed, ROOT.kRed +1, ROOT.kRed +2   ]

        qcdfiles = [
            ROOT.TFile('QCD_Pt-470to600_MuEnriched' + instring +  endstring2 +'.root'), ### FIX THIS : Add other QCD files
            ROOT.TFile('QCD_Pt-470to600_MuEnriched_ext1' + instring +  endstring2 +'.root'), 

            ]
        '''
FIX THIS: Use all QCD samples from Mu enriched and EM enriched
hadd QCD_highmass_June1.root QCD_Pt-470to600_MuEnriched_ext1_highmass_June9.root  QCD_Pt-470to600_MuEnriched_highmass_June9.root

        '''
        singletopfiles = [
            ROOT.TFile('ST_sChannel' + instring +  endstring2 +'.root'),
            ROOT.TFile('ST_tChannel_antitop' + instring +  endstring2 +'.root'),
            ROOT.TFile('ST_tChannel_top' + instring +  endstring2 +'.root'),
            ROOT.TFile('ST_tW_antitop' + instring +  endstring2 +'.root'),
            ROOT.TFile('ST_tW_antitop_ext1' + instring +  endstring2 +'.root'),
            ROOT.TFile('ST_tW_top' + instring +  endstring2 +'.root'),
            ROOT.TFile('ST_tW_top_ext1' + instring +  endstring2 +'.root')             ]
            

        objs = []

        ### Set the maximum y axis increment with respect to the maximum y axis value
        y_max_scale = 1.618

        lepTag = None
        cutTag = None

        histName0 = options.hist 
            
            
        rangenum = 15
        if options.highmass: rangenum = 21  #14

        ### Runs in stage 0 data selection
        actualRunsList = [] 
        
        hdata1 = None
        hdata = None  
        ttbarMerged = None
        ttbarUnmerged = None
        ttbarMerged1 = None
        ttbarUnmerged1 = None
        ttbarMerged2 = None
        ttbarUnmerged2 = None
        histNameM1 =None
        histNameM2 = None
        histNameU1 = None
        histNameU2 = None
        
        for istage in range(rangenum) : 

            print("The Stage is : {}".format(istage))
            histName = None
            histName1 = None
            
            if isEl : 
                histName = options.hist + lepName0 + str(istage)
                if istage == 17:
                    histNameM1 = options.hist + lepName0 + str(istage+2)
                    histNameU1 = options.hist + lepName0 + str(istage+1)
                lepTag = 'Electron Data'
                print("Data is Electrons!")
            if isMu : 
                histName = options.hist + lepName1 + str(istage)
                if istage == 17:
                    histNameM1 = options.hist + lepName1 + str(istage+2)
                    histNameU1 = options.hist + lepName1 + str(istage+1)
                lepTag = 'Muon Data'
                print("Data is Muons!")


                
            if isBoth: 
                print("Data is for Electrons and Muons!")
                histName = options.hist + lepName0 + str(istage)
                histName1 = options.hist + lepName1 + str(istage)
                lepTag = 'Electron and Muon Data'
                if istage == 17:
                    histNameM1 = options.hist + lepName0 + str(istage+2)
                    histNameU1 = options.hist + lepName0 + str(istage+1)
                    histNameM2 = options.hist + lepName1 + str(istage+2)
                    histNameU2 = options.hist + lepName1 + str(istage+1)
                    ttbarMerged1 = ttbarfile.Get(histNameM1)
                    ttbarMerged1.SetFillColor(ROOT.kGreen + 2)
                    ttbarUnmerged1 = ttbarfile.Get(histNameU1)
                    ttbarUnmerged1.SetFillColor(ROOT.kGreen - 6)
                    
                    ttbarMerged2 = ttbarfile.Get(histNameM2)
                    ttbarMerged2.SetFillColor(ROOT.kGreen + 2)
                    ttbarUnmerged2 = ttbarfile.Get(histNameU2)
                    ttbarUnmerged2.SetFillColor(ROOT.kGreen - 6)
                    
                    ttbarMerged = ttbarMerged1.Clone("ttbarMerged")
                    print("{}: adding 2 merged ttbar histos".format(lepTag ))
                    ttbarMerged.Add(ttbarMerged2)
                    ttbarMerged.SetName("ttbarMerged"+histName)
                    ttbarMerged.SetFillColor(ROOT.kGreen + 2)
                    
                    ttbarUnmerged = ttbarUnmerged1.Clone("ttbarUnmerged")
                    print("{}: adding 2 unmerged ttbar histos".format(lepTag ))
                    ttbarUnmerged.Add(ttbarUnmerged2)
                    ttbarUnmerged.SetFillColor(ROOT.kGreen - 6)
                    ttbarUnmerged.SetName("ttbarUnmerged"+histName)

                    httbar = ttbarMerged.Clone("httbar"+histName)
                    httbar.Add(ttbarUnmerged)

                httbar = ttbarfile.Get(histName) 
                httbar1 = ttbarfile.Get(histName1)
                httbar1.Sumw2()
                print("{}: adding ttbar histos".format(lepTag ))
                httbar.Add(httbar1)
                httbar.SetFillColor(ROOT.kGreen + 2)
                    
            else:    
                if istage == 17:
                    ttbarMerged = ttbarfile.Get(histNameM1)
                    ttbarMerged.SetFillColor(ROOT.kGreen + 2)
                    ttbarUnmerged = ttbarfile.Get(histNameU1)
                    ttbarUnmerged.SetFillColor(ROOT.kGreen - 6)

            httbar.Sumw2()
            httbar.SetName("httbar"+histName )
            if istage == 17 and ttbarMerged != None and ttbarUnmerged != None :
                ttbarMerged.Scale( xs_ttbar / nev_ttbar* lumi )
                ttbarUnmerged.Scale(xs_ttbar / nev_ttbar* lumi )

            else:
                httbar.Scale( xs_ttbar / nev_ttbar* lumi ) 

            ROOT.gStyle.SetOptStat(000000)
            print ("Extracting histo titled {} from file {}".format(histName, datafile))
            hdata = datafile.Get(histName)
            
            if isBoth :
                hdata1 = datafile1.Get(histName1)
                hdata1.Sumw2()
                hdata1.SetTitle("")
                hdata1.GetXaxis().SetTitle("")
                print("{}: adding 2 data histos".format(lepTag ))
                hdata.Add(hdata1)
                hdata.SetName("hdata"+histName )
                print ("Extracting histo titled {} from file {}".format(histName1, datafile1))
            hdata.Sumw2()    
            hdata.SetMarkerStyle(20)
           
            hdata.SetTitle("")
            hdata.SetTitleOffset(1.4)
            hdata.GetXaxis().SetTitle("")
            hdata.SetName("hdata"+histName )

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
                print("Opening file : {}".format(wjetsfiles[iwjet]))
                htemp = wjetsfiles[iwjet].Get(histName)
                if isBoth: 
                    htemp1 = wjetsfiles[iwjet].Get(histName1)
                    htemp1.Sumw2()
                    htemp.Add(htemp1)        
                htemp.Scale( 1.2* xs_wjets[iwjet] / nev_wjets[iwjet] * lumi )
                hwjets_list.append( htemp )
                htemp.SetFillColor( wjets_colors[iwjet] )
                if iwjet == 0 :
                    hwjets = htemp.Clone('hwjets')
                else :
                    hwjets.Add( htemp )
                hwjets_stack.Add( htemp )
            #hwjets_stack.Draw("hist")
            hwjets.SetName("hwjets"+histName )


            hwjets.SetFillColor( ROOT.kRed )


            hqcd_list = []
            hqcd = None
            hqcd_stack = ROOT.THStack("hqcd_stack", "hqcd_stack")

            for iqcd in range(len(qcdfiles)) :
                htemp = qcdfiles[iqcd].Get(histName)
                if isBoth: 
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
            hqcd.SetName("hqcd"+histName )


            hsingletop_list = []
            hsingletop = None
            hsingletop_stack = ROOT.THStack("hsingletop_stack", "hsingletop_stack")

            for isingletop in range(len(singletopfiles)) :
                htemp = singletopfiles[isingletop].Get(histName)
                if isBoth:
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
            hsingletop.SetName("hsingletop"+histName )


            hsingletop.SetFillColor( ROOT.kMagenta )
                       
                   
            hqcd.Rebin(10)
            hsingletop.Rebin(10)
            hwjets.Rebin(10)
            httbar.Rebin(10)
            if ttbarUnmerged != None : ttbarUnmerged.Rebin(10)
            if ttbarMerged != None : ttbarMerged.Rebin(10)
            if options.hist != "RunNumberHist" :
                hdata.Rebin(10)
            hdata2 = hdata.Clone('hdata2')
            
            hstack = ROOT.THStack("bkgs" + str(istage), "bkgs" + str(istage))
            hstack.Add( hqcd )
            hstack.Add( hsingletop )
            hstack.Add( hwjets )
            if istage == 17:
                hstack.Add(ttbarUnmerged)
                hstack.Add(ttbarMerged )
            else:    
                hstack.Add( httbar )
            hstack.SetName("hstack" +histName )


            hmc = hqcd.Clone('hmc'+ str(istage))
            hmc.Add(hsingletop )
            hmc.Add( hwjets )
            if istage == 17:
                hmc.Add(ttbarMerged)
                hmc.Add(ttbarUnmerged)
            else:    
                hmc.Add( httbar )
            hmc.SetName("hmc" +histName )

            hmc2 = hmc.Clone('hmc2')


            if options.highmass:    
                cutTag = CutsPerStage_Type1[str(istage)][1]    
            else: cutTag =  CutsPerStage_Type2[str(istage)][1]
            
            print("passPretag {}".format(passPretag))
            if istage != 17:
                ttbarUnmerged =  httbar
            zplot = APlot(istage , y_max_scale, hdata, hdata2, hmc,hmc2 , hstack, ttbarUnmerged, ttbarMerged, hwjets, hsingletop, hqcd, str(histName0), lumi/1000., lepTag, cutTag, options.fixFit, expectedRunsHist, self.otherttbar, fitValues, fitDiffs, passPretag, passPretagUncert, type2 )
   
            print("isWmass {} isTopmass {} istage {} type2 {} type1 {} ".format(isWmass,isTopmass, istage ,type2, type1))
            if ( isWmass and istage == 14 and type2) or ( isWmass and istage == 17 and type1) or ( isTopmass and istage == 14 and type1 ):
                hpeak = zplot.GetJMSHist()
                hwidth = zplot.GetJMRHist()
                hSFs = zplot.GetSFHist()

                hNpassDataPost = zplot.GetDataPostHist()
                hNpassDataPost.SetName("hNpassDataPost" +histName )

                hNpassMCPost = zplot.GetMCPostHist()
                hNpassMCPost.SetName("hNpassMCPost" +histName )

            if ( isWmass and istage == 13 and type2) or  ( isWmass and istage == 15 and type1) or ( isTopmass and istage == 13 and type1):
                hNpassDataPre = zplot.GetDataPreHist()
                hNpassDataPre.SetName("hNpassDataPre" +histName )

                hNpassMCPre = zplot.GetMCPreHist()
                hNpassMCPre.SetName("hNpassMCPre" +histName )

                fitValues = zplot.GetFitValues()
                print("fitValues {}".format(fitValues))
                fitDiffs = zplot.GetFitDiffs()
                print("fitDiffs {}".format(fitDiffs))

                passPretagUncert = zplot.GetpassPretagUncert()
                print("passPretagUncert {}".format(passPretagUncert))

                passPretag = zplot.GetpassPretag()
                print("passPretag {}".format(passPretag))


            if istage >= 11:    
                zplot.ResetHists()
            theCanvas = zplot.GetPlotCanvas()
            
            theCanvas.Print("./plotstack"+ str(endstring3)+ "/" + histName0 + lep + str(istage)  + instring + endstring2+tune+".pdf", "pdf")
            theCanvas.Print("./plotstack"+ str(endstring3)+ "/" + histName0 + lep + str(istage)  + instring + endstring2+tune+".png", "png")

            theOutfile.cd()
                            
            objs.append( [hdata, httbar, hwjets, hqcd, hsingletop, hmc, theCanvas, hstack, expectedRunsList, actualRunsList,  hNpassDataPre, hNpassMCPre, hpeak, hwidth, hNpassDataPost, hNpassMCPost ] )
            keepers = [hdata, httbar, hwjets, hqcd, hsingletop, hmc, theCanvas, hstack,  hNpassDataPre, hNpassMCPre , hpeak, hwidth, hNpassDataPost, hNpassMCPost, hSFs]
            keepersNames = ['hdata', 'httbar', 'hwjets', 'hqcd', 'hsingletop', 'hmc', 'theCanvas', 'hstack','hNpassDataPre', 'hNpassMCPre' , 'hpeak', 'hwidth', 'hNpassDataPost', 'hNpassMCPost' , 'hSFs']
            lenobj = 1.
            if ( isWmass and istage <= 15 ) or ( isTopmass and istage <= 13 ) :
                lenobj = len(keepers) - 5
            if ( isWmass and istage == 15 ) or ( isTopmass and istage == 13 ) :
                lenobj = len(keepers) - 3
            if ( isWmass and istage == 17 ) or ( isTopmass and istage == 14 ) :
                lenobj = len(keepers) 
            if ( isWmass and istage > 17 ) or ( isTopmass and istage > 14 ) :
                lenobj = len(keepers) - 5
            for i in range(0, int(lenobj)):
                print("obj {} is being saved to the root outfile".format(keepers[i]))
                #keepers[i].SetName(keepersNames[i] + str(istage))
                if ( isWmass and istage > 16 ) or ( isTopmass and istage > 14 ) and i >= 8  :
                    continue
                keepers[i].SetName(keepersNames[i] +histName)
                keepers[i].Write(keepersNames[i] +histName, ROOT.TObject.kWriteDelete)
            print("theOutfile is {}".format(theOutfile))
            
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
            print("       *      -0-   *           .       ^   ")
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
            
        theOutfile.Write()
        theOutfile.Close()

if __name__ == "__main__" :
    plotstack(sys.argv)

