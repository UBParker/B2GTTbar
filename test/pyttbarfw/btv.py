#! /usr/bin/env python
import ROOT

# from within CMSSW:
ROOT.gSystem.Load('libCondFormatsBTauObjects') 
ROOT.gSystem.Load('libCondToolsBTau') 

# OR using standalone code:
#ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cpp+') 

# get the sf data loaded
calib = ROOT.BTagCalibration('csvv2_ichep', 'CSVv2_ichep.csv')

# making a std::vector<std::string>> in python is a bit awkward, 
# but works with root (needed to load other sys types):
v_sys = getattr(ROOT, 'vector<string>')()
v_sys.push_back('up')
v_sys.push_back('down')

# make a reader instance and load the sf data
reader = ROOT.BTagCalibrationReader(
    0,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
    "central",      # central systematic type
    v_sys,          # vector of other sys. types
)    
reader.load(
    calib, 
    0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
    "comb"      # measurement type
)
# reader.load(...)     # for FLAV_C
# reader.load(...)     # for FLAV_UDSG

# in your event loop
sf = reader.eval_auto_bounds(
    'central',      # systematic (here also 'up'/'down' possible)
    0,              # jet flavor
    1.2,            # eta
    31.             # pt
)
print sf
