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
import B2GSelectSemiLepTTbar_Type2, B2GSelectSemiLepTTbar_IsoStd


import ROOT


class RunSemiLepTTbar() :
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
                          default = 0.7,
                          help='Tau 32 cut')
        
        parser.add_option('--bdiscmin', type='float', action='store',
                          dest='bdiscmin',
                          default = 0.7,
                          help='B discriminator cut')

        parser.add_option('--maxevents', type='int', action='store',
                          dest='maxevents',
                          default = None,
                          help='Maximum number of events')
        
        parser.add_option('--ignoreTrig', action='store_true',
                          dest='ignoreTrig',
                          default = False,
                          help='Ignore the trigger?')
        
        parser.add_option('--verbose', action='store_true',
                          dest='verbose',
                          default = False,
                          help='Verbose information printed')

        (options, args) = parser.parse_args(argv)
        argv = []



        self.outfile = ROOT.TFile(options.outfile, "RECREATE")

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

        ### Here is the semileptonic ttbar selection for W jets
        self.lepSelection = B2GSelectSemiLepTTbar_IsoStd.B2GSelectSemiLepTTbar_IsoStd( options, self.treeobj )
        self.hadSelection = B2GSelectSemiLepTTbar_Type2.B2GSelectSemiLepTTbar_Type2( options, self.treeobj, self.lepSelection )

        self.nstages = self.lepSelection.nstages + self.hadSelection.nstages
        self.nlep = 2 # Electrons and muons

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
            if jentry % 10000 == 0 :
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
        
        self.AK8PtHist = []
        self.AK8EtaHist = []
        self.AK8MHist = []
        self.AK8MSDHist = []
        self.AK8MSDSJ0Hist = []
        self.lepNames = ['Electron', 'Muon' ]

        self.hists = []
        for ilep in xrange(self.nlep) :
            self.AK8PtHist.append([])
            self.AK8EtaHist.append([])
            self.AK8MHist.append([])
            self.AK8MSDHist.append([])
            self.AK8MSDSJ0Hist.append([])

            self.LeptonPtHist.append([])
            self.LeptonEtaHist.append([])

            self.METPtHist.append([])
            self.HTLepHist.append([])
            self.Iso2DHist.append([])

                
            for ival in xrange(self.nstages):
                self.AK8PtHist[ilep].append( ROOT.TH1F("AK8PtHist" + self.lepNames[ilep] + str(ival), "Jet p_{T}, " + self.lepNames[ilep] + ", Stage " + str(ival), 1000, 0, 1000) )
                self.AK8EtaHist[ilep].append( ROOT.TH1F("AK8EtaHist" + self.lepNames[ilep] + str(ival), "Jet #eta, " + self.lepNames[ilep] + ", Stage " + str(ival), 1000, -2.5, 2.5) )
                self.AK8MHist[ilep].append( ROOT.TH1F("AK8MHist" + self.lepNames[ilep] + str(ival), "Jet Mass, " + self.lepNames[ilep] + ", Stage " + str(ival), 1000, 0, 500) )
                self.AK8MSDHist[ilep].append( ROOT.TH1F("AK8MSDHist" + self.lepNames[ilep] + str(ival), "Jet Soft Dropped Mass, " + self.lepNames[ilep] + ", Stage " + str(ival), 1000, 0, 500) )
                self.AK8MSDSJ0Hist[ilep].append( ROOT.TH1F("AK8MSDSJ0Hist" + self.lepNames[ilep] + str(ival), "Leading Subjet Soft Dropped Mass, " + self.lepNames[ilep] + ", Stage " + str(ival), 1000, 0, 500) )

                self.LeptonPtHist[ilep].append( ROOT.TH1F("LeptonPtHist" + self.lepNames[ilep] + str(ival), "Lepton p_{T}, " + self.lepNames[ilep] + ", Stage " + str(ival), 1000, 0, 1000) )
                self.LeptonEtaHist[ilep].append( ROOT.TH1F("LeptonEtaHist" + self.lepNames[ilep] + str(ival), "Lepton #eta, " + self.lepNames[ilep] + ", Stage " + str(ival), 1000, -2.5, 2.5) )

                self.METPtHist[ilep].append( ROOT.TH1F("METPtHist" + self.lepNames[ilep] + str(ival), "Missing p_{T}, " + self.lepNames[ilep] + ", Stage " + str(ival), 1000, 0, 1000) )
                self.HTLepHist[ilep].append( ROOT.TH1F("HTLepHist" + self.lepNames[ilep] + str(ival), "Lepton p_{T} + Missing p_{T}, " + self.lepNames[ilep] + ", Stage " + str(ival), 1000, 0, 1000) )
                self.Iso2DHist[ilep].append ( ROOT.TH2F("Iso2DHist" + self.lepNames[ilep] + str(ival), "Lepton 2D isolation (#Delta R vs p_{T}^{REL} ), " + self.lepNames[ilep] + ", Stage " + str(ival), 25, 0, 500, 25, 0, 1) )

            

    def fill( self, index ) :
        '''
        Fill the histograms we're interested in. If you're doing something complicated, make a
        member variable in the Selector class to cache the variable and just fill here. 
        '''
        a = self.lepSelection
        b = self.hadSelection
        ilep = a.tree.LeptonIsMu[0]
        print 'ilep = ', ilep
        if b.ak8SDJetP4 != None :
            self.AK8PtHist[ilep][index].Fill( b.ak8SDJetP4.Perp() )
            self.AK8EtaHist[ilep][index].Fill( b.ak8SDJetP4.Eta() )
            self.AK8MHist[ilep][index].Fill( b.ak8SDJetP4.M() )
            self.AK8MSDHist[ilep][index].Fill( b.ak8SDJetP4.M() )
            self.AK8MSDSJ0Hist[ilep][index].Fill( b.ak8PuppiSDJetP4_Subjet0.M() )

        if a.leptonP4 != None : 
            self.LeptonPtHist[ilep][index].Fill( a.leptonP4.Perp() )
            self.LeptonEtaHist[ilep][index].Fill( a.leptonP4.Eta() )
            self.METPtHist[ilep][index].Fill( a.nuP4.Perp() )
            self.HTLepHist[ilep][index].Fill( a.leptonP4.Perp() + a.nuP4.Perp() )
            if a.ak4Jet != None : 
                self.Iso2DHist[ilep][index].Fill( a.leptonP4.Perp( a.ak4Jet.Vect() ), a.leptonP4.DeltaR( a.ak4Jet ) )
        ### Fill the ttree
        if index == 12:            
            self.theWeight = 1.0
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
                    #if self.verbose  : print"infile is  {}   Afile is {}".format(self.infile, afile)
                    if afile == self.infile:
                        self.lumiWeight =  self.xSections[ifile] / self.nEvents[ifile] * self.lumi

                        #if self.verboseW : print"lumiweight is {}".format(self.lumiWeight)
            
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
                

            #if self.verboseW : print"FILLLLL--------   self.fillVars {}  float( self.fillVars[0])  {}   , float( self.fillVars[1])  {}, subjet tau21 {}".format( self.fillVars, float( self.fillVars[0]) , float( self.fillVars[1]), float( b.ak8SDsubjet0tau21 ) )    
            self.TTreeWeights.Fill()
            self.TTreeSemiLept.Fill()

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
    r = RunSemiLepTTbar(sys.argv)
    r.run()
