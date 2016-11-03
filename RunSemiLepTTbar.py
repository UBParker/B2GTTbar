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
                          default = 0.4,
                          help='Tau 21 cut')

        parser.add_option('--tau32Cut', type='float', action='store',
                          dest='tau32Cut',
                          default = 0.69,
                          help='Tau 32 cut')
        
        parser.add_option('--bdiscmin', type='float', action='store',
                          dest='bdiscmin',
                          default = 0.8,
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

        ### Here is the semileptonic ttbar selection for W jets
        if options.Type2 :
            self.lepSelection = B2GSelectSemiLepTTbar_IsoStd.B2GSelectSemiLepTTbar_IsoStd( options, self.treeobj )
            self.hadSelection = B2GSelectSemiLepTTbar_Type2.B2GSelectSemiLepTTbar_Type2( options, self.treeobj, self.lepSelection )
        else :
            self.lepSelection = B2GSelectSemiLepTTbar_Iso2D.B2GSelectSemiLepTTbar_Iso2D( options, self.treeobj )
            self.hadSelection = B2GSelectSemiLepTTbar_Type1.B2GSelectSemiLepTTbar_Type1( options, self.treeobj, self.lepSelection )
        self.nstages = self.lepSelection.nstages + self.hadSelection.nstages

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

        self.AK8MPt200To300Hist = []
        self.AK8MSDPt200To300Hist = []
        self.AK8MSDSJ0Pt200To300Hist = []

        self.AK8MPt300To400Hist = []
        self.AK8MSDPt300To400Hist = []
        self.AK8MSDSJ0Pt300To400Hist = []

        self.AK8MPt400To500Hist = []
        self.AK8MSDPt400To500Hist = []
        self.AK8MSDSJ0Pt400To500Hist = []

        self.AK8MPt500To800Hist = []
        self.AK8MSDPt500To800Hist = []
        self.AK8MSDSJ0Pt500To800Hist = []

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

            # Create histos for type 1 selection binned by pt of leading SD subjet 
            self.AK8MPt200To300Hist.append( ROOT.TH1F("AK8MPt200To300Hist" +  str(ival), "Jet Mass, Stage " + str(ival), 1000, 0, 500) )
            self.AK8MSDPt200To300Hist.append( ROOT.TH1F("AK8MSDPt200To300Hist" +  str(ival), "Jet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )
            self.AK8MSDSJ0Pt200To300Hist.append( ROOT.TH1F("AK8MSDSJ0Pt200To300Hist" +  str(ival), "Leading Subjet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )

            self.AK8MPt300To400Hist.append( ROOT.TH1F("AK8MPt300To400Hist" +  str(ival), "Jet Mass, Stage " + str(ival), 1000, 0, 500) )
            self.AK8MSDPt300To400Hist.append( ROOT.TH1F("AK8MSDPt300To400Hist" +  str(ival), "Jet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )
            self.AK8MSDSJ0Pt300To400Hist.append( ROOT.TH1F("AK8MSDSJ0Pt300To400Hist" +  str(ival), "Leading Subjet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )

            self.AK8MPt400To500Hist.append( ROOT.TH1F("AK8MPt400To500Hist" +  str(ival), "Jet Mass, Stage " + str(ival), 1000, 0, 500) )
            self.AK8MSDPt400To500Hist.append( ROOT.TH1F("AK8MSDPt400To500Hist" +  str(ival), "Jet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )
            self.AK8MSDSJ0Pt400To500Hist.append( ROOT.TH1F("AK8MSDSJ0Pt400To500Hist" +  str(ival), "Leading Subjet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )

            self.AK8MPt500To800Hist.append( ROOT.TH1F("AK8MPt500To800Hist" +  str(ival), "Jet Mass, Stage " + str(ival), 1000, 0, 500) )
            self.AK8MSDPt500To800Hist.append( ROOT.TH1F("AK8MSDPt500To800Hist" +  str(ival), "Jet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )
            self.AK8MSDSJ0Pt500To800Hist.append( ROOT.TH1F("AK8MSDSJ0Pt500To800Hist" +  str(ival), "Leading Subjet Soft Dropped Mass, Stage " + str(ival), 1000, 0, 500) )

            
            self.hCutFlow.append(ROOT.TH1F("hCutFlow" +  str(ival), " ;Stage " +  str(ival)+" of Selection; Events passing cuts ", 1, 0, 2 ) )

            self.WeightHist.append( ROOT.TH1F("WeightHist" +  str(ival), "Total Weight, Stage " + str(ival), 1000, -1.,2.) )

    def fill( self, index ) :
        '''
        Fill the histograms we're interested in. If you're doing something complicated, make a
        member variable in the Selector class to cache the variable and just fill here. 
        '''
        a = self.lepSelection
        b = self.hadSelection 

        #self.totalWeight = a.theWeight #* b.BtagWeight
        #print "totalweight is : {}".format(self.totalWeight)

        self.hCutFlow[index].Fill(self.passedCutCount[index])
        self.WeightHist[index].Fill(a.theWeight )

        self.ak8Jet = None
        self.ak8JetRaw = None

        self.ak8SDJet = None
        self.ak8SDJetRaw = None

        self.ak8PuppiJet = None
        self.ak8PuppiJetRaw = None

        self.ak8PuppiSDJet = None
        self.ak8PuppiSDJetRaw = None


        if b.ak8Jet != None :
            self.AK8PtHist[index].Fill( b.ak8Jet.Perp()  , a.theWeight )
            self.AK8HTHist[index].Fill( b.ak8JetHT  , a.theWeight )
            self.AK8Tau32Hist[index].Fill( b.tau32  , a.theWeight )
            self.AK8Tau21Hist[index].Fill( b.tau21  , a.theWeight )
            if b.ak8SDJet != None and b.SDptGenpt != None :
                self.AK8SDPtResponse[index].Fill( b.SDptGenpt , b.ak8Jet.Perp() )    

        if b.ak8SDJet != None :
            self.AK8SDPtHist[index].Fill( b.ak8SDJet.Perp()  , a.theWeight )

        if b.ak8PuppiJet != None :
            self.AK8PtHist[index].Fill( b.ak8PuppiJet.Perp()  , a.theWeight )

        if b.ak8PuppiJet != None :
            self.AK8PuppiPtHist[index].Fill( b.ak8PuppiJet.Perp()  , a.theWeight )
            self.AK8SDSJ0PtHist[index].Fill( b.ak8PuppiSDJet_Subjet0.Perp()  , a.theWeight )
            self.AK8EtaHist[index].Fill( b.ak8PuppiJet.Eta()  , a.theWeight )
            self.AK8puppitau21Hist[index].Fill( b.puppitau21  , a.theWeight )
            self.AK8puppitau32Hist[index].Fill( b.puppitau32  , a.theWeight )

            self.AK8MHist[index].Fill( b.ak8_Puppim  , a.theWeight )
            if b.ak8PuppiSDJet != None :
                if b.ak8PuppiJet != None and b.SDptPuppipt != None :
                    self.AK8PuppiSDPtResponse[index].Fill(b.SDptPuppipt  , b.ak8PuppiJet.Perp() )  

        if b.ak8PuppiSDJet != None :
            self.AK8MSDHist[index].Fill( b.ak8PuppiSD_m  , a.theWeight )
            if  b.SDRhoRatio  != None :
                self.AK8SDRhoRatioHist[index].Fill(b.SDRhoRatio  , a.theWeight ) 

            self.AK8MSDSJ0Hist[index].Fill( b.ak8SDsj0_m  , a.theWeight )


            # Filling jet mass histos binned by pt of the leading SD subjet
            if  b.ak8PuppiJet200.M() > 0.0001:
                self.AK8MPt200To300Hist[index].Fill( b.ak8PuppiJet200.M()  , a.theWeight )
                self.AK8MSDPt200To300Hist[index].Fill( b.ak8PuppiSDJet200.M()  , a.theWeight )
            if  b.ak8SDsj0_m200 > 0.0001:
                self.AK8MSDSJ0Pt200To300Hist[index].Fill(  b.ak8SDsj0_m200 , a.theWeight )

            if  b.ak8PuppiJet300.M() > 0.0001:
                self.AK8MPt300To400Hist[index].Fill( b.ak8PuppiJet300.M()  , a.theWeight )
                self.AK8MSDPt300To400Hist[index].Fill( b.ak8PuppiSDJet300.M()  , a.theWeight )
            if  b.ak8SDsj0_m300 > 0.0001:
                self.AK8MSDSJ0Pt300To400Hist[index].Fill(  b.ak8SDsj0_m300 , a.theWeight )

            if  b.ak8PuppiJet400.M() > 0.0001:
                self.AK8MPt400To500Hist[index].Fill(  b.ak8PuppiJet400.M()  , a.theWeight )
                self.AK8MSDPt400To500Hist[index].Fill( b.ak8PuppiSDJet400.M()  , a.theWeight )
            if  b.ak8SDsj0_m400 > 0.0001:
                self.AK8MSDSJ0Pt400To500Hist[index].Fill(  b.ak8SDsj0_m400 , a.theWeight )

            if  b.ak8PuppiJet500.M() > 0.0001:
                self.AK8MPt500To800Hist[index].Fill( b.ak8PuppiJet500.M()  , a.theWeight )
                self.AK8MSDPt500To800Hist[index].Fill( b.ak8PuppiSDJet500.M()  , a.theWeight )
            if  b.ak8SDsj0_m500 > 0.0001:
                self.AK8MSDSJ0Pt500To800Hist[index].Fill(  b.ak8SDsj0_m500 , a.theWeight )


        if a.leptonP4 != None : 
            self.LeptonPtHist[index].Fill( a.leptonP4.Perp()  , a.theWeight )
            self.LeptonEtaHist[index].Fill( a.leptonP4.Eta()  , a.theWeight )
            self.METPtHist[index].Fill( a.nuP4.Perp() , a.theWeight  )
            self.HTLepHist[index].Fill( a.leptonP4.Perp() + a.nuP4.Perp()  , a.theWeight )
            if a.ak4Jet0 != None : 
                self.Iso2DHist[index].Fill( a.leptonP4.Perp( a.ak4Jet0.Vect() ), a.leptonP4.DeltaR( a.ak4Jet0 )  , a.theWeight  )
                self.AK4BdiscHist[index].Fill(b.ak4JetBdisc , a.theWeight)





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
