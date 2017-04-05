from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import os

config = config()
config.General.requestName = 'b2gtreeV5_SingleMuon_Run2016H_03Feb2017_ver3_v1_JSONfinal_JECisHV6_try2'
config.General.transferOutputs = True
config.General.transferLogs = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'run_B2GTTbarTreeMaker_data_Run2016H.py'
config.JobType.maxJobRuntimeMin = 2750
config.Data.inputDataset = '/SingleMuon/Run2016H-03Feb2017_ver3-v1/MINIAOD'
config.Data.inputDBS = 'global'
config.JobType.inputFiles = [
'PUweight_FinalJSON2016_PileupJSONFeb2017_Xsec69200nominal_MCRunIISummer16MiniAODv2_PUMoriond17.root',

os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L1FastJet_AK8PFchs.txt'     ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L2Relative_AK8PFchs.txt'    ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L3Absolute_AK8PFchs.txt'    ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L2L3Residual_AK8PFchs.txt'  ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_Uncertainty_AK8PFchs.txt'   ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L1FastJet_AK4PFchs.txt'     ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L2Relative_AK4PFchs.txt'    ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L3Absolute_AK4PFchs.txt'    ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L2L3Residual_AK4PFchs.txt'  ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_Uncertainty_AK4PFchs.txt'   ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L1FastJet_AK8PFPuppi.txt'   ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L2Relative_AK8PFPuppi.txt'  ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L3Absolute_AK8PFPuppi.txt'  ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L2L3Residual_AK8PFPuppi.txt',
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_Uncertainty_AK8PFPuppi.txt' ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L1FastJet_AK4PFPuppi.txt'   ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L2Relative_AK4PFPuppi.txt'  ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L3Absolute_AK4PFPuppi.txt'  ,
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_L2L3Residual_AK4PFPuppi.txt',
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016HV6_DATA/Summer16_23Sep2016HV6_DATA_Uncertainty_AK4PFPuppi.txt' ,

os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JRDatabase/textFiles/Spring16_25nsV10_MC/Spring16_25nsV10_MC_PtResolution_AK4PFchs.txt',
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JRDatabase/textFiles/Spring16_25nsV10_MC/Spring16_25nsV10_MC_PtResolution_AK8PFchs.txt',
os.environ['CMSSW_BASE'] + '/src/JMEAnalysis/JRDatabase/textFiles/Spring16_25nsV10_MC/Spring16_25nsV10_MC_SF_AK8PFchs.txt'

]
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 5
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
#config.Data.runRange
config.Data.outLFNDirBase = '/store/user/asparker/B2G2016/V5TTrees/'
config.Data.publication = False
config.Site.storageSite = 'T3_US_FNALLPC'
