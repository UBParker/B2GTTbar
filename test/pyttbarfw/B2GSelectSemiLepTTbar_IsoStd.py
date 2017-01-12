#! /usr/bin/env python

import ROOT

import TrigMap

class B2GSelectSemiLepTTbar_IsoStd( ) :
    """
    Selects boosted semileptonic ttbar events with standard isolation.
    """
    def __init__(self, options, tree ):
        self.ignoreTrig = options.ignoreTrig
        self.nstages = 10
        self.tree = tree        
        self.trigMap = TrigMap.TrigMap()

        # Cached class member variables for plotting
        self.leptonP4 = None
        self.nuP4 = None
        self.trigIndex = [ self.trigMap.HLT_Mu50_v ] ### To-Do: Add other trigger as suggested here https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2
        self.printAK4Warning = True

        self.passed = [False] * self.nstages  
        self.passedCount = [0] * self.nstages
    """
        This is the "select" function that does the work for the event selection. If you have any complicated
        stuff to do, do it here and create a class member variable to cache the results. 
    """
    def select( self ) :

        self.leptonP4 = None
        self.nuP4 = None
        self.ak4Jet = None
        self.ak8Jet = None
        self.ak8SDJet = None
        

        self.leptonP4 = ROOT.TLorentzVector()
        self.leptonP4.SetPtEtaPhiM( self.tree.LeptonPt[0], self.tree.LeptonEta[0], self.tree.LeptonPhi[0], 0)
        self.nuP4 = ROOT.TLorentzVector( self.tree.SemiLeptMETpt[0], self.tree.SemiLeptMETpx[0], self.tree.SemiLeptMETpy[0], 0. )
        self.ak4Jet = ROOT.TLorentzVector()
        # INCORRECT: NEED TO FILL JET MASS FOR AK4 JETS
        # For now it is okay because we only use the 3-vector (delta r to lepton)
        self.ak4Jet.SetPtEtaPhiM( self.tree.AK4_dRminLep_Pt[0], self.tree.AK4_dRminLep_Eta[0], self.tree.AK4_dRminLep_Phi[0], self.tree.AK4_dRminLep_Mass[0] )

        # Work the cut flow
        # Stage 0 : None.
        # Stage 1 : Trigger
        # Stage 2 : Lepton selection
        # Stage 3 : MET selection
        # Stage 4 : Leptonic-side AK4 jet selection
        # Stage 5 : Wlep pt selection
        self.passed = [False] * self.nstages
        self.passedCount = [0] * self.nstages

        self.passed[0] = True
        self.passedCount[0] += 1

        if not self.ignoreTrig : 
            for itrig in self.trigIndex :
                if bool ( self.tree.SemiLeptTrigPass[itrig] ) == True :
                    self.passed[1] = True
            if not self.passed[1] : return self.passed
        else :
            self.passed[1] = True
        self.passedCount[1] += 1

        if not ( self.tree.LeptonIsMu[0] == 1  and self.tree.MuHighPt[0] ==1 ): return self.passed #or  (self.tree.LeptonIsMu[0] == 0 and self.leptonP4.Perp() > 120. and (0. < abs(self.leptonP4.Eta()) < 1.442 or 1.56  < abs(self.leptonP4.Eta()) < 2.5 )and self.tree.Electron_noiso_passTight[0] == 1 and  self.tree.Electron_iso_passHEEP[0] ==1  )  ): return self.passed
        self.passed[2] = True
        self.passedCount[2] += 1 
        
        if not ( self.tree.LeptonIsMu[0] == 1 and  self.tree.MuTight[0] == 1  ) :  return self.passed  #or  (self.tree.LeptonIsMu[0] == 0 and self.leptonP4.Perp() > 120. and (0. < abs(self.leptonP4.Eta()) < 1.442 or 1.56  < abs(self.leptonP4.Eta()) < 2.5 )and self.tree.Electron_noiso_passTight[0] == 1 and  self.tree.Electron_iso_passHEEP[0] ==1  )  ): return self.passed
        self.passed[3] = True
        self.passedCount[3] += 1         


        if not ( self.tree.LeptonIsMu[0] == 1 and self.leptonP4.Perp() > 53. and abs(self.leptonP4.Eta()) < 2.1 ): return self.passed  # and self.tree.MuTight[0] == 1 and self.tree.MuIso[0] < 0.1 and self.tree.MuHighPt[0] ==1 ) or  (self.tree.LeptonIsMu[0] == 0 and self.leptonP4.Perp() > 120. and (0. < abs(self.leptonP4.Eta()) < 1.442 or 1.56  < abs(self.leptonP4.Eta()) < 2.5 )and self.tree.Electron_noiso_passTight[0] == 1 and  self.tree.Electron_iso_passHEEP[0] ==1  )  ): return self.passed
        self.passed[4] = True
        self.passedCount[4] += 1        


        if not ( self.tree.LeptonIsMu[0] == 1 and self.tree.MuIso[0] < 0.1 ): return self.passed  # and self.tree.MuTight[0] == 1 and self.tree.MuIso[0] < 0.1 and self.tree.MuHighPt[0] ==1 ) or  (self.tree.LeptonIsMu[0] == 0 and self.leptonP4.Perp() > 120. and (0. < abs(self.leptonP4.Eta()) < 1.442 or 1.56  < abs(self.leptonP4.Eta()) < 2.5 )and self.tree.Electron_noiso_passTight[0] == 1 and  self.tree.Electron_iso_passHEEP[0] ==1  )  ): return self.passed
        self.passed[5] = True
        self.passedCount[5] += 1 
        
        
        if not ( self.tree.LeptonIsMu[0] == 1 and self.nuP4.Perp() > 40.): return self.passed  #or ( self.tree.LeptonIsMu[0] == 0 and self.nuP4.Perp() > 80.) : return self.passed
        self.passed[6] = True
        self.passedCount[6] += 1
        
        if not ( self.tree.LeptonIsMu[0] == 1 and self.ak4Jet.Perp() > 30. and abs(self.ak4Jet.Eta()) < 2.4  ) : return self.passed
        self.passed[7] = True
        self.passedCount[7] += 1
        
        if not ( self.tree.LeptonIsMu[0] == 1 and self.tree.DeltaRJetLep[0] > .4 ) : return self.passed # To-do: Hemisphere cut btw lepton and W candidate ak8 , check this is actually dR(lep, AK8)
        self.passed[8] = True
        self.passedCount[8] += 1

        if not (  self.tree.LeptonIsMu[0] == 1 and (self.leptonP4 + self.nuP4).Perp() > 200. )    : return self.passed
        self.passed[9] = True
        self.passedCount[9] += 1
        
        return self.passed

                    

    
