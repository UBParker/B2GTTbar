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

        # Cached class member variables for plotting
        self.ak4Jet = None
        self.ak8Jet = None
        self.ak8SDJet = None
        self.ak8SDJet_Subjet0 = None
        self.ak8SDJet_Subjet1 = None
        self.ak4JetBdisc = None

        self.passed = [False] * self.nstages      


    """
        This is the "select" function that does the work for the event selection. If you have any complicated
        stuff to do, do it here and create a class member variable to cache the results. 
    """
    def select( self ) :

        self.EventWeight = self.tree.SemiLeptEventWeight[0]

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
        self.ak8SDJet_Subjet0 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet1 = ROOT.TLorentzVector()
        self.ak8SDJet_Subjet0.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
        self.ak8SDJet_Subjet1.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )

        if self.ak8SDJet_Subjet0.M() < self.ak8SDJet_Subjet1.M() : 
            self.ak8SDJet_Subjet1,self.ak8SDJet_Subjet0 = self.ak8SDJet_Subjet0,self.ak8SDJet_Subjet1
        self.ak8SDJet =  self.ak8SDJet_Subjet0 +  self.ak8SDJet_Subjet1
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
        
        if not ( 40. < self.ak8SDJet.M() < 150. ) : return self.passed
        self.passed[3] = True

        if not ( self.tau21 < self.tau21Cut ) : return self.passed
        self.passed[4] = True

        return self.passed

 
