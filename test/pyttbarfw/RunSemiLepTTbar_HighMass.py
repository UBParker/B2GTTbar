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
                          default = 0.7,
                          help='Tau 21 cut')

        parser.add_option('--tau32Cut', type='float', action='store',
                          dest='tau32Cut',
                          default = 0.69,
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

        self.outfile = ROOT.TFile(options.outfile, "RECREATE")

        ### Create the tree class. This will make simple class members for each
        ### of the branches that we want to read from the Tree to save time.
        ### Also saved are some nontrivial variables that involve combinations
        ### of things from the tree
        self.treeobj = B2GTTreeSemiLep( options )

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


        self.AK8puppitau21Hist = []
        self.AK8puppitau32Hist = []

        self.AK8EtaHist = []
        self.AK8MHist = []
        self.AK8MSDHist = []
        self.AK8SDRhoRatioHist = []


        self.AK8MSDSJ0Hist = []
        self.AK8SDSJ0PtHist = []      
            
        self.lepNames = ['Electron', 'Muon' ]
        
        
        # Create histos for type 1 selection binned by pt of leading SD subjet
        self.AK8MPtBinnedHistList = [[], [] ,[], [] , []]
        self.AK8MSDPtBinnedHistList = [[], [] ,[], [] , []]
        self.AK8MSDSJ0PtBinnedHistList = [[], [] ,[], [] , []]
        self.AK8MSDSJ1PtBinnedHistList = [[], [] ,[], [] , []]
        '''
        for iptbin, ptbin in enumerate(b.ak8Jet_Ptbins) :
            if iptbin < 5:
                self.AK8MPtBinnedHistList.append([])
                self.AK8MSDPtBinnedHistList.append([])
                self.AK8MSDSJ0PtBinnedHistList.append([])
                self.AK8MSDSJ1PtBinnedHistList.append([])
        '''
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
            self.AK8SDPtResponse.append([])
            self.AK8SDSJ0PtHist.append( [])
            self.AK8EtaHist.append([])      
            self.AK8puppitau21Hist.append([])
            self.AK8puppitau32Hist.append([])
            

            self.AK8MHist.append( [] )
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
                    if self.verbose: print"self.AK8MPtBinnedHistList {} of length {}".format(self.AK8MPtBinnedHistList, len(self.AK8MPtBinnedHistList))
                    self.AK8MPtBinnedHistList[iptbin].append( [] )
                    self.AK8MSDPtBinnedHistList[iptbin].append( [] )
                    self.AK8MSDSJ0PtBinnedHistList[iptbin].append( [] )
                    self.AK8MSDSJ1PtBinnedHistList[iptbin].append( [] )
            
            for ival in xrange(self.nstages):
                self.RunNumberHist[ilep].append( ROOT.TH1F("RunNumberHist" + self.lepNames[ilep] + str(ival) , "Run Number for lepton "+self.lepNames[ilep] + str(ival), 286591, 0, 286591) )
                self.WeightHist[ilep].append( ROOT.TH1F("WeightHist" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8PtHist[ilep].append( ROOT.TH1F("AK8PtHist" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8HTHist[ilep].append( ROOT.TH1F("AK8HTHist" +  self.lepNames[ilep] + str(ival), "Jet H_{T}, Stage " + self.lepNames[ilep] + str(ival), 4000, 0, 4000) )
                self.AK8SDPtHist[ilep].append( ROOT.TH1F("AK8SDPtHist" +  self.lepNames[ilep] + str(ival), "Jet SD p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8PuppiSDPtHist[ilep].append( ROOT.TH1F("AK8PuppiSDPtHist" +  self.lepNames[ilep] + str(ival), "Jet Puppi SD p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8PuppiPtHist[ilep].append( ROOT.TH1F("AK8PuppiPtHist" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )

                self.AK8PuppiSDPtResponse[ilep].append( ROOT.TH1F("AK8PuppiSDPtResponse" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )
                self.AK8SDPtResponse[ilep].append( ROOT.TH1F("AK8SDPtResponse" +  self.lepNames[ilep] + str(ival), "Jet p_{T}, Stage " + self.lepNames[ilep] + str(ival), 1000, 0, 1000) )

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
                


    def fill( self, index ) :
        '''
        Fill the histograms we're interested in. If you're doing something complicated, make a
        member variable in the Selector class to cache the variable and just fill here. 
        '''
        a = self.lepSelection
        b = self.hadSelection 
        ilep = a.tree.LeptonIsMu[0]     
        if self.verbose: print 'ilep = ', ilep       

        ### Define the weights used for histo filling
        self.theWeight = a.theWeight
        self.EventWeight =  a.EventWeight
        self.PUWeight = a.PUWeight
        self.TriggEffIs  = a.TriggEffIs
        self.CutIDScaleFIs = a.CutIDScaleFIs
        self.CutIDScaleFLooseIs = a.CutIDScaleFLooseIs
        self.MuonHIPScaleFIs = a.MuonHIPScaleFIs
        self.BtagWeight =  a.BtagWeight

        self.theWeight = 1.

        '''
        #if self.verbose and index == 0 : print "Event weight {0:2.4f} * PU weight {1:2.4f} *Trigger Eff. {2:2.4f} * Cut ID {3:2.4f} * HIP SF {4:2.4f} * Btag SF {5:2.4f} * self.CutIDScaleFLooseIs {6:2.4f}".format(self.EventWeight , self.PUWeight , self.TriggEffIs , self.CutIDScaleFIs, self.MuonHIPScaleFIs, self.BtagWeight, self.CutIDScaleFLooseIs)

        ### The total weight depends on the stage of selection
        #self.theWeight =  self.EventWeight * self.PUWeight
        ### Before all selection (LooseID is applied)
        if index == 0: 
            self.theWeight =  self.EventWeight * self.PUWeight * self.CutIDScaleFLooseIs
            if self.verbose : print "theWeight for stage {} is : {} =  self.EventWeight {} * self.PUWeight{} * self.CutIDScaleFLooseIs {}".format(index ,self.theWeight,  self.EventWeight , self.PUWeight , self.CutIDScaleFLooseIs)
        ### Trigger
        if index == 1: 
            self.theWeight =  self.EventWeight * self.PUWeight * self.TriggEffIs * self.CutIDScaleFLooseIs
            if self.verbose : print "theWeight for stage {} is : {} =  self.EventWeight {} * self.PUWeight {} * self.TriggEffIs {} *self.CutIDScaleFLooseIs {}".format(index ,self.theWeight,  self.EventWeight , self.PUWeight ,self.TriggEffIs,  self.CutIDScaleFLooseIs)
        if index == 2: 
            self.theWeight =  self.EventWeight * self.PUWeight * self.TriggEffIs * self.CutIDScaleFLooseIs
            if self.verbose : print "theWeight for stage {} is : {}".format(index ,self.theWeight)
        ### Cut based ID
        if index == 3: 
            self.theWeight =  self.EventWeight * self.PUWeight * self.TriggEffIs  * self.CutIDScaleFIs
            if self.verbose : print "theWeight for stage {} is : {}".format(index ,self.theWeight)
        ### HighPt ID
        if index == 4: 
            self.theWeight =  self.EventWeight * self.PUWeight * self.TriggEffIs  * self.CutIDScaleFIs *self.MuonHIPScaleFIs
            if self.verbose : print "theWeight for stage {} is : {}".format(index ,self.theWeight)
        ### B tag SF
        if index == 12: 
            self.theWeight =  self.EventWeight * self.PUWeight * self.TriggEffIs  * self.CutIDScaleFIs *self.MuonHIPScaleFIs * self.BtagWeight
            if self.verbose : print "theWeight for stage {} is : {}".format(index ,self.theWeight)
        #if self.verbose : print "Event weight {1:2.4f} * PU weight {2:2.4f} *Trigger Eff. {3:2.4f} * Cut ID {4:2.4f} * HIP SF {5:2.4f} * Btag SF {6:2.4f}".format(self.EventWeight , self.PUWeight , self.TriggEffIs , self.CutIDScaleFIs, self.MuonHIPScaleFIs, self.BtagWeight)


        #self.hCutFlow[ilep][index].Fill(self.passedCutCount[ilep][index])
        self.WeightHist[ilep][index].Fill(self.theWeight )
        '''
        if a.runNum > 0. :
            if self.verbose: print"run number is filled as {}".format(a.runNum)
            self.RunNumberHist[ilep][index].Fill(a.runNum)
        if a.theWeight > -1. :
            self.WeightHist[ilep][index].Fill(a.theWeight)
            
        if b.ak8JetP4 != None :
            self.AK8PtHist[ilep][index].Fill( b.ak8JetP4.Perp()* b.PtSmear   , self.theWeight )  ### TO-DO : Implement Pt smear in hadselection and replace 1.000 with b.PtSmear
            self.AK8HTHist[ilep][index].Fill( b.ak8JetHT  , self.theWeight )
            if b.ak8SDJetP4 != None and b.SDptGenpt != None :
                self.AK8SDPtResponse[ilep][index].Fill( b.SDptGenpt , b.ak8JetP4.Perp() * b.PtSmear )    

        if b.ak8SDJetP4 != None :
            self.AK8SDPtHist[ilep][index].Fill( b.ak8SDJetP4.Perp() * b.PtSmear  , self.theWeight )
            self.AK8MSDHist[ilep][index].Fill( b.ak8PuppiSD_m  , self.theWeight )

        if b.ak8PuppiJetP4 != None :
            self.AK8PuppiPtHist[ilep][index].Fill( b.ak8PuppiJetP4.Perp() * b.PuppiPtSmear  , self.theWeight )
            self.AK8EtaHist[ilep][index].Fill( b.ak8PuppiJetP4.Eta()  , self.theWeight )
            self.AK8puppitau21Hist[ilep][index].Fill( b.puppitau21  , self.theWeight )
            self.AK8puppitau32Hist[ilep][index].Fill( b.puppitau32  , self.theWeight )

            self.AK8MHist[ilep][index].Fill( b.ak8_Puppim  , self.theWeight )
            if b.ak8PuppiSDJetP4 != None :
                if b.ak8PuppiJetP4  != None and b.SDptPuppipt != None :
                    self.AK8PuppiSDPtResponse[ilep][index].Fill(b.SDptPuppipt  , b.ak8PuppiJetP4.Perp() )# * b.PuppiPtSmear )  

        if  b.SDRhoRatio  != None :
            self.AK8SDRhoRatioHist[ilep][index].Fill(b.SDRhoRatio  , self.theWeight ) 


        if b.ak8PuppiSDJetP4 != None :
            self.AK8PuppiSDPtHist[ilep][index].Fill( b.ak8PuppiSDJetP4.Perp() * b.PuppiPtSmear  , self.theWeight )
            self.AK8SDSJ0PtHist[ilep][index].Fill( b.ak8PuppiSDJetP4_Subjet0.Perp() * b.PuppiPtSmear  , self.theWeight )
            self.AK8MSDSJ0Hist[ilep][index].Fill( b.ak8SDsj0_m  , self.theWeight )


            # Filling jet mass histos binned by pt of the leading SD subjet

            # self.ak8Jet_Ptbins = [200., 300., 400., 500., 800., 1000.]
            
            for iptbin, ptbin in enumerate(b.ak8Jet_Ptbins) :
                if iptbin < 4:
                    thePthist = self.AK8MPtBinnedHistList[iptbin]
                    theSDPthist = self.AK8MSDPtBinnedHistList[iptbin]
                    theSDsj0Pthist = self.AK8MSDSJ0PtBinnedHistList[iptbin]
                    theSDsj1Pthist = self.AK8MSDSJ1PtBinnedHistList[iptbin]


                    if  b.ak8PuppiJetP4_Binned[iptbin].M() > 0 :
                        thePthist[ilep][index].Fill( b.ak8PuppiJetP4_Binned[iptbin].M()  , self.theWeight )
                        theSDPthist[ilep][index].Fill(  b.ak8PuppiSDJetP4_Binned[iptbin].M() , self.theWeight )
                    if  b.ak8PuppiSDJetP4Subjet0PuppiCorrMass_Binned[iptbin]  > 0 :
                        theSDsj0Pthist[ilep][index].Fill(  b.ak8PuppiSDJetP4Subjet0PuppiCorrMass_Binned[iptbin] , self.theWeight )
                        theSDsj1Pthist[ilep][index].Fill(  b.ak8PuppiSDJetP4Subjet1PuppiCorrMass_Binned[iptbin] , self.theWeight )

            
        if a.leptonP4 != None : 
            self.LeptonPtHist[ilep][index].Fill( a.leptonP4.Perp()  , self.theWeight )
            self.LeptonEtaHist[ilep][index].Fill( a.leptonP4.Eta()  , self.theWeight )
            self.METPtHist[ilep][index].Fill( a.nuP4.Perp() , self.theWeight  )
            self.HTLepHist[ilep][index].Fill( a.leptonP4.Perp() + a.nuP4.Perp()  , self.theWeight )
            if a.ak4Jet != None : 
                self.Iso2DHist[ilep][index].Fill( a.leptonP4.Perp( a.ak4Jet.Vect() ), a.leptonP4.DeltaR( a.ak4Jet )  , self.theWeight  )
                self.AK4BdiscHist[ilep][index].Fill(b.ak4JetBdisc , self.theWeight)




    def close( self ) :
        '''
        Wrap it up. 
        '''
        self.outfile.cd() 
        self.outfile.Write()
        self.outfile.Close()


'''
        Executable
'''
if __name__ == "__main__" :
    r = RunSemiLepTTbar_HighMass(sys.argv)
    r.run()
