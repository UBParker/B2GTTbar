
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

        parser.add_option('--type', type='string', action='store',
                          dest='dtype',
                          default = '',
                          help='type of files to combine: mudataB-H, eldataB-H , ttjets, wjets1-9  , st1-5') 

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
                          default = 0.8484, ### Medium https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation80XReReco
                          help='B discriminator cut')

        parser.add_option('--maxevents', type='int', action='store',
                          default=None,
                          dest='maxevents',
                          help='Maximum number of events')

        parser.add_option('--ignoreTrig', action='store_true',
                          dest='ignoreTrig',
                          default = False,
                          help='Ignore the trigger?')
        
        parser.add_option('--verbose', action='store_true',
                          default=False,
                          dest='verbose',
                          help='Do you want to print values of key variables?')

        (options, args) = parser.parse_args(argv)
        argv = []

        #self.startTime = time.time()
        self.infile = options.infile
        self.outfile = ROOT.TFile(options.outfile, "RECREATE")

        self.verboseW = False # True
        
        ### Create the tree class. This will make simple class members for each
        ### of the branches that we want to read from the Tree to save time.
        ### Also saved are some nontrivial variables that involve combinations
        ### of things from the tree
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
        self.branchesArray = []
        # self.i = 0
        self.weightVal = -3.14159
        #for var in self.weights.iteritems() :
        self.SemiLeptLumiweight = (array.array( 'f', [self.weightVal] ))
        self.SemiLeptAllotherweights = (array.array( 'f', [self.weightVal] ))
        self.SubjetTau21 = (array.array( 'f', [self.weightVal] ))

        self.TTreeWeights.Branch('SemiLeptLumiweight'  , self.SemiLeptLumiweight     ,  'SemiLeptLumiweight/F'      )
        self.TTreeWeights.Branch( 'SemiLeptAllotherweights' ,  self.SemiLeptAllotherweights     ,  'SemiLeptAllotherweights/F'      )
        self.TTreeWeights.Branch( 'SubjetTau21' ,  self.SubjetTau21    ,  'SubjetTau21/F'      )

        #print"self.branchesArray {}".format(self.branchesArray)    
        #self.TTreeSemiLeptSkim.AddFriend("TTreeWeights", options.outfile)

        self.options = options
        self.verbose = options.verbose
        self.infile = options.infile
        self.maxevents = options.maxevents
        
        
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
        self.RunNumberHist = []
        ### Weights histogram with total weight applied to the event when filling histograms
        self.WeightHist = []      
                
        self.LeptonPtHist = []
        self.LeptonEtaHist = []
        self.METPtHist = []
        self.HTLepHist = []
        self.Iso2DHist = []
        self.AK4BdiscHist = []        

        self.AK8PtHist = []
        self.AK8HTHist = []
        self.AK8SDPtHist = [] 
        self.AK8PuppiSDPtHist = [] 
        self.AK8PuppiPtHist = [] 

        self.AK8PuppiSDPtResponse = []
        self.AK8SDPtResponse = []
        self.AK8SDPuppiptGenptResponse = []
        self.AK8SDPuppiptSDCHSptResponse = []
        self.AK8SDPuppimassSDCHSmassResponse = []
        self.AK8SDPuppiMasswithPuppiCorrvsSDPuppiMassResponse = []
          
        self.AK8puppitau21Hist = []
        self.AK8puppitau32Hist = []

        self.AK8EtaHist = []
        
        self.AK8MHist = []            ### ungroomed uncorrected Fat Jet mass
        self.AK8MSDHist = []
        self.AK8MSDRawHist = []                        ### Soft Drop jet mass without CHS or PUPPI
        self.AK8MSDPUPPIHist = []
        self.AK8MSDCHSHist = []

        self.AK8SDRhoRatioHist = []

        self.AK8MSDSJ0Hist = []
        self.AK8SDSJ0PtHist = []      
            
        self.lepNames = ['Electron', 'Muon' ]
        ### Create histos for type 1 selection binned by pt of AK8

        self.AK8MPtBinnedHistList = [[], [] ,[], [] , []]
        self.AK8MSDPtBinnedHistList = [[], [] ,[], [] , []]
        self.AK8MSDSJ0PtBinnedHistList = [[], [] ,[], [] , []]
        self.AK8MSDSJ1PtBinnedHistList = [[], [] ,[], [] , []]
        ### Create histos for type 1 selection binned by pt of leading SD subjet

        self.AK8MPtBinnedHistList0 = [[], [] ,[], [] , []]
        self.AK8MSDPtBinnedHistList0 = [[], [] ,[], [] , []]
        self.AK8MSDSJ0PtBinnedHistList0 = [[], [] ,[], [] , []]
        self.AK8MSDSJ0PtBinnedHistList0l2l3 = [[], [] ,[], [] , []]
        self.AK8MSDSJ1PtBinnedHistList0 = [[], [] ,[], [] , []]       
        ### Alternate binning scheme
        self.AK8MPtBinnedHistList0b = [[], [] ,[], [] , []]
        self.AK8MSDPtBinnedHistList0b = [[], [] ,[], [] , []]
        self.AK8MSDSJ0PtBinnedHistList0b = [[], [] ,[], [] , []]
        self.AK8MSDSJ0PtBinnedHistList0bl2l3 = [[], [] ,[], [] , []]

        self.AK8MSDSJ1PtBinnedHistList0b = [[], [] ,[], [] , []]  
        
        ### List of all histograms
        self.hists = []
        
        for ilep in xrange(self.nlep) :   
            self.RunNumberHist.append( [] )
            self.WeightHist.append( [] ) 
            self.AK8PtHist.append([])       
            self.AK8HTHist.append( [] )
            self.AK8SDPtHist.append( [] )
            self.AK8PuppiSDPtHist.append([])
            self.AK8PuppiPtHist.append( [] )
            self.AK8PuppiSDPtResponse.append( [] )
            self.AK8SDPuppimassSDCHSmassResponse.append( [] )
            self.AK8SDPtResponse.append([])
            self.AK8SDPuppiptGenptResponse.append([])
            self.AK8SDPuppiMasswithPuppiCorrvsSDPuppiMassResponse.append([])
            self.AK8SDSJ0PtHist.append( [])
            self.AK8EtaHist.append([])      
            self.AK8puppitau21Hist.append([])
            self.AK8puppitau32Hist.append([])
            

            self.AK8MHist.append( [] )
            self.AK8MSDRawHist.append( [] )                      
            self.AK8MSDPUPPIHist.append( [] )
            self.AK8MSDCHSHist.append( [] )
            self.AK8MSDHist.append( [] )
            self.AK8SDRhoRatioHist.append( [] )
            self.AK8MSDSJ0Hist.append( [] )

            self.LeptonPtHist.append( [] )
            self.LeptonEtaHist.append( [] )

            self.METPtHist.append( [] )
            self.HTLepHist.append([] )
            self.Iso2DHist.append ( [] )
            self.AK4BdiscHist.append( [] )

            for iptbin, ptbin in enumerate(b.ak8Jet_Ptbins) :
                if iptbin < 5:
                    #if self.verbose: print"self.AK8MPtBinnedHistList {} of length {}".format(self.AK8MPtBinnedHistList, len(self.AK8MPtBinnedHistList))
                    self.AK8MPtBinnedHistList[iptbin].append( [] )
                    self.AK8MSDPtBinnedHistList[iptbin].append( [] )
                    self.AK8MSDSJ0PtBinnedHistList[iptbin].append( [] )
                    self.AK8MSDSJ1PtBinnedHistList[iptbin].append( [] )
                    
                    self.AK8MPtBinnedHistList0[iptbin].append( [] )
                    self.AK8MSDPtBinnedHistList0[iptbin].append( [] )
                    self.AK8MSDSJ0PtBinnedHistList0[iptbin].append( [] )
                    self.AK8MSDSJ0PtBinnedHistList0l2l3[iptbin].append( [] )
                    self.AK8MSDSJ1PtBinnedHistList0[iptbin].append( [] )  
                                      
            for iptbin, ptbin in enumerate(b.ak8Jet_Ptbinsb) :
                if iptbin < 5:
                    self.AK8MPtBinnedHistList0b[iptbin].append( [] )
                    self.AK8MSDPtBinnedHistList0b[iptbin].append( [] )
                    self.AK8MSDSJ0PtBinnedHistList0b[iptbin].append( [] )
                    self.AK8MSDSJ0PtBinnedHistList0bl2l3[iptbin].append( [] )
                    self.AK8MSDSJ1PtBinnedHistList0b[iptbin].append( [] ) 
                    
            for ival in xrange(self.nstages):
                self.RunNumberHist[ilep].append( ROOT.TH1F("RunNumberHist" + self.lepNames[ilep] + str(ival) , "Run Number for lepton "+self.lepNames[ilep] + str(ival), 286591, 0, 286591) )
                self.WeightHist[ilep].append( ROOT.TH1F("WeightHist" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, -2, 2) )
                self.AK8PtHist[ilep].append( ROOT.TH1F("AK8PtHist" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8MSDRawHist[ilep].append( ROOT.TH1F("AK8MSDRawHist" +  self.lepNames[ilep] + str(ival), "AK8 Soft Drop Jet p_{T} RAW, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8MSDPUPPIHist[ilep].append( ROOT.TH1F("AK8MSDPUPPIHist" +  self.lepNames[ilep] + str(ival), "AK8 Soft Drop Jet p_{T} PUPPI, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8MSDCHSHist[ilep].append( ROOT.TH1F("AK8MSDCHSHist" +  self.lepNames[ilep] + str(ival), "AK8 Soft Drop Jet p_{T} CHS, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8HTHist[ilep].append( ROOT.TH1F("AK8HTHist" +  self.lepNames[ilep] + str(ival), "Jet H_{T}, Stage " + self.lepNames[ilep] + str(ival), 4000, 0, 4000) )
                self.AK8SDPtHist[ilep].append( ROOT.TH1F("AK8SDPtHist" +  self.lepNames[ilep] + str(ival), "Jet SD p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8PuppiSDPtHist[ilep].append( ROOT.TH1F("AK8PuppiSDPtHist" +  self.lepNames[ilep] + str(ival), "Jet Puppi SD p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8PuppiPtHist[ilep].append( ROOT.TH1F("AK8PuppiPtHist" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )

                ### TO-DO: improve description of labels of below jet pt response histos
                self.AK8PuppiSDPtResponse[ilep].append( ROOT.TH1F("AK8PuppiSDPtResponse" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000,-10, 1000) )
                self.AK8SDPtResponse[ilep].append( ROOT.TH1F("AK8SDPtResponse" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, -10, 1000) )
                self.AK8SDPuppiptGenptResponse[ilep].append( ROOT.TH1F("AK8SDPuppiptGenptResponse" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, -10, 1000)) 
                self.AK8SDPuppimassSDCHSmassResponse[ilep].append( ROOT.TH1F("AK8SDPuppimassSDCHSmassResponse" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, -10, 1000)) 
                self.AK8SDPuppiMasswithPuppiCorrvsSDPuppiMassResponse[ilep].append( ROOT.TH1F("AK8SDPuppiMasswithPuppiCorrvsSDPuppiMassResponse" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, -10, 1000))

                self.AK8SDSJ0PtHist[ilep].append( ROOT.TH1F("AK8SDSJ0PtHist" +  self.lepNames[ilep] + str(ival), "SD subjet 0 P_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8EtaHist[ilep].append( ROOT.TH1F("AK8EtaHist" +  self.lepNames[ilep] + str(ival), "Jet #eta, Stage " + self.lepNames[ilep] + str(ival), 1000, -2.5, 2.5) )
                self.AK8puppitau21Hist[ilep].append( ROOT.TH1F("AK8puppitau21Hist" +  self.lepNames[ilep] + str(ival), "Jet #tau_{21}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0., 1.) )
                self.AK8puppitau32Hist[ilep].append( ROOT.TH1F("AK8puppitau32Hist" +  self.lepNames[ilep] + str(ival), "Jet #tau_{32}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0., 1.) )


                self.AK8MHist[ilep].append( ROOT.TH1F("AK8MHist" +  self.lepNames[ilep] + str(ival), "Jet Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                self.AK8MSDHist[ilep].append( ROOT.TH1F("AK8MSDHist" +  self.lepNames[ilep] + str(ival), "Jet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                self.AK8SDRhoRatioHist[ilep].append( ROOT.TH1F("AK8SDRhoRatioHist" +  self.lepNames[ilep] + str(ival), "SD Rho Ratio, Stage " + self.lepNames[ilep] + str(ival), 1000, 0., 1.) )
                self.AK8MSDSJ0Hist[ilep].append( ROOT.TH1F("AK8MSDSJ0Hist" +  self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )

                self.LeptonPtHist[ilep].append( ROOT.TH1F("LeptonPtHist" +  self.lepNames[ilep] + str(ival), "Lepton p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.LeptonEtaHist[ilep].append( ROOT.TH1F("LeptonEtaHist" +  self.lepNames[ilep] + str(ival), "Lepton #eta, Stage " + self.lepNames[ilep] + str(ival), 1000, -2.5, 2.5) )

                self.METPtHist[ilep].append( ROOT.TH1F("METPtHist" +  self.lepNames[ilep] + str(ival), "Missing p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.HTLepHist[ilep].append( ROOT.TH1F("HTLepHist" +  self.lepNames[ilep] + str(ival), "Lepton p_{T} + Missing p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.Iso2DHist[ilep].append ( ROOT.TH2F("Iso2DHist" +  self.lepNames[ilep] + str(ival), "Lepton 2D isolation (#Delta R vs p_{T}^{REL} ), Stage " + self.lepNames[ilep] + str(ival), 25, 0, 500, 25, 0, 1) )
                self.AK4BdiscHist[ilep].append( ROOT.TH1F("AK4BdiscHist" +  self.lepNames[ilep] + str(ival), "CSVv2 B disc , Stage " + self.lepNames[ilep] + str(ival), 1000, 0., 1.) )

                for iptbin, ptbin in enumerate(b.ak8Jet_Ptbins) :
                    if iptbin < 4:
                        self.AK8MPtBinnedHistList[iptbin][ilep].append( ROOT.TH1F("AK8MPt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Jet Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8MSDPtBinnedHistList[iptbin][ilep].append( ROOT.TH1F("AK8MSDPt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Jet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8MSDSJ0PtBinnedHistList[iptbin][ilep].append( ROOT.TH1F("AK8MSDSJ0Pt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8MSDSJ1PtBinnedHistList[iptbin][ilep].append( ROOT.TH1F("AK8MSDSJ1Pt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Sub-Leading Subjet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
     
                        self.AK8MPtBinnedHistList0[iptbin][ilep].append( ROOT.TH1F("0AK8MPt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Jet Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8MSDPtBinnedHistList0[iptbin][ilep].append( ROOT.TH1F("0AK8MSDPt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Jet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8MSDSJ0PtBinnedHistList0[iptbin][ilep].append( ROOT.TH1F("0AK8MSDSJ0Pt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8MSDSJ0PtBinnedHistList0l2l3[iptbin][ilep].append( ROOT.TH1F("l2l30AK8MSDSJ0Pt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbinsb[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass+ L2L3 corr, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8MSDSJ1PtBinnedHistList0[iptbin][ilep].append( ROOT.TH1F("0AK8MSDSJ1Pt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Sub-Leading Subjet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                for iptbin, ptbin in enumerate(b.ak8Jet_Ptbinsb) :
                    if iptbin < 4:

                        self.AK8MPtBinnedHistList0b[iptbin][ilep].append( ROOT.TH1F("b0AK8MPt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbinsb[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Jet Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8MSDPtBinnedHistList0b[iptbin][ilep].append( ROOT.TH1F("b0AK8MSDPt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbinsb[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Jet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8MSDSJ0PtBinnedHistList0b[iptbin][ilep].append( ROOT.TH1F("b0AK8MSDSJ0Pt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbinsb[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass + PUPPI corr, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8MSDSJ0PtBinnedHistList0bl2l3[iptbin][ilep].append( ROOT.TH1F("l2l3b0AK8MSDSJ0Pt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbinsb[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass+ L2L3 corr, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                        self.AK8MSDSJ1PtBinnedHistList0b[iptbin][ilep].append( ROOT.TH1F("b0AK8MSDSJ1Pt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbinsb[iptbin+1]) +  self.lepNames[ilep] + str(ival), "Sub-Leading Subjet Soft Dropped Mass, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 500) )
                


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
            self.RunNumberHist[ilep][index].Fill(a.RunNumber)
        if self.theWeight > -1. :
            self.WeightHist[ilep][index].Fill(self.theWeight)
            
        if b.ak8JetP4 != None :
            self.AK8PtHist[ilep][index].Fill( b.ak8JetP4.Perp()* b.PtSmear   , self.theWeight )  ### TO-DO : Implement Pt smear in hadselection and replace 1.000 with b.PtSmear
            self.AK8HTHist[ilep][index].Fill( b.ak8JetHT  , self.theWeight )
            if b.ak8SDJetP4 != None and b.SDptGenpt != None :
                self.AK8SDPtResponse[ilep][index].Fill(  b.ak8JetP4.Perp() * b.PtSmear, b.SDptGenpt  )    
                self.AK8SDPuppiptGenptResponse[ilep][index].Fill(  b.ak8JetP4.Perp() * b.PtSmear, b.SDPuppiptGenpt  )
                self.AK8SDPuppimassSDCHSmassResponse[ilep][index].Fill(  b.ak8JetP4.M(), b.SDPuppimassSDCHSmass  )
                if b.SDPuppiMasswithPuppiCorrvsSDPuppiMass > 0. and  b.ak8PuppiSD_m_Pcorr > 0.  :
                    self.AK8SDPuppiMasswithPuppiCorrvsSDPuppiMassResponse[ilep][index].Fill( b.ak8PuppiSD_m_Pcorr , b.SDPuppiMasswithPuppiCorrvsSDPuppiMass )#, b.ak8PuppiSD_m_Pcorr ) #* b.PtSmear )
        if b.ak8SDJetP4 != None :
            self.AK8SDPtHist[ilep][index].Fill( b.ak8SDJetP4.Perp() * b.PtSmear  , self.theWeight )
            self.AK8MSDHist[ilep][index].Fill( b.ak8PuppiSD_m_Pcorr  , self.theWeight )
            self.AK8MSDRawHist[ilep][index].Fill( b.akSDRaw_m  , self.theWeight )
            self.AK8MSDPUPPIHist[ilep][index].Fill( b.ak8PuppiSD_m , self.theWeight )
            self.AK8MSDCHSHist[ilep][index].Fill( b.akCHSSD_m  , self.theWeight )

        if b.ak8PuppiJetP4 != None :
            self.AK8PuppiPtHist[ilep][index].Fill( b.ak8PuppiJetP4.Perp() * b.PuppiPtSmear  , self.theWeight )
            self.AK8EtaHist[ilep][index].Fill( b.ak8PuppiJetP4.Eta()  , self.theWeight )
            self.AK8puppitau21Hist[ilep][index].Fill( b.ak8SDsubjet0tau21  , self.theWeight ) ### actually tau21 of subjet, misleading name
            self.AK8puppitau32Hist[ilep][index].Fill( b.puppitau32  , self.theWeight )
            if b.ak8Puppi_m_Pcorr != None: 
                self.AK8MHist[ilep][index].Fill( b.ak8Puppi_m_Pcorr , self.theWeight )
            if b.ak8PuppiSDJetP4 != None :
                if b.ak8PuppiJetP4  != None and b.SDptPuppipt != None :
                    self.AK8PuppiSDPtResponse[ilep][index].Fill( b.SDptPuppipt, b.ak8PuppiJetP4.Perp()* b.PuppiPtSmear  )# * b.PuppiPtSmear )  

        if  b.SDRhoRatio  != None :
            self.AK8SDRhoRatioHist[ilep][index].Fill(b.SDRhoRatio  , self.theWeight ) 


        if b.ak8PuppiSDJetP4 != None :
            self.AK8PuppiSDPtHist[ilep][index].Fill( b.ak8PuppiSDJetP4.Perp() * b.PuppiPtSmear  , self.theWeight )
            self.AK8SDSJ0PtHist[ilep][index].Fill( b.ak8PuppiSDJetP4_Subjet0.Perp() * b.PuppiPtSmear  , self.theWeight )
            self.AK8MSDSJ0Hist[ilep][index].Fill( b.ak8SDsj0_m  , self.theWeight )


            # Filling jet mass histos binned by pt of the leading SD subjet

            self.ak8Jet_Ptbins = [200., 300., 400., 500., 800., 1000.]
            '''
            self.ak8SDPuppiP4 = None
            self.ak8SDPuppiMass =  None
            self.ak8PuppiP4 =  None
            self.ak8PuppiMass = None
            
            self.ak8SDPuppiP40 = None
            self.ak8SDPuppiMass0 =  None
            self.ak8PuppiP40 =  None
            self.ak8PuppiMass0 = None
            '''            
            self.theMassHist =  None
            self.theSDMassHist =  None
            self.theSDsj0Masshist =  None
            self.theSDsj1Masshist =  None
            
            self.theMassHist0 =  None
            self.theSDMassHist0 =  None
            self.theSDsj0Masshist0 =  None
            self.theSDsj1Masshist0 =  None         
              
            for iptbin, ptbin in enumerate(b.ak8Jet_Ptbins) :
                if ptbin <  800.:
                    if (  ptbin < b.ak8PuppiSDJetP4.Perp()  < b.ak8Jet_Ptbins[iptbin+1] ) :
                        if self.verbose : print"b.ak8PuppiSDJetP4.Perp() : {0:3.2f} ptbin [ {1:} , {2:}]".format( b.ak8PuppiSDJetP4.Perp(), ptbin, b.ak8Jet_Ptbins[iptbin+1] )
                        
                        self.ak8SDPuppiMass =  b.ak8PuppiSD_m_Pcorr
                        self.ak8PuppiMass = b.ak8Puppi_m_Pcorr
                        self.ak8SDsj0_m    = b.ak8SDsj0_m
                        self.ak8SDsj1_m    =b.ak8SDsj1_m
                        self.theMassHist = self.AK8MPtBinnedHistList[iptbin]
                        self.theSDMassHist = self.AK8MSDPtBinnedHistList[iptbin]
                        self.theSDsj0Masshist = self.AK8MSDSJ0PtBinnedHistList[iptbin]
                        self.theSDsj1Masshist = self.AK8MSDSJ1PtBinnedHistList[iptbin]
                        if  self.theMassHist != None and self.ak8PuppiMass != None :
                            #if self.verbose: print"Filling Pt binned arrays e.g. this one {0:} with the value of ak8puppimass {1:2.2f} for ipt {2:} ptbin {3:}".format(self.theMassHist[ilep][index], self.ak8PuppiMass , iptbin, ptbin)

                            self.theMassHist[ilep][index].Fill( self.ak8PuppiMass  , self.theWeight )
                            self.theSDMassHist[ilep][index].Fill(  self.ak8SDPuppiMass , self.theWeight )
                        if  self.theSDsj0Masshist != None :
                            self.theSDsj0Masshist[ilep][index].Fill(  self.ak8SDsj0_m  , self.theWeight )
                            self.theSDsj1Masshist[ilep][index].Fill(  self.ak8SDsj1_m  , self.theWeight )

                    if (  ptbin < b.ak8PuppiSDJetP4_Subjet0.Perp() < self.ak8Jet_Ptbins[iptbin+1] ) :
                        if self.verbose : print"b.ak8PuppiSDJetP4_Subjet0.Perp() : {0:3.2f} pt bin[ {1:}, {2:}]".format( b.ak8PuppiSDJetP4_Subjet0.Perp(), ptbin, b.ak8Jet_Ptbins[iptbin+1] )
                    
                        self.ak8SDPuppiMass0 =  b.ak8PuppiSD_m_Pcorr
                        self.ak8PuppiMass0 =  b.ak8Puppi_m_Pcorr
                        #print"ak8 puppi mass0 from b.ak8Puppi_m_Pcorr is {0:2.2f}".format(b.ak8Puppi_m_Pcorr)
                        self.ak8SDsj0_m0    =b.ak8SDsj0_m
                        self.ak8SDsj1_m0    =b.ak8SDsj1_m
                        self.theMassHist0 = self.AK8MPtBinnedHistList0[iptbin]
                        self.theSDMassHist0 = self.AK8MSDPtBinnedHistList0[iptbin]
                        self.theSDsj0Masshist0 = self.AK8MSDSJ0PtBinnedHistList0[iptbin]
                        self.theSDsj0Masshist0l2l3 = self.AK8MSDSJ0PtBinnedHistList0l2l3[iptbin]
                        self.theSDsj1Masshist0 = self.AK8MSDSJ1PtBinnedHistList0[iptbin] 
                      

                        if  self.theMassHist0 != None and self.ak8PuppiMass0 != None :
                            #if self.verbose: print"Filling Pt binned by SD subjet 0 pt arrays e.g. this one {0:} with the value of ak8puppimass0 {1:2.2f} for ipt {2:d} ptbin {3:d}".format(self.theMassHist0[ilep][index],float( self.ak8PuppiMass0 ), iptbin, ptbin)

                            self.theMassHist0[ilep][index].Fill( self.ak8PuppiMass0  , self.theWeight )                       
                            self.theSDMassHist0[ilep][index].Fill(  self.ak8SDPuppiMass0 , self.theWeight )

                        if  self.theSDsj0Masshist0 != None :
                            self.theSDsj0Masshist0[ilep][index].Fill(  self.ak8SDsj0_m0  , self.theWeight )
                            self.theSDsj0Masshist0l2l3[ilep][index].Fill(  b.ak8PuppiSDJetP4_Subjet0.M()  , self.theWeight )
                            self.theSDsj1Masshist0[ilep][index].Fill(  self.ak8SDsj1_m0  , self.theWeight )

            for iptbin, ptbin in enumerate(b.ak8Jet_Ptbinsb) :
                if ptbin <  1000.:
                    if (  ptbin < b.ak8PuppiSDJetP4_Subjet0.Perp() < b.ak8Jet_Ptbinsb[iptbin+1] ) :
                        if self.verbose : print"b.ak8PuppiSDJetP4_Subjet0.Perp() : {0:3.2f} pt bin[ {1:}, {2:}]".format( b.ak8PuppiSDJetP4_Subjet0.Perp(), ptbin, b.ak8Jet_Ptbinsb[iptbin+1] )
                    
                        self.ak8SDPuppiMass0 =  b.ak8PuppiSD_m_Pcorr
                        self.ak8PuppiMass0 =  b.ak8Puppi_m_Pcorr
                        #print"ak8 puppi mass0 from b.ak8Puppi_m_Pcorr is {0:2.2f}".format(b.ak8Puppi_m_Pcorr)
                        self.ak8SDsj0_m0    =b.ak8SDsj0_m
                        self.ak8SDsj1_m0    =b.ak8SDsj1_m
                        self.theMassHist0 = self.AK8MPtBinnedHistList0b[iptbin]
                        self.theSDMassHist0 = self.AK8MSDPtBinnedHistList0b[iptbin]
                        self.theSDsj0Masshist0 = self.AK8MSDSJ0PtBinnedHistList0b[iptbin]
                        self.theSDsj0Masshist0l2l3 = self.AK8MSDSJ0PtBinnedHistList0bl2l3[iptbin]
                        self.theSDsj1Masshist0 = self.AK8MSDSJ1PtBinnedHistList0b[iptbin] 
                      

                        if  self.theMassHist0 != None and self.ak8PuppiMass0 != None :
                            #if self.verbose: print"Filling Pt binned by SD subjet 0 pt arrays e.g. this one {0:} with the value of ak8puppimass0 {1:2.2f} for ipt {2:d} ptbin {3:d}".format(self.theMassHist0[ilep][index],float( self.ak8PuppiMass0 ), iptbin, ptbin)

                            self.theMassHist0[ilep][index].Fill( self.ak8PuppiMass0  , self.theWeight )                       
                            self.theSDMassHist0[ilep][index].Fill(  self.ak8SDPuppiMass0 , self.theWeight )

                        if  self.theSDsj0Masshist0 != None :
                            self.theSDsj0Masshist0[ilep][index].Fill(  self.ak8SDsj0_m0  , self.theWeight )
                            self.theSDsj0Masshist0l2l3[ilep][index].Fill(  b.ak8PuppiSDJetP4_Subjet0.M()  , self.theWeight )

                            self.theSDsj1Masshist0[ilep][index].Fill(  self.ak8SDsj1_m0  , self.theWeight )
        ### Fill the Lepton and AK4 histos
        if a.leptonP4 != None : 
            self.LeptonPtHist[ilep][index].Fill( a.leptonP4.Perp()  , self.theWeight )
            self.LeptonEtaHist[ilep][index].Fill( a.leptonP4.Eta()  , self.theWeight )
            self.METPtHist[ilep][index].Fill( a.nuP4.Perp() , self.theWeight  )
            self.HTLepHist[ilep][index].Fill( a.leptonP4.Perp() + a.nuP4.Perp()  , self.theWeight )
            if a.ak4Jet != None : 
                self.Iso2DHist[ilep][index].Fill( a.leptonP4.Perp( a.ak4Jet.Vect() ), a.leptonP4.DeltaR( a.ak4Jet )  , self.theWeight  )
                self.AK4BdiscHist[ilep][index].Fill(b.ak4JetBdisc , self.theWeight)
        ### Fill the ttree
        if index == 12:            
            
            ### Define lumi weight
            
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
                                 
                self.lumi = 35867.0 # /pb                 
                               
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
            #for ivar, var in enumerate(self.branchesArray) :            
            self.SemiLeptLumiweight[0] =  float( self.fillVars[0])
            self.SemiLeptAllotherweights[0] =  float( self.fillVars[1])
            self.SubjetTau21[0] = float( b.ak8SDsubjet0tau21 )  
                #print"*******************var  {}= float( self.fillVars[ivar])  {}".format(var , float( self.fillVars[ivar]))
                #self.weightVal = float( self.fillVars[ivar])
                

            if self.verboseW : print"FILLLLL--------   self.fillVars {}  float( self.fillVars[0])  {}   , float( self.fillVars[1])  {}, subjet tau21 {}".format( self.fillVars, float( self.fillVars[0]) , float( self.fillVars[1]), float( b.ak8SDsubjet0tau21 ) )    
            self.TTreeWeights.Fill()
            self.TTreeSemiLept.Fill()

    def close( self ) :
        '''
        Wrap it up. 
        '''

        #self.TTreeWeights.Write()
        #self.TTreeSemiLeptSkim.Write()
        
        self.outfile.cd() 
        self.outfile.Write()
        self.outfile.Close()


'''
        Executable
'''
if __name__ == "__main__" :
    r = RunSemiLepTTbar_HighMass(sys.argv)
    r.run()

