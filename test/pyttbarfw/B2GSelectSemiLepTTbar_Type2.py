#! /usr/bin/env python

import ROOT

class B2GSelectSemiLepTTbar_Type2( ) :
    """
    Selects semileptonic ttbar events with widely separated top quarks.
    This selects type 2 top events with traditional lepton isolation.
    """
    def __init__(self, options, tree, lepsel ):
        self.puppitau21Cut = options.tau21Cut
        self.puppitau32Cut = options.tau32Cut
        self.bdiscmin = options.bdiscmin
        self.infile = options.infile
        self.verbose = options.verbose
        self.ignoreTrig = options.ignoreTrig
        self.nstages = 5
        self.tree = tree
        self.lepsel = lepsel
        
        
        self.passed = [False] * self.nstages      
        self.passedCount = [0] * self.nstages

        # Cached class member variables for plotting


        self.ak8JetP4 = None
        self.ak8JetP4Raw = None

        self.ak8SDJetP4 = None
        self.ak8SDJetP4Raw = None

        self.ak8PuppiJetP4 = None
        self.ak8PuppiJetP4Raw = None

        self.ak8PuppiSDJetP4 = None
        self.ak8PuppiSDJetP4Raw = None

        self.puppitau32 = None
        self.puppitau21 = None

        self.ak8PuppiSDJetP4_Subjet0 = None
        self.ak8PuppiSDJetP4_Subjet1 = None

        self.ak4JetBdisc = None
        self.ak4Jet = None

        self.SDptPuppipt = None
        self.SDptGenpt = None
        self.ak8JetHT = None
        self.SDRhoRatio = None

        self.ak8Jet_Ptbins = [200, 300, 400, 500, 800, 1000]

        ### PUPPI jet mass corrections

        self.finCor1 = ROOT.TFile.Open( "./puppiCorr.root","READ")
        self.puppisd_corrGEN      = self.finCor1.Get("puppiJECcorr_gen")
        self.puppisd_corrRECO_cen = self.finCor1.Get("puppiJECcorr_reco_0eta1v3")
        self.puppisd_corrRECO_for = self.finCor1.Get("puppiJECcorr_reco_1v3eta2v5")


        ### Flag to distinguish data from MC
        self.itIsData = None
        theFileIs = self.infile
        if theFileIs.find("un2016")== -1 : 
            self.itIsData = False
            self.PtSmear = None
            self.PuppiPtSmear = None
            if self.verbose :  
                print "MC : Event and PU weights != 1"

        else : 
            self.itIsData = True   
            self.PtSmear = 1.0  
            self.PuppiPtSmear = 1.0             
            if self.verbose : print "DATA : weights = 1" 
    """
        This is the "select" function that does the work for the event selection. If you have any complicated
        stuff to do, do it here and create a class member variable to cache the results. 
    """
    def select( self ) :

        self.PuppiCorr = self.tree.JetPuppiCorrFactor[0]  
        self.Corr = self.tree.JetCorrFactor[0]  
        self.CorrL2L3 = self.tree.JetSDptCorrL23[0]  
        self.CorrL2L3SD = self.tree.JetSDmassCorrL23[0]
        if self.itIsData :
            self.PtSmear = 1.
            self.PuppiPtSmear = 1.
        else:
            self.PtSmear = self.tree.JetPtSmearFactor[0]
            self.PuppiPtSmear = self.tree.JetPuppiPtSmearFactor[0]
            
        self.ak8JetP4 = None
        self.ak8JetP4Raw = None

        self.ak8SDJetP4 = None
        self.ak8SDJetP4Raw = None

        self.ak8PuppiJetP4 = None
        self.ak8PuppiJetP4Raw = None

        self.ak8PuppiSDJetP4 = None
        self.ak8PuppiSDJetP4Raw = None

        self.puppitau32 = None
        self.puppitau21 = None
        self.tau32      = None
        self.tau21      = None

        self.theNeutrino = ROOT.TLorentzVector( )
        self.theNeutrino.SetPxPyPzE(self.tree.SemiLeptMETpx[0], self.tree.SemiLeptMETpy[0], 0.0, self.tree.SemiLeptMETpt[0])

        self.theLepton = ROOT.TLorentzVector()
        self.theLepton.SetPtEtaPhiM( self.tree.LeptonPt[0], self.tree.LeptonEta[0], self.tree.LeptonPhi[0], self.tree.LeptonMass[0] )

        self.ak4Jet = None
        self.ak4JetBdisc = None
        self.ak4Jet = ROOT.TLorentzVector( )        
        self.ak4Jet.SetPtEtaPhiM( self.tree.AK4_dRminLep_Pt[0], self.tree.AK4_dRminLep_Eta[0], self.tree.AK4_dRminLep_Phi[0], self.tree.AK4_dRminLep_Mass[0] )
        self.ak4JetBdisc = self.tree.AK4_dRminLep_Bdisc[0]


        self.ak8JetP4 = ROOT.TLorentzVector()
        self.ak8JetP4.SetPtEtaPhiM( self.tree.JetPt[0],
                                  self.tree.JetEta[0],
                                  self.tree.JetPhi[0],
                                  self.tree.JetMass[0] )        
        self.ak8JetP4Raw =   self.ak8JetP4
        self.ak8JetP4 =   self.ak8JetP4 * self.Corr
        if self.ak8JetP4Raw != None :
            self.ak8_m = self.CorrPUPPIMass( self.ak8JetP4Raw.Perp() , self.ak8JetP4Raw.Eta(), self.ak8JetP4Raw.M()  )
            self.ak8JetHT =         self.ak8JetHT + self.ak8JetP4.Perp()

        self.ak8SDJetP4 = ROOT.TLorentzVector()
        self.ak8SDJetP4.SetPtEtaPhiM( self.tree.JetSDptRaw[0],
                                  self.tree.JetSDetaRaw[0],
                                  self.tree.JetSDphiRaw[0],
                                  self.tree.JetSDmassRaw[0] )      
        self.ak8SDJetP4Raw =   self.ak8SDJetP4
        self.ak8SDJetP4 =   self.ak8SDJetP4 * self.Corr
        self.ak8_SDm = self.CorrPUPPIMass( self.ak8SDJetP4Raw.Perp() , self.ak8SDJetP4Raw.Eta(), self.ak8SDJetP4Raw.M()  )


        self.ak8PuppiJetP4 = ROOT.TLorentzVector()
        self.ak8PuppiJetP4.SetPtEtaPhiM( self.tree.JetPuppiPt[0],
                                  self.tree.JetPuppiEta[0],
                                  self.tree.JetPuppiPhi[0],
                                  self.tree.JetPuppiMass[0] )        
        self.ak8PuppiJetP4Raw =   self.ak8PuppiJetP4
        self.ak8PuppiJetP4 =   self.ak8PuppiJetP4 * self.PuppiCorr
        if self.ak8PuppiJetP4Raw != None :
            self.ak8_Puppim = self.CorrPUPPIMass( self.ak8PuppiJetP4Raw.Perp() , self.ak8PuppiJetP4Raw.Eta(), self.ak8PuppiJetP4Raw.M()  )
            # Pt Responses
            self.SDptGenpt = float(self.ak8SDJetP4.Perp())  / float(self.ak8JetP4.Perp() ) 
            if self.ak8PuppiJetP4Raw != None :
                self.SDptPuppipt = float(self.ak8SDJetP4.Perp())  / float(self.ak8PuppiJetP4.Perp() ) 


        self.ak8PuppiSDJetP4_Subjet0 = ROOT.TLorentzVector()
        self.ak8PuppiSDJetP4_Subjet1 = ROOT.TLorentzVector()
        self.ak8PuppiSDJetP4_Subjet0.SetPtEtaPhiM( 
                                                self.tree.JetPuppiSDsubjet0pt[0],
                                                self.tree.JetPuppiSDsubjet0eta[0], 
                                                self.tree.JetPuppiSDsubjet0phi[0], 
                                                self.tree.JetPuppiSDsubjet0mass[0] )
        self.ak8PuppiSDJetP4_Subjet1.SetPtEtaPhiM( 
                                                self.tree.JetPuppiSDsubjet1pt[0],
                                                self.tree.JetPuppiSDsubjet1eta[0],
                                                self.tree.JetPuppiSDsubjet1phi[0],
                                                self.tree.JetPuppiSDsubjet1mass[0] )

        if self.ak8PuppiSDJetP4_Subjet0.M() < self.ak8PuppiSDJetP4_Subjet1.M() : 
            self.ak8PuppiSDJetP4_Subjet1,self.ak8PuppiSDJetP4_Subjet0 = self.ak8PuppiSDJetP4_Subjet0,self.ak8PuppiSDJetP4_Subjet1
        self.ak8PuppiSDJetP4 =  self.ak8PuppiSDJetP4_Subjet0 +  self.ak8PuppiSDJetP4_Subjet1

        self.ak8PuppiSDJetP4Raw =   self.ak8PuppiSDJetP4
        if self.ak8PuppiSDJetP4Raw !=None :
            if self.ak8PuppiSDJetP4.Perp() > 0.001 :
                self.SDRhoRatio = pow( self.ak8PuppiSDJetP4.M() / (self.ak8PuppiSDJetP4.Perp()*0.8) , 2)
            self.ak8PuppiSD_m = self.CorrPUPPIMass( 
                                                   self.ak8PuppiSDJetP4Raw.Perp(),
                                                   self.ak8PuppiSDJetP4Raw.Eta(),
                                                   self.ak8PuppiSDJetP4Raw.M()  )

        self.ak8PuppiSDJetP4_Subjet0Raw =   self.ak8PuppiSDJetP4_Subjet0 
        self.ak8PuppiSDJetP4_Subjet1Raw =   self.ak8PuppiSDJetP4_Subjet1 

        self.ak8PuppiSDJetP4 =   self.ak8PuppiSDJetP4 * self.PuppiCorr
        self.ak8PuppiSDJetP4_Subjet0 =   self.ak8PuppiSDJetP4_Subjet0 * self.PuppiCorr
        self.ak8PuppiSDJetP4_Subjet1 =   self.ak8PuppiSDJetP4_Subjet1 * self.PuppiCorr

        if self.verbose : print 'ak8PuppiSDJet = (%6.2f,%8.3f,%8.3f,%6.2f)' % ( self.ak8PuppiSDJetP4.Perp(), self.ak8PuppiSDJetP4.Eta(), self.ak8PuppiSDJetP4.Phi(), self.ak8PuppiSDJetP4.M() )

        self.ak8PuppiJetP4_m = self.CorrPUPPIMass( self.ak8PuppiJetP4Raw.Perp() , self.ak8PuppiJetP4Raw.Eta(), self.ak8PuppiJetP4Raw.M()  )

        self.ak8SDsj0_m = self.CorrPUPPIMass( self.ak8PuppiSDJetP4_Subjet0Raw.Perp() , self.ak8PuppiSDJetP4_Subjet0Raw.Eta(), self.ak8PuppiSDJetP4_Subjet0Raw.M()  )

        self.ak8SDsj1_m = self.CorrPUPPIMass( self.ak8PuppiSDJetP4_Subjet1Raw.Perp() , self.ak8PuppiSDJetP4_Subjet1Raw.Eta(), self.ak8PuppiSDJetP4_Subjet1Raw.M()  )

        self.ak8Jet_Ptbins = [200, 300, 400, 500, 800, 1000]
        
        self.ak8PuppiJetP4_Binned = [ROOT.TLorentzVector()] * len(self.ak8Jet_Ptbins)
        self.ak8PuppiSDJetP4_Binned = [ROOT.TLorentzVector()] * len(self.ak8Jet_Ptbins)
        self.ak8PuppiSDJetP4Subjet0_Binned = [ROOT.TLorentzVector()] * len(self.ak8Jet_Ptbins)
        self.ak8PuppiSDJetP4Subjet1_Binned = [ROOT.TLorentzVector()] * len(self.ak8Jet_Ptbins)
        self.ak8PuppiSDJetP4Subjet0PuppiCorrMass_Binned = [0.] * len(self.ak8Jet_Ptbins)
        self.ak8PuppiSDJetP4Subjet1PuppiCorrMass_Binned = [0.] * len(self.ak8Jet_Ptbins)


        for iptbin, ptbin in enumerate(self.ak8Jet_Ptbins) :
            if ptbin <  1000.:
                if (  ptbin < self.ak8PuppiSDJetP4_Subjet0.Perp() < self.ak8Jet_Ptbins[iptbin+1] ) :
                    self.ak8PuppiJetP4_Binned[iptbin].SetPtEtaPhiM( self.tree.JetPuppiPt[0], self.tree.JetPuppiEta[0], self.tree.JetPuppiPhi[0], self.tree.JetPuppiMass[0] ) 
                    self.ak8PuppiSDJetP4Subjet0_Binned[iptbin].SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
                    self.ak8PuppiSDJetP4Subjet1_Binned[iptbin].SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )
                    self.ak8PuppiSDJetP4_Binned[iptbin] =  self.ak8PuppiSDJetP4Subjet0_Binned[iptbin] + self.ak8PuppiSDJetP4Subjet1_Binned[iptbin]
                    self.ak8PuppiSDJetP4Subjet0PuppiCorrMass_Binned[iptbin] = self.ak8SDsj0_m
                    self.ak8PuppiSDJetP4Subjet1PuppiCorrMass_Binned[iptbin] = self.ak8SDsj1_m

        self.puppitau21 = self.tree.JetPuppiTau21[0]
        self.puppitau32 = self.tree.JetPuppiTau32[0]


        self.ak8SDsubjet0tau1 = self.tree.JetSDsubjet0tau1[0]
        self.ak8SDsubjet0tau2 = self.tree.JetSDsubjet0tau2[0]

        self.ak8SDsubjet0tau21 = 1.0
        if self.ak8SDsubjet0tau1 > 0.001:
            self.ak8SDsubjet0tau21 = self.ak8SDsubjet0tau2 / self.ak8SDsubjet0tau1
            if self.verbose : print "SD subjet 0 tau21 is: {}".format(self.ak8SDsubjet0tau21)

        # Work the cut flow
        self.passed = [False] * self.nstages
        self.passedCount = [0] * self.nstages
        self.passed[0] = self.lepsel.passed[ len( self.lepsel.passed) - 1]

        if not self.passed[0] : return self.passed
        self.passedCount[0] += 1

        if not (self.ak8PuppiSDJetP4.Perp() > 200. and abs(self.ak8PuppiSDJetP4.Eta()) < 2.4 and self.ak8JetP4.DeltaR( self.lepsel.leptonP4) > 1.0  ) : return self.passed
        self.passed[1] = True
        self.passedCount[1] += 1

        if not ( self.ak4JetBdisc > self.bdiscmin ) : return self.passed
        self.passed[2] = True
        self.passedCount[2] += 1
        
        if not ( 30. < self.ak8PuppiSDJetP4.M() < 150. ) : return self.passed
        self.passed[3] = True
        self.passedCount[3] += 1

        if not ( self.puppitau21 < self.puppitau21Cut ) : return self.passed
        self.passed[4] = True
        self.passedCount[4] += 1

        return self.passed


    def CorrPUPPIMass(self, puppipt, puppieta, puppimRaw) : #{
        if puppimRaw < 0.1 : return 0.0
        self.genCorr  = 1.
        self.recoCorr = 1.
        self.totalWeight = 1.

        self.genCorr =  self.puppisd_corrGEN.Eval( puppipt )
    
        if (abs(puppieta) <=1.3 ): self.recoCorr = self.puppisd_corrRECO_cen.Eval(puppipt)
        if (abs(puppieta) > 1.3 ): self.recoCorr = self.puppisd_corrRECO_for.Eval(puppipt)
        self.totalWeight = self.genCorr * self.recoCorr
        self.puppim = self.totalWeight * puppimRaw
        #print "Puppi mass corr is {0:2.2f} for jet of Raw mass {1:2.2f} and new mass {2:2.2f}".format(totalWeight ,puppimRaw, puppim)
        return self.puppim
        #}                  

                        

    
