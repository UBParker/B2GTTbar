//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Mon May  1 14:10:36 2017 by ROOT version 6.08/06
// from TTree TTreeSemiLeptSkim/TreeSemiLept
// found on file: ./TTrees/ttbarTuneCUETP8M2T4_highmass_METmu40el80ptRel30.root
//////////////////////////////////////////////////////////

#ifndef ttbarTreesClass_h
#define ttbarTreesClass_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "vector"

class ttbarTreesClass {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   vector<bool>    *SemiLeptTrigPass;
   Float_t         JetPt;
   Float_t         JetEta;
   Float_t         JetPhi;
   Float_t         JetMass;
   Float_t         JetSDmassRaw;
   Float_t         JetSDmassCorrL23;
   Float_t         JetSDptRaw;
   Float_t         JetSDptCorrL23;
   Float_t         JetSDetaRaw;
   Float_t         JetSDphiRaw;
   Float_t         JetTau32;
   Float_t         JetTau21;
   Float_t         JetSDmaxbdisc;
   Float_t         JetSDsubjet0tau1;
   Float_t         JetSDsubjet0tau2;
   Float_t         JetSDsubjet0bdisc;
   Float_t         JetSDsubjet1bdisc;
   Float_t         JetPuppiPt;
   Float_t         JetPuppiEta;
   Float_t         JetPuppiPhi;
   Float_t         JetPuppiMass;
   Float_t         JetPuppiSDmass;
   Float_t         JetPuppiSDpt;
   Float_t         JetPuppiSDeta;
   Float_t         JetPuppiSDphi;
   Float_t         JetPuppiTau1;
   Float_t         JetPuppiTau2;
   Float_t         JetPuppiTau3;
   Float_t         JetPuppiTau4;
   Float_t         JetPuppiTau32;
   Float_t         JetPuppiTau21;
   Float_t         JetPuppiSDmaxbdisc;
   Float_t         JetPuppiSDmaxbdiscflavHadron;
   Float_t         JetPuppiSDmaxbdiscflavParton;
   Float_t         JetPuppiSDsubjet0pt;
   Float_t         JetPuppiSDsubjet0mass;
   Float_t         JetPuppiSDsubjet0eta;
   Float_t         JetPuppiSDsubjet0phi;
   Float_t         JetPuppiSDsubjet0area;
   Float_t         JetPuppiSDsubjet0flavHadron;
   Float_t         JetPuppiSDsubjet0flavParton;
   Float_t         JetPuppiSDsubjet0tau1;
   Float_t         JetPuppiSDsubjet0tau2;
   Float_t         JetPuppiSDsubjet0tau3;
   Float_t         JetPuppiSDsubjet0bdisc;
   Float_t         JetPuppiSDsubjet1pt;
   Float_t         JetPuppiSDsubjet1mass;
   Float_t         JetPuppiSDsubjet1eta;
   Float_t         JetPuppiSDsubjet1phi;
   Float_t         JetPuppiSDsubjet1area;
   Float_t         JetPuppiSDsubjet1flavHadron;
   Float_t         JetPuppiSDsubjet1flavParton;
   Float_t         JetPuppiSDsubjet1tau1;
   Float_t         JetPuppiSDsubjet1tau2;
   Float_t         JetPuppiSDsubjet1tau3;
   Float_t         JetPuppiSDsubjet1bdisc;
   Float_t         JetCHF;
   Float_t         JetNHF;
   Float_t         JetCM;
   Float_t         JetNM;
   Float_t         JetNEF;
   Float_t         JetCEF;
   Float_t         JetMF;
   Float_t         JetMult;
   Float_t         JetMassCorrFactor;
   Float_t         JetCorrFactor;
   Float_t         JetPtSmearFactor;
   Float_t         JetPuppiCorrFactor;
   Float_t         JetPuppiPtSmearFactor;
   Float_t         JetMatchedGenJetPt;
   Float_t         JetMatchedGenJetMass;
   Int_t           JetGenMatched_TopHadronic;
   Float_t         JetGenMatched_TopPt;
   Float_t         JetGenMatched_TopEta;
   Float_t         JetGenMatched_TopPhi;
   Float_t         JetGenMatched_TopMass;
   Float_t         JetGenMatched_bPt;
   Float_t         JetGenMatched_WPt;
   Float_t         JetGenMatched_Wd1Pt;
   Float_t         JetGenMatched_Wd2Pt;
   Float_t         JetGenMatched_Wd1ID;
   Float_t         JetGenMatched_Wd2ID;
   Float_t         JetGenMatched_MaxDeltaRPartonTop;
   Float_t         JetGenMatched_MaxDeltaRWPartonTop;
   Float_t         JetGenMatched_MaxDeltaRWPartonW;
   Float_t         JetGenMatched_DeltaR_t_b;
   Float_t         JetGenMatched_DeltaR_t_W;
   Float_t         JetGenMatched_DeltaR_t_Wd1;
   Float_t         JetGenMatched_DeltaR_t_Wd2;
   Float_t         JetGenMatched_DeltaR_W_b1;
   Float_t         JetGenMatched_DeltaR_W_Wd1;
   Float_t         JetGenMatched_DeltaR_W_Wd2;
   Float_t         JetGenMatched_DeltaR_Wd1_Wd2;
   Float_t         JetGenMatched_DeltaR_Wd1_b;
   Float_t         JetGenMatched_DeltaR_Wd2_b;
   Float_t         JetGenMatched_DeltaR_jet_t;
   Float_t         JetGenMatched_DeltaR_jet_W;
   Float_t         JetGenMatched_DeltaR_jet_b;
   Float_t         JetGenMatched_DeltaR_jet_Wd1;
   Float_t         JetGenMatched_DeltaR_jet_Wd2;
   Float_t         JetGenMatched_DeltaR_pup0_b;
   Float_t         JetGenMatched_DeltaR_pup0_Wd1;
   Float_t         JetGenMatched_DeltaR_pup0_Wd2;
   Float_t         JetGenMatched_DeltaR_pup1_b;
   Float_t         JetGenMatched_DeltaR_pup1_Wd1;
   Float_t         JetGenMatched_DeltaR_pup1_Wd2;
   Float_t         JetGenMatched_partonPt;
   Float_t         JetGenMatched_partonEta;
   Float_t         JetGenMatched_partonPhi;
   Float_t         JetGenMatched_partonMass;
   Float_t         JetGenMatched_partonID;
   Float_t         JetGenMatched_DeltaRjetParton;
   Float_t         SemiLeptMETpx;
   Float_t         SemiLeptMETpy;
   Float_t         SemiLeptMETpt;
   Float_t         SemiLeptMETphi;
   Float_t         SemiLeptMETsumET;
   Float_t         SemiLeptNvtx;
   Float_t         SemiLeptRho;
   Float_t         SemiLeptEventWeight;
   Float_t         SemiLeptPUweight;
   Float_t         SemiLeptPUweight_MBup;
   Float_t         SemiLeptPUweight_MBdn;
   Float_t         SemiLeptGenTTmass;
   Float_t         HTlep;
   Float_t         ST;
   Int_t           SemiLeptRunNum;
   Int_t           SemiLeptLumiBlock;
   Int_t           SemiLeptEventNum;
   Int_t           SemiLeptPassMETFilters;
   Float_t         AK4_dRminLep_Pt;
   Float_t         AK4_dRminLep_Eta;
   Float_t         AK4_dRminLep_Phi;
   Float_t         AK4_dRminLep_Mass;
   Float_t         AK4_dRminLep_Bdisc;
   Float_t         AK4_dRminLep_dRlep;
   Int_t           LepHemiContainsAK4BtagLoose;
   Int_t           LepHemiContainsAK4BtagMedium;
   Int_t           LepHemiContainsAK4BtagTight;
   Float_t         LeptonPhi;
   Float_t         LeptonPt;
   Float_t         LeptonEta;
   Float_t         LeptonMass;
   Float_t         PtRel;
   Int_t           LeptonIsMu;
   Int_t           MuMedium;
   Int_t           MuTight;
   Int_t           MuHighPt;
   Float_t         DeltaRJetLep;
   Float_t         DeltaPhiJetLep;
   Float_t         MuIso;
   Int_t           Electron_iso_passHEEP;
   Int_t           Electron_noiso_passLoose;
   Int_t           Electron_noiso_passMedium;
   Int_t           Electron_noiso_passTight;

   // List of branches
   TBranch        *b_SemiLeptTrigPass;   //!
   TBranch        *b_JetPt;   //!
   TBranch        *b_JetEta;   //!
   TBranch        *b_JetPhi;   //!
   TBranch        *b_JetMass;   //!
   TBranch        *b_JetSDmassRaw;   //!
   TBranch        *b_JetSDmassCorrL23;   //!
   TBranch        *b_JetSDptRaw;   //!
   TBranch        *b_JetSDptCorrL23;   //!
   TBranch        *b_JetSDetaRaw;   //!
   TBranch        *b_JetSDphiRaw;   //!
   TBranch        *b_JetTau32;   //!
   TBranch        *b_JetTau21;   //!
   TBranch        *b_JetSDmaxbdisc;   //!
   TBranch        *b_JetSDsubjet0tau1;   //!
   TBranch        *b_JetSDsubjet0tau2;   //!
   TBranch        *b_JetSDsubjet0bdisc;   //!
   TBranch        *b_JetSDsubjet1bdisc;   //!
   TBranch        *b_JetPuppiPt;   //!
   TBranch        *b_JetPuppiEta;   //!
   TBranch        *b_JetPuppiPhi;   //!
   TBranch        *b_JetPuppiMass;   //!
   TBranch        *b_JetPuppiSDmass;   //!
   TBranch        *b_JetPuppiSDpt;   //!
   TBranch        *b_JetPuppiSDeta;   //!
   TBranch        *b_JetPuppiSDphi;   //!
   TBranch        *b_JetPuppiTau1;   //!
   TBranch        *b_JetPuppiTau2;   //!
   TBranch        *b_JetPuppiTau3;   //!
   TBranch        *b_JetPuppiTau4;   //!
   TBranch        *b_JetPuppiTau32;   //!
   TBranch        *b_JetPuppiTau21;   //!
   TBranch        *b_JetPuppiSDmaxbdisc;   //!
   TBranch        *b_JetPuppiSDmaxbdiscflavHadron;   //!
   TBranch        *b_JetPuppiSDmaxbdiscflavParton;   //!
   TBranch        *b_JetPuppiSDsubjet0pt;   //!
   TBranch        *b_JetPuppiSDsubjet0mass;   //!
   TBranch        *b_JetPuppiSDsubjet0eta;   //!
   TBranch        *b_JetPuppiSDsubjet0phi;   //!
   TBranch        *b_JetPuppiSDsubjet0area;   //!
   TBranch        *b_JetPuppiSDsubjet0flavHadron;   //!
   TBranch        *b_JetPuppiSDsubjet0flavParton;   //!
   TBranch        *b_JetPuppiSDsubjet0tau1;   //!
   TBranch        *b_JetPuppiSDsubjet0tau2;   //!
   TBranch        *b_JetPuppiSDsubjet0tau3;   //!
   TBranch        *b_JetPuppiSDsubjet0bdisc;   //!
   TBranch        *b_JetPuppiSDsubjet1pt;   //!
   TBranch        *b_JetPuppiSDsubjet1mass;   //!
   TBranch        *b_JetPuppiSDsubjet1eta;   //!
   TBranch        *b_JetPuppiSDsubjet1phi;   //!
   TBranch        *b_JetPuppiSDsubjet1area;   //!
   TBranch        *b_JetPuppiSDsubjet1flavHadron;   //!
   TBranch        *b_JetPuppiSDsubjet1flavParton;   //!
   TBranch        *b_JetPuppiSDsubjet1tau1;   //!
   TBranch        *b_JetPuppiSDsubjet1tau2;   //!
   TBranch        *b_JetPuppiSDsubjet1tau3;   //!
   TBranch        *b_JetPuppiSDsubjet1bdisc;   //!
   TBranch        *b_JetCHF;   //!
   TBranch        *b_JetNHF;   //!
   TBranch        *b_JetCM;   //!
   TBranch        *b_JetNM;   //!
   TBranch        *b_JetNEF;   //!
   TBranch        *b_JetCEF;   //!
   TBranch        *b_JetMF;   //!
   TBranch        *b_JetMult;   //!
   TBranch        *b_JetMassCorrFactor;   //!
   TBranch        *b_JetCorrFactor;   //!
   TBranch        *b_JetPtSmearFactor;   //!
   TBranch        *b_JetPuppiCorrFactor;   //!
   TBranch        *b_JetPuppiPtSmearFactor;   //!
   TBranch        *b_JetMatchedGenJetPt;   //!
   TBranch        *b_JetMatchedGenJetMass;   //!
   TBranch        *b_JetGenMatched_TopHadronic;   //!
   TBranch        *b_JetGenMatched_TopPt;   //!
   TBranch        *b_JetGenMatched_TopEta;   //!
   TBranch        *b_JetGenMatched_TopPhi;   //!
   TBranch        *b_JetGenMatched_TopMass;   //!
   TBranch        *b_JetGenMatched_bPt;   //!
   TBranch        *b_JetGenMatched_WPt;   //!
   TBranch        *b_JetGenMatched_Wd1Pt;   //!
   TBranch        *b_JetGenMatched_Wd2Pt;   //!
   TBranch        *b_JetGenMatched_Wd1ID;   //!
   TBranch        *b_JetGenMatched_Wd2ID;   //!
   TBranch        *b_JetGenMatched_MaxDeltaRPartonTop;   //!
   TBranch        *b_JetGenMatched_MaxDeltaRWPartonTop;   //!
   TBranch        *b_JetGenMatched_MaxDeltaRWPartonW;   //!
   TBranch        *b_JetGenMatched_DeltaR_t_b;   //!
   TBranch        *b_JetGenMatched_DeltaR_t_W;   //!
   TBranch        *b_JetGenMatched_DeltaR_t_Wd1;   //!
   TBranch        *b_JetGenMatched_DeltaR_t_Wd2;   //!
   TBranch        *b_JetGenMatched_DeltaR_W_b1;   //!
   TBranch        *b_JetGenMatched_DeltaR_W_Wd1;   //!
   TBranch        *b_JetGenMatched_DeltaR_W_Wd2;   //!
   TBranch        *b_JetGenMatched_DeltaR_Wd1_Wd2;   //!
   TBranch        *b_JetGenMatched_DeltaR_Wd1_b;   //!
   TBranch        *b_JetGenMatched_DeltaR_Wd2_b;   //!
   TBranch        *b_JetGenMatched_DeltaR_jet_t;   //!
   TBranch        *b_JetGenMatched_DeltaR_jet_W;   //!
   TBranch        *b_JetGenMatched_DeltaR_jet_b;   //!
   TBranch        *b_JetGenMatched_DeltaR_jet_Wd1;   //!
   TBranch        *b_JetGenMatched_DeltaR_jet_Wd2;   //!
   TBranch        *b_JetGenMatched_DeltaR_pup0_b;   //!
   TBranch        *b_JetGenMatched_DeltaR_pup0_Wd1;   //!
   TBranch        *b_JetGenMatched_DeltaR_pup0_Wd2;   //!
   TBranch        *b_JetGenMatched_DeltaR_pup1_b;   //!
   TBranch        *b_JetGenMatched_DeltaR_pup1_Wd1;   //!
   TBranch        *b_JetGenMatched_DeltaR_pup1_Wd2;   //!
   TBranch        *b_JetGenMatched_partonPt;   //!
   TBranch        *b_JetGenMatched_partonEta;   //!
   TBranch        *b_JetGenMatched_partonPhi;   //!
   TBranch        *b_JetGenMatched_partonMass;   //!
   TBranch        *b_JetGenMatched_partonID;   //!
   TBranch        *b_JetGenMatched_DeltaRjetParton;   //!
   TBranch        *b_SemiLeptMETpx;   //!
   TBranch        *b_SemiLeptMETpy;   //!
   TBranch        *b_SemiLeptMETpt;   //!
   TBranch        *b_SemiLeptMETphi;   //!
   TBranch        *b_SemiLeptMETsumET;   //!
   TBranch        *b_SemiLeptNvtx;   //!
   TBranch        *b_SemiLeptRho;   //!
   TBranch        *b_SemiLeptEventWeight;   //!
   TBranch        *b_SemiLeptPUweight;   //!
   TBranch        *b_SemiLeptPUweight_MBup;   //!
   TBranch        *b_SemiLeptPUweight_MBdn;   //!
   TBranch        *b_SemiLeptGenTTmass;   //!
   TBranch        *b_HTlep;   //!
   TBranch        *b_ST;   //!
   TBranch        *b_SemiLeptRunNum;   //!
   TBranch        *b_SemiLeptLumiBlock;   //!
   TBranch        *b_SemiLeptEventNum;   //!
   TBranch        *b_SemiLeptPassMETFilters;   //!
   TBranch        *b_AK4_dRminLep_Pt;   //!
   TBranch        *b_AK4_dRminLep_Eta;   //!
   TBranch        *b_AK4_dRminLep_Phi;   //!
   TBranch        *b_AK4_dRminLep_Mass;   //!
   TBranch        *b_AK4_dRminLep_Bdisc;   //!
   TBranch        *b_AK4_dRminLep_dRlep;   //!
   TBranch        *b_LepHemiContainsAK4BtagLoose;   //!
   TBranch        *b_LepHemiContainsAK4BtagMedium;   //!
   TBranch        *b_LepHemiContainsAK4BtagTight;   //!
   TBranch        *b_LeptonPhi;   //!
   TBranch        *b_LeptonPt;   //!
   TBranch        *b_LeptonEta;   //!
   TBranch        *b_LeptonMass;   //!
   TBranch        *b_PtRel;   //!
   TBranch        *b_LeptonIsMu;   //!
   TBranch        *b_MuMedium;   //!
   TBranch        *b_MuTight;   //!
   TBranch        *b_MuHighPt;   //!
   TBranch        *b_DeltaRJetLep;   //!
   TBranch        *b_DeltaPhiJetLep;   //!
   TBranch        *b_MuIso;   //!
   TBranch        *b_Electron_iso_passHEEP;   //!
   TBranch        *b_Electron_noiso_passLoose;   //!
   TBranch        *b_Electron_noiso_passMedium;   //!
   TBranch        *b_Electron_noiso_passTight;   //!

   ttbarTreesClass(TTree *tree=0);
   virtual ~ttbarTreesClass();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef ttbarTreesClass_cxx
ttbarTreesClass::ttbarTreesClass(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("./TTrees/ttbarTuneCUETP8M2T4_highmass_METmu40el80ptRel30.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("./TTrees/ttbarTuneCUETP8M2T4_highmass_METmu40el80ptRel30.root");
      }
      f->GetObject("TTreeSemiLeptSkim",tree);

   }
   Init(tree);
}

ttbarTreesClass::~ttbarTreesClass()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t ttbarTreesClass::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t ttbarTreesClass::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void ttbarTreesClass::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   SemiLeptTrigPass = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("SemiLeptTrigPass", &SemiLeptTrigPass, &b_SemiLeptTrigPass);
   fChain->SetBranchAddress("JetPt", &JetPt, &b_JetPt);
   fChain->SetBranchAddress("JetEta", &JetEta, &b_JetEta);
   fChain->SetBranchAddress("JetPhi", &JetPhi, &b_JetPhi);
   fChain->SetBranchAddress("JetMass", &JetMass, &b_JetMass);
   fChain->SetBranchAddress("JetSDmassRaw", &JetSDmassRaw, &b_JetSDmassRaw);
   fChain->SetBranchAddress("JetSDmassCorrL23", &JetSDmassCorrL23, &b_JetSDmassCorrL23);
   fChain->SetBranchAddress("JetSDptRaw", &JetSDptRaw, &b_JetSDptRaw);
   fChain->SetBranchAddress("JetSDptCorrL23", &JetSDptCorrL23, &b_JetSDptCorrL23);
   fChain->SetBranchAddress("JetSDetaRaw", &JetSDetaRaw, &b_JetSDetaRaw);
   fChain->SetBranchAddress("JetSDphiRaw", &JetSDphiRaw, &b_JetSDphiRaw);
   fChain->SetBranchAddress("JetTau32", &JetTau32, &b_JetTau32);
   fChain->SetBranchAddress("JetTau21", &JetTau21, &b_JetTau21);
   fChain->SetBranchAddress("JetSDmaxbdisc", &JetSDmaxbdisc, &b_JetSDmaxbdisc);
   fChain->SetBranchAddress("JetSDsubjet0tau1", &JetSDsubjet0tau1, &b_JetSDsubjet0tau1);
   fChain->SetBranchAddress("JetSDsubjet0tau2", &JetSDsubjet0tau2, &b_JetSDsubjet0tau2);
   fChain->SetBranchAddress("JetSDsubjet0bdisc", &JetSDsubjet0bdisc, &b_JetSDsubjet0bdisc);
   fChain->SetBranchAddress("JetSDsubjet1bdisc", &JetSDsubjet1bdisc, &b_JetSDsubjet1bdisc);
   fChain->SetBranchAddress("JetPuppiPt", &JetPuppiPt, &b_JetPuppiPt);
   fChain->SetBranchAddress("JetPuppiEta", &JetPuppiEta, &b_JetPuppiEta);
   fChain->SetBranchAddress("JetPuppiPhi", &JetPuppiPhi, &b_JetPuppiPhi);
   fChain->SetBranchAddress("JetPuppiMass", &JetPuppiMass, &b_JetPuppiMass);
   fChain->SetBranchAddress("JetPuppiSDmass", &JetPuppiSDmass, &b_JetPuppiSDmass);
   fChain->SetBranchAddress("JetPuppiSDpt", &JetPuppiSDpt, &b_JetPuppiSDpt);
   fChain->SetBranchAddress("JetPuppiSDeta", &JetPuppiSDeta, &b_JetPuppiSDeta);
   fChain->SetBranchAddress("JetPuppiSDphi", &JetPuppiSDphi, &b_JetPuppiSDphi);
   fChain->SetBranchAddress("JetPuppiTau1", &JetPuppiTau1, &b_JetPuppiTau1);
   fChain->SetBranchAddress("JetPuppiTau2", &JetPuppiTau2, &b_JetPuppiTau2);
   fChain->SetBranchAddress("JetPuppiTau3", &JetPuppiTau3, &b_JetPuppiTau3);
   fChain->SetBranchAddress("JetPuppiTau4", &JetPuppiTau4, &b_JetPuppiTau4);
   fChain->SetBranchAddress("JetPuppiTau32", &JetPuppiTau32, &b_JetPuppiTau32);
   fChain->SetBranchAddress("JetPuppiTau21", &JetPuppiTau21, &b_JetPuppiTau21);
   fChain->SetBranchAddress("JetPuppiSDmaxbdisc", &JetPuppiSDmaxbdisc, &b_JetPuppiSDmaxbdisc);
   fChain->SetBranchAddress("JetPuppiSDmaxbdiscflavHadron", &JetPuppiSDmaxbdiscflavHadron, &b_JetPuppiSDmaxbdiscflavHadron);
   fChain->SetBranchAddress("JetPuppiSDmaxbdiscflavParton", &JetPuppiSDmaxbdiscflavParton, &b_JetPuppiSDmaxbdiscflavParton);
   fChain->SetBranchAddress("JetPuppiSDsubjet0pt", &JetPuppiSDsubjet0pt, &b_JetPuppiSDsubjet0pt);
   fChain->SetBranchAddress("JetPuppiSDsubjet0mass", &JetPuppiSDsubjet0mass, &b_JetPuppiSDsubjet0mass);
   fChain->SetBranchAddress("JetPuppiSDsubjet0eta", &JetPuppiSDsubjet0eta, &b_JetPuppiSDsubjet0eta);
   fChain->SetBranchAddress("JetPuppiSDsubjet0phi", &JetPuppiSDsubjet0phi, &b_JetPuppiSDsubjet0phi);
   fChain->SetBranchAddress("JetPuppiSDsubjet0area", &JetPuppiSDsubjet0area, &b_JetPuppiSDsubjet0area);
   fChain->SetBranchAddress("JetPuppiSDsubjet0flavHadron", &JetPuppiSDsubjet0flavHadron, &b_JetPuppiSDsubjet0flavHadron);
   fChain->SetBranchAddress("JetPuppiSDsubjet0flavParton", &JetPuppiSDsubjet0flavParton, &b_JetPuppiSDsubjet0flavParton);
   fChain->SetBranchAddress("JetPuppiSDsubjet0tau1", &JetPuppiSDsubjet0tau1, &b_JetPuppiSDsubjet0tau1);
   fChain->SetBranchAddress("JetPuppiSDsubjet0tau2", &JetPuppiSDsubjet0tau2, &b_JetPuppiSDsubjet0tau2);
   fChain->SetBranchAddress("JetPuppiSDsubjet0tau3", &JetPuppiSDsubjet0tau3, &b_JetPuppiSDsubjet0tau3);
   fChain->SetBranchAddress("JetPuppiSDsubjet0bdisc", &JetPuppiSDsubjet0bdisc, &b_JetPuppiSDsubjet0bdisc);
   fChain->SetBranchAddress("JetPuppiSDsubjet1pt", &JetPuppiSDsubjet1pt, &b_JetPuppiSDsubjet1pt);
   fChain->SetBranchAddress("JetPuppiSDsubjet1mass", &JetPuppiSDsubjet1mass, &b_JetPuppiSDsubjet1mass);
   fChain->SetBranchAddress("JetPuppiSDsubjet1eta", &JetPuppiSDsubjet1eta, &b_JetPuppiSDsubjet1eta);
   fChain->SetBranchAddress("JetPuppiSDsubjet1phi", &JetPuppiSDsubjet1phi, &b_JetPuppiSDsubjet1phi);
   fChain->SetBranchAddress("JetPuppiSDsubjet1area", &JetPuppiSDsubjet1area, &b_JetPuppiSDsubjet1area);
   fChain->SetBranchAddress("JetPuppiSDsubjet1flavHadron", &JetPuppiSDsubjet1flavHadron, &b_JetPuppiSDsubjet1flavHadron);
   fChain->SetBranchAddress("JetPuppiSDsubjet1flavParton", &JetPuppiSDsubjet1flavParton, &b_JetPuppiSDsubjet1flavParton);
   fChain->SetBranchAddress("JetPuppiSDsubjet1tau1", &JetPuppiSDsubjet1tau1, &b_JetPuppiSDsubjet1tau1);
   fChain->SetBranchAddress("JetPuppiSDsubjet1tau2", &JetPuppiSDsubjet1tau2, &b_JetPuppiSDsubjet1tau2);
   fChain->SetBranchAddress("JetPuppiSDsubjet1tau3", &JetPuppiSDsubjet1tau3, &b_JetPuppiSDsubjet1tau3);
   fChain->SetBranchAddress("JetPuppiSDsubjet1bdisc", &JetPuppiSDsubjet1bdisc, &b_JetPuppiSDsubjet1bdisc);
   fChain->SetBranchAddress("JetCHF", &JetCHF, &b_JetCHF);
   fChain->SetBranchAddress("JetNHF", &JetNHF, &b_JetNHF);
   fChain->SetBranchAddress("JetCM", &JetCM, &b_JetCM);
   fChain->SetBranchAddress("JetNM", &JetNM, &b_JetNM);
   fChain->SetBranchAddress("JetNEF", &JetNEF, &b_JetNEF);
   fChain->SetBranchAddress("JetCEF", &JetCEF, &b_JetCEF);
   fChain->SetBranchAddress("JetMF", &JetMF, &b_JetMF);
   fChain->SetBranchAddress("JetMult", &JetMult, &b_JetMult);
   fChain->SetBranchAddress("JetMassCorrFactor", &JetMassCorrFactor, &b_JetMassCorrFactor);
   fChain->SetBranchAddress("JetCorrFactor", &JetCorrFactor, &b_JetCorrFactor);
   fChain->SetBranchAddress("JetPtSmearFactor", &JetPtSmearFactor, &b_JetPtSmearFactor);
   fChain->SetBranchAddress("JetPuppiCorrFactor", &JetPuppiCorrFactor, &b_JetPuppiCorrFactor);
   fChain->SetBranchAddress("JetPuppiPtSmearFactor", &JetPuppiPtSmearFactor, &b_JetPuppiPtSmearFactor);
   fChain->SetBranchAddress("JetMatchedGenJetPt", &JetMatchedGenJetPt, &b_JetMatchedGenJetPt);
   fChain->SetBranchAddress("JetMatchedGenJetMass", &JetMatchedGenJetMass, &b_JetMatchedGenJetMass);
   fChain->SetBranchAddress("JetGenMatched_TopHadronic", &JetGenMatched_TopHadronic, &b_JetGenMatched_TopHadronic);
   fChain->SetBranchAddress("JetGenMatched_TopPt", &JetGenMatched_TopPt, &b_JetGenMatched_TopPt);
   fChain->SetBranchAddress("JetGenMatched_TopEta", &JetGenMatched_TopEta, &b_JetGenMatched_TopEta);
   fChain->SetBranchAddress("JetGenMatched_TopPhi", &JetGenMatched_TopPhi, &b_JetGenMatched_TopPhi);
   fChain->SetBranchAddress("JetGenMatched_TopMass", &JetGenMatched_TopMass, &b_JetGenMatched_TopMass);
   fChain->SetBranchAddress("JetGenMatched_bPt", &JetGenMatched_bPt, &b_JetGenMatched_bPt);
   fChain->SetBranchAddress("JetGenMatched_WPt", &JetGenMatched_WPt, &b_JetGenMatched_WPt);
   fChain->SetBranchAddress("JetGenMatched_Wd1Pt", &JetGenMatched_Wd1Pt, &b_JetGenMatched_Wd1Pt);
   fChain->SetBranchAddress("JetGenMatched_Wd2Pt", &JetGenMatched_Wd2Pt, &b_JetGenMatched_Wd2Pt);
   fChain->SetBranchAddress("JetGenMatched_Wd1ID", &JetGenMatched_Wd1ID, &b_JetGenMatched_Wd1ID);
   fChain->SetBranchAddress("JetGenMatched_Wd2ID", &JetGenMatched_Wd2ID, &b_JetGenMatched_Wd2ID);
   fChain->SetBranchAddress("JetGenMatched_MaxDeltaRPartonTop", &JetGenMatched_MaxDeltaRPartonTop, &b_JetGenMatched_MaxDeltaRPartonTop);
   fChain->SetBranchAddress("JetGenMatched_MaxDeltaRWPartonTop", &JetGenMatched_MaxDeltaRWPartonTop, &b_JetGenMatched_MaxDeltaRWPartonTop);
   fChain->SetBranchAddress("JetGenMatched_MaxDeltaRWPartonW", &JetGenMatched_MaxDeltaRWPartonW, &b_JetGenMatched_MaxDeltaRWPartonW);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_t_b", &JetGenMatched_DeltaR_t_b, &b_JetGenMatched_DeltaR_t_b);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_t_W", &JetGenMatched_DeltaR_t_W, &b_JetGenMatched_DeltaR_t_W);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_t_Wd1", &JetGenMatched_DeltaR_t_Wd1, &b_JetGenMatched_DeltaR_t_Wd1);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_t_Wd2", &JetGenMatched_DeltaR_t_Wd2, &b_JetGenMatched_DeltaR_t_Wd2);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_W_b1", &JetGenMatched_DeltaR_W_b1, &b_JetGenMatched_DeltaR_W_b1);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_W_Wd1", &JetGenMatched_DeltaR_W_Wd1, &b_JetGenMatched_DeltaR_W_Wd1);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_W_Wd2", &JetGenMatched_DeltaR_W_Wd2, &b_JetGenMatched_DeltaR_W_Wd2);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_Wd1_Wd2", &JetGenMatched_DeltaR_Wd1_Wd2, &b_JetGenMatched_DeltaR_Wd1_Wd2);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_Wd1_b", &JetGenMatched_DeltaR_Wd1_b, &b_JetGenMatched_DeltaR_Wd1_b);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_Wd2_b", &JetGenMatched_DeltaR_Wd2_b, &b_JetGenMatched_DeltaR_Wd2_b);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_jet_t", &JetGenMatched_DeltaR_jet_t, &b_JetGenMatched_DeltaR_jet_t);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_jet_W", &JetGenMatched_DeltaR_jet_W, &b_JetGenMatched_DeltaR_jet_W);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_jet_b", &JetGenMatched_DeltaR_jet_b, &b_JetGenMatched_DeltaR_jet_b);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_jet_Wd1", &JetGenMatched_DeltaR_jet_Wd1, &b_JetGenMatched_DeltaR_jet_Wd1);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_jet_Wd2", &JetGenMatched_DeltaR_jet_Wd2, &b_JetGenMatched_DeltaR_jet_Wd2);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_pup0_b", &JetGenMatched_DeltaR_pup0_b, &b_JetGenMatched_DeltaR_pup0_b);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_pup0_Wd1", &JetGenMatched_DeltaR_pup0_Wd1, &b_JetGenMatched_DeltaR_pup0_Wd1);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_pup0_Wd2", &JetGenMatched_DeltaR_pup0_Wd2, &b_JetGenMatched_DeltaR_pup0_Wd2);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_pup1_b", &JetGenMatched_DeltaR_pup1_b, &b_JetGenMatched_DeltaR_pup1_b);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_pup1_Wd1", &JetGenMatched_DeltaR_pup1_Wd1, &b_JetGenMatched_DeltaR_pup1_Wd1);
   fChain->SetBranchAddress("JetGenMatched_DeltaR_pup1_Wd2", &JetGenMatched_DeltaR_pup1_Wd2, &b_JetGenMatched_DeltaR_pup1_Wd2);
   fChain->SetBranchAddress("JetGenMatched_partonPt", &JetGenMatched_partonPt, &b_JetGenMatched_partonPt);
   fChain->SetBranchAddress("JetGenMatched_partonEta", &JetGenMatched_partonEta, &b_JetGenMatched_partonEta);
   fChain->SetBranchAddress("JetGenMatched_partonPhi", &JetGenMatched_partonPhi, &b_JetGenMatched_partonPhi);
   fChain->SetBranchAddress("JetGenMatched_partonMass", &JetGenMatched_partonMass, &b_JetGenMatched_partonMass);
   fChain->SetBranchAddress("JetGenMatched_partonID", &JetGenMatched_partonID, &b_JetGenMatched_partonID);
   fChain->SetBranchAddress("JetGenMatched_DeltaRjetParton", &JetGenMatched_DeltaRjetParton, &b_JetGenMatched_DeltaRjetParton);
   fChain->SetBranchAddress("SemiLeptMETpx", &SemiLeptMETpx, &b_SemiLeptMETpx);
   fChain->SetBranchAddress("SemiLeptMETpy", &SemiLeptMETpy, &b_SemiLeptMETpy);
   fChain->SetBranchAddress("SemiLeptMETpt", &SemiLeptMETpt, &b_SemiLeptMETpt);
   fChain->SetBranchAddress("SemiLeptMETphi", &SemiLeptMETphi, &b_SemiLeptMETphi);
   fChain->SetBranchAddress("SemiLeptMETsumET", &SemiLeptMETsumET, &b_SemiLeptMETsumET);
   fChain->SetBranchAddress("SemiLeptNvtx", &SemiLeptNvtx, &b_SemiLeptNvtx);
   fChain->SetBranchAddress("SemiLeptRho", &SemiLeptRho, &b_SemiLeptRho);
   fChain->SetBranchAddress("SemiLeptEventWeight", &SemiLeptEventWeight, &b_SemiLeptEventWeight);
   fChain->SetBranchAddress("SemiLeptPUweight", &SemiLeptPUweight, &b_SemiLeptPUweight);
   fChain->SetBranchAddress("SemiLeptPUweight_MBup", &SemiLeptPUweight_MBup, &b_SemiLeptPUweight_MBup);
   fChain->SetBranchAddress("SemiLeptPUweight_MBdn", &SemiLeptPUweight_MBdn, &b_SemiLeptPUweight_MBdn);
   fChain->SetBranchAddress("SemiLeptGenTTmass", &SemiLeptGenTTmass, &b_SemiLeptGenTTmass);
   fChain->SetBranchAddress("HTlep", &HTlep, &b_HTlep);
   fChain->SetBranchAddress("ST", &ST, &b_ST);
   fChain->SetBranchAddress("SemiLeptRunNum", &SemiLeptRunNum, &b_SemiLeptRunNum);
   fChain->SetBranchAddress("SemiLeptLumiBlock", &SemiLeptLumiBlock, &b_SemiLeptLumiBlock);
   fChain->SetBranchAddress("SemiLeptEventNum", &SemiLeptEventNum, &b_SemiLeptEventNum);
   fChain->SetBranchAddress("SemiLeptPassMETFilters", &SemiLeptPassMETFilters, &b_SemiLeptPassMETFilters);
   fChain->SetBranchAddress("AK4_dRminLep_Pt", &AK4_dRminLep_Pt, &b_AK4_dRminLep_Pt);
   fChain->SetBranchAddress("AK4_dRminLep_Eta", &AK4_dRminLep_Eta, &b_AK4_dRminLep_Eta);
   fChain->SetBranchAddress("AK4_dRminLep_Phi", &AK4_dRminLep_Phi, &b_AK4_dRminLep_Phi);
   fChain->SetBranchAddress("AK4_dRminLep_Mass", &AK4_dRminLep_Mass, &b_AK4_dRminLep_Mass);
   fChain->SetBranchAddress("AK4_dRminLep_Bdisc", &AK4_dRminLep_Bdisc, &b_AK4_dRminLep_Bdisc);
   fChain->SetBranchAddress("AK4_dRminLep_dRlep", &AK4_dRminLep_dRlep, &b_AK4_dRminLep_dRlep);
   fChain->SetBranchAddress("LepHemiContainsAK4BtagLoose", &LepHemiContainsAK4BtagLoose, &b_LepHemiContainsAK4BtagLoose);
   fChain->SetBranchAddress("LepHemiContainsAK4BtagMedium", &LepHemiContainsAK4BtagMedium, &b_LepHemiContainsAK4BtagMedium);
   fChain->SetBranchAddress("LepHemiContainsAK4BtagTight", &LepHemiContainsAK4BtagTight, &b_LepHemiContainsAK4BtagTight);
   fChain->SetBranchAddress("LeptonPhi", &LeptonPhi, &b_LeptonPhi);
   fChain->SetBranchAddress("LeptonPt", &LeptonPt, &b_LeptonPt);
   fChain->SetBranchAddress("LeptonEta", &LeptonEta, &b_LeptonEta);
   fChain->SetBranchAddress("LeptonMass", &LeptonMass, &b_LeptonMass);
   fChain->SetBranchAddress("PtRel", &PtRel, &b_PtRel);
   fChain->SetBranchAddress("LeptonIsMu", &LeptonIsMu, &b_LeptonIsMu);
   fChain->SetBranchAddress("MuMedium", &MuMedium, &b_MuMedium);
   fChain->SetBranchAddress("MuTight", &MuTight, &b_MuTight);
   fChain->SetBranchAddress("MuHighPt", &MuHighPt, &b_MuHighPt);
   fChain->SetBranchAddress("DeltaRJetLep", &DeltaRJetLep, &b_DeltaRJetLep);
   fChain->SetBranchAddress("DeltaPhiJetLep", &DeltaPhiJetLep, &b_DeltaPhiJetLep);
   fChain->SetBranchAddress("MuIso", &MuIso, &b_MuIso);
   fChain->SetBranchAddress("Electron_iso_passHEEP", &Electron_iso_passHEEP, &b_Electron_iso_passHEEP);
   fChain->SetBranchAddress("Electron_noiso_passLoose", &Electron_noiso_passLoose, &b_Electron_noiso_passLoose);
   fChain->SetBranchAddress("Electron_noiso_passMedium", &Electron_noiso_passMedium, &b_Electron_noiso_passMedium);
   fChain->SetBranchAddress("Electron_noiso_passTight", &Electron_noiso_passTight, &b_Electron_noiso_passTight);
   Notify();
}

Bool_t ttbarTreesClass::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void ttbarTreesClass::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t ttbarTreesClass::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef ttbarTreesClass_cxx
