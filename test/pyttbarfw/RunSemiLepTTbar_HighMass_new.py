
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
from optparse import OptionParser

from B2GTTreeSemiLep import B2GTTreeSemiLep
from B2GTTreeSemiLepOut import B2GTTreeSemiLepOut

import B2GSelectSemiLepTTbar_Type1, B2GSelectSemiLepTTbar_Iso2D

import ROOT


class RunSemiLepTTbar_HighMass() :
    '''
    Driver class for Semileptonic TTbar analyses.
    This will use "Selection" classes (the first below is B2GSelectSemiLepTTbar)
    that return a bitset of cuts at different phases. This class can then
    make plots at those stages of selection.

    The factorization allows different drivers to use the same selection classes
    with the same bitsets, or to use different selections to use the same histogramming
    functionality.


    '''
    

    def __init__(self, argv ) : 

        ###
        ### Get the command line options
        ###
        parser = OptionParser()


        parser.add_option('--infile', type='string', action='store',
                          dest='infile',
                          default = '',
                          help='Input file string')

        parser.add_option('--outfile', type='string', action='store',
                          dest='outfile',
                          default = '',
                          help='Output file string')

        parser.add_option('--tau21Cut', type='float', action='store',
                          dest='tau21Cut',
                          default = 0.55,
                          help='Tau 21 cut')

        parser.add_option('--tau32Cut', type='float', action='store',
                          dest='tau32Cut',
                          default = 0.8,
                          help='Tau 32 cut')
        
        parser.add_option('--bdiscmin', type='float', action='store',
                          dest='bdiscmin',
                          default = 0.8484, ### Medium WP CSVv2  https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation80XReReco
                          help='B discriminator cut')

        parser.add_option('--maxevents', type='int', action='store',
                          default=None,
                          dest='maxevents',
                          help='Maximum number of events')

        parser.add_option('--ignoreTrig', action='store_true',
                          dest='ignoreTrig',
                          default = False,
                          help='Ignore the trigger?')

        parser.add_option('--v5', action='store_true',
                          default=True,
                          dest='v5',
                          help='Do you want to use v5 ttrees?')        

        parser.add_option('--verbose', action='store_true',
                          default=False,
                          dest='verbose',
                          help='Do you want to print values of key variables?')

        parser.add_option('--verboseW', action='store_true',
                          default=False,
                          dest='verboseW',
                          help='Do you want to print values of key W jet variables?')

        (options, args) = parser.parse_args(argv)
        argv = []

        #self.startTime = time.time()
        self.infile = options.infile
        self.outfile = ROOT.TFile(options.outfile, "RECREATE")
        self.options = options
        self.verbose = options.verbose
        self.verboseW = options.verboseW

        self.infile = options.infile
        self.maxevents = options.maxevents

        
        ### Create the tree class. This will make simple class members for each
        ### of the branches that we want to read from the Tree to save time.
        ### Also saved are some nontrivial variables that involve combinations
        ### of things from the tree
        if options.v5 : from B2GTTreeSemiLepV5 import B2GTTreeSemiLep

        self.treeobj = B2GTTreeSemiLep( options )
        self.TTreeSemiLeptSkim = self.treeobj.tree.CloneTree(0)
        self.TTreeSemiLeptSkim.SetName("TTreeSemiLeptSkim") 
        self.TTreeSemiLeptSkim.SetDirectory(self.outfile)
        self.TTreeSemiLept  = self.TTreeSemiLeptSkim.GetTree()        

        self.TTreeWeights = ROOT.TTree("TTreeWeights", "TTreeWeights")
        self.TTreeWeights.SetName("TTreeWeights") 
        self.TTreeWeights.SetDirectory(self.outfile)
        
        self.theCount = 0
        self.lumiWeight = None
        self.theWeight = None
        self.weights = {
            'SemiLeptLumiweight':'f',
            'SemiLeptAllotherweights':'f',
          }
       

        self.weightVal = -3.14159

        self.SemiLeptLumiweight = (array.array( 'f', [self.weightVal] ))
        self.SemiLeptAllotherweights = (array.array( 'f', [self.weightVal] ))
        self.SubjetTau21 = (array.array( 'f', [self.weightVal] ))

        self.TTreeWeights.Branch('SemiLeptLumiweight'  , self.SemiLeptLumiweight     ,  'SemiLeptLumiweight/F'      )
        self.TTreeWeights.Branch( 'SemiLeptAllotherweights' ,  self.SemiLeptAllotherweights     ,  'SemiLeptAllotherweights/F'      )
        self.TTreeWeights.Branch( 'SubjetTau21' ,  self.SubjetTau21    ,  'SubjetTau21/F'      )
        
        print 'Getting entries'
        entries = self.treeobj.tree.GetEntries()              
        if options.maxevents == None or options.maxevents < 0 :
            self.eventsToRun = entries      
        else :      
            self.eventsToRun = min( options.maxevents, entries )


        ### Here is the semileptonic ttbar selection for top jets
        self.lepSelection = B2GSelectSemiLepTTbar_Iso2D.B2GSelectSemiLepTTbar_Iso2D( options, self.treeobj )
        self.hadSelection = B2GSelectSemiLepTTbar_Type1.B2GSelectSemiLepTTbar_Type1( options, self.treeobj, self.lepSelection )


        self.nstages = self.lepSelection.nstages + self.hadSelection.nstages
        self.nlep = 2 # Electron and Muon

        ### Book histograms
        self.book()

    '''
    Coarse flow control. Loops over events, reads, and fills histograms. 
    Try not to modify anything here if you add something.
    Add whatever you can in "book" and "fill". If you need to add something
    complicated, cache it as a member variable in the Selector class you're interested
    in, and just make simple plots here. 
    '''
    def run(self):
        
        print 'processing ', self.eventsToRun, ' events'

        for jentry in xrange( self.eventsToRun ):
            if jentry % 100000 == 0 :
                print 'processing ' + str(jentry)
            # get the next tree in the chain and verify            
            ientry = self.treeobj.tree.GetEntry( jentry )        
            # Select events, get the bitset corresponding to the cut flow
            passbitsLep = self.lepSelection.select()
            passbitsHad = self.hadSelection.select()
            passbits = passbitsLep + passbitsHad
            # For each stage in the cut flow, make plots
            for ipassbit in xrange( len(passbits) ) :
                if passbits[ipassbit] :
                    self.fill( ipassbit )

        # Wrap it up. 
        print 'Finished looping'
        self.close()
        print 'Closed'



        
    def book( self ) :

        a = self.lepSelection
        b = self.hadSelection 
                
        self.outfile.cd()
        
        
        '''
        Book histograms, one for each stage of the selection. 
        '''
        ### Run number - Use to check luminosity of data samples
        self.RunNumber_Hist = []
        ### Weights histogram with total weight applied to the event when filling histograms
        self.Weight_Hist = []      
                
        self.Lepton_Pt_Hist = []
        self.Lepton_Eta_Hist = []

        self.MET_Pt_Hist = []
        self.LepW_Pt_Hist = []
        self.Iso2D_Hist = []

        self.AK4_Bdisc_Hist = []        
        self.AK4_Pt_Hist = []
        self.AK4_Eta_Hist = []

        self.AK8_Pt_Hist = []
        self.AK8_HT_Hist = []
        self.AK8_SDPt_Hist = [] 
        self.AK8_PUPPISDPt_Hist = [] 
        self.AK8_PUPPIPt_Hist = [] 
          
        self.AK8_puppitau32_Hist = []

        self.AK8_Eta_Hist = []
        
        self.AK8_Mass_Hist = []            ### ungroomed uncorrected Fat Jet mass
        self.AK8_SDMass_Hist = []
        self.AK8_SDMassRaw_Hist = []                        ### Soft Drop jet mass without CHS or PUPPI
        self.AK8_PUPPISDMass_Hist = []
        self.AK8_CHSSDMass_Hist = []

        self.AK8_SDRhoRatio_Hist = []

        self.WcandSJ_Pt_Hist = []
        self.WcandSJ_Mass_Hist = []     
        self.WcandSJ_PUPPItau21_Hist = [] 
        self.WcandSJ_Eta_Hist = []


        self.BcandSJ_Pt_Hist = []
        self.BcandSJ_Mass_Hist = []
        self.BcandSJ_PUPPItau21_Hist = []

        self.lepNames = ['Electron', 'Muon' ]
        ### Create histos for type 1 selection binned by pt of AK8_

        self.AK8_Mass_AK8PtBinned_HistList = [[], [] ,[], [] , []]
        self.AK8_SDMass_AK8PtBinned_HistList  = [[], [] ,[], [] , []]
        self.WcandSJ_SDMass_AK8PtBinned_HistList = [[], [] ,[], [] , []]
        self.BcandSJ_SDMass_AK8PtBinned_HistList = [[], [] ,[], [] , []]
        ### Create histos for type 1 selection binned by pt of leading SD subjet

        ### WORKING HERE to correct naming scheme and improve overall script Aug. 6, 2017
        self.AK8_Mass_WcandSJPtBinned_HistList = [[], [] ,[], [] , []]
        self.AK8_SDMass_WcandSJPtBinned_HistList = [[], [] ,[], [] , []]
        self.WcandSJ_SDMass_WcandSJPtBinned_HistList = [[], [] ,[], [] , []]
        self.WcandSJ_SDMass_WcandSJPtBinned_HistListl2l3 = [[], [] ,[], [] , []]
        self.BcandSJ_SDMass_WcandSJPtBinned_HistList = [[], [] ,[], [] , []]       
        ### Alternate binning scheme
        ''' 
        self.AK8_Mass_WcandSJPtBinned_HistListb = [[], [] ,[], [] , []]
        self.AK8_SDMass_WcandSJPtBinned_HistListb = [[], [] ,[], [] , []]
        self.WcandSJ_SDMass_WcandSJPtBinned_HistListb = [[], [] ,[], [] , []]
        self.WcandSJ_SDMass_WcandSJPtBinned_HistListbl2l3 = [[], [] ,[], [] , []]
        self.BcandSJ_SDMass_WcandSJPtBinned_HistListb = [[], [] ,[], [] , []]  
        '''
        ### List of all histograms
        self.hists = []
        
        for ilep in xrange(self.nlep) :   
            self.RunNumber_Hist.append( [] )
            self.Weight_Hist.append( [] ) 
            self.AK8_Pt_Hist.append([])       
            self.AK8_HT_Hist.append( [] )
            self.AK8_SDPt_Hist.append( [] )
            self.AK8_PUPPISDPt_Hist.append([])
            self.AK8_PUPPIPt_Hist.append( [] )
          
            self.WcandSJ_Pt_Hist.append( [])
            self.WcandSJ_Eta_Hist.append( [])
            self.BcandSJ_Pt_Hist.append( [])
            self.WcandSJ_Mass_Hist.append( [])
            self.BcandSJ_Mass_Hist.append( [])
        
            self.AK8_Eta_Hist.append([])      
            self.WcandSJ_PUPPItau21_Hist.append([])
            self.BcandSJ_PUPPItau21_Hist.append([])
          
            self.AK8_puppitau32_Hist.append([])
            

            self.AK8_Mass_Hist.append( [] )
            self.AK8_SDMassRaw_Hist.append( [] )                      
            self.AK8_PUPPISDMass_Hist.append( [] )
            self.AK8_CHSSDMass_Hist.append( [] )
            self.AK8_SDMass_Hist.append( [] )
            self.AK8_SDRhoRatio_Hist.append( [] )
            self.AK8_SDMassSJ0_Hist.append( [] )

            self.Lepton_Pt_Hist.append( [] )
            self.Lepton_Eta_Hist.append( [] )

            self.MET_Pt_Hist.append( [] )
            self.LepW_Pt_Hist.append([] )
            self.Iso2D_Hist.append ( [] )

            self.AK4_Bdisc_Hist.append( [] )
            self.AK4_Pt_Hist.append( [] )
            self.AK4_Eta_Hist.append( [] )

            for iptbin, ptbin in enumerate(b.ak8Jet_Ptbins) :
                if iptbin < 5:
                    #if self.verbose: print"self.AK8_Mass_AK8PtBinnedHistList {} of length {}".format(self.AK8_Mass_AK8PtBinnedHistList, len(self.AK8_Mass_AK8PtBinnedHistList))
                    self.AK8_Mass_AK8PtBinned_HistList[iptbin].append( [] )
                    self.AK8_SDMass_AK8PtBinned_HistList[iptbin].append( [] )
                    self.WcandSJ_SDMass_AK8PtBinned_HistList[iptbin].append( [] )
                    self.BcandSJ_SDMass_AK8PtBinned_HistList[iptbin].append( [] )
                    
                    self.AK8_Mass_WcandSJPtBinned_HistList[iptbin].append( [] )
                    self.AK8_SDMass_WcandSJPtBinned_HistList[iptbin].append( [] )
                    self.WcandSJ_SDMass_WcandSJPtBinned_HistList[iptbin].append( [] )
                    self.WcandSJ_SDMass_WcandSJPtBinned_HistListl2l3[iptbin].append( [] )
                    self.BcandSJ_SDMass_WcandSJPtBinned_HistList[iptbin].append( [] )  
            '''                          
            for iptbin, ptbin in enumerate(b.ak8Jet_Ptbinsb) :
                if iptbin < 5:
                    self.AK8_Mass_WcandSJPtBinned_HistListb[iptbin].append( [] )
                    self.AK8_SDMass_AK8PtBinnedHistList 0b[iptbin].append( [] )
                    self.WcandSJ_SDMass_WcandSJPtBinned_HistListb[iptbin].append( [] )
                    self.WcandSJ_SDMass_WcandSJPtBinned_HistListbl2l3[iptbin].append( [] )
                    self.BcandSJ_SDMass_WcandSJPtBinned_HistListb[iptbin].append( [] ) 
            '''        
            for ival in xrange(self.nstages):
                self.RunNumber_Hist[ilep].append( ROOT.TH1F("RunNumber_Hist" + self.lepNames[ilep] + str(ival) , "Run Number for lepton "+self.lepNames[ilep] + str(ival), 286591, 0, 286591) )
                self.Weight_Hist[ilep].append( ROOT.TH1F("Weight_Hist" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, -2, 2) )
                self.AK8_Pt_Hist[ilep].append( ROOT.TH1F("AK8_Pt_Hist" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8_SDMassRaw_Hist[ilep].append( ROOT.TH1F("AK8_SDMassRaw_Hist" +  self.lepNames[ilep] + str(ival), "AK8_ Soft Drop Jet p_{T} RAW, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8_PUPPISDMass_Hist[ilep].append( ROOT.TH1F("AK8_PUPPISDMass_Hist" +  self.lepNames[ilep] + str(ival), "AK8_ Soft Drop Jet p_{T} PUPPI, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8_CHSSDMass_Hist[ilep].append( ROOT.TH1F("AK8_CHSSDMass_Hist" +  self.lepNames[ilep] + str(ival), "AK8_ Soft Drop Jet p_{T} CHS, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8_HT_Hist[ilep].append( ROOT.TH1F("AK8_HT_Hist" +  self.lepNames[ilep] + str(ival), "Jet H_{T}, Stage " + self.lepNames[ilep] + str(ival), 4000, 0, 4000) )
                self.AK8_SDPt_Hist[ilep].append( ROOT.TH1F("AK8_SDPt_Hist" +  self.lepNames[ilep] + str(ival), "Jet SD p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8_PUPPISDPt_Hist[ilep].append( ROOT.TH1F("AK8_PUPPISDPt_Hist" +  self.lepNames[ilep] + str(ival), "Jet PUPPI SD p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8_PUPPIPt_Hist[ilep].append( ROOT.TH1F("AK8_PUPPIPt_Hist" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )

                self.WcandSJ_Pt_Hist[ilep].append( ROOT.TH1F("WcandSJ_Pt_Hist" +  self.lepNames[ilep] + str(ival), "W Subjet  P_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.BcandSJ_Pt_Hist[ilep].append( ROOT.TH1F("BcandSJ_Pt_Hist" +  self.lepNames[ilep] + str(ival), "B Subjet P_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
              
                self.WcandSJ_Eta_Hist[ilep].append( ROOT.TH1F("WcandSJ_Eta_Hist" +  self.lepNames[ilep] + str(ival), "W Subjet #eta, Stage " + self.lepNames[ilep] + str(ival), 1000, -2.5, 2.5) )
                self.AK8_Eta_Hist[ilep].append( ROOT.TH1F("AK8_Eta_Hist" +  self.lepNames[ilep] + str(ival), "Jet #eta, Stage " + self.lepNames[ilep] + str(ival), 1000, -2.5, 2.5) )
                self.WcandSJ_PUPPItau21_Hist[ilep].append( ROOT.TH1F("WcandSJ_PUPPItau21_Hist" +  self.lepNames[ilep] + str(ival), "W Subjet #tau_{21}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0., 1.) )
                self.BcandSJ_PUPPItau21_Hist[ilep].append( ROOT.TH1F("BcandSJ_PUPPItau21_Hist" +  self.lepNames[ilep] + str(ival), "B Subjet #tau_{21}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0., 1.) )


                self.AK8_puppitau32_Hist[ilep].append( ROOT.TH1F("AK8_puppitau32_Hist" +  self.lepNames[ilep] + str(ival), "Jet #tau_{32}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0., 1.) )


                self.WcandSJ_Mass_Hist[ilep].append( ROOT.TH1F("WcandSJ_Mass_Hist" +  self.lepNames[ilep] + str(ival), "W Subjet Mass (GeV), Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                self.BcandSJ_Mass_Hist[ilep].append( ROOT.TH1F("BcandSJ_Mass_Hist" +  self.lepNames[ilep] + str(ival), "B Subjet Mass (GeV) , Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                self.AK8_Mass_Hist[ilep].append( ROOT.TH1F("AK8_Mass_Hist" +  self.lepNames[ilep] + str(ival), "Jet Mass (GeV) , Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )


                self.AK8_SDMass_Hist[ilep].append( ROOT.TH1F("AK8_SDMass_Hist" +  self.lepNames[ilep] + str(ival), "Jet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                self.AK8_SDRhoRatio_Hist[ilep].append( ROOT.TH1F("AK8_SDRhoRatio_Hist" +  self.lepNames[ilep] + str(ival), "SD Rho Ratio, Stage " + self.lepNames[ilep] + str(ival), 1000, 0., 1.) )
                self.AK8_SDMassSJ0_Hist[ilep].append( ROOT.TH1F("AK8_SDMassSJ0_Hist" +  self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )

                self.Lepton_Pt_Hist[ilep].append( ROOT.TH1F("Lepton_Pt_Hist" +  self.lepNames[ilep] + str(ival), "Lepton p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.Lepton_Eta_Hist[ilep].append( ROOT.TH1F("Lepton_Eta_Hist" +  self.lepNames[ilep] + str(ival), "Lepton #eta, Stage " + self.lepNames[ilep] + str(ival), 1000, -2.5, 2.5) )

                self.MET_Pt_Hist[ilep].append( ROOT.TH1F("MET_Pt_Hist" +  self.lepNames[ilep] + str(ival), "Missing p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.LepW_Pt_Hist[ilep].append( ROOT.TH1F("LepW_Pt_Hist" +  self.lepNames[ilep] + str(ival), "Lepton p_{T} + Missing p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.Iso2D_Hist[ilep].append ( ROOT.TH2F("Iso2D_Hist" +  self.lepNames[ilep] + str(ival), "Lepton 2D isolation (#Delta R vs p_{T}^{REL} ), Stage " + self.lepNames[ilep] + str(ival), 25, 0, 500, 25, 0, 1) )
                self.AK4_Bdisc_Hist[ilep].append( ROOT.TH1F("AK4_Bdisc_Hist" +  self.lepNames[ilep] + str(ival), "CSVv2 B disc , Stage " + self.lepNames[ilep] + str(ival), 1000, 0., 1.) )
                self.AK4_Pt_Hist[ilep].append( ROOT.TH1F("AK4_Pt_Hist" +  self.lepNames[ilep] + str(ival), "AK4 p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK4_Eta_Hist[ilep].append( ROOT.TH1F("AK4_Eta_Hist" +  self.lepNames[ilep] + str(ival), "AK4 #eta, Stage " + self.lepNames[ilep] + str(ival), 1000, -2.5, 2.5) )

                for iptbin, ptbin in enumerate(b.ak8Jet_Ptbins) :
                    if iptbin < 4:
                        self.AK8_Mass_AK8PtBinned_HistList[iptbin][ilep].append( ROOT.TH1F("AK8_MPt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Jet Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8_SDMass_AK8PtBinned_HistList [iptbin][ilep].append( ROOT.TH1F("AK8_SDMassPt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Jet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.WcandSJ_SDMass_AK8PtBinned_HistList[iptbin][ilep].append( ROOT.TH1F("AK8_SDMassSJ0Pt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.BcandSJ_SDMass_AK8PtBinned_HistList[iptbin][ilep].append( ROOT.TH1F("AK8_SDMassSJ1Pt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Sub-Leading Subjet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
     
                        self.AK8_Mass_WcandSJPtBinned_HistList[iptbin][ilep].append( ROOT.TH1F("0AK8_MPt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Jet Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8_SDMass_WcandSJPtBinned_HistList 0[iptbin][ilep].append( ROOT.TH1F("0AK8_SDMassPt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Jet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.WcandSJ_SDMass_WcandSJPtBinned_HistList[iptbin][ilep].append( ROOT.TH1F("0AK8_SDMassSJ0Pt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.WcandSJ_SDMass_WcandSJPtBinned_HistListl2l3[iptbin][ilep].append( ROOT.TH1F("l2l30AK8_SDMassSJ0Pt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbinsb[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass+ L2L3 corr, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.BcandSJ_SDMass_WcandSJPtBinned_HistList[iptbin][ilep].append( ROOT.TH1F("0AK8_SDMassSJ1Pt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Sub-Leading Subjet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                '''
                for iptbin, ptbin in enumerate(b.ak8Jet_Ptbinsb) :
                    if iptbin < 4:

                        self.AK8_Mass_WcandSJPtBinned_HistListb[iptbin][ilep].append( ROOT.TH1F("b0AK8_MPt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbinsb[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Jet Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8_SDMass_AK8PtBinnedHistList 0b[iptbin][ilep].append( ROOT.TH1F("b0AK8_SDMassPt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbinsb[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Jet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.WcandSJ_SDMass_WcandSJPtBinned_HistListb[iptbin][ilep].append( ROOT.TH1F("b0AK8_SDMassSJ0Pt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbinsb[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass + PUPPI corr, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.WcandSJ_SDMass_WcandSJPtBinned_HistListbl2l3[iptbin][ilep].append( ROOT.TH1F("l2l3b0AK8_SDMassSJ0Pt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbinsb[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass+ L2L3 corr, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.BcandSJ_SDMass_WcandSJPtBinned_HistListb[iptbin][ilep].append( ROOT.TH1F("b0AK8_SDMassSJ1Pt%sTo%s_Hist"%(ptbin, b.ak8Jet_Ptbinsb[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Sub-Leading Subjet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                '''


    def fill( self, index ) :
        '''
        Fill the histograms we're interested in. If you're doing something complicated, make a
        member variable in the Selector class to cache the variable and just fill here. 
        '''
        a = self.lepSelection
        b = self.hadSelection 
        ilep = a.tree.LeptonIsMu[0]
        if ilep == 1:         
            if self.verbose: print 'Muon Candidate'
        if ilep== 0:
            if self.verbose: print 'Electron Candidate'

        ### Define the weights used for histo filling
        self.theWeight = a.theWeight

        #self.theWeight = 1.

        ### B tag SF
        if index >= 12: 
            self.theWeight =  a.EventWeight * a.PUWeight * a.CutIDScaleFIs * a.recoSFIs * a.TriggEffIs * a.MuHighPtScaleFIs * a.HEEPSFIs * a.BtagWeight
            if self.verbose : print "theWeight for stage {0:} is : {1:2.4f} = eventWeight {2:2.2f} * self.PUWeight{3:2.2f} * self.CutIDScaleFIs {4:2.2f} * self.recoSFIs  {5:2.2f} * self.TriggEffIs {6:2.3f} *  self.MuHighPtScaleFIs {7:2.3f} * self.HEEPSFIs {8:2.3f} * BtagWeight {9:2.3f}".format( 0, a.theWeight, a.EventWeight , a.PUWeight , a.CutIDScaleFIs, a.recoSFIs , a.TriggEffIs ,  a.MuHighPtScaleFIs , a.HEEPSFIs, a.BtagWeight)

        if index == 17: 
            self.theWeight =  a.EventWeight * a.PUWeight * a.CutIDScaleFIs * a.recoSFIs * a.TriggEffIs * a.MuHighPtScaleFIs * a.HEEPSFIs * a.BtagWeight * a.BtagWeightsubjet
            if self.verbose : print "theWeight for stage {0:} is : {1:2.4f} = eventWeight {2:2.2f} * self.PUWeight{3:2.2f} * self.CutIDScaleFIs {4:2.2f} * self.recoSFIs  {5:2.2f} * self.TriggEffIs {6:2.3f} *  self.MuHighPtScaleFIs {7:2.3f} * self.HEEPSFIs {8:2.3f} * BtagWeight {9:2.3f} *  a.BtagWeightsubjet {10:2.3f}".format( 0, a.theWeight, a.EventWeight , a.PUWeight , a.CutIDScaleFIs, a.recoSFIs , a.TriggEffIs ,  a.MuHighPtScaleFIs , a.HEEPSFIs, a.BtagWeight,  a.BtagWeightsubjet)

        if self.verbose: print"a.RunNumber: {}".format( a.RunNumber)
        if a.RunNumber > 0. :
            self.RunNumber_Hist[ilep][index].Fill(a.RunNumber)
        if self.theWeight > -1. :
            self.Weight_Hist[ilep][index].Fill(self.theWeight)
            
        if b.ak8JetP4 != None :
            self.AK8_Pt_Hist[ilep][index].Fill( b.ak8JetP4.Perp()* b.PtSmear   , self.theWeight )  ### TO-DO : Implement Pt smear in hadselection and replace 1.000 with b.PtSmear
            self.AK8_HT_Hist[ilep][index].Fill( b.ak8JetHT  , self.theWeight )
    
        if b.ak8SDJetP4 != None :
            self.AK8_SDPt_Hist[ilep][index].Fill( b.ak8SDJetP4.Perp() * b.PtSmear  , self.theWeight )
            self.AK8_SDMass_Hist[ilep][index].Fill( b.ak8PUPPISD_m_Pcorr  , self.theWeight )
            self.AK8_SDMassRaw_Hist[ilep][index].Fill( b.akSDRaw_m  , self.theWeight )
            self.AK8_PUPPISDMass_Hist[ilep][index].Fill( b.ak8PUPPISD_m , self.theWeight )
            #self.AK8_CHSSDMass_Hist[ilep][index].Fill( b.akCHSSD_m  , self.theWeight )

        if b.ak8PUPPIJetP4 != None :
            self.AK8_PUPPIPt_Hist[ilep][index].Fill( b.ak8PUPPIJetP4.Perp() * b.PUPPIPtSmear  , self.theWeight )
            self.AK8_Eta_Hist[ilep][index].Fill( b.ak8PUPPIJetP4.Eta()  , self.theWeight )
            self.WcandSJ_PUPPItau21_Hist[ilep][index].Fill( b.wcandtau21  , self.theWeight ) ### actually tau21 of subjet, misleading name
            self.AK8_puppitau32_Hist[ilep][index].Fill( b.puppitau32  , self.theWeight )
            if b.ak8PUPPI_m_Pcorr != None: 
                self.AK8_Mass_Hist[ilep][index].Fill( b.ak8PUPPI_m_Pcorr , self.theWeight )
            if b.ak8PUPPISDJetP4 != None :
                if b.ak8PUPPIJetP4  != None and b.SDptPUPPIpt != None :
                    self.AK8_PUPPISDPtResponse[ilep][index].Fill( b.SDptPUPPIpt, b.ak8PUPPIJetP4.Perp()* b.PUPPIPtSmear  )# * b.PUPPIPtSmear )  

        if  b.SDRhoRatio  != None :
            self.AK8_SDRhoRatio_Hist[ilep][index].Fill(b.SDRhoRatio  , self.theWeight ) 


        if b.ak8PUPPISDJetP4 != None :
            self.AK8_PUPPISDPt_Hist[ilep][index].Fill( b.ak8PUPPISDJetP4.Perp() * b.PUPPIPtSmear  , self.theWeight )
            self.WcandSJ_Pt_Hist[ilep][index].Fill( b.wcandp4.Perp() * b.PUPPIPtSmear  , self.theWeight )
            self.AK8_SDMassSJ0_Hist[ilep][index].Fill( b.wcandp4.M()  , self.theWeight )


            # Filling jet mass histos binned by pt of the leading SD subjet

            self.ak8Jet_Ptbins = [200., 300., 400., 500., 800., 1000.]
            '''
            self.ak8SDPUPPIP4 = None
            self.ak8SDPUPPIMass =  None
            self.ak8PUPPIP4 =  None
            self.ak8PUPPIMass = None
            
            self.ak8SDPUPPIP40 = None
            self.ak8SDPUPPIMass0 =  None
            self.ak8PUPPIP40 =  None
            self.ak8PUPPIMass0 = None
            '''            
            self.theMass_Hist =  None
            self.theSDMass_Hist =  None
            self.theSDsj0Masshist =  None
            self.theSDsj1Masshist =  None
            
            self.theMass_Hist0 =  None
            self.theSDMass_Hist0 =  None
            self.theSDsj0Masshist0 =  None
            self.theSDsj1Masshist0 =  None         
              
            for iptbin, ptbin in enumerate(b.ak8Jet_Ptbins) :
                if ptbin <  800.:
                    if (  ptbin < b.ak8PUPPISDJetP4.Perp()  < b.ak8Jet_Ptbins[iptbin+1] ) :
                        if self.verbose : print"b.ak8PUPPISDJetP4.Perp() : {0:3.2f} ptbin [ {1:} , {2:}]".format( b.ak8PUPPISDJetP4.Perp(), ptbin, b.ak8Jet_Ptbins[iptbin+1] )
                        
                        self.ak8SDPUPPIMass =  b.ak8PUPPISD_m_Pcorr
                        self.ak8PUPPIMass = b.ak8PUPPI_m_Pcorr
                        self.ak8SDsj0_m    = b.ak8SDsj0_m
                        self.ak8SDsj1_m    =b.ak8SDsj1_m
                        self.theMass_Hist = self.AK8_Mass_AK8PtBinnedHistList[iptbin]
                        self.theSDMass_Hist = self.AK8_SDMass_AK8PtBinnedHistList [iptbin]
                        self.theSDsj0Masshist = self.WcandSJ_SDMass_AK8PtBinned_HistList[iptbin]
                        self.theSDsj1Masshist = self.BcandSJ_SDMass_AK8PtBinned_HistList[iptbin]
                        if  self.theMass_Hist != None and self.ak8PUPPIMass != None :
                            #if self.verbose: print"Filling Pt binned arrays e.g. this one {0:} with the value of ak8puppimass {1:2.2f} for ipt {2:} ptbin {3:}".format(self.theMass_Hist[ilep][index], self.ak8PUPPIMass , iptbin, ptbin)

                            self.theMass_Hist[ilep][index].Fill( self.ak8PUPPIMass  , self.theWeight )
                            self.theSDMass_Hist[ilep][index].Fill(  self.ak8SDPUPPIMass , self.theWeight )
                        if  self.theSDsj0Masshist != None :
                            self.theSDsj0Masshist[ilep][index].Fill(  self.ak8SDsj0_m  , self.theWeight )
                            self.theSDsj1Masshist[ilep][index].Fill(  self.ak8SDsj1_m  , self.theWeight )

                    if (  ptbin < b.ak8PUPPISDJetP4_Subjet0.Perp() < self.ak8Jet_Ptbins[iptbin+1] ) :
                        if self.verbose : print"b.ak8PUPPISDJetP4_Subjet0.Perp() : {0:3.2f} pt bin[ {1:}, {2:}]".format( b.ak8PUPPISDJetP4_Subjet0.Perp(), ptbin, b.ak8Jet_Ptbins[iptbin+1] )
                    
                        self.ak8SDPUPPIMass0 =  b.ak8PUPPISD_m_Pcorr
                        self.ak8PUPPIMass0 =  b.ak8PUPPI_m_Pcorr
                        #print"ak8 puppi mass0 from b.ak8PUPPI_m_Pcorr is {0:2.2f}".format(b.ak8PUPPI_m_Pcorr)
                        self.ak8SDsj0_m0    = b.wcandp4.M()  #b.ak8SDsj0_m
                        self.ak8SDsj1_m0    = b.ak8SDsj1_m
                        self.theMass_Hist0 = self.AK8_Mass_WcandSJPtBinned_HistList[iptbin]
                        self.theSDMass_Hist0 = self.AK8_SDMass_AK8PtBinnedHistList 0[iptbin]
                        self.theSDsj0Masshist0 = self.WcandSJ_SDMass_WcandSJPtBinned_HistList[iptbin]
                        self.theSDsj0Masshist0l2l3 = self.WcandSJ_SDMass_WcandSJPtBinned_HistListl2l3[iptbin]
                        self.theSDsj1Masshist0 = self.BcandSJ_SDMass_WcandSJPtBinned_HistList[iptbin] 
                      

                        if  self.theMass_Hist0 != None and self.ak8PUPPIMass0 != None :
                            #if self.verbose: print"Filling Pt binned by SD subjet 0 pt arrays e.g. this one {0:} with the value of ak8puppimass0 {1:2.2f} for ipt {2:d} ptbin {3:d}".format(self.theMass_Hist0[ilep][index],float( self.ak8PUPPIMass0 ), iptbin, ptbin)

                            self.theMass_Hist0[ilep][index].Fill( self.ak8PUPPIMass0  , self.theWeight )                       
                            self.theSDMass_Hist0[ilep][index].Fill(  self.ak8SDPUPPIMass0 , self.theWeight )

                        if  self.theSDsj0Masshist0 != None :
                            self.theSDsj0Masshist0[ilep][index].Fill(  self.ak8SDsj0_m0  , self.theWeight )
                            self.theSDsj0Masshist0l2l3[ilep][index].Fill(  b.wcandp4.M()  , self.theWeight )
                            self.theSDsj1Masshist0[ilep][index].Fill(  self.ak8SDsj1_m0  , self.theWeight )

            for iptbin, ptbin in enumerate(b.ak8Jet_Ptbinsb) :
                if ptbin <  1000.:
                    if (  ptbin < b.ak8PUPPISDJetP4_Subjet0.Perp() < b.ak8Jet_Ptbinsb[iptbin+1] ) :
                        if self.verbose : print"b.ak8PUPPISDJetP4_Subjet0.Perp() : {0:3.2f} pt bin[ {1:}, {2:}]".format( b.ak8PUPPISDJetP4_Subjet0.Perp(), ptbin, b.ak8Jet_Ptbinsb[iptbin+1] )
                    
                        self.ak8SDPUPPIMass0 =  b.ak8PUPPISD_m_Pcorr
                        self.ak8PUPPIMass0 =  b.ak8PUPPI_m_Pcorr
                        #print"ak8 puppi mass0 from b.ak8PUPPI_m_Pcorr is {0:2.2f}".format(b.ak8PUPPI_m_Pcorr)
                        self.ak8SDsj0_m0    =b.wcandp4.M()
                        self.ak8SDsj1_m0    =b.ak8SDsj1_m
                        self.theMass_Hist0 = self.AK8_Mass_WcandSJPtBinned_HistListb[iptbin]
                        self.theSDMass_Hist0 = self.AK8_SDMass_AK8PtBinnedHistList 0b[iptbin]
                        self.theSDsj0Masshist0 = self.WcandSJ_SDMass_WcandSJPtBinned_HistListb[iptbin]
                        self.theSDsj0Masshist0l2l3 = self.WcandSJ_SDMass_WcandSJPtBinned_HistListbl2l3[iptbin]
                        self.theSDsj1Masshist0 = self.BcandSJ_SDMass_WcandSJPtBinned_HistListb[iptbin] 
                      

                        if  self.theMass_Hist0 != None and self.ak8PUPPIMass0 != None :
                            #if self.verbose: print"Filling Pt binned by SD subjet 0 pt arrays e.g. this one {0:} with the value of ak8puppimass0 {1:2.2f} for ipt {2:d} ptbin {3:d}".format(self.theMass_Hist0[ilep][index],float( self.ak8PUPPIMass0 ), iptbin, ptbin)

                            self.theMass_Hist0[ilep][index].Fill( self.ak8PUPPIMass0  , self.theWeight )                       
                            self.theSDMass_Hist0[ilep][index].Fill(  self.ak8SDPUPPIMass0 , self.theWeight )

                        if  self.theSDsj0Masshist0 != None :
                            self.theSDsj0Masshist0[ilep][index].Fill(  self.ak8SDsj0_m0  , self.theWeight )
                            self.theSDsj0Masshist0l2l3[ilep][index].Fill(  b.wcandp4.M()  , self.theWeight )

                            self.theSDsj1Masshist0[ilep][index].Fill(  self.ak8SDsj1_m0  , self.theWeight )
        ### Fill the Lepton and AK4_ histos
        if a.leptonP4 != None : 
            self.Lepton_Pt_Hist[ilep][index].Fill( a.leptonP4.Perp()  , self.theWeight )
            self.Lepton_Eta_Hist[ilep][index].Fill( a.leptonP4.Eta()  , self.theWeight )
            self.MET_Pt_Hist[ilep][index].Fill( a.nuP4.Perp() , self.theWeight  )
            self.LepW_Pt_Hist[ilep][index].Fill( a.leptonP4.Perp() + a.nuP4.Perp()  , self.theWeight )
            if a.ak4Jet != None : 
                self.Iso2D_Hist[ilep][index].Fill( a.leptonP4.Perp( a.ak4Jet.Vect() ), a.leptonP4.DeltaR( a.ak4Jet )  , self.theWeight  )
                self.AK4_Bdisc_Hist[ilep][index].Fill(b.ak4JetBdisc , self.theWeight)
        ### Fill the ttree
        #if index > 5 : print "index is {}".format(index)
        if index == 12:            
            
            ### Define lumi weight
            if self.options.v5 :
                if self.theCount < 1 :
                    self.lumiWeight = 1.0
                    self.theCount +=1
                    self.xrdprefix = 'root://cmsxrootd.fnal.gov/'

                    self.eosDir = '/store/user/asparker/B2G2016/V5Trees/'

                    self.infiles = [
                    'b2gtreeV5_QCD_Pt-470to600_MuEnriched_pythia8_RunIISummer16MiniAODv2_try2.root',
                    'b2gtreeV5_QCD_Pt-470to600_MuEnriched_pythia8_RunIISummer16MiniAODv2_ext1_try3.root', 
                    'b2gtreeV5_ST_s-channel_amcatnlo-pythia8_RunIISummer16MiniAODv2_try4.root',
                    'b2gtreeV5_ST_t-channel_antitop_powhegV2-madspin-pythia8_RunIISummer16MiniAODv2_try3.root',
                    'b2gtreeV5_ST_t-channel_top_powhegV2-madspin-pythia8_RunIISummer16MiniAODv2_try3.root',
                    'b2gtreeV5_ST_tW_antitop_RunIISummer16MiniAODv2_try4.root',
                    'b2gtreeV5_ST_tW_antitop_powheg-pythia8_RunIISummer16MiniAODv2_ext1_try4.root',
                    'b2gtreeV5_ST_tW_top_powheg-pythia8_RunIISummer16MiniAODv2_try5.root',
                    'b2gtreeV5_ST_tW_top_powheg-pythia8_RunIISummer16MiniAODv2_ext1_try4.root',
                    'b2gtreeV5_TT_TuneCUETP8M2T4_All_13TeV-powheg-pythia8_RunIISummer16MiniAODv2.root',
                    'b2gtreeV5_TT_TuneEE5C_All_13TeV-powheg-herwigpp_RunIISummer16MiniAODv2.root',
                    'b2gtreeV5_WJetsToLNu_HT-100To200_All_madgraphMLM-pythia8_RunIISummer16MiniAODv2.root',
                    'b2gtreeV5_WJetsToLNu_HT-1200To2500_All_madgraphMLM-pythia8_RunIISummer16MiniAODv2.root',
                    'b2gtreeV5_WJetsToLNu_HT-200To400_All_madgraphMLM-pythia8_RunIISummer16MiniAODv2.root',
                    'b2gtreeV5_WJetsToLNu_HT-2500ToInf_All_madgraphMLM-pythia8_RunIISummer16MiniAODv2.root',
                    'b2gtreeV5_WJetsToLNu_HT-400To600_All_madgraphMLM-pythia8_RunIISummer16MiniAODv2.root',
                    'b2gtreeV5_WJetsToLNu_HT-600To800_All_madgraphMLM-pythia8_RunIISummer16MiniAODv2.root',
                    'b2gtreeV5_WJetsToLNu_HT-800To1200_All_madgraphMLM-pythia8_RunIISummer16MiniAODv2.root',

                    ]

                    self.nEvents = [  3851524., # QCD Muenriched 470-600
                                      5663755., # QCD Muenriched 470-600 ext1
                                      1000000., # ST_schannel
                                    35038862., # ST t channel antitop
                                    67240808., # ST t channel top
                                      998276.,#ST_tW_antitop
                                      6846954., #ST_tW_antitop ext1
                                      992024., # ST tW top
                                      6733210., # ST tW top ext1
                                   154938481.,# TT_TuneCUETP8M2T4_All (sum of 2) 77229341 + 77709140
                                      68375043., # TT herwig (sum of 3)
                                    78403814.,# WJetsToLNu_HT-100To200_All 10235198 + 28550829 + 39617787
                                     6797731.,# 1200To2500_All 244532 + 6553199
                                    39680891.,# 200To400_All  4950373 + 14815928 + 19914590
                                     2637821.,# 2500ToInf 253561 + 2384260
                                     7759701.,# 400To600_All 1963464 + 5796237
                                    18425597.,# 600To800  14819287 + 3606310
                                     7352465., # 800To1200_  1544513 + 5807952
                                    ]

                    self.xSections = [  645.528 ,  # QCD Muenriched 470-600 
                                       645.528 ,  # QCD Muenriched 470-600  
                                               3.36 , # ST_schannel
                                        80.95*0.322, # ST t channel antitop
                                        136.02*0.322, # ST t channel top
                                        35.6 ,  #singletop_tWantitop
                                        35.6 ,  #singletop_tWantitop ext1
                                        35.6 ,  #singletop_tW top
                                        35.6 ,  #singletop_tW top ext1
                                        831., # ttbar 
                                        831., # other ttbar
                                        1345.,     #100To200  W + jets
                                        1.329,     #1200To2500
                                        359.7,     #200To400  
                                        0.03216,   #2500ToInf
                                        48.91,     #400To600  
                                        12.05,     #600To800  
                                        5.501     #800To1200 
                                        ]
                                        
                    self.lumi = 35860.0 # /pb     ### This is the correct luminosity of the new samples

                    for ifile, afile in enumerate(self.infiles):
                        if self.verboseW  : print"infile is  {}   Afile is {}".format( self.infile,  self.xrdprefix +self.eosDir + afile)
                        if self.xrdprefix +self.eosDir + afile ==  self.infile:
                            self.lumiWeight =  self.xSections[ifile] / self.nEvents[ifile] * self.lumi

                            if self.verboseW : print"lumiweight is {}".format(self.lumiWeight)
                
            if not self.options.v5 :
                if self.theCount < 1 :
                    self.lumiWeight = 1.0
                    self.theCount +=1
                    self.infiles = ['root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_ttbar_all_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_ttbarTuneCUETP8M2T4_all_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_100_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_200_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_400_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_600_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_800_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_1200_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_2500_V4.root',
                                    '/uscms_data/d2/rappocc/analysis/B2G/CMSSW_8_0_22/src/Analysis/B2GTTbar/test/pyttbarfw/b2gtree_MC_ST_tchannel-top_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_ST_tchannel-antitop_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_ST_tW-top_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtreeV4_ST_tW_antitop_1of1.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_ST_schannel_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht100_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht200_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht300_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht500_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht700_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht1000_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht1500_V4.root',
                                    'root://131.225.207.127:1094//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht2000_V4.root'

                                    ]
                                    
                    self.nEvents = [  92925926., # original ttbar
                                      70452080., # Otherttbar  - different tune, same MC generator
                                      10231928., #100To200   W + jets
                                      4963240.,  #200To400 
                                      1963464.,  #400To600 
                                      3722395.,  #600To800
                                      1540477.,  #800To1200 
                                      246737.,   #1200To2500 
                                      253561.,   #2500ToInf 
                                    32808300.,   #singletop_tchanneltop_outfile.root
                                    19825855.,   #singletop_tchannel_outfile.root
                                      998400.,   #singletop_tW_outfile.root
                                      985000.,   #singletop_tWantitop_outfile.root
                                      1000000.,   #singletop_schannel_outfile.root 
                                     82073090., # 100To200  
                                    18523829., # 200To300  
                                    16830696., # 300To500  
                                    19199088., # 500To700  
                                    15621634., # 700To1000 
                                    4980387.,  # 1000To1500
                                    3846616.,  # 1500To2000
                                    1960245.   # 2000ToInf 
                                   ]
                                   
                    self.xSections = [  831.,
                                        831.,
                                        1345.,     #100To200  W + jets
                                        359.7,     #200To400  
                                        48.91,     #400To600  
                                        12.05,     #600To800  
                                        5.501,     #800To1200 
                                        1.329,     #1200To2500
                                        0.03216,   #2500ToInf 
                                        136.02 * 0.322,#singletop_tchanneltop_outfile.root
                                        80.95 * 0.322, #singletop_tchannel_outfile.root
                                        35.6,          #singletop_tW_outfile.root
                                        35.6,          #singletop_tWantitop_outfile.root
                                        3.36,           #singletop_schannel_outfile.root 
                                        27990000., # 100To200
                                        1712000.,  # 200To300
                                        347700.,   # 300To500
                                        32100.,    # 500To700
                                        6831.,     # 700To1000
                                        1207.,     # 1000To1500
                                        119.9,     # 1500To2000
                                        25.24      # 2000ToInf 
                                     ]
                                     
                    self.lumi = 35860.0 # /pb ### This is the correct luminosity of the new samples                     
                                   
                    for ifile, afile in enumerate(self.infiles):
                        if self.verboseW  : print"infile is  {}   Afile is {}".format(self.infile, afile)
                        if afile == self.infile:
                            self.lumiWeight =  self.xSections[ifile] / self.nEvents[ifile] * self.lumi

                            if self.verboseW : print"lumiweight is {}".format(self.lumiWeight)
            
            '''
            self.weights = {
                             'SemiLeptLumiweight':'f',
                             'SemiLeptAllotherweights':'f',
                            } 
            '''
            self.fillVars = [self.lumiWeight , self.theWeight ]
        
            self.SemiLeptLumiweight[0] =  float( self.fillVars[0])
            self.SemiLeptAllotherweights[0] =  float( self.fillVars[1])
            self.SubjetTau21[0] = float( b.ak8SDsubjet0tau21 )  
                #print"*******************var  {}= float( self.fillVars[ivar])  {}".format(var , float( self.fillVars[ivar]))
                #self.weightVal = float( self.fillVars[ivar])
                

            #if self.verboseW : print"FILLLLL--------   self.fillVars {}  float( self.fillVars[0])  {}   , float( self.fillVars[1])  {}, subjet tau21 {}".format( self.fillVars, float( self.fillVars[0]) , float( self.fillVars[1]), float( b.ak8SDsubjet0tau21 ) )    
            self.TTreeWeights.Fill()
            self.TTreeSemiLept.Fill()

    def close( self ) :
        '''
        Wrap it up. 
        '''

        #self.TTreeWeights.Write()
        #self.TTreeSemiLept.Write()
        
        self.outfile.cd() 
        self.outfile.Write()
        self.outfile.Close()


'''
        Executable
'''

if __name__ == "__main__" :
    r = RunSemiLepTTbar_HighMass(sys.argv)
    r.run()

