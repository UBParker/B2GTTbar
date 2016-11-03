#! /usr/bin/env python

import ROOT

class B2GSelectSemiLepTTbar_Type1( ) :
    """
    Selects semileptonic ttbar events with widely separated top quarks.
    This selects type 2 top events with traditional lepton isolation.
    """
    def __init__(self, options, tree, lepsel ):
        self.tau21Cut = options.tau21Cut
        self.tau32Cut = options.tau32Cut
        self.bdiscmin = options.bdiscmin
        self.ignoreTrig = options.ignoreTrig
        self.verbose = options.verbose

        self.infile = options.infile
        if self.verbose : print "The infile is : {}".format(self.infile)

        self.nstages = 7
        self.tree = tree
        self.lepsel = lepsel
        self.passed = [False] * self.nstages
        self.passedCount = [0] * self.nstages


        # Stage 0 - Pass Leptonic Selection

        # Stage 1 - AK8 Jet Pt and eta cut
        self.AK8PtCut = 500.
        self.AK8EtaCut = 2.4

        # Stage 2 - AK4 Jet bdisc cut
        # see self.bdiscmin above

        # Stage 3 - AK8 Jet tau32 cut
        #  see self.tau32Cut above

        # Stage 4 - AK8 SD Jet mass cut
        self.minAK8Mass = 110.
        self.maxAK8Mass = 210.

        # Stage 5 - AK8 SD Subjet 0 mass cut
        self.minAK8sjMass = 55.
        self.maxAK8sjMass = 115.

        #Stage 6 - AK8 SD Subjt 0 tau21 cut
        # see self.tau21Cut above


        # Cached class member variables for plotting

        self.ak8Jet = None
        self.ak8JetRaw = None

        self.ak8SDJet = None
        self.ak8SDJetRaw = None

        self.ak8PuppiJet = None
        self.ak8PuppiJetRaw = None

        self.ak8PuppiSDJet = None
        self.ak8PuppiSDJetRaw = None

        self.puppitau32 = None
        self.puppitau21 = None
        self.tau32      = None
        self.tau21      = None

        self.ak8PuppiSDJet_Subjet0 = None
        self.ak8PuppiSDJet_Subjet1 = None
        self.ak8PuppiSDJet_Subjet0Raw = None
        self.ak8PuppiSDJet_Subjet1Raw = None

        self.ak8PuppiJet200 = None
        self.ak8PuppiSDJet200 =  None
        self.ak8PuppiSDJet_Subjet0M200 =  None
        self.ak8PuppiSDJet_Subjet1M200 =  None

        self.ak8PuppiJet300 = None
        self.ak8PuppiSDJet300 =  None
        self.ak8PuppiSDJet_Subjet0M300 =  None
        self.ak8PuppiSDJet_Subjet1M300 =  None

        self.ak8PuppiJet400 = None
        self.ak8PuppiSDJet400 =  None
        self.ak8PuppiSDJet_Subjet0M400 =  None
        self.ak8PuppiSDJet_Subjet1M400 =  None

        self.ak8PuppiJet500 = None
        self.ak8PuppiSDJet500 =  None
        self.ak8PuppiSDJet_Subjet0M500 =  None
        self.ak8PuppiSDJet_Subjet1M500 =  None

        self.ak8PuppiJet600 = None
        self.ak8PuppiSDJet600 =  None
        self.ak8PuppiSDJet_Subjet0M600 =  None
        self.ak8PuppiSDJet_Subjet1M600 =  None

        self.ak4Jet = None
        self.ak4JetBdisc = None        

        self.ak8SDsubjet0tau1 = None
        self.ak8SDsubjet0tau2 = None
        self.ak8SDsubjet0tau21 = None

        self.SDptPuppipt = None
        self.SDptGenpt = None
        self.ak8JetHT = None
        self.SDRhoRatio = None
 
        ### PUPPI jet mass corrections

        self.finCor1 = ROOT.TFile.Open( "./puppiCorr.root","READ")
        self.puppisd_corrGEN      = self.finCor1.Get("puppiJECcorr_gen")
        self.puppisd_corrRECO_cen = self.finCor1.Get("puppiJECcorr_reco_0eta1v3")
        self.puppisd_corrRECO_for = self.finCor1.Get("puppiJECcorr_reco_1v3eta2v5")

        ### B tag weights       TO-DO: Apply the B tag SFs
        '''
        ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cc+') 
        calib = ROOT.BTagCalibration("csvv1", "CSVV1.csv")
        reader = ROOT.BTagCalibrationReader(calib, 1, "lt", "central") 
        # (, operating point 0=loose 1=medium, measurementType="lt", central up or down)
        '''
        self.BtagWeight = 1.0


        ### Flag to distinguish data from MC
        self.itIsData = None
        theFileIs = self.infile
        if theFileIs.find("Run2016")== -1 : 
            self.itIsData = False
            if self.verbose :  
                print "MC : Event and PU weights != 1"

        else : 
            self.itIsData = True                     
            if self.verbose : print "DATA : weights = 1" 
    """
        This is the "select" function that does the work for the event selection. If you have any complicated
        stuff to do, do it here and create a class member variable to cache the results. 
    """
    def select( self ) :

        self.passedCount = [0] * self.nstages

        self.PuppiCorr = self.tree.JetPuppiCorrFactor[0]  
        self.Corr = self.tree.JetCorrFactor[0]  
        self.CorrL2L3 = self.tree.JetSDptCorrL23[0]  
        self.CorrL2L3SD = self.tree.JetSDmassCorrL23[0]

        self.ak8Jet = None
        self.ak8JetRaw = None

        self.ak8SDJet = None
        self.ak8SDJetRaw = None

        self.ak8PuppiJet = None
        self.ak8PuppiJetRaw = None

        self.ak8PuppiSDJet = None
        self.ak8PuppiSDJetRaw = None

        self.puppitau32 = None
        self.puppitau21 = None
        self.tau32      = None
        self.tau21      = None

        self.ak8PuppiSDJet_Subjet0 = None
        self.ak8PuppiSDJet_Subjet1 = None
        self.ak8PuppiSDJet_Subjet0Raw = None
        self.ak8PuppiSDJet_Subjet1Raw = None       
        
        self.ak8PuppiJet200 = None
        self.ak8PuppiSDJet200 =  None
        self.ak8PuppiSDJet_Subjet0M200 =  None
        self.ak8PuppiSDJet_Subjet1M200 =  None

        self.ak8PuppiJet300 = None
        self.ak8PuppiSDJet300 =  None
        self.ak8PuppiSDJet_Subjet0M300 =  None
        self.ak8PuppiSDJet_Subjet1M300 =  None

        self.ak8PuppiJet400 = None
        self.ak8PuppiSDJet400 =  None
        self.ak8PuppiSDJet_Subjet0M400 =  None
        self.ak8PuppiSDJet_Subjet1M400 =  None

        self.ak8PuppiJet500 = None
        self.ak8PuppiSDJet500 =  None
        self.ak8PuppiSDJet_Subjet0M500 =  None
        self.ak8PuppiSDJet_Subjet1M500 =  None

        self.ak8PuppiJet600 = None
        self.ak8PuppiSDJet600 =  None
        self.ak8PuppiSDJet_Subjet0M600 =  None
        self.ak8PuppiSDJet_Subjet1M600 =  None

        self.ak4Jet = None
        self.ak4JetBdisc = None 

        self.ak8SDsubjet0tau1 = None
        self.ak8SDsubjet0tau2 = None
        self.ak8SDsubjet0tau21 = None

        self.ak8JetHT = 0.0
        self.SDRhoRatio = None

        self.SDptPuppipt = None
        self.SDptGenpt = None

        self.ak4Jet = ROOT.TLorentzVector( )        
        self.ak4Jet.SetPtEtaPhiM( self.tree.AK4_dRminLep_Pt[0],
                                  self.tree.AK4_dRminLep_Eta[0],
                                  self.tree.AK4_dRminLep_Phi[0],
                                  self.tree.AK4_dRminLep_Mass[0] )
        self.ak4JetBdisc = self.tree.AK4_dRminLep_Bdisc[0]
        #self.BtagWeight = reader.eval( csvscore,  ak4Jet.Eta(),  ak4Jet.Perp() )


        self.ak8Jet = ROOT.TLorentzVector()
        self.ak8Jet.SetPtEtaPhiM( self.tree.JetPt[0],
                                  self.tree.JetEta[0],
                                  self.tree.JetPhi[0],
                                  self.tree.JetMass[0] )   

        self.ak8JetRaw =   self.ak8Jet
        self.ak8Jet =   self.ak8Jet * self.Corr
        if self.ak8JetRaw != None :
            self.ak8_m = self.CorrPUPPIMass( self.ak8JetRaw.Perp() , self.ak8JetRaw.Eta(), self.ak8JetRaw.M()  )
            self.ak8JetHT =         self.ak8JetHT + self.ak8Jet.Perp()
        self.ak8PuppiJet = ROOT.TLorentzVector()
        self.ak8PuppiJet.SetPtEtaPhiM( self.tree.JetPuppiPt[0],
                                  self.tree.JetPuppiEta[0],
                                  self.tree.JetPuppiPhi[0],
                                  self.tree.JetPuppiMass[0] )        
        self.ak8PuppiJetRaw =   self.ak8PuppiJet
        self.ak8PuppiJet =   self.ak8PuppiJet * self.PuppiCorr
        if self.ak8PuppiJetRaw != None :
            self.ak8_Puppim = self.CorrPUPPIMass( self.ak8PuppiJetRaw.Perp() , self.ak8PuppiJetRaw.Eta(), self.ak8PuppiJetRaw.M()  )

        self.ak8SDJet = ROOT.TLorentzVector()
        self.ak8SDJet.SetPtEtaPhiM( self.tree.JetSDptRaw[0],
                                  self.tree.JetSDetaRaw[0],
                                  self.tree.JetSDphiRaw[0],
                                  self.tree.JetSDmassRaw[0] )        
        self.ak8SDJetRaw =   self.ak8SDJet
        self.ak8SDJet =   self.ak8SDJet * self.Corr
        if self.ak8SDJetRaw != None :
            self.ak8_SDm = self.CorrPUPPIMass( self.ak8SDJetRaw.Perp() , self.ak8SDJetRaw.Eta(), self.ak8SDJetRaw.M()  )
            # Pt Responses
            self.SDptGenpt = float(self.ak8SDJet.Perp())  / float(self.ak8Jet.Perp() ) 
            if self.ak8PuppiJetRaw != None :
                self.SDptPuppipt = float(self.ak8SDJet.Perp())  / float(self.ak8PuppiJet.Perp() ) 
        self.ak8PuppiSDJet_Subjet0 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet0.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0],
                                            self.tree.JetPuppiSDsubjet0eta[0], 
                                            self.tree.JetPuppiSDsubjet0phi[0], 
                                            self.tree.JetPuppiSDsubjet0mass[0] )
        self.ak8PuppiSDJet_Subjet0Raw =   self.ak8PuppiSDJet_Subjet0 
        self.ak8PuppiSDJet_Subjet0 =   self.ak8PuppiSDJet_Subjet0  * self.PuppiCorr
        if self.ak8PuppiSDJet_Subjet0 != None :
            self.ak8PuppiSD_subjet0_m = self.CorrPUPPIMass( 
                                                           self.ak8PuppiSDJet_Subjet0Raw.Perp(), 
                                                           self.ak8PuppiSDJet_Subjet0Raw.Eta(), 
                                                           self.ak8PuppiSDJet_Subjet0Raw.M()       )

        self.ak8PuppiSDJet_Subjet1 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet1.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0],
                                            self.tree.JetPuppiSDsubjet1eta[0], 
                                            self.tree.JetPuppiSDsubjet1phi[0],
                                            self.tree.JetPuppiSDsubjet1mass[0] )
        self.ak8PuppiSDJet_Subjet1Raw =   self.ak8PuppiSDJet_Subjet1 
        self.ak8PuppiSDJet_Subjet1 =   self.ak8PuppiSDJet_Subjet1 * self.PuppiCorr


        self.ak8PuppiSDJet =  self.ak8PuppiSDJet_Subjet0 +  self.ak8PuppiSDJet_Subjet1
        self.ak8PuppiSDJetRaw =   self.ak8PuppiSDJet
        self.ak8PuppiSDJet =   self.ak8PuppiSDJet * self.PuppiCorr
        if self.ak8PuppiSDJetRaw !=None :
            if self.ak8PuppiSDJet.Perp() > 0.001 :
                self.SDRhoRatio = pow( self.ak8PuppiSDJet.M() / (self.ak8PuppiSDJet.Perp()*0.8) , 2)
            self.ak8PuppiSD_m = self.CorrPUPPIMass( 
                                                   self.ak8PuppiSDJetRaw.Perp(),
                                                   self.ak8PuppiSDJetRaw.Eta(),
                                                   self.ak8PuppiSDJetRaw.M()  )

        if self.ak8PuppiSDJet_Subjet0Raw !=None :
            self.ak8SDsj0_m = self.CorrPUPPIMass( 
                                                 self.ak8PuppiSDJet_Subjet0Raw.Perp(),
                                                 self.ak8PuppiSDJet_Subjet0Raw.Eta(),
                                                 self.ak8PuppiSDJet_Subjet0Raw.M()  )


        self.ak8PuppiJet200 =ROOT.TLorentzVector()
        self.ak8PuppiSDJet200 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet0M200 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet1M200 = ROOT.TLorentzVector()

        if (  200. < self.ak8PuppiSDJet_Subjet0.Perp() < 300. ) :
            self.ak8PuppiJet200.SetPtEtaPhiM( self.tree.JetPuppiPt[0],
                                              self.tree.JetPuppiEta[0], 
                                              self.tree.JetPuppiPhi[0], 
                                              self.tree.JetPuppiMass[0] ) 
            self.ak8PuppiSDJet_Subjet0M200.SetPtEtaPhiM( 
                                                        self.tree.JetPuppiSDsubjet0pt[0],
                                                        self.tree.JetPuppiSDsubjet0eta[0], 
                                                        self.tree.JetPuppiSDsubjet0phi[0],
                                                        self.tree.JetPuppiSDsubjet0mass[0] )
            self.ak8PuppiSDJet_Subjet1M200.SetPtEtaPhiM( 
                                                        self.tree.JetPuppiSDsubjet1pt[0],
                                                        self.tree.JetPuppiSDsubjet1eta[0],
                                                        self.tree.JetPuppiSDsubjet1phi[0],
                                                        self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8PuppiSDJet200 =  self.ak8PuppiSDJet_Subjet0M200 + self.ak8PuppiSDJet_Subjet1M200

        self.ak8PuppiJet300 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet300 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet0M300 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet1M300 = ROOT.TLorentzVector()
        if (  300. < self.ak8PuppiSDJet_Subjet0.Perp() < 400. ) :
            self.ak8PuppiJet300.SetPtEtaPhiM( 
	                                         self.tree.JetPuppiPt[0],
                                             self.tree.JetPuppiEta[0],
                                             self.tree.JetPuppiPhi[0],
                                             self.tree.JetPuppiMass[0] ) 

            self.ak8PuppiSDJet_Subjet0M300.SetPtEtaPhiM( 
                                                        self.tree.JetPuppiSDsubjet0pt[0],
                                                        self.tree.JetPuppiSDsubjet0eta[0],  
                                                        self.tree.JetPuppiSDsubjet0phi[0],
                                                        self.tree.JetPuppiSDsubjet0mass[0] )

            self.ak8PuppiSDJet_Subjet1M300.SetPtEtaPhiM( 
                                                        self.tree.JetPuppiSDsubjet1pt[0],
                                                        self.tree.JetPuppiSDsubjet1eta[0], 
                                                        self.tree.JetPuppiSDsubjet1phi[0],
                                                        self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8PuppiSDJet300 =  self.ak8PuppiSDJet_Subjet0M300 + self.ak8PuppiSDJet_Subjet1M300

        self.ak8PuppiJet400 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet400 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet0M400 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet1M400 = ROOT.TLorentzVector()
        if (  400. < self.ak8PuppiSDJet_Subjet0.Perp() < 500. ) :
            self.ak8PuppiJet400.SetPtEtaPhiM( 
                                             self.tree.JetPuppiPt[0],
                                             self.tree.JetPuppiEta[0],
                                             self.tree.JetPuppiPhi[0], 
                                             self.tree.JetPuppiMass[0] ) 
            self.ak8PuppiSDJet_Subjet0M400.SetPtEtaPhiM( 
                                                        self.tree.JetPuppiSDsubjet0pt[0], 
                                                        self.tree.JetPuppiSDsubjet0eta[0], 
                                                        self.tree.JetPuppiSDsubjet0phi[0],
                                                        self.tree.JetPuppiSDsubjet0mass[0] )
            #if self.verbose : print "Raw mass of sd subjet0 is {0:2.3f}".format(self.ak8PuppiSDJet_Subjet0M400.M())
            self.ak8PuppiSDJet_Subjet1M400.SetPtEtaPhiM( 
                                                        self.tree.JetPuppiSDsubjet1pt[0], 
                                                        self.tree.JetPuppiSDsubjet1eta[0],
                                                        self.tree.JetPuppiSDsubjet1phi[0], 
                                                        self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8PuppiSDJet400 =  self.ak8PuppiSDJet_Subjet0M400 + self.ak8PuppiSDJet_Subjet1M400

        self.ak8PuppiJet500 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet500 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet0M500 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet1M500 = ROOT.TLorentzVector()
        if (  500. < self.ak8PuppiSDJet_Subjet0.Perp() < 800. ) :
            self.ak8PuppiJet500.SetPtEtaPhiM( 
                                             self.tree.JetPuppiPt[0], 
                                             self.tree.JetPuppiEta[0], 
                                             self.tree.JetPuppiPhi[0], 
                                             self.tree.JetPuppiMass[0] ) 
            self.ak8PuppiSDJet_Subjet0M500.SetPtEtaPhiM( 
                                                        self.tree.JetPuppiSDsubjet0pt[0],
                                                        self.tree.JetPuppiSDsubjet0eta[0],
                                                        self.tree.JetPuppiSDsubjet0phi[0],
                                                        self.tree.JetPuppiSDsubjet0mass[0] )
            self.ak8PuppiSDJet_Subjet1M500.SetPtEtaPhiM( 
                                                        self.tree.JetPuppiSDsubjet1pt[0],
                                                        self.tree.JetPuppiSDsubjet1eta[0], 
                                                        self.tree.JetPuppiSDsubjet1phi[0],
                                                        self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8PuppiSDJet500 =  self.ak8PuppiSDJet_Subjet0M500 + self.ak8PuppiSDJet_Subjet1M500



        self.ak8SDsj0_m200 = self.CorrPUPPIMass( 
                                                self.ak8PuppiSDJet_Subjet0M200.Perp()* self.PuppiCorr,
                                                self.ak8PuppiSDJet_Subjet0M200.Eta(), 
                                                self.ak8PuppiSDJet_Subjet0M200.M()  )
        self.ak8SDsj0_m300 =  self.CorrPUPPIMass( 
                                                 self.ak8PuppiSDJet_Subjet0M300.Perp() * self.PuppiCorr,
                                                 self.ak8PuppiSDJet_Subjet0M300.Eta(),
                                                 self.ak8PuppiSDJet_Subjet0M300.M()  )

        self.ak8SDsj0_m400 =  self.CorrPUPPIMass( 
                                                 self.ak8PuppiSDJet_Subjet0M400.Perp()* self.PuppiCorr,
                                                 self.ak8PuppiSDJet_Subjet0M400.Eta(),
                                                 self.ak8PuppiSDJet_Subjet0M400.M()  )
        self.ak8SDsj0_m500 =  self.CorrPUPPIMass( 
                                                 self.ak8PuppiSDJet_Subjet0M500.Perp()* self.PuppiCorr,
                                                 self.ak8PuppiSDJet_Subjet0M500.Eta(), 
                                                 self.ak8PuppiSDJet_Subjet0M500.M()  )


        self.puppitau32 = self.tree.JetPuppiTau32[0]
        self.puppitau21 = self.tree.JetPuppiTau21[0]
        self.tau32      = self.tree.JetTau32[0]
        self.tau21      = self.tree.JetTau21[0]

        self.ak8SDsubjet0tau1 = self.tree.JetSDsubjet0tau1[0]
        self.ak8SDsubjet0tau2 = self.tree.JetSDsubjet0tau2[0]

        self.ak8SDsubjet0tau21 = 1.0
        if self.ak8SDsubjet0tau1 > 0.001:
            self.ak8SDsubjet0tau21 = self.ak8SDsubjet0tau2 / self.ak8SDsubjet0tau1
            #if self.verbose : print "SD subjet 0 tau21 is: {0:2.2f}".format(self.ak8SDsubjet0tau21)


        # Work the cut flow
        self.passedCount = [0] * self.nstages
        self.passed = [False] * self.nstages
        self.passed[0] = self.lepsel.passed[ len(self.lepsel.passed) - 1]
        if not self.passed[0] : return self.passed
        self.passedCount[0] += 1
        if self.verbose : print "Stage 8 : Event passed leptonic selection"

        if not (self.ak8Jet.Perp() > self.AK8PtCut and abs(self.ak8Jet.Eta()) < self.AK8EtaCut ) : return self.passed
        self.passed[1] = True
        self.passedCount[1] += 1
        if self.verbose : print "Stage 9 : AK8 Pt  {0:2.2f}  > ( {1:2.2f} GeV) and eta {2:2.2f} < ( {3:2.2f} )".format( 
                                                                                                                   self.ak8Jet.Perp(),
                                                                                                                        self.AK8PtCut,
                                                                                                                    self.ak8Jet.Eta(),
                                                                                                                       self.AK8EtaCut)
        if not ( self.ak4JetBdisc >  self.bdiscmin  ) : return self.passed
        self.passed[2] = True
        self.passedCount[2] += 1
        if self.verbose : print "Stage 10 :AK4 bdisc {0:2.2f}  > ( {1:2.2f} ) ".format(  self.ak4JetBdisc , self.bdiscmin )
        
        if not ( self.minAK8Mass < self.ak8SDJet.M() < self.maxAK8Mass ) : return self.passed
        self.passed[3] = True
        self.passedCount[3] += 1
        if self.verbose : print "Stage 12: AK8 SD mass  ({0:2.2f}) < {1:2.2f} GeV < ({2:2.2f})  [For comparison SD Puppi mass after puppi corr is  {2:2.2f} ]".format(  self.minAK8Mass , self.ak8SDJet.M() , self.maxAK8Mass, self.ak8PuppiSD_m)



        if not ( self.tau32 < self.tau32Cut ) : return self.passed
        self.passed[4] = True
        self.passedCount[4] += 1
        if self.verbose : print "Stage 11: AK8 tau32  {0:2.2f}  > ( {1:2.2f} ) [For comparison puppi tau32 is  {2:2.2f} ]".format(  self.tau32 , self.tau32Cut, self.puppitau32)



        #W tag the SD subjet 0 fix this: later see if bdisc is higher for subjet 0 or 1
        if self.verbose : print "Mass of SD subjet 0 before puppi corr is: {0:2.2f}".format( float(self.ak8PuppiSDJet_Subjet0.M()))
        if not ( self.minAK8sjMass <  self.ak8PuppiSD_subjet0_m  <  self.maxAK8sjMass) : return self.passed
        self.passed[5] = True
        self.passedCount[5] += 1
        if self.verbose : print "Stage 13: AK8 SD subjet 0 mass  ({0}) < {1:2.2f} GeV < ({2})  [mass is after puppi mass corr]".format( self.minAK8sjMass ,  self.ak8PuppiSD_subjet0_m  , self.maxAK8sjMass)

        if self.verbose : print "mass of sd subjet 0 after puppi corr in bin 200-300 {0:2.3f}, 300-400 {1:2.3f}, 400-500 {2:2.3f}, 500-800 {3:2.3f}".format(self.ak8SDsj0_m200,self.ak8SDsj0_m300,self.ak8SDsj0_m400,self.ak8SDsj0_m500)


        if self.verbose :print "Stage 14: tau21 of SD subjet 0 is: {0:2.2f}".format( float( self.ak8SDsubjet0tau21) )
        if not ( self.ak8SDsubjet0tau21 < self.tau21Cut ) : return self.passed
        self.passed[6] = True
        self.passedCount[6] += 1
        if self.verbose : print "AK8 SD subjet 0 tau21  {0:2.2f}  < ( {1} ) ".format( self.ak8SDsubjet0tau21 , self.tau21Cut )

        return self.passed


    def CorrPUPPIMass(self, puppiptcorr, puppieta, puppimRaw) : #{ Adapted from https://github.com/thaarres/PuppiSoftdropMassCorr

        if puppimRaw < 0.0001 : return 0.0
        self.genCorr  = 1.
        self.recoCorr = 1.
        self.totalWeight = 1.

        self.genCorr =  self.puppisd_corrGEN.Eval(     puppiptcorr )
    
        if (abs(puppieta) <=1.3 ): self.recoCorr = self.puppisd_corrRECO_cen.Eval(    puppiptcorr)
        if (abs(puppieta) > 1.3 ): self.recoCorr = self.puppisd_corrRECO_for.Eval(    puppiptcorr)
        self.totalWeight = self.genCorr * self.recoCorr
        self.puppim = self.totalWeight * puppimRaw
        #if 0. <puppimRaw<0.1 :
        #if self.verbose : print "Puppi mass corr is {0:2.2f} for jet of Raw mass {1:2.2f} and new mass {2:2.2f}".format(self.totalWeight ,puppimRaw, self.puppim)
        return self.puppim
        #}                  


  
