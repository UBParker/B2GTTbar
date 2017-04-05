# Run2016G data cfg for crab submission of B2GTTbarTreeMaker

import FWCore.ParameterSet.Config as cms

process = cms.Process("Ana")

#----------------------------------------------------------------------------------------
### SETUP
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = '80X_dataRun2_2016SeptRepro_v7' 
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.options.allowUnscheduled = cms.untracked.bool(True)

isMC   = False

#----------------------------------------------------------------------------------------
### INPUT
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 5000

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      'file:root://cmsxrootd.fnal.gov///store/data/Run2016H/SingleMuon/MINIAOD/03Feb2017_ver2-v1/110000/008BE852-89EA-E611-A265-001E67396AEA.root',
      'file:root://cmsxrootd.fnal.gov////store/data/Run2016H/SingleMuon/MINIAOD/03Feb2017_ver2-v1/110000/009A586B-A6EA-E611-B612-001E674FD1DD.root',

    )
)

#----------------------------------------------------------------------------------------
### MET Filters
process.load('RecoMET.METFilters.BadChargedCandidateFilter_cfi')
process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")
process.BadChargedCandidateFilter.debug = cms.bool(False)
process.BadPFMuonFilter.muons = cms.InputTag("slimmedMuons")
process.BadPFMuonFilter.PFCandidates = cms.InputTag("packedPFCandidates")
process.BadPFMuonFilter.debug = cms.bool(False)


#----------------------------------------------------------------------------------------
### VID
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
dataFormat = DataFormat.MiniAOD
switchOnVIDElectronIdProducer(process, dataFormat)
my_id_modules = [
    'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronHLTPreselecition_Summer16_V1_cff',
    'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff',
    'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV70_cff'
]

for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

#----------------------------------------------------------------------------------------
### MET   //https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

# If you only want to re-correct and get the proper uncertainties
runMetCorAndUncFromMiniAOD(process,
                       isData=not isMC,
                       )

# If you would like to re-cluster and get the proper uncertainties
# runMetCorAndUncFromMiniAOD(process,
#                        isData=True (or False),
#                        pfCandColl=cms.InputTag("packedPFCandidates"),
#                        recoMetFromPFCs=True,
#                        )



#----------------------------------------------------------------------------------------
### Puppi (https://twiki.cern.ch/twiki/bin/viewauth/CMS/PUPPI)
process.load('CommonTools/PileupAlgos/Puppi_cff')
process.puppi.candName = cms.InputTag('packedPFCandidates')
process.puppi.vertexName = cms.InputTag('offlineSlimmedPrimaryVertices')
process.puppi.useExistingWeights = cms.bool(True)
process.puppiOnTheFly = process.puppi.clone()
process.puppiOnTheFly.useExistingWeights = True

#----------------------------------------------------------------------------------------
### Toolbox (https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetToolbox)
from JMEAnalysis.JetToolbox.jetToolbox_cff import jetToolbox

ak8Cut    = 'pt > 30 && abs(eta) < 2.5'
ak8pupCut = 'pt > 140 && abs(eta) < 2.5'


listBTagInfos = [
     'pfInclusiveSecondaryVertexFinderTagInfos',
]
listBtagDiscriminatorsAK8 = [ 
    # 'pfJetProbabilityBJetTags',
    'pfCombinedInclusiveSecondaryVertexV2BJetTags',
    # 'pfCombinedMVAV2BJetTags',
    # 'pfCombinedCvsLJetTags',
    # 'pfCombinedCvsBJetTags',
    # 'pfBoostedDoubleSecondaryVertexAK8BJetTags',
    # 'pfBoostedDoubleSecondaryVertexCA15BJetTags',
]

# |---- jetToolBox: JETTOOLBOX RUNNING ON MiniAOD FOR AK8 JETS USING CHS
# |---- jetToolBox: Applying this corrections: ('AK8PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')
# |---- jetToolBox: Running ak8PFJetsCHSSoftDropMass, selectedPatJetsAK8PFCHSSoftDropPacked, selectedPatJetsAK8PFCHSSoftDropSubjets, ak8PFJetsCHSPrunedMass, ak8PFJetsCHSTrimmedMass, ak8PFJetsCHSFilteredMass, NjettinessAK8CHS, NsubjettinessAK8PFCHSSoftDropSubjets.
# |---- jetToolBox: Creating selectedPatJetsAK8PFCHS collection.
# vector<pat::Jet>                      "selectedPatJetsAK8PFCHS"   ""               "Ana"     
# vector<pat::Jet>                      "selectedPatJetsAK8PFCHSSoftDropPacked"   ""               "Ana"     
# vector<pat::Jet>                      "selectedPatJetsAK8PFCHSSoftDropPacked"   "SubJets"        "Ana"     
# vector<reco::GenJet>                  "selectedPatJetsAK8PFCHS"   "genJets"        "Ana"     
# vector<reco::PFCandidate>             "selectedPatJetsAK8PFCHS"   "pfCandidates"   "Ana"    

jetToolbox( process, 'ak8', 'ak8JetSubs', 'out', 
  runOnMC = isMC, 
  PUMethod='CHS', 
  JETCorrLevels = [ 'None' ],
  subJETCorrLevels = [ 'None' ],
  addSoftDropSubjets = True, 
  addTrimming = True, rFiltTrim=0.2, ptFrac=0.05,
  addPruning = True, 
  addFiltering = True, 
  addSoftDrop = True, 
  addNsub = True, 
  bTagInfos = listBTagInfos, 
  bTagDiscriminators = listBtagDiscriminatorsAK8, 
  addCMSTopTagger = False, 
  Cut = ak8Cut , 
  addNsubSubjets = True, 
  subjetMaxTau = 3 )


# |---- jetToolBox: JETTOOLBOX RUNNING ON MiniAOD FOR AK8 JETS USING Puppi
# |---- jetToolBox: Applying this corrections: ('AK8PFPuppi', ['L2Relative', 'L3Absolute'], 'None')
# |---- jetToolBox: Running ak8PFJetsPuppiSoftDropMass, selectedPatJetsAK8PFPuppiSoftDropPacked, selectedPatJetsAK8PFPuppiSoftDropSubjets, ak8PFJetsPuppiPrunedMass, ak8PFJetsPuppiTrimmedMass, ak8PFJetsPuppiFilteredMass, NjettinessAK8Puppi, NsubjettinessAK8PFPuppiSoftDropSubjets.
# |---- jetToolBox: Creating selectedPatJetsAK8PFPuppi collection.
# vector<pat::Jet>                      "selectedPatJetsAK8PFPuppi"   ""               "Ana"     
# vector<pat::Jet>                      "selectedPatJetsAK8PFPuppiSoftDropPacked"   ""               "Ana"  
# vector<pat::Jet>                      "selectedPatJetsAK8PFPuppiSoftDropPacked"   "SubJets"        "Ana"     
# vector<reco::GenJet>                  "selectedPatJetsAK8PFPuppi"   "genJets"        "Ana"     
# vector<reco::PFCandidate>             "selectedPatJetsAK8PFPuppi"   "pfCandidates"   "Ana"     


jetToolbox( process, 'ak8', 'ak8JetSubs', 'out', 
  runOnMC = isMC, 
  newPFCollection=True, 
  nameNewPFCollection='puppiOnTheFly',
  PUMethod='Puppi', 
  JETCorrLevels = [ 'None' ],
  subJETCorrLevels = [ 'None' ],
  addSoftDropSubjets = True, 
  addTrimming = True,  rFiltTrim=0.2, ptFrac=0.05,
  addPruning = True, 
  addFiltering = True, 
  addSoftDrop = True, 
  addNsub = True, 
  bTagInfos = listBTagInfos, 
  bTagDiscriminators = listBtagDiscriminatorsAK8, 
  addCMSTopTagger = False, 
  Cut = ak8pupCut , 
  addNsubSubjets = True, 
  subjetMaxTau = 3 )

#----------------------------------------------------------------------------------------
### Analyzer

## LOCAL RUNNING
# JECtxtlocation = '../../../JMEAnalysis/JECDatabase/textFiles/Summer16_23Sep2016GV3_DATA/'
# JERtxtlocation = '../../../JMEAnalysis/JRDatabase/textFiles/Spring16_25nsV6_DATA/'
## CRAB SUBMIT
JECtxtlocation=''
JERtxtlocation=''

# Note: JER text files exist for multiple jet collections but at the moment they use the same numbers

process.ana = cms.EDAnalyzer('B2GTTbarTreeMaker',
   
    verbose              = cms.bool(False),
    verboseGen           = cms.bool(False),
    useToolbox           = cms.bool(True),

    runGenLoop           = cms.bool(False),
    runAllHadTree        = cms.bool(True),
    runSemiLeptTree      = cms.bool(True),

    isZprime             = cms.bool(False),
    isttbar              = cms.bool(False),
    isRSG                = cms.bool(False),
    isRun2016F           = cms.bool(False),

    ak8chsInput          = cms.InputTag("selectedPatJetsAK8PFCHS"),   
    ak8puppiInput        = cms.InputTag("selectedPatJetsAK8PFPuppi"),
    ak8chsSubjetsInput   = cms.InputTag("selectedPatJetsAK8PFCHSSoftDropPacked","SubJets"),
    ak8puppiSubjetsInput = cms.InputTag("selectedPatJetsAK8PFPuppiSoftDropPacked","SubJets"),
    triggerBits          = cms.InputTag("TriggerResults", "", "HLT"),
    lheSrc               = cms.InputTag("externalLHEProducer", "", "LHE"),
    eleIdFullInfoMapToken_HLTpre  = cms.InputTag("egmGsfElectronIDs:cutBasedElectronHLTPreselection-Summer16-V1"),
    eleIdFullInfoMapToken_Loose   = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose"),
    eleIdFullInfoMapToken_Medium  = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium"),
    eleIdFullInfoMapToken_Tight   = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight"),
    eleIdFullInfoMapToken_HEEP    = cms.InputTag("egmGsfElectronIDs:heepElectronID-HEEPV70"), 
    jecPayloadsAK8chs = cms.vstring([
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L1FastJet_AK8PFchs.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L2Relative_AK8PFchs.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L3Absolute_AK8PFchs.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L2L3Residual_AK8PFchs.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_Uncertainty_AK8PFchs.txt'
                                    ]),
    jecPayloadsAK4chs = cms.vstring([
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L1FastJet_AK4PFchs.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L2Relative_AK4PFchs.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L3Absolute_AK4PFchs.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L2L3Residual_AK4PFchs.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_Uncertainty_AK4PFchs.txt'
                                    ]),
    jecPayloadsAK8pup = cms.vstring([
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L1FastJet_AK8PFPuppi.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L2Relative_AK8PFPuppi.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L3Absolute_AK8PFPuppi.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L2L3Residual_AK8PFPuppi.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_Uncertainty_AK8PFPuppi.txt'
                                    ]),
    jecPayloadsAK4pup = cms.vstring([
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L1FastJet_AK4PFPuppi.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L2Relative_AK4PFPuppi.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L3Absolute_AK4PFPuppi.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_L2L3Residual_AK4PFPuppi.txt',
                                    JECtxtlocation+'Summer16_23Sep2016HV4_DATA_Uncertainty_AK4PFPuppi.txt'
                                    ]),

    jecPayloadsAK8chsSecondary = cms.vstring([
                                    '',
                                    '',
                                    '',
                                    '',
                                    ''
                                    ]),
    jecPayloadsAK4chsSecondary = cms.vstring([
                                    '',
                                    '',
                                    '',
                                    '',
                                    ''
                                    ]),
    jecPayloadsAK8pupSecondary = cms.vstring([
                                    '',
                                    '',
                                    '',
                                    '',
                                    ''
                                    ]),
    jecPayloadsAK4pupSecondary = cms.vstring([
                                    '',
                                    '',
                                    '',
                                    '',
                                    ''
                                    ]),

    jertextAK4        = cms.string(JERtxtlocation+'Spring16_25nsV10_MC_PtResolution_AK4PFchs.txt'),    # no specific data txt for 25nsV10 but this will be updated soon                        
    jertextAK8        = cms.string(JERtxtlocation+'Spring16_25nsV10_MC_PtResolution_AK8PFchs.txt'),    # no specific data txt for 25nsV10 but this will be updated soon                        
    jerSFtext         = cms.string(JERtxtlocation+'Spring16_25nsV10_MC_SF_AK8PFchs.txt')               # no specific data txt for 25nsV10 but this will be updated soon             
 
)


#----------------------------------------------------------------------------------------
### Out

# If you want to output the newly recoconstruted jets
# process.out = cms.OutputModule(
#     "PoolOutputModule",
#     fileName = cms.untracked.string('tool.root'),
#     outputCommands = cms.untracked.vstring(
#       "keep *_selectedPatJetsAK8PFCHS_*_*",
#       "keep *_selectedPatJetsAK8PFCHSSoftDropPacked_*_*",
#       "keep *_selectedPatJetsAK8PFPuppi_*_*",
#       "keep *_selectedPatJetsAK8PFPuppiSoftDropPacked_*_*"
#       )
#     )
# process.endpath = cms.EndPath(process.out) 

process.SimpleMemoryCheck=cms.Service("SimpleMemoryCheck",
                                   ignoreTotal=cms.untracked.int32(1), #->start logging event N
                                   oncePerEventMode=cms.untracked.bool(False), # true->report every event, false->report only high memory events 
                                   moduleMemorySummary=cms.untracked.bool(True),
                                   monitorPssAndPrivate=cms.untracked.bool(False)

)

process.TFileService = cms.Service("TFileService",
      fileName = cms.string("b2gtreeV5_dataH.root"),
      closeFileFast = cms.untracked.bool(True)
  )

process.p = cms.Path(
  process.BadChargedCandidateFilter*
  process.BadPFMuonFilter*
  process.egmGsfElectronIDSequence*
  process.fullPatMetSequence *
  process.ana
)

