from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'QCDAnaTrees_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_noTrigger'
config.General.workArea = 'QCDAnaRunII'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.inputFiles = ['FrameworkJobReport.xml', 'execute_for_crab_qcd.py', 'NtupleReader_fwlite.py', 'leptonic_nu_z_component.py', 'JECs', 'ModMass_2015_09_22.root', 'MistagRate_2015_09_25.root', 'pileup_reweight.root']
config.JobType.outputFiles = ['outplots.root']
config.JobType.scriptExe = 'execute_for_crab_qcd.sh'

config.section_("Data")
config.Data.inputDataset = '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/decosa-QCD_HT300to500-50153fb607659b6f9fb41d9f35391d0e/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.Data.ignoreLocality = True
config.Data.publication = False
# This string is used to construct the output dataset name

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
#config.Site.whitelist = ["T2_HU_Budapest"]
