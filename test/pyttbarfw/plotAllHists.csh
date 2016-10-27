#type 1


python plotstack.py --hist AK8MSDHist --allMC --includeQCD --ttSF --fixFit --verbose >& AK8MSDHist.txt &

python plotstack.py --hist AK8PtHist  --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8PtHist.txt &

python plotstack.py --hist AK8EtaHist  --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8EtaHist.txt &

python plotstack.py --hist AK8puppitau21Hist  --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8Tau21Hist.txt &

python plotstack.py --hist AK8puppitau32Hist  --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8Tau32Hist.txt &

python plotstack.py --hist AK8MHist --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8MHist.txt &

python plotstack.py --hist AK8MSDSJ0Hist --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8MSDSJ0Hist.txt &

python plotstack.py --hist LeptonPtHist  --allMC --includeQCD --ttSF --fixFit --verbose  >& LeptonPtHist.txt &

python plotstack.py --hist LeptonEtaHist --allMC --includeQCD --ttSF --fixFit --verbose  >& LeptonEtaHist.txt &

python plotstack.py --hist METPtHist --allMC --includeQCD --ttSF --fixFit --verbose  >& METPtHist.txt &
 
python plotstack.py --hist HTLepHist  --allMC --includeQCD --ttSF --fixFit --verbose  >& HTLepHist.txt &

python plotstack.py --hist AK4BdiscHist --allMC --includeQCD --ttSF --fixFit --verbose  >& AK4BdiscHist.txt &


python plotstack.py --hist AK8MSDSJ0Pt200To300Hist --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8MSDSJ0Pt200To300Hist.txt &
python plotstack.py --hist AK8MSDSJ0Pt300To400Hist --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8MSDSJ0Pt300To400Hist.txt &
python plotstack.py --hist AK8MSDSJ0Pt400To500Hist --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8MSDSJ0Pt400To500Hist.txt &
python plotstack.py --hist AK8MSDSJ0Pt500To800Hist --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8MSDSJ0Pt500To600Hist.txt &

python plotstack.py --hist AK8PtHist  --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8PtHist.txt &
python plotstack.py --hist AK8SDPtHist  --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8SDPtHist.txt &
python plotstack.py --hist AK8PuppiSDPtHist  --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8PuppiSDPtHist.txt &
python plotstack.py --hist AK8PuppiPtHist  --allMC --includeQCD --ttSF --fixFit --verbose  >& AK8PuppiPtHist.txt &

#type 2


python plotstack.py --hist AK8MSDHist --allMC --includeQCD --ttSF --fixFit --verbose --Type2 >& AK8MSDHist2.txt &

python plotstack.py --hist AK8PtHist  --allMC --includeQCD --ttSF --fixFit --verbose --Type2 >& AK8PtHist2.txt &

python plotstack.py --hist AK8EtaHist  --allMC --includeQCD --ttSF --fixFit --verbose --Type2 >& AK8EtaHist2.txt &

python plotstack.py --hist AK8puppitau21Hist  --allMC --includeQCD --ttSF --fixFit --verbose --Type2  >& AK8Tau21Hist2.txt &

python plotstack.py --hist AK8puppitau32Hist  --allMC --includeQCD --ttSF --fixFit --verbose --Type2 >& AK8Tau32Hist2.txt &

python plotstack.py --hist AK8MHist --allMC --includeQCD --ttSF --fixFit --verbose --Type2 >& AK8MHist2.txt &

python plotstack.py --hist AK8MSDSJ0Hist --allMC --includeQCD --ttSF --fixFit --verbose --Type2  >& AK8MSDSJ0Hist2.txt &

python plotstack.py --hist LeptonPtHist  --allMC --includeQCD --ttSF --fixFit --verbose --Type2  >& LeptonPtHist2.txt &

python plotstack.py --hist LeptonEtaHist --allMC --includeQCD --ttSF --fixFit --verbose --Type2 >& LeptonEtaHist2.txt &

python plotstack.py --hist METPtHist --allMC --includeQCD --ttSF --fixFit --verbose --Type2 >& METPtHist2.txt &
 
python plotstack.py --hist HTLepHist  --allMC --includeQCD --ttSF --fixFit --verbose --Type2  >& HTLepHist2.txt &

python plotstack.py --hist AK4BdiscHist --allMC --includeQCD --ttSF --fixFit --verbose --Type2 >& AK4BdiscHist2.txt &


python plotstack.py --hist AK8PtHist  --allMC --includeQCD --ttSF --fixFit --verbose --Type2 >& AK8PtHist2.txt &
python plotstack.py --hist AK8SDPtHist  --allMC --includeQCD --ttSF --fixFit --verbose  --Type2 >& AK8SDPtHist2.txt &
python plotstack.py --hist AK8PuppiSDPtHist  --allMC --includeQCD --ttSF --fixFit --verbose  --Type2 >& AK8PuppiSDPtHist2.txt &
python plotstack.py --hist AK8PuppiPtHist  --allMC --includeQCD --ttSF --fixFit --verbose --Type2   >& AK8PuppiPtHist2.txt &










'''
TO-DO : Add commands for the following after implementing them in plotstack.py
       LeptonEtaHist
            self.AK8MPt200To300Hist
            self.AK8MSDPt200To300Hist

            self.AK8MPt300To400Hist
            self.AK8MSDPt300To400Hist

            self.AK8MPt400To500Hist
            self.AK8MSDPt400To500Hist
            self.AK8MPt500To600Hist
            self.AK8MSDPt500To600Hist

            self.AK8MPt600To800Hist
            self.AK8MSDPt600To800Hist
            self.AK8MSDSJ0Pt600To800Hist
python plotstack.py --hist Iso2DHist # TO-DO : Fix plotter to work with TH2F


'''
