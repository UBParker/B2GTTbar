#! /usr/bin/env python

import ROOT

import TrigMap

class B2GSelectSemiLepTTbar_Iso2D( ) :
    """
    Selects boosted semileptonic ttbar events with standard isolation.
    """
    def __init__(self, options, tree ):
        self.ignoreTrig = options.ignoreTrig
        self.verbose = options.verbose
        self.infile = options.infile

        self.nstages = 8
        if self.verbose: print "Begin leptonic top selection with {} stages".format(self.nstages)
        self.tree = tree        
        self.trigMap = TrigMap.TrigMap()

        # Define Kinematic Cut Values
        
        #Stage 1 (Trigger) TO-DO: add electron triggers

        #Stage 2
        self.muonPtCut = 50.
        self.muonEtaCut = 2.1

        #Stage 3
        self.muonMETPtCut = 50.

        #Stage 4
        self.AK4jet0PtCut = 30.

        # Stage 5
        self.AK4jet1PtCut = 50.
        self.AK4EtaCut = 2.4
            
        #Stage 6
        self.DrAK4Lep = 0.4
        self.PtRel = 20.

        #Stage 7 - DR(AK8, Lepton) > 1.

        #Stage 8
        self.MuonHtLepCut = 150.




        # Cached class member variables for plotting
        self.leptonP4 = None
        self.nuP4 = None
        self.ak4Jet0 = None
        self.ak4Jet1 = None
        self.ak4Jet1Pt = None
        self.ak4Jet1Eta = None

        self.trigIndex = [
            self.trigMap.HLT_Mu45_eta2p1_v,
            #self.trigMap.HLT_Mu30_eta2p1_PFJet150_PFJet50_v,
            #self.trigMap.HLT_Mu40_eta2p1_PFJet200_PFJet50_v,
            #self.trigMap.HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v,
            #self.trigMap.HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet140_v,
            #self.trigMap.HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v
            ]

        #self.printAK4Warning = True

        self.passed = [False] * self.nstages  
        self.passedCount = [0] * self.nstages


        ### The total weight
        self.theWeight = None

        ### Muon trigger efficiency corrections
  
        self.TriggEffIs = 1.0  
        self.finCor1 = ROOT.TFile.Open( "./SingleMuonTrigger_Z_RunBCD_prompt80X_7p65.root","READ")
        self.PtetaTriggEff_Run273158_to_274093      = self.finCor1.Get("Mu45_eta2p1_PtEtaBins_Run273158_to_274093/efficienciesDATA/pt_abseta_DATA")
        self.PtetaTriggEff_Run274094_to_276097      = self.finCor1.Get("Mu45_eta2p1_PtEtaBins_Run274094_to_276097/efficienciesDATA/pt_abseta_DATA")
        ### Muon cut based ID corrections
  
        self.CutIDScaleFIs = 1.0  
        self.finCor2 = ROOT.TFile.Open( "./MuonID_Z_RunBCD_prompt80X_7p65.root","READ")
        self.PtetaCutIDScaleF      = self.finCor2.Get("MC_NUM_MediumID_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio")

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

        self.leptonP4 = None
        self.nuP4 = None
        self.ak4Jet0 = None
        self.ak4Jet1 = None
        self.ak4Jet1Pt = None
        self.ak4Jet1Eta = None
        self.theWeight = None

        self.leptonP4 = ROOT.TLorentzVector()
        self.leptonP4.SetPtEtaPhiM( 
                                   self.tree.LeptonPt[0],
                                   self.tree.LeptonEta[0],
                                   self.tree.LeptonPhi[0], 
                                                       0. )

        ### MC generator weights and PU  weights
        if self.itIsData :
            self.EventWeight = 1.0
            self.PUWeight = 1.0
        else:
            self.EventWeight = self.tree.SemiLeptEventWeight[0]
            self.PUWeight = self.tree.SemiLeptPUweight[0]               


        ### Muon trigger efficiency and cut based ID weights  (NOTE: Add these to type 2 and also add Iso SF in that case)
        if self.tree.LeptonIsMu[0] == 1 and not self.itIsData :
            self.TriggEffIs = self.MuonTriggEff( self.leptonP4.Perp() , abs(self.leptonP4.Eta())   , self.tree.SemiLeptRunNum[0] )
            if self.verbose : "Muon trigger eff is {0:2.4f} for pt {1:2.4f} and abs(eta) {2:2.4f}".format(self.TriggEffIs,self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )

            self.CutIDScaleFIs = self.MuonCutIDScaleF( self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )
            if self.verbose : "Muon Cut ID eff is {0:2.4f} for pt {1:2.4f} and abs(eta) {2:2.4f}".format(self.CutIDScaleFIs,self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )

        self.theWeight =  self.EventWeight * self.PUWeight * self.TriggEffIs * self.CutIDScaleFIs
        if self.verbose : print "Total Weight {0:2.4f} = Event weight {1:2.4f} * PU weight {2:2.4f} *Trigger Eff. {3:2.4f} * Cut ID {4:2.4f} ".format(self.theWeight, self.EventWeight , self.PUWeight , self.TriggEffIs , self.CutIDScaleFIs)


        ### Define the 4 vectors of the leptonic top system

        self.nuP4 = ROOT.TLorentzVector()
        self.nuP4 = ROOT.TLorentzVector( 
                                        self.tree.SemiLeptMETpt[0],
                                        self.tree.SemiLeptMETpx[0], 
                                        self.tree.SemiLeptMETpy[0], 
                                                                0. )
        self.ak4Jet0 = ROOT.TLorentzVector()
        self.ak4Jet0.SetPtEtaPhiM( 
	                                self.tree.AK4_dRminLep_Pt[0], 
                                    self.tree.AK4_dRminLep_Eta[0], 
                                    self.tree.AK4_dRminLep_Phi[0], 
                                    self.tree.AK4_dRminLep_Mass[0] )

        '''
        if self.printAK4Warning :
            print '----------------------------------- WARNING --------------------------------------'
            print '    AK4 jet mass is not set correctly. It is set to zero because it is not filled.'
            print '    To be fixed. Do NOT use the AK4 four vector, but you can use the three vector.'
            self.printAK4Warning = False
        '''
        # Work the cut flow
        # Stage 0 : None.
        # Stage 1 : Trigger
        # Stage 2 : Lepton selection
        # Stage 3 : MET selection
        # Stage 4 : Leptonic-side AK4 jet selection
        # Stage 5 : Hemisphere cut (keep leptons far from AK8 Jet)
        # Stage 6 : Wlep pt selection


        self.passed = [False] * self.nstages
        self.passedCount = [0] * self.nstages

        self.passed[0] = True
        self.passedCount[0] += 1

        if not self.ignoreTrig : 
            for itrig in self.trigIndex :
                if bool ( self.tree.SemiLeptTrigPass[itrig] ) == True :
                    self.passed[1] = True
                    self.passedCount[1] += 1
                    self.passedTrigIndex = itrig 
            if not self.passed[1] : return self.passed
            #if self.verbose :             print "Passed trig index is {}".format( self.passedTrigIndex)

            self.passedTrig = "Did not Pass"
            if self.passedTrigIndex == 16 :        self.passedTrig = "HLT_Mu45_eta2p1_v"
            #if self.passedTrigIndex == 22 :        self.passedTrig = "HLT_Mu30_eta2p1_PFJet150_PFJet50_v"
            #if self.passedTrigIndex == 23 :        self.passedTrig = "HLT_Mu40_eta2p1_PFJet200_PFJet50_v"
            if ( self.passedTrigIndex != 16 ) :   print "TRIGGER ERROR! Passed unexpected trigger {}".format(self.TrigMap.names[self.passedTrigIndex])
            # See trigger list here https://github.com/UBParker/B2GTTbar/blob/TreeV3/test/pyttbarfw/TrigMap.py

            if self.verbose : 
                print "Event number {0:5.0f} passed :".format(self.tree.SemiLeptEventNum[0])
                print "Stage 1: Trigger {}".format(self.passedTrig) 
        else :
            self.passed[1] = True
            self.passedCount[1] += 1
            if self.verbose : 
                print "Event passed :"
                print "Stage 1: No Trigger cut applied to this MC sample"


        if not (( self.tree.LeptonIsMu[0] == 1 and self.leptonP4.Perp() > self.muonPtCut and abs(self.leptonP4.Eta()) < self.muonEtaCut and self.tree.MuMedium[0] == 1) or (self.tree.LeptonIsMu[0] == 0 and  self.leptonP4.Perp() > 50. and abs(self.leptonP4.Eta()) < 2.5 )) : #and self.tree.MuTight[0]
            return self.passed
        self.passed[2] = True
        self.passedCount[2] += 1
        if self.verbose : print "Stage 2: lepton pt {0:2.4f} GeV > ({1:2.4f} GeV), eta {2:2.4f} < ( {3:2.4f} ), MediumID is {4}".format(
                                                                        self.leptonP4.Perp(),
                                                                        self.muonPtCut,                       
                                                                        self.leptonP4.Eta(),
                                                                        self.muonEtaCut,
                                                                        self.tree.MuMedium[0])

        if not ( self.nuP4.Perp() > self.muonMETPtCut) : return self.passed 
        self.passed[3] = True
        self.passedCount[3] += 1
        if self.verbose : print "Stage 3: MET pt {0:2.4f} GeV > ( {1:2.4f} GeV ) ".format(
                                                                        self.nuP4.Perp(),
                                                                        self.muonMETPtCut )

 
        if not ( self.ak4Jet0.Perp() > self.AK4jet0PtCut and abs(self.ak4Jet0.Eta()) < self.AK4EtaCut  ) : return self.passed    
        self.passed[4] = True
        self.passedCount[4] += 1
        if self.verbose : print "Stage 4: AK4 jet 0 pt {0:2.4f} GeV > ( {1:2.4f} GeV ) and eta {2:2.4f} < ( {3:2.4f} )".format( 
                                                                                             self.ak4Jet0.Perp(),
                                                                                             self.AK4jet0PtCut, 
                                                                                             self.ak4Jet0.Eta(),
                                                                                             self.AK4EtaCut)       

        # NOTE: This jet cut was found to be strongly suboptimal by the semileptonic team. They had better performance at pt > 15 GeV, with 
        # delta R < 0.4 and ptrel > 20. For now, we will raise the HTLep cut and ptrel cut but we need to fix this.
        if not  (self.tree.AK4_dRminLep_dRlep[0] > 0.4 or self.tree.PtRel[0] > self.PtRel ) : return self.passed
        self.passed[5] = True
        self.passedCount[5] += 1
        if self.verbose : print "Stage 5: DR(AK4, lep) {0:2.4f}  > ( {1:2.4f} ) and PtRel(AK4, lep) {2:2.4f} > ( {3:2.4f} )".format( 
                                                                                                      self.tree.AK4_dRminLep_dRlep[0],
                                                                                                                        self.DrAK4Lep,
                                                                                                                   self.tree.PtRel[0],
                                                                                                                           self.PtRel)
        if not ( self.tree.DeltaRJetLep[0] > 1. ) : return self.passed # Hemisphere cut btw lepton and the ak8
        self.passed[6] = True
        self.passedCount[6] += 1
        if self.verbose : print "Stage 6: DR(AK8, lep) {0:2.4f}  > ( 1.0 )".format( self.tree.DeltaRJetLep[0] )

        if not ( (self.leptonP4 + self.nuP4).Perp() > self.MuonHtLepCut ) : return self.passed
        self.passed[7] = True
        self.passedCount[7] += 1
        if self.verbose : print "Stage 7: Leptonic W Pt (Lepton Pt + MET Pt ) {0:2.4f} > ( {1:2.4f} GeV )".format( (self.leptonP4 + self.nuP4).Perp(), self.MuonHtLepCut )

        return self.passed

    def MuonTriggEff(self, muonpt, muoneta, runNum) : #{ROOT file from
        #https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults
        TriggEff = 1.
        runNumIs = None
        if muonpt >= 500. :
            TriggEff = 0.0
        else :
            ### Note: This needs to be updated as SFs for new data become available...
            ### To-DO: decide which percentage to weight by each run histo
            binx = self.PtetaTriggEff_Run274094_to_276097.GetXaxis().FindBin( muonpt  )
            biny = self.PtetaTriggEff_Run274094_to_276097.GetYaxis().FindBin( muoneta )
            TriggEff = self.PtetaTriggEff_Run274094_to_276097.GetBinContent(binx, biny )
            if self.verbose : print "get bin: x (using pt) {}, y (using eta) {}, CUt ID Eff is {}".format(binx, biny, TriggEff )
            '''
            if 273150. <= runNum <= 274093. :
                runNumIs = "Run273158_to_274093"
                binx = self.PtetaTriggEff_Run273158_to_274093.GetXaxis().FindBin( muonpt  )
                biny = self.PtetaTriggEff_Run273158_to_274093.GetYaxis().FindBin( muoneta )
                TriggEff = self.PtetaTriggEff_Run273158_to_274093.GetBinContent(binx, biny )
                if self.verbose : print "get bin: x (using pt) {}, y (using eta) {}, TriggEff is {}".format(binx, biny, TriggEff )


            if 274094. <= runNum: #  <= 276097. :
                runNumIs = "Run274094_to_276097"
                binx = self.PtetaTriggEff_Run274094_to_276097.GetXaxis().FindBin( muonpt  )
                biny = self.PtetaTriggEff_Run274094_to_276097.GetYaxis().FindBin( muoneta )
                TriggEff = self.PtetaTriggEff_Run274094_to_276097.GetBinContent(binx, biny )
                if self.verbose : print "get bin: x (using pt) {}, y (using eta) {}, CUt ID Eff is {}".format(binx, biny, TriggEff )
            
            if self.verbose : print "Run number is : {}, using {} histo to find Trigger Eff".format(runNum, runNumIs)

            '''
        return float(TriggEff)      
  
    def MuonCutIDScaleF(self, muonpt, muoneta) : #{ROOT file from
        #https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults
        if muonpt >= 500. :
            CutIDScaleF = 0.0
        else :
            binx = self.PtetaCutIDScaleF.GetXaxis().FindBin( muonpt  )
            biny = self.PtetaCutIDScaleF.GetYaxis().FindBin( muoneta )
            CutIDScaleF = self.PtetaCutIDScaleF.GetBinContent(binx, biny )
            if self.verbose : print "get bin: x (using pt) {}, y (using eta) {}, CUt ID Eff is {}".format(binx, biny, CutIDScaleF )
        return float(CutIDScaleF)      



