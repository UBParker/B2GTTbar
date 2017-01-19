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
        self.verbose = options.verbose
        self.infile = options.infile

        # Cached class member variables for plotting
        self.leptonP4 = None
        self.nuP4 = None
        self.ak4Jet = None
        self.ak8Jet = None
        self.ak8SDJet = None
        self.trigIndex = [ self.trigMap.HLT_Mu50_v ] ### To-Do: Add other trigger as suggested here https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2
        self.printAK4Warning = True

        self.passed = [False] * self.nstages  
        self.passedCount = [0] * self.nstages
        
        ### Create empty weights used for histo filling
        self.theWeight = 1.
        self.EventWeight = 1.
        self.PUWeight = 1.

        ### Muon trigger efficiency corrections
  
        self.TriggEffIs = 1.0  
        self.finCor1 = ROOT.TFile.Open( "./SingleMuonTrigger_Z_RunBCD_prompt80X_7p65.root","READ")
        self.PtetaTriggEff_Run273158_to_274093      = self.finCor1.Get("Mu45_eta2p1_PtEtaBins_Run273158_to_274093/efficienciesDATA/pt_abseta_DATA")
        self.PtetaTriggEff_Run274094_to_276097      = self.finCor1.Get("Mu45_eta2p1_PtEtaBins_Run274094_to_276097/efficienciesDATA/pt_abseta_DATA")
        ### Muon cut based ID corrections
  
        self.CutIDScaleFIs = 1.0  
        self.CutIDScaleFLooseIs = 1.0  
        self.finCor2 = ROOT.TFile.Open( "./MuonID_Z_RunBCD_prompt80X_7p65.root","READ")
        self.PtetaCutIDScaleFTight      = self.finCor2.Get("MC_NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio")
        self.PtetaCutIDScaleFLoose      = self.finCor2.Get("MC_NUM_LooseID_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio")
        ### Muon HIP SF
  
        self.MuonHIPScaleFIs = 1.0  
        self.finCor3 = ROOT.TFile.Open( "./ratios.root","READ")
        self.ratio_eta   =   self.finCor3.Get("ratio_eta")
        ### B tag weights       
        ### Adapted from example https://twiki.cern.ch/twiki/bin/view/CMS/BTagCalibration#Code_example_in_Python
        ### Applied work around 2. listed here  https://twiki.cern.ch/twiki/bin/view/CMS/BTagCalibration#Additional_scripts

        # from within CMSSW:
        ROOT.gSystem.Load('libCondFormatsBTauObjects') 
        ROOT.gSystem.Load('libCondToolsBTau') 

        # OR using standalone code:
        #ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cpp+') 

        # get the sf data loaded
        self.calib = ROOT.BTagCalibration('csvv2_ichep', 'CSVv2_ichep.csv')

        # making a std::vector<std::string>> in python is a bit awkward, 
        # but works with root (needed to load other sys types):
        self.v_sys = getattr(ROOT, 'vector<string>')()
        self.v_sys.push_back('up')
        self.v_sys.push_back('down')

        # make a reader instance and load the sf data
        self.reader = ROOT.BTagCalibrationReader(
            1,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
            "central",      # central systematic type
            self.v_sys,          # vector of other sys. types
        )    
        self.reader.load(
            self.calib, 
            0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
            "comb"      # measurement type
        )        
        self.BtagWeight = 1.0

        ### Flag to distinguish data from MC
        self.itIsData = None
        theFileIs = self.infile
        if theFileIs.find("un2016")== -1 : 
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
        self.ak4Jet = None
        

        ### Define the 4 vectors of the leptonic top system


        self.leptonP4 = ROOT.TLorentzVector()
        self.leptonP4.SetPtEtaPhiM( 
                                   self.tree.LeptonPt[0],
                                   self.tree.LeptonEta[0],
                                   self.tree.LeptonPhi[0], 
                                                       0. )

        self.nuP4 = ROOT.TLorentzVector()
        self.nuP4 = ROOT.TLorentzVector( 
                                        self.tree.SemiLeptMETpt[0],
                                        self.tree.SemiLeptMETpx[0], 
                                        self.tree.SemiLeptMETpy[0], 
                                                                0. )

        
        ### B tag SF (To be applied after b-tag is required at stage 12 in type1 and type2)
        self.ak4Jet = ROOT.TLorentzVector( )        
        self.ak4Jet.SetPtEtaPhiM( self.tree.AK4_dRminLep_Pt[0],
                                  self.tree.AK4_dRminLep_Eta[0],
                                  self.tree.AK4_dRminLep_Phi[0],
                                  self.tree.AK4_dRminLep_Mass[0] )

        ### MC generator weights and PU  weights
        if self.itIsData :
            self.EventWeight = 1.0
            self.PUWeight = 1.0
        else:
            self.EventWeight = self.tree.SemiLeptEventWeight[0]
            self.PUWeight = self.tree.SemiLeptPUweight[0]  
            
        ### Muon trigger efficiency and cut based ID weights  (NOTE: Add these to type 2 and also add Iso SF in that case)
        if self.tree.LeptonIsMu[0] == 1 and not self.itIsData and self.leptonP4 != None  :
            self.TriggEffIs = self.MuonTriggEff( self.leptonP4.Perp() , abs(self.leptonP4.Eta())   , self.tree.SemiLeptRunNum[0] )
            if self.verbose : "Muon trigger eff is {0:2.2f} for pt {1:2.2f} and abs(eta) {2:2.2f}".format(self.TriggEffIs,self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )

            self.CutIDScaleFLooseIs = self.MuonCutIDScaleFLoose( self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )
            if self.verbose : "Muon Cut ID LOOSE  eff is {0:2.2f} for pt {1:2.2f} and abs(eta) {2:2.2f}".format(self.CutIDScaleFLooseIs ,self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )

            self.CutIDScaleFIs = self.MuonCutIDScaleFTight( self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )
            if self.verbose : "Muon Cut ID MEDIUM eff is {0:2.2f} for pt {1:2.2f} and abs(eta) {2:2.2f}".format(self.CutIDScaleFIs,self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )

            self.MuonHIPScaleFIs = self.MuonHIPScaleF( self.leptonP4.Eta() )
            if self.verbose : "Muon HIP SF is {0:2.2f} for eta {1:2.2f}".format(self.MuonHIPScaleFIs, self.leptonP4.Eta()  )

        ### B tag SF (To be applied after b-tag is required)

        if  self.itIsData :        self.BtagWeight = 1.0
        else: 
            self.BtagWeight = self.reader.eval_auto_bounds(
                                                        'central',      # systematic (here also 'up'/'down' possible)
                                                        0,              # jet flavor (0 for b jets)
                                                        self.ak4Jet.Eta() ,            # eta
                                                        self.ak4Jet.Perp()            # pt
                                                    )
        print"BtagWeight is {0:2.2f}".format(self.BtagWeight)                                        

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

    def MuonTriggEff(self, muonpt, muoneta, runNum) : #{ROOT file from
        #https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults
        ### TO-DO: Implement this for type 2 selection
        TriggEff = 1.
        runNumIs = None
        if  muonpt >= 500. and abs(muoneta) > 1.2 :
            TriggEff = 0.0
        else :
            ### Note: This needs to be updated as SFs for new data become available...
            ### To-DO: decide which percentage to weight by each run histo
            binx = self.PtetaTriggEff_Run274094_to_276097.GetXaxis().FindBin( muonpt  )
            biny = self.PtetaTriggEff_Run274094_to_276097.GetYaxis().FindBin( muoneta )
            TriggEff = self.PtetaTriggEff_Run274094_to_276097.GetBinContent(binx, biny )
            if self.verbose : print "get bin: x (using pt) {}, y (using eta) {}, CUt ID Eff is {}".format(binx, biny, TriggEff )

        return float(TriggEff)      
  

    def MuonCutIDScaleFTight(self, muonpt, muoneta) : #{ROOT file from
        #https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults
        ### TO-DO: Implement this for type 2 selection
        if muonpt >= 500. and abs(muoneta) > 1.2 :
            CutIDScaleFt = 0.0
        else :
            binx = self.PtetaCutIDScaleFTight.GetXaxis().FindBin( muonpt  )
            biny = self.PtetaCutIDScaleFTight.GetYaxis().FindBin( muoneta )
            CutIDScaleFt = self.PtetaCutIDScaleFTight.GetBinContent(binx, biny )
            if self.verbose : print "get bin: x (using pt) {}, y (using eta) {}, CUt ID Eff is {}".format(binx, biny, CutIDScaleFt )
        return float(CutIDScaleFt) 
     
    def MuonCutIDScaleFLoose(self, muonpt, muoneta) : #{ROOT file from
        #https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults
        ### TO-DO: Implement this for type 2 selection
        if  muonpt >= 500. and abs(muoneta) > 1.2 :
            CutIDScaleFl = 0.0
        else :
            binx = self.PtetaCutIDScaleFLoose.GetXaxis().FindBin( muonpt  )
            biny = self.PtetaCutIDScaleFLoose.GetYaxis().FindBin( muoneta )
            CutIDScaleFl = self.PtetaCutIDScaleFLoose.GetBinContent(binx, biny )
            if self.verbose : print "get bin: x (using pt) {}, y (using eta) {}, CUt ID Eff is {}".format(binx, biny, CutIDScaleFl )
        return float(CutIDScaleFl)    

    ### SF for High-pT ID and (detector based) Tracker Relative Isolation
    def MuonIsoScaleF(self, muonpt, muoneta) : #{ROOT file from
        #https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults            ### TO-DO: Implement this for type 2 selection
        MuonIsoScaleF = 1.
        if muonpt >= 500. and abs(muoneta) > 1.2 :
            MuonIsoScaleF = 0.0
        else :
            binx = self.fff.GetXaxis().FindBin( muonpt  )
            biny = self.fff.GetYaxis().FindBin( muoneta )
            MuonIsoScaleF = self.fff.GetBinContent(binx, biny )
            if self.verbose : print "get bin: x (using pt) {}, y (using eta) {}, CUt ID Eff is {}".format(binx, biny, MuonIsoScaleF )
        return float(MuonIsoScaleF)    

    ### HIP SF : muon tracking specific SFs covering HIP inefficiencies
    def MuonHIPScaleF(self,  muoneta) : #{ROOT file from
        #https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2#Tracking_efficiency_provided_by       
        ### TO-DO: Implement this for type 2 selection
        theMuonHIPScaleF = 1.

        theMuonHIPScaleF = self.ratio_eta.Eval(muoneta)
        if self.verbose : print "(using eta) {}, HIP SF is {}".format(muoneta,  theMuonHIPScaleF )
        return float(theMuonHIPScaleF)    


    ### TO-DO: Eventually apply Kalman corrections
    '''
    if options.isMC :
        c=ROOT.KalmanMuonCalibrator("MC_80X_13TeV")
    else :
        c=ROOT.KalmanMuonCalibrator("DATA_80X_13TeV")
    def getKalmanMuonCorr(pt, eta, phi, charge) : #{
        # apply muon corrections as described here https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonScaleResolKalman
        if pt > 200. : return pt # shoulld add inner tracker eta cut
        if options.verbose : print 'HIP Correcting Muon Pt = {0:4.3f} GeV'.format(pt)
        if charge < 0. :
            chargeSign = -1 
        if charge > 0. :
            chargeSign = 1    
        CorrMuPt =c.getCorrectedPt(pt, eta, phi, chargeSign)
        if options.verbose : print 'After HIP Correcting Muon Pt = {0:4.3f} GeV'.format(CorrMuPt)
        dpt = abs( pt- CorrMuPt )
        dptopt = dpt/ pt
        CorrMuPtError = c.getCorrectedError(CorrMuPt , eta, dptopt)#'Recall! This correction is only valid after smearing'
        CorrMuPt = c.smear(CorrMuPt , eta)
        
        #print 'propagate the statistical error of the calibration
        #print 'first get number of parameters'
        #N=c.getN()
        #print N,'parameters'
        #for i in range(0,N):
            #c.vary(i,+1)
            #print 'variation',i,'ptUp', c.getCorrectedPt(pt, eta phi, charge)
            #c.vary(i,-1)
            #print 'variation',i,'ptDwn', c.getCorrectedPt(pt, eta phi, charge)
        #c.reset()
        #print 'propagate the closure error 
        #c.varyClosure(+1)
        
        #newpt =  c.getCorrectedPt(pt, eta, phi, chargeSign)
        if options.verbose : print 'After HIP Correcting Muon Pt and vary closure and smear  = {0:4.3f}'.format(CorrMuPt)
        #newpt2 = c.smear(pt , eta)
        #if options.verbose : print 'After HIP Correcting Muon Pt and vary closure and smear  = {0:4.3f}'.format(newpt2)

        return CorrMuPt
    '''

    
