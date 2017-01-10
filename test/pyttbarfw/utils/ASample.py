#! /usr/bin/env python

import ROOT
import array as array
ROOT.gStyle.SetOptTitle(0)

class ASample ():
    
    lumiFull = 0.0
    nTotalSamples = 0 

  
    #def NextStage():
         
    def __init__(self, isstage = None , isData = None, color= None, treename="", Outfile = "",  name = "", nameTag = "", iswhere = "", hist = ""):
        self.name = name
        self.nameTag = nameTag
        self.iswhere = iswhere
        self.hist = hist
        self.isstage = isstage
        self.isData = isData
        self.color = color
        self.treename = treename
        self.fileout = Outfile

        ASample.nTotalSamples += 1

    '''
    def fillCutFlow(self, Nevents, hCutFlow , isstage ) : #(hcutflow1stage, hCutFlowAllstages , thestage ) :
        # Define cut-flow histos for counting number of events passing
        
        stageBs = array.array('d',  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])

        nstageBs = len(stageBs) - 1

        CutFlowAllstages = []
        CutFlowAllstages_names = []   
         
        cutbin = hCutFlow.GetXaxis().FindBin(int(isstage))
        hCutFlow.SetBinContent(cutbin, Nevents ) 
        #ASample.CutFlowAllstages.append(ROOT.TH1F("hCutFlowAllstages"+ str(self.name) , " ;; Events passing cuts ", nstageBs, stageBs ))
        #ASample.CutFlowAllstages_names.append(str(self.name))
        return hCutFlow    
    '''
class DataSample (ASample):
    
    nDataSamples = 0    
    data_hists = []
    
    def GetDataHists():
        return data_hists
        
        
    def __init__(self, isstage = None, lumiSample = None, Outfile = None, name = "", nameTag = "", iswhere = "", hist = "") :
        ASample.__init__(self,  isstage, True ,  1 , "", Outfile , name , nameTag , iswhere , hist )
        self.lumiSample = lumiSample
        if self.lumiSample != None :
            ASample.lumiFull += self.lumiSample
            DataSample.nDataSamples += 1
        else:
            print( " ERROR: NO luminosity input for sample named {}".format( self.name) )
         
        datafile_list = [ROOT.TFile( self.iswhere + "/mudata_" + self.name  +"_" + self.nameTag  + ".root" ) ]
        # e.g.  mudata_Run2016B_Dec12_type1.root
        #print("TFile is {}".format(datafile_list[0]))
        #print( "Using file named : {}".format( self.iswhere + "/mudata_" + self.name  +"_" + self.nameTag  + ".root"))
        self.hdatat = datafile_list[0].Get(str(self.hist) + str(self.isstage))
        print( " Extracting histogram named {} : ".format( str(self.hist) + str(self.isstage) ))
        self.hdatat.Sumw2()
        self.hdatat.SetDirectory(0)
         
        DataSample.data_hists.append(self.hdatat)
 
        if DataSample.nDataSamples == 1 :
            #DataSample.__hAllData = self.hdatat.Clone("__hAllData")
            #DataSample.__hAllData.SetName("DataSample.__hAllData")
            binSizeData = self.hdatat.GetBinWidth(0)
            nbinsData = self.hdatat.GetSize()
            print("Bin size is {} and there are {} bins".format(binSizeData, nbinsData))
        if DataSample.nDataSamples > 1 :
            binSizeData = self.hdatat.GetBinWidth(0)
            nbinsData = self.hdatat.GetSize()
            print("Bin size is {} and there are {} bins".format(binSizeData, nbinsData))
            #DataSample.__hAllData = DataSample.__hAllData.Add(self.hdatat)   
                         
    def GetDataHist(self)  :  
        return self.hdatat
        
    @staticmethod
    def GetLumi () :
        return ASample.lumiFull

    @staticmethod
    def GetnDatasets () :
        return DataSample.nDataSamples 

    def ResetData (self) :
        ASample.lumiFull = 0.
        DataSample.nDataSamples = 0.   
        data_hists = []
        print("Reset data objects: Lumi {} /fb, ndatasamples {} ".format(ASample.lumiFull, DataSample.nDataSamples))
        return None
         
    '''    
    @staticmethod
    def GetAllDataHist()  :  
        #print( "The AllData histogram is the sum of {} data histos with total integrated luminosity of {} /fb ".format(DataSample.__nDataSamples , DataSample.__lumiFull))
        return DataSample.__hAllData
    '''                
class MCSample (ASample):
    ### Count number of MC samples
    nMCSamples = 0
        
    @staticmethod
    def GetnMCsamples () :
        return MCSample.nMCSamples     
            
    def GetMCHist( self ) :
        return self.hmc
        
    def ResetMC(self) :
        MCSample.nMCSamples = 0
        print("Reset nMCSamples = {} ".format(MCSample.nMCSamples))        
        return None 
        
    def __init__(self, isstage = None, Outfile = None, xs_list = None, nevents_list = None, color = None, mc_Colors = None, name = "", sampleName_list = "", nameTag = "", iswhere = "", hist = ""):
        ASample.__init__(self,  isstage, False , color , "", Outfile , name , nameTag , iswhere , hist )
        self.xs_list = xs_list
        self.nevents_list = nevents_list
        self.mc_Colors = mc_Colors
        self.sampleName_list = sampleName_list
        MCSample.nMCSamples += 1
        
        self.mcfile_list = []
        self.nfiles = len(self.xs_list)
        for imc in range( self.nfiles ) :
            self.mcfile = ROOT.TFile(  self.iswhere + '/'+ self.name + '_'  + self.sampleName_list[imc] + '_' + self.nameTag + '.root'  ) 
            #print("TFile is {}".format(self.mcfile))
            self.mcfile_list.append(self.mcfile)
            
        self.hmc = None 
        self.hmc_list = []
           
        self.hmc_stack = ROOT.THStack("hmc_stack", "hmc_stack")
        #self.hCutFlowmc = None
        self.scale_list = []
        self.fileout.cd()

        for ifile in range(len(self.mcfile_list)) :
            htemps = self.mcfile_list[ifile].Get(self.hist + str(self.isstage))
            scaleis = xs_list[ifile]     /  nevents_list[ifile]   * (ASample.lumiFull * 1000.) # *1000. since lumi is in /fb and others are in /pb
            print(str(self.name) + "scaleIs {}".format(scaleis))
            self.scale_list.append( scaleis)
            htemps.Scale( scaleis   )
            Nev = htemps.Integral()
            #self.hCutFlowAllstages =  self.fillCutFlow( Nev , self.hCutFlowAllstages , int(self.isstage) )
            self.hmc_list.append( htemps )
            htemps.SetFillColor( mc_Colors[ifile] )
            if ifile == 0 :
                self.hmc = htemps.Clone('hmc')
            else :
                self.hmc.Add( htemps )
            self.hmc_stack.Add( htemps )
        self.hmc.Sumw2()
        self.hmc.SetDirectory(0)
        self.hmc.SetName('hmc')
        self.hmc.SetFillColor( self.color )

        
       
        '''
        if MCSample.__nMCSamples == 1 :
            MCSample.__stackAllMC = ROOT.THStack("MCSample.__stackAllMC", "MCSample.__stackAllMC")
            MCSample.__stackAllMC.Add(self.hmc)         
            MCSample.__hmcAll = self.hmc.Clone('MCSample.__hmcAll')
        if MCSample.__nMCSamples > 1 :
            MCSample.__stackAllMC.Add(self.hmc)
            MCSample.__hmcAll.Add(self.hmc)         
        '''
