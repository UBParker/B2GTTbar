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
import B2GSelectSemiLepTTbar_Type2, B2GSelectSemiLepTTbar_IsoStd , B2GSelectSemiLepTTbar_Type1, B2GSelectSemiLepTTbar_Iso2D

import time as time
import ROOT


class RunSemiLepTTbar(OptionParser) :
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

        parser.add_option('--maxevents', type='int', action='store',
                          default=-1,
                          dest='maxevents',
                          help='Number of events to run. -1 is all events')

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

        parser.add_option('--ignoreTrig', action='store_true',
                          dest='ignoreTrig',
                          default = False,
                          help='Ignore the trigger?')
        
        parser.add_option('--Type2', action='store_true',
                          default=False,
                          dest='Type2',
                          help='Do you want to apply selection for type 2 tops as described in AN-16-215 ?')

        parser.add_option('--verbose', action='store_true',
                          default=False,
                          dest='verbose',
                          help='Do you want to print values of key variables?')

        (options, args) = parser.parse_args(argv)
        argv = []

        self.startTime = time.time()


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
        self.eventsToRun = entries

        ### Create empty weights used for histo filling
        ### The total weight
        self.theWeight = 1.
        self.EventWeight = None
        self.PUWeight = None
        self.TriggEffIs  = None
        self.CutIDScaleFIs = None 
        self.MuonHIPScaleFIs = None 


        ### Here is the semileptonic ttbar selection for W jets
        if options.Type2 :
            self.lepSelection = B2GSelectSemiLepTTbar_IsoStd.B2GSelectSemiLepTTbar_IsoStd( options, self.treeobj )
            self.hadSelection = B2GSelectSemiLepTTbar_Type2.B2GSelectSemiLepTTbar_Type2( options, self.treeobj, self.lepSelection )
        else :
            self.lepSelection = B2GSelectSemiLepTTbar_Iso2D.B2GSelectSemiLepTTbar_Iso2D( options, self.treeobj )
            self.hadSelection = B2GSelectSemiLepTTbar_Type1.B2GSelectSemiLepTTbar_Type1( options, self.treeobj, self.lepSelection )
        self.nstages = self.lepSelection.nstages + self.hadSelection.nstages


        ### TO-DO: Apply additional 1.5% systematic uncertainty to account for SFs and efficiencies 

        ### Array to count events passing each stage 
        self.passedCutCount = [] 
        for count in xrange(0, self.lepSelection.nstages):
            self.passedCutCount.append(    self.lepSelection.passedCount[count]            )
        for count in xrange(0, self.hadSelection.nstages):
            self.passedCutCount.append(    self.hadSelection.passedCount[count]            )


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
     
        if self.maxevents > 0. :
            self.eventsToRun = self.maxevents
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
        '''
        Book histograms, one for each stage of the selection. 
        '''
        self.outfile.cd()

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
        self.AK8Tau21Hist      = []
        self.AK8Tau32Hist      = []

        self.AK8EtaHist = []
        self.AK8MHist = []
        self.AK8MSDHist = []
        self.AK8SDRhoRatioHist = []


        self.AK8MSDSJ0Hist = []
        self.AK8SDSJ0PtHist = []          

        # Create histos for type 1 selection binned by pt of leading SD subjet 
        b = self.hadSelection 
        #self.ak8Jet_Ptbins = [200, 300, 400, 500, 800, 1000]
        self.AK8MPtBinnedHistList = []* len(b.ak8Jet_Ptbins)
        self.AK8MSDPtBinnedHistList = [] * len(b.ak8Jet_Ptbins)
        self.AK8MSDSJ0PtBinnedHistList = [] * len(b.ak8Jet_Ptbins)
        self.AK8MSDSJ1PtBinnedHistList = [] * len(b.ak8Jet_Ptbins)
        ### ^^^ Check this, may be wrong

        ### Cut-Flow Histogram with number of events passing each cut
        self.hCutFlow = []
 
        ### Weights histogram with total weight applied to the event when filling histograms
        self.WeightHist = []

        ### List of all histograms
        self.hists = []

        for ival in xrange(self.nstages):
            self.AK8PtHist.append( ROOT.TH1F("AK8PtHist" +  str(ival), "Jet p_{T}, Stage " + str(ival), 1000, 0, 1000) )
            self.AK8HTHist.append( ROOT.TH1F("AK8HTHist" +  str(ival), "Jet H_{T}, Stage " + str(ival), 4000, 0, 4000) )
            self.AK8SDPtHist.append( ROOT.TH1F("AK8SDPtHist" +  str(ival), "Jet SD p_{T}, Stage " + str(ival), 1000, 0, 1000) )
            self.AK8PuppiSDPtHist.append( ROOT.TH1F("AK8PuppiSDPtHist" +  str(ival), "Jet Puppi SD p_{T}, Stage " + str(ival), 1000, 0, 1000) )
            self.AK8PuppiPtHist.append( ROOT.TH1F("AK8PuppiPtHist" +  str(ival), "Jet p_{T}, Stage " + str(ival), 1000, 0, 1000) )

            self.AK8PuppiSDPtResponse.append( ROOT.TH1F("AK8PuppiSDPtResponse" +  str(ival), "Jet p_{T}, Stage " + str(ival), 1000, 0, 1000) )
            self.AK8SDPtResponse.append( ROOT.TH1F("AK8SDPtResponse" +  str(ival), "Jet p_{T}, Stage " + str(ival), 1000, 0, 1000) )

            self.AK8SDSJ0PtHist.append( ROOT.TH1F("AK8SDSJ0PtHist" +  str(ival), "SD subjet 0 P_{T}, Stage " + str(ival), 1000, 0, 1000) )
            self.AK8EtaHist.append( ROOT.TH1F("AK8EtaHist" +  str(ival), "Jet #eta, Stage " + str(ival), 1000, -2.5, 2.5) )
            self.AK8puppitau21Hist.append( ROOT.TH1F("AK8puppitau21Hist" +  str(ival), "Jet #tau_{21}, Stage " + str(ival), 1000, 0., 1.) )
            self.AK8puppitau32Hist.append( ROOT.TH1F("AK8puppitau32Hist" +  str(ival), "Jet #tau_{32}, Stage " + str(ival), 1000, 0., 1.) )
            self.AK8Tau21Hist.append( ROOT.TH1F("AK8Tau21Hist" +  str(ival), "Jet #tau_{21}, Stage " + str(ival), 1000, 0., 1.) )
            self.AK8Tau32Hist.append( ROOT.TH1F("AK8Tau32Hist" +  str(ival), "Jet #tau_{32}, Stage " + str(ival), 1000, 0., 1.) )


            self.AK8MHist.append( ROOT.TH1F("AK8MHist" +  str(ival), "Jet Mass, Stage " + str(ival), 1000, 0, 500) )
            self.AK8MSDHist.append( ROOT.TH1F("AK8MSDHist" +  str(ival), "Jet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )
            self.AK8SDRhoRatioHist.append( ROOT.TH1F("AK8SDRhoRatioHist" +  str(ival), "SD Rho Ratio, Stage " + str(ival), 1000, 0., 1.) )
            self.AK8MSDSJ0Hist.append( ROOT.TH1F("AK8MSDSJ0Hist" +  str(ival), "Leading Subjet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )

            self.LeptonPtHist.append( ROOT.TH1F("LeptonPtHist" +  str(ival), "Lepton p_{T}, Stage " + str(ival), 1000, 0, 1000) )
            self.LeptonEtaHist.append( ROOT.TH1F("LeptonEtaHist" +  str(ival), "Lepton #eta, Stage " + str(ival), 1000, -2.5, 2.5) )

            self.METPtHist.append( ROOT.TH1F("METPtHist" +  str(ival), "Missing p_{T}, Stage " + str(ival), 1000, 0, 1000) )
            self.HTLepHist.append( ROOT.TH1F("HTLepHist" +  str(ival), "Lepton p_{T} + Missing p_{T}, Stage " + str(ival), 1000, 0, 1000) )
            self.Iso2DHist.append ( ROOT.TH2F("Iso2DHist" +  str(ival), "Lepton 2D isolation (#Delta R vs p_{T}^{REL} ), Stage " + str(ival), 25, 0, 500, 25, 0, 1) )
            self.AK4BdiscHist.append( ROOT.TH1F("AK4BdiscHist" +  str(ival), "CSVv2 B disc , Stage " + str(ival), 1000, 0., 1.) )

            for iptbin, ptbin in enumerate(b.ak8Jet_Ptbins) :
                if iptbin < 4:
                    self.AK8MPtBinnedHistList.append( ROOT.TH1F("AK8MPt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  str(ival), "Jet Mass, Stage " + str(ival), 1000, 0, 500) )
                    self.AK8MSDPtBinnedHistList.append( ROOT.TH1F("AK8MSDPt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  str(ival), "Jet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )
                    self.AK8MSDSJ0PtBinnedHistList.append( ROOT.TH1F("AK8MSDSJ0Pt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  str(ival), "Leading Subjet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )
                    self.AK8MSDSJ1PtBinnedHistList.append( ROOT.TH1F("AK8MSDSJ1Pt%sTo%sHist"%(ptbin, b.ak8Jet_Ptbins[iptbin+1]) +  str(ival), "Sub-Leading Subjet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )
            
            self.hCutFlow.append(ROOT.TH1F("hCutFlow" +  str(ival), " ;Stage " +  str(ival)+" of Selection; Events passing cuts ", 1, 0, 2 ) )

            self.WeightHist.append( ROOT.TH1F("WeightHist" +  str(ival), "Total Weight, Stage " + str(ival), 1000, -1.,2.) )

    def fill( self, index ) :
        '''
        Fill the histograms we're interested in. If you're doing something complicated, make a
        member variable in the Selector class to cache the variable and just fill here. 
        '''
        a = self.lepSelection
        b = self.hadSelection 

        ### Define the weights used for histo filling
        self.EventWeight = 1. # self.lepSelection.EventWeight
        self.PUWeight = 1. #self.lepSelection.PUWeight
        self.TriggEffIs  = 1.#self.lepSelection.TriggEffIs
        self.CutIDScaleFIs = 1.#self.lepSelection.CutIDScaleFIs
        self.CutIDScaleFLooseIs = 1.#self.lepSelection.CutIDScaleFLooseIs
        self.MuonHIPScaleFIs = 1.#self.lepSelection.MuonHIPScaleFIs
        self.BtagWeight =  1.#self.lepSelection.BtagWeight
        print "ERROR: All weights set to 1. To-Do: Implement weights in leptonic selection,"
        ####   FIXXX   THIS

        if self.verbose and index == 0 : print "Event weight {0:2.4f} * PU weight {1:2.4f} *Trigger Eff. {2:2.4f} * Cut ID {3:2.4f} * HIP SF {4:2.4f} * Btag SF {5:2.4f} * self.CutIDScaleFLooseIs {6:2.4f}".format(self.EventWeight , self.PUWeight , self.TriggEffIs , self.CutIDScaleFIs, self.MuonHIPScaleFIs, self.BtagWeight, self.CutIDScaleFLooseIs)

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


        self.hCutFlow[index].Fill(self.passedCutCount[index])
        self.WeightHist[index].Fill(self.theWeight )

        self.ak8JetP4 = None
        self.ak8JetP4Raw = None

        self.ak8SDJetP4 = None
        self.ak8SDJetP4Raw = None

        self.ak8PuppiJetP4 = None
        self.ak8PuppiJetP4Raw = None

        self.ak8PuppiSDJetP4 = None
        self.ak8PuppiSDJetP4Raw = None


        if b.ak8JetP4 != None :
            self.AK8PtHist[index].Fill( b.ak8JetP4.Perp()* 1.000  , self.theWeight )  ### TO-DO : Implement Pt smear in hadselection and replace 1.000 with b.PtSmear
            self.AK8HTHist[index].Fill( b.ak8JetHT  , self.theWeight )
            #self.AK8Tau32Hist[index].Fill( b.puppitau32  , self.theWeight )
            #self.AK8Tau21Hist[index].Fill( b.puppitau21  , self.theWeight )
            if b.ak8SDJetP4 != None and b.SDptGenpt != None :
                self.AK8SDPtResponse[index].Fill( b.SDptGenpt , b.ak8JetP4.Perp() )#* b.PtSmear )    

        if b.ak8SDJetP4 != None :
            self.AK8SDPtHist[index].Fill( b.ak8SDJetP4.Perp() * 1.000  , self.theWeight )

        if b.ak8PuppiJetP4 != None :
            self.AK8PuppiPtHist[index].Fill( b.ak8PuppiJetP4.Perp() * 1.000  , self.theWeight ) #  b.PuppiPtSmear
            self.AK8EtaHist[index].Fill( b.ak8PuppiJetP4.Eta()  , self.theWeight )
            self.AK8puppitau21Hist[index].Fill( b.puppitau21  , self.theWeight )
            self.AK8puppitau32Hist[index].Fill( b.puppitau32  , self.theWeight )

            self.AK8MHist[index].Fill( b.ak8_Puppim  , self.theWeight )
            if b.ak8PuppiSDJetP4 != None :
                if b.ak8PuppiJetP4  != None and b.SDptPuppipt != None :
                    self.AK8PuppiSDPtResponse[index].Fill(b.SDptPuppipt  , b.ak8PuppiJetP4.Perp()  ) #* b.PuppiPtSmear )  

        if  b.SDRhoRatio  != None :
            self.AK8SDRhoRatioHist[index].Fill(b.SDRhoRatio  , self.theWeight ) 


        if b.ak8PuppiSDJetP4 != None :
            self.AK8MSDHist[index].Fill( b.ak8PuppiSD_m  , self.theWeight )
            self.AK8PuppiSDPtHist[index].Fill( b.ak8PuppiSDJetP4.Perp() ) #* b.PuppiPtSmear  , self.theWeight )
            self.AK8SDSJ0PtHist[index].Fill( b.ak8PuppiSDJetP4_Subjet0.Perp() ) #* b.PuppiPtSmear  , self.theWeight )
            self.AK8MSDSJ0Hist[index].Fill( b.ak8SDsj0_m  , self.theWeight )


            # Filling jet mass histos binned by pt of the leading SD subjet

            # self.ak8Jet_Ptbins = [200., 300., 400., 500., 800., 1000.]
            '''
            for iptbin, ptbin in enumerate(b.ak8Jet_Ptbins) :
                if iptbin < 4:
                    thePthist = self.AK8MPtBinnedHistList[iptbin]
                    theSDPthist = self.AK8MSDPtBinnedHistList[iptbin]
                    theSDsj0Pthist = self.AK8MSDSJ0PtBinnedHistList[iptbin]
                    theSDsj1Pthist = self.AK8MSDSJ1PtBinnedHistList[iptbin]


                    if  b.ak8PuppiJetP4_Binned[iptbin].M() > 0 :
                        thePthist[index].Fill( b.ak8PuppiJetP4_Binned[iptbin].M()  , self.theWeight )
                        theSDPthist[index].Fill(  b.ak8PuppiSDJetP4_Binned[iptbin].M() , self.theWeight )
                    if  b.ak8PuppiSDJetP4Subjet0PuppiCorrMass_Binned[iptbin]  > 0 :
                        theSDsj0Pthist[index].Fill(  b.ak8PuppiSDJetP4Subjet0PuppiCorrMass_Binned[iptbin] , self.theWeight )
                        theSDsj1Pthist[index].Fill(  b.ak8PuppiSDJetP4Subjet1PuppiCorrMass_Binned[iptbin] , self.theWeight )

            '''
        if a.leptonP4 != None : 
            self.LeptonPtHist[index].Fill( a.leptonP4.Perp()  , self.theWeight )
            self.LeptonEtaHist[index].Fill( a.leptonP4.Eta()  , self.theWeight )
            self.METPtHist[index].Fill( a.nuP4.Perp() , self.theWeight  )
            self.HTLepHist[index].Fill( a.leptonP4.Perp() + a.nuP4.Perp()  , self.theWeight )
            if a.ak4Jet != None : 
                self.Iso2DHist[index].Fill( a.leptonP4.Perp( a.ak4Jet.Vect() ), a.leptonP4.DeltaR( a.ak4Jet )  , self.theWeight  )
                self.AK4BdiscHist[index].Fill(b.ak4JetBdisc , self.theWeight)





    def close( self ) :
        '''
        Wrap it up. 
        '''

        self.ts = (time.time() - self.startTime)

        self.unitIs = 'Seconds'
        if self.ts > 60. :
            self.ts /= 60.
            self.unitIs = 'Minutes'
        if self.ts > 60. :
            self.ts /= 60.
            self.unitIs = 'Hours' 

        print ('The script took {0}  {1}!'.format(   self.ts  , self.unitIs    ) )


        self.outfile.cd() 
        self.outfile.Write()
        self.outfile.Close()


'''
        Executable
'''
if __name__ == "__main__" :
    r = RunSemiLepTTbar(sys.argv)
    r.run()
