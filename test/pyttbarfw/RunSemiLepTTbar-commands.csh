#type 2 

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_ttjets_b2gtreeV3.root --outfile ttjets_outfile_type2.root --Type2 >& ttjets_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/b2gtree_SingleMuon_Run2016BCD.root --outfile data_BCD_outfile_type2.root --Type2 >& dataBCD_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets1_b2gtreeV3_incomplete.root --outfile wjets1_outfile_type2.root --Type2  --ignoreTrig >& wjets1_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets2_b2gtreeV3.root --outfile wjets2_outfile_type2.root --Type2  --ignoreTrig >& wjets2_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets3_b2gtreeV3.root --outfile wjets3_outfile_type2.root --Type2  --ignoreTrig >& wjets3_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets4_b2gtreeV3.root --outfile wjets4_outfile_type2.root --Type2  --ignoreTrig >& wjets4_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets5_b2gtreeV3.root --outfile wjets5_outfile_type2.root --Type2  --ignoreTrig >& wjets5_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets6_b2gtreeV3_incomplete.root --outfile wjets6_outfile_type2.root --Type2  --ignoreTrig >& wjets6_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets7_b2gtreeV3.root --outfile wjets7_outfile_type2.root --Type2  --ignoreTrig >& wjets7_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_st1_b2gtreeV3_incomplete.root --outfile st1_outfile_type2.root --Type2  --ignoreTrig >& st1_incomplete_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_st2_b2gtreeV3.root --outfile st2_outfile_type2.root --Type2  --ignoreTrig >& st2_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_st3_b2gtreeV3.root --outfile st3_outfile_type2.root --Type2  --ignoreTrig >& st3_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_st4_b2gtreeV3.root --outfile st4_outfile_type2.root --Type2  --ignoreTrig >& st4_outfile_type2.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_st5_b2gtreeV3.root --outfile st5_outfile_type2.root --Type2  --ignoreTrig >& st5_outfile_type2.txt &

# QCD MC

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_1000to1400_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD5_outfile_type2.root --Type2  --ignoreTrig >& QCD5_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_1400to1800_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD6_outfile_type2.root --Type2  --ignoreTrig >& QCD6_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_1800to2400_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD7_outfile_type2.root --Type2  --ignoreTrig >& QCD7_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_2400to3200_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD8_outfile_type2.root --Type2  --ignoreTrig >& QCD8_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_300to470_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD1_outfile_type2.root --Type2  --ignoreTrig >& QCD1_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_3200toInf_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD9_outfile_type2.root --Type2  --ignoreTrig >& QCD9_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_470to600_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD2_outfile_type2.root --Type2  --ignoreTrig >& QCD2_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_600to800_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD3_outfile_type2.root --Type2  --ignoreTrig >& QCD3_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_800to1000_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD4_outfile_type2.root --Type2  --ignoreTrig >& QCD4_outfile_type1.txt &





# type 1

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_ttjets_b2gtreeV3.root --outfile ttjets_outfile_type1.root   >& ttjets_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/b2gtree_SingleMuon_Run2016BCD.root --outfile data_BCD_outfile_type1.root  >& dataBCD_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets1_b2gtreeV3_incomplete.root --outfile wjets1_outfile_type1.root  --ignoreTrig  >& wjets1_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets2_b2gtreeV3.root --outfile wjets2_outfile_type1.root  --ignoreTrig  >& wjets2_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets3_b2gtreeV3.root --outfile wjets3_outfile_type1.root  --ignoreTrig  >& wjets3_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets4_b2gtreeV3.root --outfile wjets4_outfile_type1.root  --ignoreTrig >& wjets4_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets5_b2gtreeV3.root --outfile wjets5_outfile_type1.root  --ignoreTrig  >& wjets5_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets6_b2gtreeV3_incomplete.root --outfile wjets6_outfile_type1.root  --ignoreTrig  >& wjets6_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_wjets7_b2gtreeV3.root --outfile wjets7_outfile_type1.root  --ignoreTrig  >& wjets7_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_st1_b2gtreeV3_incomplete.root --outfile st1_outfile_type1.root  --ignoreTrig >& st1_incomplete_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_st2_b2gtreeV3.root --outfile st2_outfile_type1.root  --ignoreTrig >& st2_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_st3_b2gtreeV3.root --outfile st3_outfile_type1.root  --ignoreTrig >& st3_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_st4_b2gtreeV3.root --outfile st4_outfile_type1.root --ignoreTrig >& st4_outfile_type1.txt &

python RunSemiLepTTbar.py --infile root://cmseos.fnal.gov//store/user/asparker/B2G2016/haddFiles/Puppi_st5_b2gtreeV3.root --outfile st5_outfile_type1.root  --ignoreTrig >& st5_outfile_type1.txt &

# QCD MC

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_1000to1400_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD5_outfile_type1.root  --ignoreTrig >& QCD5_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_1400to1800_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD6_outfile_type1.root  --ignoreTrig >& QCD6_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_1800to2400_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD7_outfile_type1.root  --ignoreTrig >& QCD7_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_2400to3200_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD8_outfile_type1.root  --ignoreTrig >& QCD8_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_300to470_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD1_outfile_type1.root  --ignoreTrig >& QCD1_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_3200toInf_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD9_outfile_type1.root  --ignoreTrig >& QCD9_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_470to600_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD2_outfile_type1.root  --ignoreTrig >& QCD2_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_600to800_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD3_outfile_type1.root  --ignoreTrig >& QCD3_outfile_type1.txt &

python RunSemiLepTTbar.py --infile  /uscmst1b_scratch/lpc1/lpcphys/jdolen/B2G2016/V3/b2gtree_QCD_Pt_800to1000_pythia8_RunIISpring16MiniAODv2_reHLT_V3.root  --outfile QCD4_outfile_type1.root  --ignoreTrig >& QCD4_outfile_type1.txt &




