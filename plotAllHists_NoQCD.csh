#type 1


###################################################


python plotstack.py --hist LeptonPtHist  --allMC  
python plotstack.py --hist AK8MSDHist --allMC   
python plotstack.py --hist AK8MHist --allMC   
python plotstack.py --hist AK8PtHist  --allMC
python plotstack.py --hist METPtHist --allMC
python plotstack.py --hist AK8HTHist  --allMC  
python plotstack.py --hist AK8Tau32Hist  --allMC
python plotstack.py --hist LeptonEtaHist  --allMC
python plotstack.py --hist HTLepHist  --allMC 
python plotstack.py --hist AK4BdiscHist --allMC 
python plotstack.py --hist AK8SDPtHist  --allMC  
python plotstack.py --hist AK8MSDSJ0Hist --allMC
python plotstack.py --hist AK8MSDSJ0Pt200To300Hist --allMC    
python plotstack.py --hist AK8MSDSJ0Pt300To400Hist --allMC    
python plotstack.py --hist AK8MSDSJ0Pt400To500Hist --allMC    
python plotstack.py --hist AK8MSDSJ0Pt500To800Hist --allMC 

python plotstack.py --hist LeptonPtHist  --allMC  --includeQCD
python plotstack.py --hist AK8MSDHist --allMC  --includeQCD  
python plotstack.py --hist AK8MHist --allMC    --includeQCD  
python plotstack.py --hist AK8PtHist  --allMC --includeQCD
python plotstack.py --hist METPtHist --allMC --includeQCD 
python plotstack.py --hist AK8HTHist  --allMC --includeQCD  
python plotstack.py --hist AK8Tau32Hist  --allMC --includeQCD
python plotstack.py --hist LeptonEtaHist  --allMC --includeQCD
python plotstack.py --hist HTLepHist  --allMC  --includeQCD
python plotstack.py --hist AK4BdiscHist --allMC  --includeQCD
python plotstack.py --hist AK8SDPtHist  --allMC  --includeQCD 
python plotstack.py --hist AK8MSDSJ0Hist --allMC --includeQCD 
python plotstack.py --hist AK8MSDSJ0Pt200To300Hist --allMC  --includeQCD  
python plotstack.py --hist AK8MSDSJ0Pt300To400Hist --allMC  --includeQCD  
python plotstack.py --hist AK8MSDSJ0Pt400To500Hist --allMC  --includeQCD  
python plotstack.py --hist AK8MSDSJ0Pt500To800Hist --allMC --includeQCD

python plotstack.py --hist LeptonPtHist  --allMC  --includeQCD --drawOnlyQCD
python plotstack.py --hist AK8MSDHist --allMC  --includeQCD --drawOnlyQCD 
python plotstack.py --hist AK8MHist --allMC    --includeQCD  --drawOnlyQCD 
python plotstack.py --hist AK8PtHist  --allMC --includeQCD --drawOnlyQCD
python plotstack.py --hist METPtHist --allMC --includeQCD --drawOnlyQCD 
python plotstack.py --hist AK8HTHist  --allMC --includeQCD   --drawOnlyQCD 
python plotstack.py --hist AK8Tau32Hist  --allMC --includeQCD  --drawOnlyQCD
python plotstack.py --hist LeptonEtaHist  --allMC --includeQCD --drawOnlyQCD
python plotstack.py --hist HTLepHist  --allMC  --includeQCD --drawOnlyQCD
python plotstack.py --hist AK4BdiscHist --allMC  --includeQCD --drawOnlyQCD
python plotstack.py --hist AK8SDPtHist  --allMC  --includeQCD  --drawOnlyQCD
python plotstack.py --hist AK8MSDSJ0Hist --allMC --includeQCD  --drawOnlyQCD
python plotstack.py --hist AK8MSDSJ0Pt200To300Hist --allMC  --includeQCD   --drawOnlyQCD
python plotstack.py --hist AK8MSDSJ0Pt300To400Hist --allMC  --includeQCD   --drawOnlyQCD
python plotstack.py --hist AK8MSDSJ0Pt400To500Hist --allMC  --includeQCD  --drawOnlyQCD  
python plotstack.py --hist AK8MSDSJ0Pt500To800Hist --allMC --includeQCD  --drawOnlyQCD

######################################################




Histos = [  "AK8MSDHist", #0
         "AK8MSDSJ0Hist", #1
             "AK8PtHist", #2
            "AK8EtaHist", #3
     "AK8puppitau21Hist", #4
     "AK8puppitau32Hist", #5
              "AK8MHist", #6
          "LeptonPtHist", #7
         "LeptonEtaHist", #8
             "METPtHist", #9
             "HTLepHist", #10
             "Iso2DHist", #11
          "AK4BdiscHist", #12
"AK8MSDSJ0Pt200To300Hist", #13
"AK8MSDSJ0Pt300To400Hist", #14
"AK8MSDSJ0Pt400To500Hist", #15
"AK8MSDSJ0Pt500To800Hist", #16  
"AK8HTHist",               #17 
"AK8SDPtHist",             #18 
"AK8PuppiSDPtHist",        #19 
"AK8PuppiPtHist",          #20 
"AK8MPt200To300Hist", #21
"AK8MPt300To400Hist", #22
"AK8MPt400To500Hist", #23
"AK8MPt500To800Hist", #24 
"AK8MSDPt200To300Hist", #25
"AK8MSDPt300To400Hist", #26
"AK8MSDPt400To500Hist", #27
"AK8MSDPt500To800Hist", #28 
"AK8Tau32Hist",         #29


#type 2


python plotstack.py --hist AK8MSDHist --allMC    --fixFit --verbose --Type2 >& AK8MSDHist2.txt &

python plotstack.py --hist AK8PtHist  --allMC    --fixFit --verbose --Type2 >& AK8PtHist2.txt &

python plotstack.py --hist AK8EtaHist  --allMC    --fixFit --verbose --Type2 >& AK8EtaHist2.txt &

python plotstack.py --hist AK8Tau21Hist  --allMC    --fixFit --verbose --Type2  >& AK8Tau21Hist2.txt &

python plotstack.py --hist AK8Tau32Hist  --allMC    --fixFit --verbose --Type2 >& AK8Tau32Hist2.txt &

python plotstack.py --hist AK8MHist --allMC    --fixFit --verbose --Type2 >& AK8MHist2.txt &

python plotstack.py --hist AK8MSDSJ0Hist --allMC    --fixFit --verbose --Type2  >& AK8MSDSJ0Hist2.txt &

python plotstack.py --hist LeptonPtHist  --allMC    --fixFit --verbose --Type2  >& LeptonPtHist2.txt &

python plotstack.py --hist LeptonEtaHist --allMC    --fixFit --verbose --Type2 >& LeptonEtaHist2.txt &

python plotstack.py --hist METPtHist --allMC    --fixFit --verbose --Type2 >& METPtHist2.txt &
 
python plotstack.py --hist HTLepHist  --allMC    --fixFit --verbose --Type2  >& HTLepHist2.txt &

python plotstack.py --hist AK4BdiscHist --allMC    --fixFit --verbose --Type2 >& AK4BdiscHist2.txt &


python plotstack.py --hist AK8PtHist  --allMC    --fixFit --verbose --Type2 >& AK8PtHist2.txt &
python plotstack.py --hist AK8SDPtHist  --allMC    --fixFit --verbose  --Type2 >& AK8SDPtHist2.txt &
python plotstack.py --hist AK8PuppiSDPtHist  --allMC    --fixFit --verbose  --Type2 >& AK8PuppiSDPtHist2.txt &
python plotstack.py --hist AK8PuppiPtHist  --allMC    --fixFit --verbose --Type2   >& AK8PuppiPtHist2.txt &






