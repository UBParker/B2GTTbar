#! /usr/bin/env python

import ROOT

class B2GSelectSemiLepTTbar_Type1( ) :
    """
    Selects semileptonic ttbar events with widely separated top quarks.
    This selects type 2 top events with traditional lepton isolation.
    """
    def __init__(self, options, tree, lepsel ):
        self.puppitau21Cut = options.tau21Cut
        self.puppitau32Cut = options.tau32Cut
        self.bdiscmin = options.bdiscmin
        self.ignoreTrig = options.ignoreTrig
        self.nstages = 5
        self.tree = tree
        self.lepsel = lepsel
        self.passed = [False] * self.nstages
        self.passedCount = [0] * self.nstages

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

        # PUPPI jet mass corrections

        self.finCor1 = ROOT.TFile.Open( "./puppiCorr.root","READ")
        self.puppisd_corrGEN      = self.finCor1.Get("puppiJECcorr_gen")
        self.puppisd_corrRECO_cen = self.finCor1.Get("puppiJECcorr_reco_0eta1v3")
        self.puppisd_corrRECO_for = self.finCor1.Get("puppiJECcorr_reco_1v3eta2v5")

    """
        This is the "select" function that does the work for the event selection. If you have any complicated
        stuff to do, do it here and create a class member variable to cache the results. 
    """
    def select( self ) :

        self.passedCount = [0] * self.nstages

        self.EventWeight = self.tree.SemiLeptEventWeight[0]
        self.PUWeight = self.tree.SemiLeptPUweight[0]  
        '''
        if 'root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/b2gtree_SingleMuon_Run2016BCD.root' is options.infile:
            self.EventWeight = 1.0                                    FIx THis ???
            self.PUWeight = 1.0                         QUESTION: How do I import options for use in this function definition ???
            print "setting weights to 1."                      ANSWER: equate option to self member variable!!!
        '''
        self.PuppiCorr = self.tree.JetPuppiCorrFactor[0]  
        self.Corr = self.tree.JetCorrFactor[0]  
        self.CorrL2L3 = self.tree.JetSDptCorrL23[0]  
        self.CorrL2L3SD = self.tree.JetSDmassCorrL23

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



        self.ak4Jet = ROOT.TLorentzVector( )        
        self.ak4Jet.SetPtEtaPhiM( self.tree.AK4_dRminLep_Pt[0],
                                  self.tree.AK4_dRminLep_Eta[0],
                                  self.tree.AK4_dRminLep_Phi[0],
                                  self.tree.AK4_dRminLep_Mass[0] )
        self.ak4JetBdisc = self.tree.AK4_dRminLep_Bdisc[0]

        self.ak8Jet = ROOT.TLorentzVector()
        self.ak8Jet.SetPtEtaPhiM( self.tree.JetPt[0],
                                  self.tree.JetEta[0],
                                  self.tree.JetPhi[0],
                                  self.tree.JetMass[0] )        
        self.ak8JetRaw =   self.ak8Jet
        self.ak8Jet =   self.ak8Jet * self.Corr
        self.ak8_m = self.CorrPUPPIMass( self.ak8JetRaw.Perp() , self.ak8JetRaw.Eta(), self.ak8JetRaw.M()  )

        self.ak8PuppiJet = ROOT.TLorentzVector()
        self.ak8PuppiJet.SetPtEtaPhiM( self.tree.JetPuppiPt[0],
                                  self.tree.JetPuppiEta[0],
                                  self.tree.JetPuppiPhi[0],
                                  self.tree.JetPuppiMass[0] )        
        self.ak8PuppiJetRaw =   self.ak8PuppiJet
        self.ak8PuppiJet =   self.ak8PuppiJet * self.PuppiCorr
        self.ak8_Puppim = self.CorrPUPPIMass( self.ak8PuppiJetRaw.Perp() , self.ak8PuppiJetRaw.Eta(), self.ak8PuppiJetRaw.M()  )

        self.ak8SDJet = ROOT.TLorentzVector()
        self.ak8SDJet.SetPtEtaPhiM( self.tree.JetSDptRaw[0],
                                  self.tree.JetSDetaRaw[0],
                                  self.tree.JetSDphiRaw[0],
                                  self.tree.JetSDmassRaw[0] )        
        self.ak8SDJetRaw =   self.ak8SDJet
        self.ak8SDJet =   self.ak8SDJet * self.Corr
        self.ak8_SDm = self.CorrPUPPIMass( self.ak8SDJetRaw.Perp() , self.ak8SDJetRaw.Eta(), self.ak8SDJetRaw.M()  )


        self.ak8PuppiSDJet_Subjet0 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet0.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0],
                                            self.tree.JetPuppiSDsubjet0eta[0], 
                                            self.tree.JetPuppiSDsubjet0phi[0], 
                                            self.tree.JetPuppiSDsubjet0mass[0] )
        self.ak8PuppiSDJet_Subjet0Raw =   self.ak8PuppiSDJet_Subjet0 
        self.ak8PuppiSDJet_Subjet0 =   self.ak8PuppiSDJet_Subjet0  * self.PuppiCorr

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
        self.ak8PuppiSD_m = self.CorrPUPPIMass( self.ak8PuppiSDJetRaw.Perp() , self.ak8PuppiSDJetRaw.Eta(), self.ak8PuppiSDJetRaw.M()  )

        self.ak8SDsj0_m = self.CorrPUPPIMass( self.ak8PuppiSDJet_Subjet0Raw.Perp() , self.ak8PuppiSDJet_Subjet0Raw.Eta(), self.ak8PuppiSDJet_Subjet0Raw.M()  )


        self.ak8PuppiJet200 =ROOT.TLorentzVector()
        self.ak8PuppiSDJet200 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet0M200 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet1M200 = ROOT.TLorentzVector()

        if (  200. < self.ak8PuppiSDJet_Subjet0.Perp() < 300. ) :
            self.ak8PuppiJet200.SetPtEtaPhiM( self.tree.JetPuppiPt[0], self.tree.JetPuppiEta[0], self.tree.JetPuppiPhi[0], self.tree.JetPuppiMass[0] ) 
            self.ak8PuppiSDJet_Subjet0M200.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
            self.ak8PuppiSDJet_Subjet1M200.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8PuppiSDJet200 =  self.ak8PuppiSDJet_Subjet0M200 + self.ak8PuppiSDJet_Subjet1M200

        self.ak8PuppiJet300 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet300 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet0M300 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet1M300 = ROOT.TLorentzVector()
        if (  300. < self.ak8PuppiSDJet_Subjet0.Perp() < 400. ) :
            self.ak8PuppiJet300.SetPtEtaPhiM( self.tree.JetPuppiPt[0], self.tree.JetPuppiEta[0], self.tree.JetPuppiPhi[0], self.tree.JetPuppiMass[0] ) 
            self.ak8PuppiSDJet_Subjet0M300.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
            self.ak8PuppiSDJet_Subjet1M300.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8PuppiSDJet300 =  self.ak8PuppiSDJet_Subjet0M300 + self.ak8PuppiSDJet_Subjet1M300
        self.ak8PuppiJet400 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet400 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet0M400 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet1M400 = ROOT.TLorentzVector()
        if (  400. < self.ak8PuppiSDJet_Subjet0.Perp() < 500. ) :
            self.ak8PuppiJet400.SetPtEtaPhiM( self.tree.JetPuppiPt[0], self.tree.JetPuppiEta[0], self.tree.JetPuppiPhi[0], self.tree.JetPuppiMass[0] ) 
            self.ak8PuppiSDJet_Subjet0M400.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
            #print "Raw mass of sd subjet0 is {0:2.3f}".format(self.ak8PuppiSDJet_Subjet0M400.M())
            self.ak8PuppiSDJet_Subjet1M400.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8PuppiSDJet400 =  self.ak8PuppiSDJet_Subjet0M400 + self.ak8PuppiSDJet_Subjet1M400

        self.ak8PuppiJet500 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet500 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet0M500 = ROOT.TLorentzVector()
        self.ak8PuppiSDJet_Subjet1M500 = ROOT.TLorentzVector()
        if (  500. < self.ak8PuppiSDJet_Subjet0.Perp() < 800. ) :
            self.ak8PuppiJet500.SetPtEtaPhiM( self.tree.JetPuppiPt[0], self.tree.JetPuppiEta[0], self.tree.JetPuppiPhi[0], self.tree.JetPuppiMass[0] ) 
            self.ak8PuppiSDJet_Subjet0M500.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
            self.ak8PuppiSDJet_Subjet1M500.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )
            self.ak8PuppiSDJet500 =  self.ak8PuppiSDJet_Subjet0M500 + self.ak8PuppiSDJet_Subjet1M500



        self.ak8SDsj0_m200 = self.CorrPUPPIMass( self.ak8PuppiSDJet_Subjet0M200.Perp()* self.PuppiCorr , self.ak8PuppiSDJet_Subjet0M200.Eta(), self.ak8PuppiSDJet_Subjet0M200.M()  )
        self.ak8SDsj0_m300 =  self.CorrPUPPIMass( self.ak8PuppiSDJet_Subjet0M300.Perp() * self.PuppiCorr , self.ak8PuppiSDJet_Subjet0M300.Eta(), self.ak8PuppiSDJet_Subjet0M300.M()  )

        self.ak8SDsj0_m400 =  self.CorrPUPPIMass( self.ak8PuppiSDJet_Subjet0M400.Perp()* self.PuppiCorr , self.ak8PuppiSDJet_Subjet0M400.Eta(), self.ak8PuppiSDJet_Subjet0M400.M()  )
        self.ak8SDsj0_m500 =  self.CorrPUPPIMass( self.ak8PuppiSDJet_Subjet0M500.Perp()* self.PuppiCorr , self.ak8PuppiSDJet_Subjet0M500.Eta(), self.ak8PuppiSDJet_Subjet0M500.M()  )

        #if (  400. < self.ak8PuppiSDJet_Subjet0.Perp() < 500. ) :print "mass of sd subjet0 after puppi corr is {0:2.3f}".format(self.ak8SDsj0_m400)
        self.puppitau32 = self.tree.JetPuppiTau32[0]
        self.puppitau21 = self.tree.JetPuppiTau21[0]
        #if options.verbose : print 'ak8PuppiSDJet = (%6.2f,%8.3f,%8.3f,%6.2f)' % ( self.ak8PuppiSDJet.Perp(), self.ak8PuppiSDJet.Eta(), self.ak8PuppiSDJet.Phi(), self.ak8PuppiSDJet.M() )


        # Work the cut flow
        self.passedCount = [0] * self.nstages
        self.passed = [False] * self.nstages
        self.passed[0] = self.lepsel.passed[ len(self.lepsel.passed) - 1]
        if not self.passed[0] : return self.passed
        self.passedCount[0] += 1

        if not (self.ak8PuppiJet.Perp() > 250. and abs(self.ak8PuppiJet.Eta()) < 2.4 ) : return self.passed
        self.passed[1] = True
        self.passedCount[1] += 1

        if not ( self.ak4JetBdisc >  self.bdiscmin  ) : return self.passed
        self.passed[2] = True
        self.passedCount[2] += 1
        
        if not ( 110. < self.ak8PuppiSDJet.M() < 210. ) : return self.passed
        self.passed[3] = True
        self.passedCount[3] += 1

        if not ( self.puppitau32 < self.puppitau32Cut ) : return self.passed
        self.passed[4] = True
        self.passedCount[4] += 1
        #print "mass of sd subjet0 after puppi corr in bin 200-300 {0:2.3f}, 300-400 {1:2.3f}, 400-500 {2:2.3f}, 500-600 {3:2.3f}, 600-800 {4:2.3f}".format(self.ak8SDsj0_m200,self.ak8SDsj0_m300,self.ak8SDsj0_m400,self.ak8SDsj0_m500,self.ak8SDsj0_m600)

        return self.passed#, self.passedCount


    def CorrPUPPIMass(self, puppiptcorr, puppieta, puppimRaw) : #{ Adapted from https://github.com/thaarres/PuppiSoftdropMassCorr

        if puppimRaw < 0.0000000000001 : return 0.0
        self.genCorr  = 1.
        self.recoCorr = 1.
        self.totalWeight = 1.

        self.genCorr =  self.puppisd_corrGEN.Eval(     puppiptcorr )
    
        if (abs(puppieta) <=1.3 ): self.recoCorr = self.puppisd_corrRECO_cen.Eval(    puppiptcorr)
        if (abs(puppieta) > 1.3 ): self.recoCorr = self.puppisd_corrRECO_for.Eval(    puppiptcorr)
        self.totalWeight = self.genCorr * self.recoCorr
        self.puppim = self.totalWeight * puppimRaw
        #if 0. <puppimRaw<0.1 :
        #print "Puppi mass corr is {0:2.2f} for jet of Raw mass {1:2.2f} and new mass {2:2.2f}".format(self.totalWeight ,puppimRaw, self.puppim)
        return self.puppim
        #}                  

    
