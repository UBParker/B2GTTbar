


### highmass

CutsPerStage_Type1 =            {
                              "0" :  [ "Stage 0" , "No Weights or Efficiencies" ],  
                              "1" :  [ "Stage 1", "Trigger " ],  
                              "2" :  [ "Stage 2", "Lep Pt > 53 GeV"], # , eta < 2.1 (2.5)"],  
                              "3" :  [ "Stage 3", "Tight(noiso)"],   
                              "4" :  [ "Stage 4" , "MuHighPt(MET Filters)"],  
                              "5" :  [ "Stage 5", "E_{T}^{miss} > 50 GeV " ],  
                              "6" :  [ "Stage 6", "AK4 Pt > 50 GeV"],  
                              "7" :  [ "Stage 7", "2Dcut"],  # 2D cut (decrease QCD contamination) self.DrAK4Lep = 0.4 self.PtRel = 40.
                              "8" :  [ "Stage 8" , "Hemi"],          # Stage 8 : Hemisphere cut (keep leptons far from AK8 Jet DR(AK8, Lepton) > 1.
                              "9" :  [ "Stage 9", "W_{lep} Pt > 200 GeV" ],  
                              "10" :  [ "Stage 10", ""],  
                              "11" :  [ "Stage 11", "AK8 Pt > 400 GeV"],   
                              "12" :  [ "Stage 12" , "AK4 Btag CSVv2Med"],  
                              "13" :  [ "Stage 13", "AK8 #tau_{32} < 0.7" ],  
                              "14" :  [ "Stage 14", "110 < M_{SD AK8} < 210"],  
                              "15" :  [ "Stage 15", "55 < M_{SD SJ0 AK8} < 115"],   
                              "16" :  [ "Stage 16" , "AK8 SDSJ0 #tau_{21} < 0.55"],                                                              
                              "17" :  [ "Stage 17" , "AK8 SDSJ0 Btag CSVv2Med"]             }                              

### low mass

CutsPerStage_Type2 =            {
                              "0" :  [ "Stage 0" , "No Weights or Efficiencies" ],  
                              "1" :  [ "Stage 1", "Trigger" ],  
                              "2" :  [ "Stage 2", "MuHighPt"], # , eta < 2.1 (2.5)"],  
                              "3" :  [ "Stage 3", "Tight(noiso)"],   
                              "4" :  [ "Stage 4" , "Lep Pt > 53 GeV"],  
                              "5" :  [ "Stage 5", "MuIso <0.1" ],  
                              "6" :  [ "Stage 6", "MET > 40(80)GeV"],  
                              "7" :  [ "Stage 7", "AK4 Pt > 30 GeV"],  
                              "8" :  [ "Stage 8" , "LepOutsideBjet"],                                
                              "9" :  [ "Stage 9", "W_{lep} Pt > 200GeV" ],  
                              "10" :  [ "Stage 10", ""],  
                              "11" :  [ "Stage 11", "Pt_{AK8}>200 GeV Hemi"],   
                              "12" :  [ "Stage 12" ,"AK4 Btag CSVv2Med"],  
                              "13" :  [ "Stage 13", "30 < M_{SD AK8} < 150" ],  
                              "14" :  [ "Stage 14", "AK8 #tau_{21} < 0.55"]
           }                                  
                              
