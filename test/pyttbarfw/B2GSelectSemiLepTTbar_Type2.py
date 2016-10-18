#! /usr/bin/env python

import ROOT

class B2GSelectSemiLepTTbar_Type2( ) :
    """
    Selects semileptonic ttbar events with widely separated top quarks.
    This selects type 2 top events with traditional lepton isolation.
    """
    def __init__(self, options, tree, lepsel ):
        self.tau21Cut = options.tau21Cut
        self.tau32Cut = options.tau32Cut
        self.bdiscmin = options.bdiscmin
        self.ignoreTrig = options.ignoreTrig
        self.nstages = 5
        self.tree = tree
        self.lepsel = lepsel
        self.passed = [False] * self.nstages      

        # Cached class member variables for plotting
        self.ak4Jet = None
        self.ak8Jet = None
        self.ak8SDJet = None
        self.ak8SDJet_Subjet0 = None
        self.ak8SDJet_Subjet1 = None
        self.ak4JetBdisc = None

        self.finCor1 = ROOT.TFile.Open( "./puppiCorr.root","READ")
        self.puppisd_corrGEN      = self.finCor1.Get("puppiJECcorr_gen")
        self.puppisd_corrRECO_cen = self.finCor1.Get("puppiJECcorr_reco_0eta1v3")
        self.puppisd_corrRECO_for = self.finCor1.Get("puppiJECcorr_reco_1v3eta2v5")


    """
        This is the "select" function that does the work for the event selection. If you have any complicated
        stuff to do, do it here and create a class member variable to cache the results. 
    """
    def select( self ) :

        self.EventWeight = self.tree.SemiLeptEventWeight[0]
        self.PUWeight = self.tree.SemiLeptPUweight[0]  
        self.PuppiCorr = self.tree.JetPuppiCorrFactor[0]  


        self.theNeutrino = None
        self.theLepton = None
        self.ak4Jet = None
        self.ak8Jet = None
        self.ak8SDJet = None
        self.ak8SDJet_Subjet0 = None
        self.ak8SDJet_Subjet1 = None
        self.ak4JetBdisc = None        
        
        self.theNeutrino = ROOT.TLorentzVector( )
        self.theNeutrino.SetPxPyPzE(self.tree.SemiLeptMETpx[0], self.tree.SemiLeptMETpy[0], 0.0, self.tree.SemiLeptMETpt[0])

        self.theLepton = ROOT.TLorentzVector()
        self.theLepton.SetPtEtaPhiM( self.tree.LeptonPt[0], self.tree.LeptonEta[0], self.tree.LeptonPhi[0], self.tree.LeptonMass[0] )

        self.ak4Jet = ROOT.TLorentzVector( )        
        self.ak4Jet.SetPtEtaPhiM( self.tree.AK4_dRminLep_Pt[0], self.tree.AK4_dRminLep_Eta[0], self.tree.AK4_dRminLep_Phi[0], self.tree.AK4_dRminLep_Mass[0] )
        self.ak4JetBdisc = self.tree.AK4_dRminLep_Bdisc[0]
        self.ak8Jet = ROOT.TLorentzVector()
        self.ak8Jet.SetPtEtaPhiM( self.tree.JetPuppiPt[0], self.tree.JetPuppiEta[0], self.tree.JetPuppiPhi[0], self.tree.JetPuppiMass[0] )        
        self.ak8Jetraw =   self.ak8Jet
        self.ak8Jet =   self.ak8Jet * self.PuppiCorr

        self.ak8SDJet_Subjet0 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet1 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet0.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
        self.ak8SDJet_Subjet1.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )

        if self.ak8SDJet_Subjet0.M() < self.ak8SDJet_Subjet1.M() : 
            self.ak8SDJet_Subjet1,self.ak8SDJet_Subjet0 = self.ak8SDJet_Subjet0,self.ak8SDJet_Subjet1
        self.ak8SDJet =  self.ak8SDJet_Subjet0 +  self.ak8SDJet_Subjet1

        self.ak8SDJetraw =   self.ak8SDJet
        self.ak8SDJet_Subjet0raw =   self.ak8SDJet_Subjet0 
        self.ak8SDJet_Subjet1raw =   self.ak8SDJet_Subjet1 

        self.ak8SDJet =   self.ak8SDJet * self.PuppiCorr
        self.ak8SDJet_Subjet0 =   self.ak8SDJet_Subjet0 * self.PuppiCorr
        self.ak8SDJet_Subjet1 =   self.ak8SDJet_Subjet1 * self.PuppiCorr
        # mass is initially raw, multiply by correction factor to give corrected mass (check on this)
        self.ak8_m = self.CorrPUPPIMass( self.ak8Jetraw.Perp() , self.ak8Jetraw.Eta(), self.ak8Jetraw.M()  )
        self.ak8SD_m = self.CorrPUPPIMass( self.ak8SDJetraw.Perp() , self.ak8SDJetraw.Eta(), self.ak8SDJetraw.M()  )
        self.ak8SDsj0_m = self.CorrPUPPIMass( self.ak8SDJet_Subjet0raw.Perp() , self.ak8SDJet_Subjet0raw.Eta(), self.ak8SDJet_Subjet0raw.M()  )


        self.ak8Jet200 =ROOT.TLorentzVector()
        self.ak8SDJet200 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet0M200 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet1M200 = ROOT.TLorentzVector()

        if (  200. < self.ak8SDJet_Subjet0.Perp() < 300. ) :
            self.ak8Jet200.SetPtEtaPhiM( self.tree.JetPuppiPt[0], self.tree.JetPuppiEta[0], self.tree.JetPuppiPhi[0], self.tree.JetPuppiMass[0] ) 
            self.ak8SDJet_Subjet0M200.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
            self.ak8SDJet_Subjet1M200.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8SDJet200 =  self.ak8SDJet_Subjet0M200 + self.ak8SDJet_Subjet1M200

        self.ak8Jet300 = ROOT.TLorentzVector()
        self.ak8SDJet300 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet0M300 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet1M300 = ROOT.TLorentzVector()
        if (  300. < self.ak8SDJet_Subjet0.Perp() < 400. ) :
            self.ak8Jet300.SetPtEtaPhiM( self.tree.JetPuppiPt[0], self.tree.JetPuppiEta[0], self.tree.JetPuppiPhi[0], self.tree.JetPuppiMass[0] ) 
            self.ak8SDJet_Subjet0M300.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
            self.ak8SDJet_Subjet1M300.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8SDJet300 =  self.ak8SDJet_Subjet0M300 + self.ak8SDJet_Subjet1M300
        self.ak8Jet400 = ROOT.TLorentzVector()
        self.ak8SDJet400 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet0M400 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet1M400 = ROOT.TLorentzVector()
        if (  400. < self.ak8SDJet_Subjet0.Perp() < 500. ) :
            self.ak8Jet400.SetPtEtaPhiM( self.tree.JetPuppiPt[0], self.tree.JetPuppiEta[0], self.tree.JetPuppiPhi[0], self.tree.JetPuppiMass[0] ) 
            self.ak8SDJet_Subjet0M400.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
            self.ak8SDJet_Subjet1M400.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8SDJet400 =  self.ak8SDJet_Subjet0M400 + self.ak8SDJet_Subjet1M400

        self.ak8Jet500 = ROOT.TLorentzVector()
        self.ak8SDJet500 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet0M500 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet1M500 = ROOT.TLorentzVector()
        if (  500. < self.ak8SDJet_Subjet0.Perp() < 600. ) :
            self.ak8Jet500.SetPtEtaPhiM( self.tree.JetPuppiPt[0], self.tree.JetPuppiEta[0], self.tree.JetPuppiPhi[0], self.tree.JetPuppiMass[0] ) 
            self.ak8SDJet_Subjet0M500.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
            self.ak8SDJet_Subjet1M500.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8SDJet500 =  self.ak8SDJet_Subjet0M500 + self.ak8SDJet_Subjet1M500

        self.ak8Jet600 = ROOT.TLorentzVector()
        self.ak8SDJet600 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet0M600 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet1M600 = ROOT.TLorentzVector()
        if (  600. < self.ak8SDJet_Subjet0.Perp() < 800. ) :
            self.ak8Jet600.SetPtEtaPhiM( self.tree.JetPuppiPt[0], self.tree.JetPuppiEta[0], self.tree.JetPuppiPhi[0], self.tree.JetPuppiMass[0] ) 
            self.ak8SDJet_Subjet0M600.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
            self.ak8SDJet_Subjet1M600.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8SDJet600 =  self.ak8SDJet_Subjet0M600 + self.ak8SDJet_Subjet1M600


        self.ak8SDsj0_m200 = self.CorrPUPPIMass( self.ak8SDJet_Subjet0M200.Perp() , self.ak8SDJet_Subjet0M200.Eta(), self.ak8SDJet_Subjet0M200.M()  )
        self.ak8SDsj0_m300 = self.CorrPUPPIMass( self.ak8SDJet_Subjet0M300.Perp() , self.ak8SDJet_Subjet0M300.Eta(), self.ak8SDJet_Subjet0M300.M()  )
        self.ak8SDsj0_m400 = self.CorrPUPPIMass( self.ak8SDJet_Subjet0M400.Perp() , self.ak8SDJet_Subjet0M400.Eta(), self.ak8SDJet_Subjet0M400.M()  )
        self.ak8SDsj0_m500 = self.CorrPUPPIMass( self.ak8SDJet_Subjet0M500.Perp() , self.ak8SDJet_Subjet0M500.Eta(), self.ak8SDJet_Subjet0M500.M()  )
        self.ak8SDsj0_m600 = self.CorrPUPPIMass( self.ak8SDJet_Subjet0M600.Perp() , self.ak8SDJet_Subjet0M600.Eta(), self.ak8SDJet_Subjet0M600.M()  )


        self.tau21 = self.tree.JetPuppiTau21[0]
        self.tau32 = self.tree.JetPuppiTau32[0]
        #print 'ak8SDJet = (%6.2f,%8.3f,%8.3f,%6.2f)' % ( self.ak8SDJet.Perp(), self.ak8SDJet.Eta(), self.ak8SDJet.Phi(), self.ak8SDJet.M() )


        # Work the cut flow
        self.passed = [False] * self.nstages
        self.passed[0] = self.lepsel.passed[ len( self.lepsel.passed) - 1]

        if not self.passed[0] : return self.passed

        if not (self.ak8Jet.Perp() > 200. and abs(self.ak8Jet.Eta()) < 2.4  ) : return self.passed
        self.passed[1] = True

        if not ( self.ak4JetBdisc > self.bdiscmin ) : return self.passed
        self.passed[2] = True
        
        if not ( 30. < self.ak8SDJet.M() < 150. ) : return self.passed
        self.passed[3] = True

        if not ( self.tau21 < self.tau21Cut ) : return self.passed
        self.passed[4] = True

        return self.passed


    def CorrPUPPIMass(self, puppipt, puppieta, puppimraw) : #{
        if puppimraw < 0.1 : return 0.0
        self.genCorr  = 1.
        self.recoCorr = 1.
        self.totalWeight = 1.

        self.genCorr =  self.puppisd_corrGEN.Eval( puppipt )
    
        if (abs(puppieta) <=1.3 ): self.recoCorr = self.puppisd_corrRECO_cen.Eval(puppipt)
        if (abs(puppieta) > 1.3 ): self.recoCorr = self.puppisd_corrRECO_for.Eval(puppipt)
        self.totalWeight = self.genCorr * self.recoCorr
        self.puppim = self.totalWeight * puppimraw
        #print "Puppi mass corr is {0:2.2f} for jet of raw mass {1:2.2f} and new mass {2:2.2f}".format(totalWeight ,puppimraw, puppim)
        return self.puppim
        #}                  

                        

    
