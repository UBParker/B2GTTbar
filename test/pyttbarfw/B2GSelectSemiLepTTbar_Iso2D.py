#! /UsrtheWeight for stage/bin/env python
import ROOT

import TrigMap

class B2GSelectSemiLepTTbar_Iso2D( ) :
    """
    Selects boosted semileptonic ttbar events with non-isolated leptons , as described in CMS AN-15-107
    """
    def __init__(self, options, tree ):
        self.ignoreTrig = options.ignoreTrig
        self.verbose = options.verbose
        self.infile = options.infile

        self.nstages = 10
        if self.verbose: print "Begin leptonic top selection with {} stages".format(self.nstages)
        self.tree = tree
        self.trigMap = TrigMap.TrigMap()
        # Define Kinematic Cut Values

        # Work the cut flow
        # Stage 0 : None.
        # Stage 1 : Trigger and AK8 pt cut for electron channel

        # AK8 pt cut for electron events
        self.ak8ptCut = 140.

        self.trigIndex = [
            self.trigMap.HLT_Mu45_eta2p1_v,
            #elf.trigMap.HLT_Mu30_eta2p1_PFJet150_PFJet50_v,
            #self.trigMap.HLT_Mu30_eta2p1_PFJet150_PFJet50_v,
            #self.trigMap.HLT_Mu40_eta2p1_PFJet200_PFJet50_v,
            self.trigMap.HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v,
            self.trigMap.HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet140_v,
            self.trigMap.HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v
            ]

        # Stage 2 : Lepton kinematic selection

        self.muonPtCut = 53.
        self.muonEtaCut = 2.1

        self.electronPtCut = 53.
        self.electronEtaCut = 2.5

        #self.passMuon_Pt = self.tree.LeptonIsMu[0] == 1 and self.leptonP4.Perp() > self.muonPtCut
        #self.passElectron_Pt = self.tree.LeptonIsMu[0] == 0 and self.leptonP4.Perp() > self.electronPtCut

        #self.passMuon_Eta = self.tree.LeptonIsMu[0] == 1 and abs(self.leptonP4.Eta()) < self.muonEtaCut
        #self.passElectron_Eta = self.tree.LeptonIsMu[0] == 0  and abs(self.leptonP4.Eta()) < self.electronEtaCut

        ### There is a problem with cut based ID currently where nothing is passing Electron_noiso_*


        # Stage 3 : Lepton Cut based ID selection
        # Tight (no iso for electrons).   ### Was Medium for muons in paper however Tight is suggested by semi-lept group for new 2016 data.

        # self.passMuon_Tight = self.tree.LeptonIsMu[0] > 0. and self.tree.MuTight[0] > 0.
        #self.passElectron_Tight_noIso = self.tree.LeptonIsMu[0] < 1.  and self.tree.Electron_noiso_passTight[0] > 0.

        # Stage 4 : Muon High Pt ID selection

        # Stage 5 : MET selection
        self.muonMETPtCut = 50.
        self.electronMETPtCut = 120.


        # Stage 6 : Leptonic-side AK4 jet selection
        self.AK4jetPtCut = 50.
        self.AK4EtaCut = 2.4

        # Stage 7 : 2D cut (decrease QCD contamination)
        self.DrAK4Lep = 0.4
        self.PtRel = 40.


        # Stage 8 : Hemisphere cut (keep leptons far from AK8 Jet)
        #  DR(AK8, Lepton) > 1.

        # Stage 9 : Wlep pt selection
        self.MuonHtLepCut = 200.
        self.ElectronHtLepCut = 200.

        ### Cached class member variables for plotting
        self.RunNumber = None
        self.theWeight = None
        self.leptonP4 = None
        self.nuP4 = None
        self.ak4Jet = None
        self.ak8Jet = None
        self.ak8SDJetP4 = None

        if self.verbose: print "self.trigIndex[0] {}".format(self.trigIndex[0])
        #self.printAK4Warning = True

        self.passed = [False] * self.nstages
        self.passedCount = [0] * self.nstages

        ### Create empty weights used for histo filling
        self.theWeight = 1.
        self.EventWeight = 1.
        self.PUWeight = 1.
        self.TriggEffIs  = 1.
        self.CutIDScaleFTightIs = 1.
        self.CutIDScaleFLooseIs =1.
        self.CutIDScaleFMediumIs = 1.
        #self.MuonHIPScaleFIs =1.
        self.recoSFIs = 1.
        self.HEEPSFIs = 1.


        ### Muon Scale factors and efficiencies
        ### See https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults#Results_on_the_full_2016_data


        ### Muon trigger efficiency corrections
        self.printtriggerWarning = True
        self.TriggEffIs = 1.0

        self.finCor1 = ROOT.TFile.Open( "./muon_trg_summer16.root","READ")

        ### SFs to apply to data and/or MC after requiring event passes mu50 or trkmu50

        if self.printtriggerWarning :
            print '----------------------------------- WARNING --------------------------------------'
            print  ' The MC samples used here are old, must update to Moriond2017 samples to be accurate.'
            print  ' Trigger SFs and efficiencies are not accurate for this data/MC as it was processed requiring trigger:'
            print  ' Muons: HLT_Mu50 .'
            print  ' Electrons: Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50 OR Ele50_CaloIdVT_GsfTrkIdT_PFJet140 OR Ele50_CaloIdVT_GsfTrkIdT_PFJet165'
            print  ' Update of triggers will occur after V5 ttrees have been produced'
            print '-----------------------------------------------------------------------------------'

        ### Not applying trigger SFs for the data

        ### SFs for the ttbar mc since the trigger was applied to it
        self.PtetaTriggSFmc_Period1      = self.finCor1.Get("h_eff_trg_mu50tkmu50_sf_1")
        self.PtetaTriggSFmc_Period2      = self.finCor1.Get("h_eff_trg_mu50tkmu50_sf_2")
        self.PtetaTriggSFmc_Period3      = self.finCor1.Get("h_eff_trg_mu50tkmu50_sf_3")
        self.PtetaTriggSFmc_Period4      = self.finCor1.Get("h_eff_trg_mu50tkmu50_sf_4")

        ### efficiencies for the rest of the MC since the trigger was not applied  (Also need SFs)
        self.PtetaTriggEffmc_Period1      = self.finCor1.Get("h_eff_trg_mu50tkmu50_mc_1")
        self.PtetaTriggEffmc_Period2      = self.finCor1.Get("h_eff_trg_mu50tkmu50_mc_2")
        self.PtetaTriggEffmc_Period3      = self.finCor1.Get("h_eff_trg_mu50tkmu50_mc_3")
        self.PtetaTriggEffmc_Period4      = self.finCor1.Get("h_eff_trg_mu50tkmu50_mc_4")

        ### HighPt Muon


        ### This is the official recommandation plus temp SFs for muons pt > 120 GeV (See Hengne's email for further information)
        self.finCor2 = ROOT.TFile.Open( "./muon_idiso_summer16.root","READ")

        self.HighPteffIs = 1.0

        ### Muon cut based ID corrections

        self.CutIDScaleFTightIs = 1.0
        self.CutIDScaleFLooseIs = 1.0
        self.finCor3 = ROOT.TFile.Open( "./EfficienciesAndSF_BCDEF.root","READ")
        self.finCor4 = ROOT.TFile.Open( "./EfficienciesAndSF_GH.root","READ")

        self.PtetaCutIDMuScaleFTightBtoF      = self.finCor3.Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio")
        self.PtetaCutIDMuScaleFTightGH      = self.finCor4.Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio")

        self.PtetaCutIDMuScaleFLooseBtoF      = self.finCor3.Get("MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio")
        self.PtetaCutIDMuScaleFLooseGH      = self.finCor4.Get("MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio")

        ### Only valid for pt < 120 Gev
        self.PtetaCutIDMuScaleFHighPtBtoF      = self.finCor3.Get("MC_NUM_HighPtID_DEN_genTracks_PAR_newpt_eta/abseta_pair_ne_ratio")
        self.PtetaCutIDMuScaleFHighPtGH      = self.finCor4.Get("MC_NUM_HighPtID_DEN_genTracks_PAR_newpt_eta/abseta_pair_ne_ratio")

        ### These should be the same as those above but with coverage for pt >120 Gev
        self.PtetaCutIDMuScaleFdataHighPtBtoF = self.finCor2.Get("h_mu_hpt_data_1")
        self.PtetaCutIDMuScaleFdataHighPtGH = self.finCor2.Get("h_mu_hpt_data_2")
        self.PtetaCutIDMuScaleFmcHighPtBtoF = self.finCor2.Get("h_mu_hpt_mc_1")
        self.PtetaCutIDMuScaleFmcHighPtGH = self.finCor2.Get("h_mu_hpt_mc_2")

        '''
        ### Muon HIP SF   I THINK THIS IS NOT NEEDED AFTER REReco CHECK THIS

        self.MuonHIPScaleFIs = 1.0
        self.finCor3 = ROOT.TFile.Open( "./ratios.root","READ")
        self.ratio_eta   =   self.finCor3.Get("ratio_eta")
        '''

        ### Electron reconstruction SF
        ###  Info here https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaIDRecipesRun2#Electron_efficiencies_and_scale
        self.recoSFIs = 1.
        self.finCor5 = ROOT.TFile.Open( "./egammaEff_reconstructionSF.root","READ")

        #effdatareco = self.finCor5.Get("Gamma_EffData2D")
        #effmcreco =   self.finCor5.Get("EGamma_EffMC2D")

        hSFreco =      self.finCor5.Get("EGamma_SF2D")

        ### Electron cut based ID corrections

        self.CutIDScaleFMediumIs = 1.0
        self.CutIDScaleFLooseIs = 1.0
        self.finCor6 = ROOT.TFile.Open( "./egammaEffi_MedCutBasedID.root","READ")
        self.finCor7 = ROOT.TFile.Open( "./egammaEffi_LooseCutBasedID.root","READ")

        self.PtetaCutIDElScaleFMedium     = self.finCor6.Get("EGamma_SF2D")
        self.PtetaCutIDEldataEffMedium     = self.finCor6.Get("EGamma_EffData2D")
        self.PtetaCutIDElmcEffMedium     = self.finCor6.Get("EGamma_EffMC2D")

        self.PtetaCutIDElScaleFLoose      = self.finCor7.Get("EGamma_SF2D")
        self.PtetaCutIDEldataEffLoose     = self.finCor7.Get("EGamma_EffData2D")
        self.PtetaCutIDElmcEffLoose     = self.finCor7.Get("EGamma_EffMC2D")

        ### B tag weights
        ### Adapted from example https://twiki.cern.ch/twiki/bin/view/CMS/BTagCalibration#Code_example_in_Python
        ### Applied work around 2. listed here  https://twiki.cern.ch/twiki/bin/view/CMS/BTagCalibration#Additional_scripts

        # from within CMSSW:
        ROOT.gSystem.Load('libCondFormatsBTauObjects')
        ROOT.gSystem.Load('libCondToolsBTau')

        # OR using standalone code:
        #ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cpp+')

        # get the sf data loaded
        self.calib = ROOT.BTagCalibration('CSVv2_Moriond17_B_H','CSVv2_Moriond17_B_H.csv')#('csvv2_ichep', 'CSVv2_ichep.csv')

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

        ### Flags to distinguish different input files
        self.itIsData = None
        self.itIsTTbar = None

        theFileIs = self.infile
        if theFileIs.find("un2016")== -1 :
            self.itIsData = False
            if self.verbose :
                print "MC : Event and PU weights != 1"

        else :
            self.itIsData = True
            if self.verbose : print "DATA : weights = 1"

        if (theFileIs.find("ttbar")== -1 and theFileIs.find("un2016")== -1 ):
            if self.verbose :print "other MC : Event triggers were NOT applied so trigger efficiency will be !"

        else :
            self.itIsTTbar = True
            if self.verbose : print "ttbar MC : Event triggers were applied so trigger efficiency will NOT be !"

    """
        This is the "select" function that does the work for the event selection. If you have any complicated
        stuff to do, do it here and create a class member variable to cache the results.
    """
    def select( self ) :
        self.RunNumber = None
        self.theWeight = None

        self.leptonP4 = None
        self.nuP4 = None
        self.ak4Jet = None
        self.ak8SDJetP4 = None

        ### Get Run Number of data event
        self.RunNumber =  self.tree.SemiLeptRunNum[0]
        #if self.verbose : print"run number in Iso2D is self.runNum {} from tree value is  {}".format(self.RunNumber, self.tree.SemiLeptRunNum[0])

        ### Define the 4 vectors of the leptonic top system

        self.leptonP4 = ROOT.TLorentzVector()
        self.leptonP4.SetPtEtaPhiM(
                                   self.tree.LeptonPt[0],
                                   self.tree.LeptonEta[0],
                                   self.tree.LeptonPhi[0],
                                                       0. )
        #if self.verbose : print"lepton pt from iso2D is {0:2.2f}".format(self.tree.LeptonPt[0])

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

        ### AK8 Soft Drop Jets    
        self.ak8SDJetP4 = ROOT.TLorentzVector()
        self.ak8SDJetP4.SetPtEtaPhiM( self.tree.JetSDptRaw[0],
                                     self.tree.JetSDetaRaw[0],
                                     self.tree.JetSDphiRaw[0],
                                    self.tree.JetSDmassRaw[0] ) 


        self.EventWeight = 1.
        self.PUWeight = 1.
        self.TriggEffIs = 1.
        self.CutIDScaleFLooseIs = 1.
        self.CutIDScaleFIs = 1.
        self.MuonHIPScaleFIs = 1.
        self.BtagWeight = 1.
        self.ElHEEPeffIs = 1.
        self.recoSFIs = 1.
        self.HEEPSFIs = 1.

        if  self.itIsData :        self.BtagWeight = 1.0
        else: self.BtagWeight = self.reader.eval_auto_bounds(
                                                        'central',      # systematic (here also 'up'/'down' possible)
                                                        0,              # jet flavor (0 for b jets)
                                                        self.ak4Jet.Eta() ,            # eta
                                                        self.ak4Jet.Perp()            # pt
                                                    )


        '''
        if self.printAK4Warning :
            print '----------------------------------- WARNING --------------------------------------'
            print  ' error resolved'
        '''
        self.passed = [False] * self.nstages
        self.passedCount = [0] * self.nstages
                                                                                                               
        ### MC generator weights and PU  weights
        if self.itIsData :
            self.EventWeight = 1.0
            self.PUWeight = 1.0
        else:
            self.EventWeight = self.tree.SemiLeptEventWeight[0]
            self.PUWeight = self.tree.SemiLeptPUweight[0]

        self.CutIDScaleFLooseIs =  1.0

        if self.leptonP4 != None  and not self.itIsData: # self.RunNumber
            if self.tree.LeptonIsMu[0] == 1:
                self.CutIDScaleFLooseIs = self.MuonCutIDScaleFLoose( self.leptonP4.Perp() , (self.leptonP4.Eta()) , self.tree.SemiLeptRunNum[0] )
                if self.verbose : "MuonCutIDScaleFLoose: {0:2.4f} for pt {1:2.2f} and abs(eta) {2:2.2f}".format(self.CutIDScaleFLooseIs ,self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )
            elif self.tree.LeptonIsMu[0] == 0  :
                #print"WARNING: ElectronCutIDScaleFLoose not yet applied"
                self.CutIDScaleFLooseIs = self.ElectronCutIDScaleFLoose( self.leptonP4.Perp() , (self.leptonP4.Eta()) , self.tree.SemiLeptRunNum[0] )
                if self.verbose : "ElectronCutIDScaleFLoose: {0:2.4f} for pt {1:2.2f} and abs(eta) {2:2.2f}".format(self.CutIDScaleFLooseIs ,self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )
                self.recoSFIs = self.ElectronRecoSF( self.leptonP4.Eta(), self.leptonP4.Perp( ))

        self.theWeight =  self.EventWeight * self.PUWeight * self.CutIDScaleFLooseIs * self.recoSFIs 
        if self.verbose : print "theWeight for stage {0:} is : {1:2.4f} = eventWeight {2:2.2f} * self.PUWeight{3:2.2f} * self.CutIDScaleFLooseIs {4:2.2f} * self.recoSFIs  {5:2.2f}".format( 0, self.theWeight,  self.EventWeight , self.PUWeight , self.CutIDScaleFLooseIs, self.recoSFIs  )

        self.passed[0] = True
        self.passedCount[0] += 1
        if self.verbose: print"Stage 0: Preliminary cuts from B2GTreeMaker V4"

        if self.tree.LeptonIsMu[0] == 1 and self.leptonP4 != None  : # self.RunNumber
            self.TriggEffIs = 1.
            if not self.itIsData :
                self.TriggEffIs = self.MuonTriggEff( self.leptonP4.Perp() , abs(self.leptonP4.Eta())   , self.tree.SemiLeptRunNum[0] )

        if self.tree.LeptonIsMu[0] == 0 and not self.itIsData and self.leptonP4 != None  :
            print"WARNING: Electron trigger SF and eff not yet applied" 
              
        ### Trigger efficiency for morind MC + ReReco data Mu50 PR TRKMu50                                               
        ### we are using Mu50, switching with v5 ttrees                                                                  
                                                                                                                     
        self.theWeight =  self.EventWeight * self.PUWeight * self.CutIDScaleFLooseIs *  self.TriggEffIs * self.recoSFIs 
        if self.verbose : print "theWeight for stage {0:} is : {1:2.2f} = eventWeight {2:2.2f} * self.PUWeight{3:2.2f} * self.CutIDScaleFLooseIs {4:2.2f} *nTriggEffIs {5:2.2f} * self.recoSFIs  {6:2.2f}".format( 0, self.theWeight,  self.EventWeight , self.PUWeight , self.CutIDScaleFLooseIs * self.CutIDScaleFLooseIs, self.TriggEffIs, self.recoSFIs )

        self.trigIs = ""
        if not self.ignoreTrig :
            self.trigIs = ""
            for itrig in self.trigIndex :
                if bool ( self.tree.SemiLeptTrigPass[itrig] ) == True :
                    if self.verbose: print"trigIs {}".format( self.trigMap.names[itrig] )
                    self.trigIs = self.trigMap.names[itrig]
                    #self.passed[1] = True
                    if self.tree.LeptonIsMu[0] == 0 :
                        if  self.ak8SDJetP4.Perp() > self.ak8ptCut:
                            if self.verbose: print"Stage 1: Electron associated AK8 passed trigger threshold pt cut {0:3.3f} > {1:3.3f} GeV".format(self.ak8SDJetP4.Perp() , self.ak8ptCut)
                            self.passed[1] = True
                    else:
                       self.passed[1] = True
            if not self.passed[1] : return self.passed
        else :
            if self.tree.LeptonIsMu[0] == 0 :
                if  self.ak8SDJetP4.Perp() > self.ak8ptCut:
                    if self.verbose: print"Stage 1: Electron associated AK8 passed trigger threshold pt cut {0:3.3f} > {1:3.3f} GeV".format(self.ak8SDJetP4.Perp() , self.ak8ptCut)

                    self.passed[1] = True
            else:
                self.passed[1] = True
        self.passedCount[1] += 1
        if self.verbose: print"Stage 1: Passed trigger {}".format(self.trigIs)


        self.passMuon_Pt = self.tree.LeptonIsMu[0] == 1 and self.leptonP4.Perp() > self.muonPtCut
        self.passElectron_Pt = self.tree.LeptonIsMu[0] == 0 and self.leptonP4.Perp() > self.electronPtCut

        self.passMuon_Eta = self.tree.LeptonIsMu[0] == 1 and abs(self.leptonP4.Eta()) < self.muonEtaCut
        self.passElectron_Eta = self.tree.LeptonIsMu[0] == 0  and abs(self.leptonP4.Eta()) < self.electronEtaCut

        if self.tree.LeptonIsMu[0] > 0. : ### Muon
            if not ( self.leptonP4.Perp() > self.muonPtCut and   abs(self.leptonP4.Eta()) < self.muonEtaCut ) : return self.passed
        if self.tree.LeptonIsMu[0] < 1. : ### Electron
            if not ( self.leptonP4.Perp() > self.electronPtCut and   abs(self.leptonP4.Eta()) < self.electronEtaCut ) : return self.passed
        self.passed[2] = True
        self.passedCount[2] += 1
        if self.verbose :
            if self.passMuon_Eta :print "Stage 2a: Exactly 1 muon candidate  eta {0:2.2f} < ( {1:2.2f} )".format(
                                                                        self.leptonP4.Eta(),
                                                                        self.muonEtaCut)
            else :print "Stage 2a: Exactly 1 electron candidate  eta {0:2.2f} < ( {1:2.2f} )".format(
                                                                        self.leptonP4.Eta(),
                                                                        self.electronEtaCut)

        if self.verbose : print "Stage 2b: lepton candidate pt {0:2.2f} GeV > ({1:2.2f} GeV)".format(
                                                                        self.leptonP4.Perp(),
                                                                        self.muonPtCut)


        self.passMuon_Tight = self.tree.LeptonIsMu[0] > 0. and self.tree.MuTight[0] > 0.
        self.passElectron_Tight_noIso = self.tree.LeptonIsMu[0] < 1.  and self.tree.Electron_noiso_passTight[0] > 0.

        if self.tree.LeptonIsMu[0] == 1 and self.leptonP4 != None  : # self.RunNumber

                self.CutIDScaleFIs = self.MuonCutIDScaleFTight( self.leptonP4.Perp() , abs(self.leptonP4.Eta()) , self.tree.SemiLeptRunNum[0] )
                if self.verbose : "MuonCutIDScaleFTight: {0:2.2f} for pt {1:2.2f} and abs(eta) {2:2.2f}".format(self.CutIDScaleFIs,self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )

        if self.tree.LeptonIsMu[0] == 0 and not self.itIsData and self.leptonP4 != None  :
            print"WARNING: ElectronCutIDScaleFTight not yet available yet"



        if self.leptonP4 != None  and not self.itIsData: # self.RunNumber                                                                                                                                        
            if self.tree.LeptonIsMu[0] == 1:
                self.CutIDScaleFLooseIs = self.MuonCutIDScaleFLoose( self.leptonP4.Perp() , (self.leptonP4.Eta()) , self.tree.SemiLeptRunNum[0] )
                if self.verbose : "MuonCutIDScaleFLoose: {0:2.4f} for pt {1:2.2f} and abs(eta) {2:2.2f}".format(self.CutIDScaleFLooseIs ,self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )
            elif self.tree.LeptonIsMu[0] == 0  :
                #print"WARNING: ElectronCutIDScaleFLoose not yet applied"                                                                                                                                        
                self.CutIDScaleFLooseIs = self.ElectronCutIDScaleFLoose( self.leptonP4.Perp() , (self.leptonP4.Eta()) , self.tree.SemiLeptRunNum[0] )
                if self.verbose : "ElectronCutIDScaleFLoose: {0:2.4f} for pt {1:2.2f} and abs(eta) {2:2.2f}".format(self.CutIDScaleFLooseIs ,self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )
                self.recoSFIs = self.ElectronRecoSF( self.leptonP4.Eta(), self.leptonP4.Perp( ))

        self.theWeight =  self.EventWeight * self.PUWeight * self.CutIDScaleFLooseIs * self.recoSFIs
        if self.verbose : print "theWeight for stage {0:} is : {1:2.4f} = eventWeight {2:2.2f} * self.PUWeight{3:2.2f} * self.CutIDScaleFLooseIs {4:2.2f} * self.recoSFIs  {5:2.2f}".format( 0, self.theWeight, self.EventWeight , self.PUWeight , self.CutIDScaleFLooseIs, self.recoSFIs  )


        if self.verbose  : print "Stage 3 CHECK: ELECTRON  passnoiso loose {} med {} tight {}- MUON is High Pt {} is tight {}".format(
                                 self.tree.Electron_noiso_passLoose[0] ,
                                 self.tree.Electron_noiso_passMedium[0],
                                 self.tree.Electron_noiso_passTight[0],
                                 self.tree.MuHighPt[0],
                                 self.tree.MuTight[0]  )


        if self.tree.LeptonIsMu[0] > 0. : ### Muon
            if not self.tree.MuTight[0] > 0.  : return self.passed
        if self.tree.LeptonIsMu[0] < 1. : ### Electron
            if not self.tree.Electron_noiso_passMedium[0] > 0.  : return self.passed
        self.passed[3] = True
        self.passedCount[3] += 1
        if self.verbose  : print "Stage 3: Muon (Electron) passed Tight (Medium) Cut based ID (with no iso) passnoiso loose {} med {} tight {}".format(self.tree.Electron_noiso_passLoose[0] , self.tree.Electron_noiso_passMedium[0], self.tree.Electron_noiso_passTight[0] )


        if self.tree.LeptonIsMu[0] == 1 and self.leptonP4 != None and  not self.itIsData  :
            self.MuHighPtScaleFIs = self.MuonHighPtScaleF( self.leptonP4.Perp() , abs(self.leptonP4.Eta()) ,  self.RunNumber )
            if self.verbose : "MuonHighPtScaleF: {0:2.2f} for pt {1:2.2f} and abs(eta) {2:2.2f}".format(self.CutIDScaleFIs,self.leptonP4.Perp() , abs(self.leptonP4.Eta())  )

        if self.tree.LeptonIsMu[0] == 0 and not self.itIsData and self.leptonP4 != None  :
            self.HEEPSFIs = self.ElectronHEEPEff(self.leptonP4.Perp() , self.leptonP4.Eta() )
            print"ElectronHEEPEff: {0:2.3f} for eta {1:2.3f}".format(self.HEEPSFIs,  self.leptonP4.Eta() )

        ### NOTE : High Pt Muon ID is now required as suggested here https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#2016_Data
        if not (( self.tree.LeptonIsMu[0] == 1 and self.tree.MuHighPt[0] == 1 and self.tree.SemiLeptPassMETFilters[0] == 1) or  (self.tree.LeptonIsMu[0] == 0 and  self.tree.SemiLeptPassMETFilters[0] == 1 )) :
            return self.passed
        self.passed[4] = True
        self.passedCount[4] += 1
        if self.verbose  : print "Stage 4: Muon is HighPt and lepton pass self.tree.SemiLeptPassMETFilters[0] == {} ".format(self.tree.SemiLeptPassMETFilters[0] )


        if self.verbose: print"Stage 5 CHECK: Lepton is a Muon bool {0:}, MET is {1:2.2f} GeV".format(self.tree.LeptonIsMu[0] , self.nuP4.Perp() )

        if self.tree.LeptonIsMu[0] > 0. :
            if not self.nuP4.Perp() > self.muonMETPtCut  : return self.passed
        if self.tree.LeptonIsMu[0] < 1. :
            if not self.nuP4.Perp() > self.electronMETPtCut  : return self.passed
        self.passed[5] = True
        self.passedCount[5] += 1
        if self.verbose :
            if self.tree.LeptonIsMu[0] == 1 :


                print "Stage 5: Muon  MET pt {0:2.2f} GeV > ( {1:2.2f} GeV ) ".format(
                                                                        self.nuP4.Perp(),
                                                                        self.muonMETPtCut )
            else:
                print "Stage 5: Electron MET pt {0:2.2f} GeV > ( {1:2.2f} GeV ) ".format(
                                                                        self.nuP4.Perp(),
                                                                        self.electronMETPtCut )

        if not ( self.ak4Jet.Perp() > self.AK4jetPtCut and abs(self.ak4Jet.Eta()) < self.AK4EtaCut  ) : return self.passed
        self.passed[6] = True
        self.passedCount[6] += 1
        if self.verbose : print "Stage 6: AK4 jet pt {0:2.2f} GeV > ( {1:2.2f} GeV ) and eta {2:2.2f} < ( {3:2.2f} )".format(
                                                                                             self.ak4Jet.Perp(),
                                                                                             self.AK4jetPtCut,
                                                                                             self.ak4Jet.Eta(),
                                                                                             self.AK4EtaCut)

        # NOTE: This jet cut was found to be strongly suboptimal by the semileptonic team. They had better performance at pt > 15 GeV, with
        # delta R < 0.4 and ptrel > 20. For now, we will raise the HTLep cut and ptrel cut but we need to fix this.
        if not  (self.tree.AK4_dRminLep_dRlep[0] > self.DrAK4Lep or self.tree.PtRel[0] > self.PtRel ) : return self.passed
        self.passed[7] = True
        self.passedCount[7] += 1
        if self.verbose : print "Stage 7: DR(AK4, lep) {0:2.2f}  > ( {1:2.2f} ) or PtRel(AK4, lep) {2:2.2f} > ( {3:2.2f} )".format(
                                                                                                      self.tree.AK4_dRminLep_dRlep[0],
                                                                                                                        self.DrAK4Lep,
                                                                                                                   self.tree.PtRel[0],
                                                                                                                           self.PtRel)
        if not ( self.tree.DeltaRJetLep[0] > 1. ) : return self.passed # Hemisphere cut btw lepton and the ak8
        self.passed[8] = True
        self.passedCount[8] += 1
        if self.verbose : print "Stage 8: DR(AK8, lep) {0:2.2f}  > ( 1.0 )".format( self.tree.DeltaRJetLep[0] )

        if self.tree.LeptonIsMu[0] > 0. :
            if not (self.leptonP4 + self.nuP4 ).Perp() > self.MuonHtLepCut  : return self.passed
        if self.tree.LeptonIsMu[0] < 1. :
            if not (self.leptonP4 + self.nuP4 ).Perp() > self.ElectronHtLepCut  : return self.passed
        self.passed[9] = True
        self.passedCount[9] += 1
        if self.verbose : print "Stage 9: Leptonic W Pt  (Lepton Pt + MET Pt ) {0:2.2f} > ( {1:2.2f} GeV )".format( (self.leptonP4 + self.nuP4).Perp(), self.MuonHtLepCut )

        return self.passed

    def MuonTriggEff(self, muonpt, muoneta, runNum) : #{ROOT file from
        #https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults
        TriggEff = 1.
        TriggSF = 1.

        runNumIs = None
        binx = None
        biny = None
        binxsf = None
        binysf = None


        if self.itIsData :
            return float(TriggSF)
        if 0. < runNum <= 274094. : ### Run Period 1
            binxsf = self.PtetaTriggSFmc_Period1.GetXaxis().FindBin( muoneta )
            binysf = self.PtetaTriggSFmc_Period1.GetYaxis().FindBin( muonpt )
            TriggSF = self.PtetaTriggSFmc_Period1.GetBinContent(binxsf, binysf )

            binx = self.PtetaTriggEffmc_Period1.GetXaxis().FindBin( muoneta  )
            biny = self.PtetaTriggEffmc_Period1.GetYaxis().FindBin( muonpt )
            TriggEff = self.PtetaTriggEffmc_Period1.GetBinContent(binx, biny )
        if 274094. < runNum < 278167. : ### Run Period 2
            binxsf = self.PtetaTriggSFmc_Period2.GetXaxis().FindBin( muoneta )
            binysf = self.PtetaTriggSFmc_Period2.GetYaxis().FindBin( muonpt )
            TriggSF = self.PtetaTriggSFmc_Period2.GetBinContent(binxsf , binysf )

            binx = self.PtetaTriggEffmc_Period2.GetXaxis().FindBin( muoneta  )
            biny = self.PtetaTriggEffmc_Period2.GetYaxis().FindBin( muonpt )
            TriggEff = self.PtetaTriggEffmc_Period2.GetBinContent(binx, biny )
        if  278167. <= runNum < 278820.: ### Run Period 3
            binxsf = self.PtetaTriggSFmc_Period3.GetXaxis().FindBin( muoneta )
            binysf = self.PtetaTriggSFmc_Period3.GetYaxis().FindBin( muonpt )
            TriggSF = self.PtetaTriggSFmc_Period3.GetBinContent(binxsf, binysf )

            binx = self.PtetaTriggEffmc_Period3.GetXaxis().FindBin( muoneta  )
            biny = self.PtetaTriggEffmc_Period3.GetYaxis().FindBin( muonpt )
            TriggEff = self.PtetaTriggEffmc_Period3.GetBinContent(binx, biny )
        if  278820.<= runNum : ### Run Period 4
            binxsf = self.PtetaTriggSFmc_Period4.GetXaxis().FindBin( muoneta )
            binysf = self.PtetaTriggSFmc_Period4.GetYaxis().FindBin( muonpt )
            TriggSF = self.PtetaTriggSFmc_Period4.GetBinContent(binxsf, binysf )

            binx = self.PtetaTriggEffmc_Period4.GetXaxis().FindBin( muoneta  )
            biny = self.PtetaTriggEffmc_Period4.GetYaxis().FindBin( muonpt )
            TriggEff = self.PtetaTriggEffmc_Period4.GetBinContent(binx, biny )

        if TriggSF > 3. :
            TriggSF =float( TriggSF/100.)
            if TriggEff > 3.:
                    TriggEff =float( TriggEff/100.)
        if self.itIsTTbar :
            TriggEff = TriggSF
            if self.verbose : print "MuonTriggEff ttbar : Muon trigger SF is {0:2.2f} : using pt {1:2.2f},  eta {2:2.2f}".format( TriggEff, muonpt, muoneta)
        else:
            TriggEff =  TriggEff * TriggSF
            if self.verbose : print "MuonTriggEff other MC : Muon trigger Eff*SF is {0:2.2f} : pt {1:2.2f}, and eta {2:2.2f}".format( TriggEff, muonpt, muoneta)
        return float(TriggEff)


    def MuonCutIDScaleFTight(self, muonpt, muoneta, runNum) :
        if muonpt > 120.:
            print "MuonCutIDScaleFTight is for pt 0-120 GeV, this pt is {0:2.2f}".format(muonpt)
            return 1.
        if runNum < 278808. : #run2106B-F
            PtetaCutIDMuScaleFTight = self.PtetaCutIDMuScaleFTightBtoF
        else : #run2106GH
            PtetaCutIDMuScaleFTight =    self.PtetaCutIDMuScaleFTightGH

        binx = PtetaCutIDMuScaleFTight.GetXaxis().FindBin( muoneta )
        biny = PtetaCutIDMuScaleFTight.GetYaxis().FindBin( muonpt )
        CutIDScaleFl = PtetaCutIDMuScaleFTight.GetBinContent(binx, biny )
        if self.verbose : print "MuonCutIDScaleFTight: eta {0:2.2f}, pt {1:2.2f}, SF is {2:2.2f}".format( muoneta , muonpt, CutIDScaleFl )

        #if self.verbose : print "MuonCutIDScaleFTight: get bin: x (using eta) {}, y (using pt) {}, SF is {}".format(binx, biny, CutIDScaleFl )
        return float(CutIDScaleFl)
    '''
    def MuonCutIDScaleFLoose(self, muonpt, muoneta, runNum) :
        if runNum < 278808. : #run2106B-F
            PtetaCutIDMuScaleFLoose = self.PtetaCutIDMuScaleFLooseBtoF
        else : #run2106GH
            PtetaCutIDMuScaleFLoose =    self.PtetaCutIDMuScaleFLooseGH

        binx = PtetaCutIDMuScaleFLoose.GetXaxis().FindBin( muoneta  )
        biny = PtetaCutIDMuScaleFLoose.GetYaxis().FindBin( muonpt )
        CutIDScaleFl = PtetaCutIDScaleFLoose.GetBinContent(binx, biny )
        if self.verbose : print "MuonCutIDScaleFLoose: get bin: x (using eta) {}, y (using pt) {}, SF is {}".format(binx, biny, CutIDScaleFl )
        return float(CutIDScaleFl)
    #PtetaCutIDMuScaleFLoose = 1.0
    '''
    def MuonCutIDScaleFLoose(self, muonpt, muoneta, runNum) :
        PtetaCutIDMuScaleFLoose = None
        if muonpt > 120.:
            print "MuonCutIDScaleFLoose is for pt 0-120 GeV, this pt is {}".format(muonpt) 
            return 1. 
        if runNum < 278808. : #run2106B-F
            PtetaCutIDMuScaleFLoose = self.PtetaCutIDMuScaleFLooseBtoF
        else : #run2106GH
            PtetaCutIDMuScaleFLoose =    self.PtetaCutIDMuScaleFLooseGH

        binx = PtetaCutIDMuScaleFLoose.GetXaxis().FindBin( muoneta  )
        biny = PtetaCutIDMuScaleFLoose.GetYaxis().FindBin( muonpt )
        CutIDScaleFl = PtetaCutIDMuScaleFLoose.GetBinContent(binx, biny )
        if self.verbose : print "MuonCutIDScaleFLoose: eta {0:2.2f}, pt {1:2.2f}, SF is {2:2.2f}".format( muoneta , muonpt, CutIDScaleFl )
        #print "MuonCutIDScaleFLoose hist is {0:} for pt {1:2.2f} bin {2:} and eta {3:2.2f} bin {4:} the SF is {5:2.2f} ".format( PtetaCutIDMuScaleFLoose, muonpt, binx, muoneta, biny, CutIDScaleFl)
        return CutIDScaleFl     

    def MuonHighPtScaleF(self, muonpt, muoneta, runNum) :
        highSF = 1.0
        if runNum < 278808. : #run2106B-F                                     
            if self.itIsData:
                HighPt = self.PtetaCutIDMuScaleFdataHightPtBtoF
            else:
                HighPt = self.PtetaCutIDMuScaleFmcHighPtBtoF

        else :
            if self.itIsData:
                HighPt = self.PtetaCutIDMuScaleFdataHighPtGH
            else:
                HighPt = self.PtetaCutIDMuScaleFmcHighPtGH

        binx = HighPt.GetXaxis().FindBin( muoneta  )
        biny = HighPt.GetYaxis().FindBin( muonpt )
        CutIDScaleFl = HighPt.GetBinContent(binx, biny )
        if self.verbose : print "MuonHighPtScaleF: eta {0:2.2f}, pt {1:2.2f}, SF is {2:2.2f}".format( muoneta , muonpt, CutIDScaleFl )
        return float(CutIDScaleFl)


    def ElectronCutIDScaleFLoose(self, elpt, eleta, runNum) :
        PtetaCutIDElScaleFLoose = self.PtetaCutIDElScaleFLoose
        binx = PtetaCutIDElScaleFLoose.GetXaxis().FindBin( eleta  )
        biny = PtetaCutIDElScaleFLoose.GetYaxis().FindBin( elpt )
        CutIDScaleFl = PtetaCutIDElScaleFLoose.GetBinContent(binx, biny )
        if self.verbose : print "ElectronCutIDScaleFLoose: eta {0:2.2f}, pt {1:2.2f}, SF is {2:2.2f}".format( eleta , elpt, CutIDScaleFl )

        #print "ElectronCutIDScaleFLoose hist is {0:} for pt {1:2.2f} bin {2:} and eta {3:2.2f} bin {4:} the SF is {5:2.2f} ".format( PtetaCutIDElScaleFLoose, muonpt, binx, muoneta, biny, CutIDScaleFl)
        return CutIDScaleFl
    '''
       self.PtetaCutIDElScaleFMedium     = self.finCor6.Get("EGamma_SF2D")
        self.PtetaCutIDEldataEffMedium     = self.finCor6.Get("EGamma_EffData2D")
        self.PtetaCutIDElmcEffMedium     = self.finCor6.Get("EGamma_EffMC2D")

        self.PtetaCutIDElScaleFLoose      = self.finCor7.Get("EGamma_SF2D")
        self.PtetaCutIDEldataEffLoose     = self.finCor7.Get("EGamma_EffData2D")
        self.PtetaCutIDElmcEffLoose     = self.finCor7.Get("EGamma_EffMC2D")



        self.PtetaCutIDMuScaleFdataHighPtBtoF = self.finCor2.Get("h_mu_hpt_data\
_1")
        self.PtetaCutIDMuScaleFdataHighPtGH = self.finCor2.Get("h_mu_hpt_data_2\
")
        self.PtetaCutIDMuScaleFmcHighPtBtoF = self.finCor2.Get("h_mu_hpt_mc_1")
        self.PtetaCutIDMuScaleFmcHighPtGH = self.finCor2.Get("h_mu_hpt_mc_2")



    ### SF for High-pT ID and (detector based) Tracker Relative Isolation
    def MuonIsoScaleF(self, muonpt, muoneta) : #{ROOT file from
        #https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults            ### TO-DO: Implement this for type 2 selection
        MuonIsoScaleF = 1.
        binx = self.fff.GetXaxis().FindBin( muonpt  )
        biny = self.fff.GetYaxis().FindBin( muoneta )
        MuonIsoScaleF = self.fff.GetBinContent(binx, biny )
        if self.verbose : print "get bin: x (using pt) {}, y (using eta) {}, CUt ID Eff is {}".format(binx, biny, MuonIsoScaleF )
        return float(MuonIsoScaleF)

    ### Not needed after Re-Reco CHECK THIS, either way fixed in 2016GH

    ### HIP SF : muon tracking specific SFs covering HIP inefficiencies
    def MuonHIPScaleF(self,  muoneta) : #{ROOT file from
        #https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2#Tracking_efficiency_provided_by
        ### TO-DO: Implement this for type 2 selection
        MuonHIPScaleF = 1.

        MuonHIPScaleF = self.ratio_eta.Eval(muoneta)
        if self.verbose : print "(using eta) {}, HIP SF is {}".format(muoneta,  MuonHIPScaleF )
        return float(MuonHIPScaleF)
    '''
    def ElectronHEEPEff(self, eleta) :
        ### UNAPPROVED
        ### we used HEEP 6    https://github.com/cmsb2g/B2GTTbar/blob/master/test/run_B2GTTbarTreeMaker_MC2_Toolbox.py#L70
        ### eff for HEEP 7
        ### https://indico.cern.ch/event/609862/contributions/2458684/attachments/1405493/2147118/HEEP7_Moriond_ScaleFactor_0130.pdf
        effHEEP = 1.
        etabinnedHEEPefficiency = [  [ 0.984, 0.971, 0.961, 0.973, 0.978 , 0.980], [0.002, 0.001, 0.001, 0.001, 0.001, 0.002] ]
        etabins = [-2.5, -1.566, -1.4442, -.5, 0., 0.5, 1.4442, 1.566, 2.5]
        for ebin, ibin in enumerate(etabins):
            if  ebin < eleta < etabins[ibin+1]:
                effHEEP = etabinnedHEEPefficiency[0][ibin]
        if self.verbose : print "ElectronHEEPEff: {0:2.2f}, pt {1:2.2f}, eta {2:2.2f}".format( effHEEP, elpt, eleta)
        return float(effHEEP)

    def ElectronRecoSF(self, eleta, elpt)    :
        ### https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaIDRecipesRun2#Electron_efficiencies_and_scale
        ### https://indico.cern.ch/event/604907/contributions/2452907/attachments/1401460/2139067/RecoSF_ApprovalMoriond17_25Jan2017.pdf
        ### 1D, not Pt dependant
        recoSF = 1.
        rbinx = self.hSFreco.GetXaxis().FindBin( eleta )
        rbiny = self.hSFreco.GetYaxis().FindBin( elpt )
        recoSF = self.hSFreco.GetBinContent(rbinx, rbiny )
        if self.verbose : print "ElectronRecoSF: {0:2.2f}, pt {1:2.2f}, eta {2:2.2f}".format( recoSF, elpt, eleta)
        return float(recoSF)

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
