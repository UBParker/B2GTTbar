# pyttbarfw


##Recipe for running semi-leptonic ttbar selection (type1) on B2G2016 V4 TTrees:

###Data
```
python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/rappocc/B2GAnaFWFiles16Dec2016/singlemu_run2016B.root --outfile mudata_Run2016B_Jan4_type1.root >& mudata_Run2016B_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/rappocc/B2GAnaFWFiles16Dec2016/singlemu_run2016C.root --outfile mudata_Run2016C_Jan4_type1.root >& mudata_Run2016C_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/rappocc/B2GAnaFWFiles16Dec2016/singlemu_run2016D.root --outfile mudata_Run2016D_Jan4_type1.root >& mudata_Run2016D_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/rappocc/B2GAnaFWFiles16Dec2016/singlemu_run2016E.root --outfile mudata_Run2016E_Jan4_type1.root >& mudata_Run2016E_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/aparker/B2G2016/V4Trees/b2gtree_mudata_Run2016F-23Sep_all_V4.root --outfile mudata_Run2016F_Jan4_type1.root >& mudata_Run2016F_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/aparker/B2G2016/V4Trees/b2gtree_mudata_Run2016G-23Sep_all_V4.root --outfile mudata_Run2016G_Jan4_type1.root >& mudata_Run2016G_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/rappocc/B2GAnaFWFiles16Dec2016/singlemu_run2016H.root --outfile mudata_Run2016H_Jan4_type1.root >& mudata_Run2016H_Jan4_type1.txt &
```
#### MC

###### ttbar
```
python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_ttjets_b2gtreeV3.root --outfile ttjets__Jan4_type1.root >& ttjets_Jan4_type1.txt &
```
###### wjets
```
python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_100_V4.root --outfile wjets_100_Jan4_type1.root --ignoreTrig >& wjets100_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_200_V4.root --outfile wjets_200_Jan4_type1.root --ignoreTrig >& wjets200_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_400_V4.root --outfile wjets_400_Jan4_type1.root --ignoreTrig >& wjets400_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_600_V4.root --outfile wjets_600_Jan4_type1.root --ignoreTrig >& wjets600_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_800_V4.root --outfile wjets_800_Jan4_type1.root --ignoreTrig >& wjets800_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_1200_V4.root --outfile wjets_1200_Jan4_type1.root --ignoreTrig >& wjets1200_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_wjets_2500_V4.root --outfile wjets_2500_Jan4_type1.root --ignoreTrig >& wjets2500_Jan4_type1.txt &
```
######  ST
```
python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_ST_schannel_V4.root --outfile ST_schannel_Jan4_type1.root --ignoreTrig >& ST_schannel_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_ST_tW-top_V4.root --outfile ST_tW-top_Jan4_type1.root --ignoreTrig >& ST_tW-top_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_ST_tchannel-antitop_V4.root --outfile ST_tchannel-antitop_Jan4_type1.root --ignoreTrig >& ST_tchannel-antitop_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtreeV4_ST_t-channel_top_1of1.root --outfile ST_t-channel_top_Jan4_type1.root --ignoreTrig >& ST_t-channel_top_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtreeV4_ST_tW_antitop_1of1.root --outfile ST_tW_antitop_Jan4_type1.root --ignoreTrig >& ST_tW_antitop_Jan4_type1.txt &
```
##### QCD
```
python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht100_V4.root --outfile QCD_Ht100_Jan4_type1.root --ignoreTrig >& QCD_Ht100_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht200_V4.root --outfile QCD_Ht200_Jan4_type1.root --ignoreTrig >& QCD_Ht200_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht300_V4.root --outfile QCD_Ht300_Jan4_type1.root --ignoreTrig >& QCD_Ht300_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht500_V4.root --outfile QCD_Ht500_Jan4_type1.root --ignoreTrig >& QCD_Ht500_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht700_V4.root --outfile QCD_Ht700_Jan4_type1.root --ignoreTrig >& QCD_Ht700_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht1000_V4.root --outfile QCD_Ht1000_Jan4_type1.root --ignoreTrig >& QCD_Ht1000_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht1500_V4.root --outfile QCD_Ht1500_Jan4_type1.root --ignoreTrig >& QCD_Ht1500_Jan4_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/V4Trees/b2gtree_MC_QCD_Ht2000_V4.root --outfile QCD_Ht2000_Jan4_type1.root --ignoreTrig >& QCD_Ht2000_Jan4_type1.txt &
```

##Recipe for plotting files from above:

NOTE: B2GSelectionPlotter is written in python 3.4
main differences  2.7  -> 3.4 : 
- print “” -> print(“”)
- xrange() -> range()

```
python B2GSelectionPlotter.py 
```

