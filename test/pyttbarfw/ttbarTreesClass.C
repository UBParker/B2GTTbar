#define ttbarTreesClass_cxx
#include "ttbarTreesClass.h"
#include <TFile.h>
#include <TTree.h>
#include <TLorentzVector.h>
#include <iostream>
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void ttbarTreesClass::Loop(std::string outFileName )
{
//   In a ROOT session, you can do:
//      root> .L ttbarTreesClass.C
//      root> ttbarTreesClass t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
    fChain->SetBranchStatus("*",0);  // disable all branches

    fChain->SetBranchStatus("JetPuppiCorrFactor",1);
    fChain->SetBranchStatus("JetTau32",1);

    fChain->SetBranchStatus("JetPuppiSDsubjet0pt",1); 
    fChain->SetBranchStatus("JetPuppiSDsubjet0mass",1);
    fChain->SetBranchStatus("JetPuppiSDsubjet0eta",1);
    fChain->SetBranchStatus("JetPuppiSDsubjet0phi",1);
    fChain->SetBranchStatus("JetPuppiSDsubjet0tau1",1);
    fChain->SetBranchStatus("JetPuppiSDsubjet0tau2",1);
    fChain->SetBranchStatus("JetPuppiSDsubjet0bdisc",1);

    fChain->SetBranchStatus("JetGenMatched_DeltaR_pup0_b",1);
    fChain->SetBranchStatus("JetGenMatched_DeltaR_pup0_Wd1",1);
    fChain->SetBranchStatus("JetGenMatched_DeltaR_pup0_Wd2",1);

    fChain->SetBranchStatus("JetPuppiSDsubjet1pt",1);
    fChain->SetBranchStatus("JetPuppiSDsubjet1mass",1);
    fChain->SetBranchStatus("JetPuppiSDsubjet1eta",1);
    fChain->SetBranchStatus("JetPuppiSDsubjet1phi",1);
    fChain->SetBranchStatus("JetPuppiSDsubjet1tau1",1);
    fChain->SetBranchStatus("JetPuppiSDsubjet1tau2",1);
    fChain->SetBranchStatus("JetPuppiSDsubjet1bdisc",1);

    fChain->SetBranchStatus("JetGenMatched_DeltaR_pup1_b",1);
    fChain->SetBranchStatus("JetGenMatched_DeltaR_pup1_Wd1",1);
    fChain->SetBranchStatus("JetGenMatched_DeltaR_pup1_Wd2",1);

// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;

   // Create an output file and ttree for later use
   TFile* myoutFile  = new TFile(outFileName.c_str(), "RECREATE");
   TTree* myoutTree  = new TTree("SemiLeptSkim_ttbar", "SemiLeptSkim_ttbar");

   // Initialize the vectors

   // leading and sub-leading Softdrop subjets (e.g. pup0 is leading pt subjet of AK8 PUPPI jet)
   TLorentzVector AK8P4_pup0_raw      =  TLorentzVector()  ;
   TLorentzVector AK8P4_pup1_raw      =  TLorentzVector()  ; 
   TLorentzVector AK8P4_pup0          =  TLorentzVector()  ;
   TLorentzVector AK8P4_pup1          =  TLorentzVector()  ;
   // Leading AK8 jet after PUPPI + Softdrop + L2L3 corrections
   TLorentzVector AK8P4               =  TLorentzVector()  ;

   // Define variables to fill branches of myoutTree
   float jetCorrFactor                 =  -100 ;
   float jetTau32                      =  -100 ;

   float subjetmass_MostMassive        =  -100 ;
   float subjetmass_HighestPt          =  -100 ;
   float subjetmass_LowestBdisc        =  -100 ;
   float dR_pup0_b                     =  -100 ;
   float dR_pup1_b                     =  -100 ;
   float dR_pup0_Wd1                   =  -100 ;
   float dR_pup1_Wd1                   =  -100 ;
   float dR_pup0_Wd2                   =  -100 ;
   float dR_pup1_Wd2                   =  -100 ;

   // Assign the variables to branches in myoutTree
   myoutTree->Branch("jetCorrFactor" , &jetCorrFactor );
   myoutTree->Branch("jetTau32" , &jetTau32 );
   myoutTree->Branch("subjetmass_MostMassive" , &subjetmass_MostMassive );
   myoutTree->Branch("subjetmass_HighestPt" , &subjetmass_HighestPt );
   myoutTree->Branch("subjetmass_LowestBdisc" , &subjetmass_LowestBdisc );
   myoutTree->Branch("dR_pup0_b" , &dR_pup0_b );
   myoutTree->Branch("dR_pup0_Wd1" , &dR_pup0_Wd1 );
   myoutTree->Branch("dR_pup0_Wd2" , &dR_pup0_Wd2 );
   myoutTree->Branch("dR_pup1_b" , &dR_pup1_b );
   myoutTree->Branch("dR_pup1_Wd1" , &dR_pup1_Wd1 );
   myoutTree->Branch("dR_pup1_Wd2" , &dR_pup1_Wd2 );

   // Loop over events
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;
      // Define 4-vectors for the AK8 jet and its 2 softdrop subjets (ordered in pt)
      AK8P4_pup0_raw.SetPtEtaPhiM(   JetPuppiSDsubjet0pt ,
				 JetPuppiSDsubjet0eta ,	
                                 JetPuppiSDsubjet0phi ,
				     JetPuppiSDsubjet0mass );

      AK8P4_pup1_raw.SetPtEtaPhiM(     JetPuppiSDsubjet1pt ,
				   JetPuppiSDsubjet1eta ,
				   JetPuppiSDsubjet1phi ,
				       JetPuppiSDsubjet1mass );					
      // Apply L2+L3 corrections for AK8jets to subjets (possibly want AK4 corrections instead)   
	AK8P4_pup0 = AK8P4_pup0_raw * JetPuppiCorrFactor ;
        AK8P4_pup1 = AK8P4_pup1_raw * JetPuppiCorrFactor ;              
                                                     
        AK8P4 = AK8P4_pup0 + AK8P4_pup1 ;
           
      // Recall that the input ttrees are the SemiLeptSkimTrees from stage 12 of the selection
      // code here 
      // https://github.com/UBParker/B2GTTbar/blob/TreeV4/test/pyttbarfw/RunSemiLepTTbar_HighMass.py

      // Top mass window cut
      if  ( 110. <= AK8P4.M() )  continue;
      if  ( AK8P4.M() >= 210. )  continue;

      // Top tag loose n-subjettiness cut
      if  ( JetTau32 > 0.8 ) continue;

      // Assign proper values to variables filled in myoutTree
      if (AK8P4_pup0.M() > AK8P4_pup1.M() ) subjetmass_MostMassive =  AK8P4_pup0.M()  ;
      if (AK8P4_pup0.M() < AK8P4_pup1.M() ) subjetmass_MostMassive =  AK8P4_pup1.M()  ;

      if (AK8P4_pup0.Pt() > AK8P4_pup1.Pt() ) subjetmass_HighestPt =  AK8P4_pup0.M()  ;
      if (AK8P4_pup0.Pt() < AK8P4_pup1.Pt() ) subjetmass_HighestPt =  AK8P4_pup1.M()  ;

      if (JetPuppiSDsubjet1bdisc > JetPuppiSDsubjet0bdisc  ) subjetmass_LowestBdisc  =   AK8P4_pup0.M() ;
      if (JetPuppiSDsubjet1bdisc < JetPuppiSDsubjet0bdisc  ) subjetmass_LowestBdisc  =  AK8P4_pup0.M() ;

      dR_pup0_b = JetGenMatched_DeltaR_pup0_b ;
      dR_pup1_b = JetGenMatched_DeltaR_pup1_b ;
      dR_pup0_Wd1 = JetGenMatched_DeltaR_pup0_Wd1 ;
      dR_pup1_Wd1 = JetGenMatched_DeltaR_pup1_Wd1 ;
      dR_pup0_Wd2 = JetGenMatched_DeltaR_pup0_Wd2 ;
      dR_pup1_Wd2 = JetGenMatched_DeltaR_pup1_Wd2 ;    
     
      // Fill the tree
      myoutTree->Fill();

   } // End loop over events
   myoutFile->cd();
   myoutTree->Write();
   myoutFile->Close();

}
