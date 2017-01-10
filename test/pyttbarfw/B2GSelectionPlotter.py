#! /usr/bin/env python


## _________                _____.__                            __  .__               
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____  
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \ 
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/ 
import sys
import math
import array as array
#import CMS_lumi, tdrstyle

import ROOT
from optparse import OptionParser

from hist.titles import HistoTitles

from sample.info import *

from utils.ASample import ASample, DataSample , MCSample
#from utils.AScaleFactor import *
from utils.APlot import APlot

#from RunSemiLepTTbar import nstages ### Not importing since that code is in python 2.7 and this one is in python 3.4 

class B2GSelectionPlotter() : 
    '''
    This class uses as input the output histograms from the RunSemiLepTTbar class.
    It combines and scales the input hists and plots them in proper CMS PubCom format.
    '''
    def __init__(self,  argv, theStage, histo) :
            
        parser = OptionParser()
        '''
        parser.add_option('--hist', type='string', action='store',
                          dest='hist',
                          default = 'AK8MSDHist',
                          help='Hist string')
        '''
        parser.add_option('--nameTag', type='string', action='store',
                          dest='nameTag',
                          default = 'Jan4_type1',
                          help='nam of infiles e.g. agreewithSemilep_type1') # or type2
        '''                  
        parser.add_option('--allMC', action='store_true',
                          default=True,
                          dest='allMC',
                          help='Do you want to plot all MC? (or just ttjets)')
        '''
        parser.add_option('--rebinNum', type='float', action='store',
                          dest='rebinNum',
                          default = 10,
                          help='number to rebin the histograms by')

        parser.add_option('--Type2', action='store_true',
                          default=False,
                          dest='Type2',
                          help='Do you want to apply selection for type 2 tops as described in AN-16-215 ?')

        parser.add_option('--AllStages', action='store_true',
                          default=False,
                          dest='AllStages',
                          help='Plot all stages (for a given sample) on same canvas?')

        parser.add_option('--AllStagesSample', type='string', action='store',
                          dest='AllStagesSample',
                          default = 'data2', #'data1',# 'ttbar1', #'QCD1', #'st1', #'wjets1', #, #
                          help='AllStagesSample options ; data1, ttbar1, wjets1, st1 , QCD1')

        parser.add_option('--AllStagesLog', action='store_true',
                          default=True,
                          dest='AllStagesLog',
                          help='Plot all stages on log y scale?')

        parser.add_option('--fixFit', action='store_true',
                          default=False,
                          dest='fixFit',
                          help='Do you want to constrain the gaussian fit?')

        parser.add_option('--electrons', action='store_true',
                          default=False,
                          dest='electrons',
                          help='Do you want to add electron data to the plots???')
                          
        parser.add_option('--verbose', action='store_true',
                          default=False,
                          dest='verbose',
                          help='Do you want to print values of key variables?')

        (options, args) = parser.parse_args(sys.argv)
        argv = []

        #### nstages gives number of selection stages from RunSemiLepTTbar.py (can import the variable but then need to switch to python3 print syntax)
        self.istage = theStage #14
        
        
        ### Check which selection we are dealing with (type1 or type2)
        if (options.nameTag.find("type2")) == -1 :
            print( "These histograms are labeled as type1")
        else :
            print( "These histograms are labeled as type2")
            options.Type2 = True
                    

        ### Open output root file   (to store cut-flow histos, SF, JMR, JMS ) 

        self.theOutfile = ROOT.TFile( 'B2GSelectionPlotter_outfile_'+ histo + '_' + options.nameTag +'.root' , "RECREATE") 

        self.theOutfile.cd()
        
        objs = []

        ### Store the luminosity 
        self.lumi = 0.
        
        ### Get the data histogram which is the sum of all runs that has already been rebinned by options.rebinNum
        self.nDatasamples = 0        
        self.dataHist = self.GetDataHist(self.istage, options)
        #self.dataHist.Rebin(options.rebinNum)
        self.dataHist2 = self.dataHist.Clone('self.dataHist2')
        
        '''    
        Remember to define data samples BEFORE any MC.
        This is important since MC are scaled by lumi.
        '''
        ### Get (scaled and summed hists ) and rebin all MC histograms
        self.mcttbar = MCSample(self.istage , self.theOutfile, xs_ttbar, nev_ttbar , ROOT.kGreen + 2 , ttbar_colors, "ttjets" ,  ttbar_names, str(options.nameTag) , "sample", str(histo)  )
        self.hmcttbar = self.mcttbar.GetMCHist() 
        self.hmcttbar.Rebin(options.rebinNum ) 
        
        self.mcwjets = MCSample(self.istage, self.theOutfile, xs_wjets, nev_wjets , ROOT.kRed + 1 , wjets_colors, "wjets" , wjets_names, str(options.nameTag) , "sample", str(histo)  )
        self.hmcwjets = self.mcwjets.GetMCHist()
        self.hmcwjets.Rebin(options.rebinNum)
                                
        self.mcST = MCSample(self.istage, self.theOutfile, xs_ST , nev_ST  , ROOT.kCyan , ST_colors, "ST" ,  ST_names, str(options.nameTag) , "sample", str(histo)  )
        self.hmcST = self.mcST.GetMCHist()  
        self.hmcST.Rebin(options.rebinNum)
        
        self.mcQCD = MCSample(self.istage, self.theOutfile, xs_QCD, nev_QCD , ROOT.kYellow  , QCD_colors, "QCD" , QCD_names, str(options.nameTag) , "sample", str(histo)  )
        self.hmcQCD = self.mcQCD.GetMCHist()
        self.hmcQCD.Rebin(options.rebinNum)
        
        ### Check the number of MC samples
        self.nMCsamples = self.mcQCD.GetnMCsamples()
        
        ### Get a THStack of all MC sample types combined
        self.mcStack = self.GetMCStack()

        ### Get a histogram of all MC sample types combined for use in the ratio plot
        self.mcHist = self.GetAllMCHist()
        self.mcHist2 = self.mcHist.Clone('self.mcHist2')
        self.mcHist2.SetDirectory(0)
        
        ### Fill the cut-flow histograms after scaling 
        #Nevttbar = hmcttbar.Integral()
        #hCutFlowttbar =  ASample.fillCutFlow( Nevttbar , ASample.hCutFlowAllstagesttjets , int(istage) )
        ### TO-DO: Fill all cutflow histos 
        
        '''
        Fitting Time
        '''
        ### Set the min and max values for the gaussian fit
        
        if options.Type2 :
            minFit = 65.
            maxFit = 105.
        else :
            minFit = 55.
            maxFit = 115.     
            
        ### For type1 tops ,only fit the mass of AK8 soft drop subjet 0 
        if not options.Type2 :
            if ( histo.find("AK8MSDSJ0Pt")) == -1 :
                print( "Not fitting this histo.")
            else :
                ### Only fit the histos of SD mass of subjet 0 (binned by own Pt) of leading AK8 jet for type 1.
                if theStage >= (nstages-2) : 
                    ### Only fit the last 2 stages of selection.
                    #theIndex = iHisto - (options.nstages-2)
                    print( "NOW you must add the fitting")
                    
                    #AScaleFactor.FitGaussian(minFitData, maxfitData, fitter_data )
                    #fitter_data = GetGaussianFit()
                    
                    if options.verbose : print( "Fitting range for {0} ,istage {1}, is from {2:2.2f} to {3:2.2f} GeV for data and {2:2.2f} to {3:2.2f} GeV for MC".format(histo, istage, minFit, maxFit) )
                else :
                    print( "Not fitting this histo.")
        else : # if  options.Type2 
            print( "Fitting not yet configured for Type2 top quark candidates.")      

        if not options.AllStages :
            
            ### Set the maximum y axis increment with respect to the maximum y axis value
            self.y_max_scale = 4.2
            
            self.plot = APlot(theStage , self.y_max_scale, self.dataHist, self.dataHist2, self.mcHist, self.mcHist2, self.mcStack, self.hmcttbar, self.hmcwjets, self.hmcST, self.hmcQCD, histo, self.lumi)

            self.theCanvas = self.plot.GetPlotCanvas()
            
            self.theCanvas.Print("./plots/" + histo +'_Stage'+ str(self.istage) +'_'+options.nameTag +".pdf", "pdf")

            self.theOutfile.cd()


            #objs.append( [self.dataHist, self.hmcttbar, self.hmcwjets, self.hmcST, self.hmcQCD,  self.theCanvas, self.mcStack] ) #, leg] )

        else :   # if options.AllStages :
            print( "This section in progress.")

        self.mcQCD.ResetMC() 
        self.tempdata.ResetData()    
        
        self.close()
       
    def GetDataHist(self, istage, options):

        ### Histogram of data after adding up all runs
        self.hist_AllData = []

        ### Histograms from individual runs
        self.hists_Data = []
        
        self.hists_MuData = []
        self.hists_ElData = []

        self.runs = ["Run2016B", "Run2016C", "Run2016D", "Run2016E", "Run2016F", "Run2016G", "Run2016H"]

        ### Luminosity unit is inverse femtobarn
        self.runs_lumis_MuData = [5.888, 2.646, 4.353, 4.050, 3.157, 7.55, ( 8.633 + 0.217 ) ] 
        #self.runs_lumis_ElData = []  
              
        for irun, run in enumerate(self.runs):
            self.tempdata = DataSample( istage , self.runs_lumis_MuData[irun] , self.theOutfile, run, str(options.nameTag) , "sample", str(histo)  )
            if options.verbose : print("Getting histo {} from {} with lumi {} /fb".format(str(histo), run , self.runs_lumis_MuData[irun] ))
            temphist = self.tempdata.GetDataHist()
            self.hists_MuData.append(temphist)
            if irun == 0 :
                self.tempdatasum = temphist.Clone('self.tempdatasum')
                self.tempdatasum.SetDirectory(0)
            if irun > 0 :
                self.tempdatasum.Add(temphist) 
                
        ### Rebin the histogram to ensure sufficient number of events per bin
        self.tempdatasum.Rebin(options.rebinNum)          
        
        if not options.electrons :
            self.hists_Data = self.hists_MuData
            self.hist_AllData.append(self.tempdatasum)
        else: #if options.electrons :
            print("TO-DO: Fix the ASample class to handle electrons, now only allows muon data.")
            '''
            for irun, run in enumerate(self.runs):
                tempdata = DataSample( istage , runs_lumis_ElData[irun] , theOutfile, run, str(options.nameTag) , "sample", str(histo)  )
                temphist = tempdata.GetDataHist()
                hists_ElData.append(temphist)           
            hists_Data = hists_MuData.append(hists_ElData)
            '''
            
        ### Get the total luminosity of the samples above.      
        self.lumi = self.tempdata.GetLumi()
        self.nDatasamples = self.tempdata.GetnDatasets()
        
        if self.lumi <= 40. :
            print( "The combined luminosity of the {} data samples is {} /fb ".format(self.nDatasamples, self.lumi))
        else :
            print("ERROR: The combined luminosity is larger than it should be!")
        
        if self.nDatasamples != 7: print("ERROR: There are {}, rather than 7, datasets (B, C, D, E, F, G, H), something is wrong!".format(self.nDatasamples))    
            
        return self.hist_AllData[0]
    
        
                
    def GetMCStack(self) :  
        ### THStack of all MC sample types
        self.stack_AllMC = ROOT.THStack("self.stack_AllMC", "self.stack_AllMC")

        self.stack_AllMC.Add( self.hmcttbar )        
        self.stack_AllMC.Add( self.hmcwjets )  
        self.stack_AllMC.Add( self.hmcST ) 
        self.stack_AllMC.Add( self.hmcQCD ) 

        if self.nMCsamples != 4:
            print("ERROR: There are {}, rather than 4, MC sample types (ttbar, wjets, ST, QCD), something is wrong!".format(self.nMCsamples))
        else :  
            print("There are {} MC samples being added to the MCStack.".format(self.nMCsamples))
                
    
        return self.stack_AllMC

    def GetAllMCHist(self) : 
        ### Histogram of MC after adding up all sample types
        self.hist_AllMC = []

        ### Histograms from individual sample types
        
        self.hists_MC = []
        self.hists_MC_names = ["ttjets", "wjets", "ST", "QCD"]

        #Scale ttbar MC by ratio of integrals of data MC
        #hmcttbar = ScalettMC(httbar, hdata, hMC ,  xAxisrange[iHisto][0] , xAxisrange[iHisto][1] )    
        self.hists_MC.append( self.hmcttbar )
        self.hist_AllMC.append( self.hmcttbar.Clone() )
        self.hist_AllMC[0].SetName('histofAllMC')
        self.hist_AllMC[0].SetDirectory(0)
        
        self.hists_MC.append( self.hmcwjets )
        self.hist_AllMC[0].Add( self.hmcwjets )
        
        self.hists_MC.append( self.hmcST )
        self.hist_AllMC[0].Add( self.hmcST ) 
        
        self.hists_MC.append( self.hmcQCD )
        self.hist_AllMC[0].Add( self.hmcQCD ) 

        if self.nMCsamples != 4:
            print("ERROR: There are {}, rather than 4, MC sample types (ttbar, wjets, ST, QCD), something is wrong!".format(self.nMCsamples))
        else :  
            print("There are {} MC samples being added to the all MC histogram.".format(self.nMCsamples))
        
        return self.hist_AllMC[0]    

    def close( self ) :
        self.theOutfile.cd() 
        self.theOutfile.Write()
        self.theOutfile.Close()

if __name__ == "__main__" :
    nstages = 17
    for histo in HistoTitles :
        for theStage in range(0, nstages):
            B2GSelectionPlotter(sys.argv, theStage, histo)
