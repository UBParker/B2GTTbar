import ROOT
import math 
import array as array
from utils.HistoTitles import HistoTitles
import tdrstyle

class APlot () :
    
    def __init__(self, isstage = None , y_max = None, histofAlldata = None, histofAlldata2 = None, histofAllMC = None, histofAllMC2 = None, mcStack = None, httbar = None, hwjets = None, hST = None, hQCD = None, histoName = None, lumi = None, tagg = None, cuttag = None, fixFit = None, expectedRuns = None, otherttbar = None, fitValues = None, fitDiffs = None, passPretag = None, passPretagUncert = None, typeis = None) :
        self.isstage = isstage
        self.y_max = y_max
        self.histofAlldata = histofAlldata
        self.histofAlldata2 = histofAlldata2

        self.histofAllMC = histofAllMC
        self.histofAllMC2 = histofAllMC2
        self.mcStack = mcStack
        self.httbar = httbar
        self.hwjets = hwjets
        self.hST = hST
        self.hQCD = hQCD
        self.histoName = histoName
        self.lumi = lumi
        self.otherttbar = otherttbar

        self.tagg = tagg
        self.cuttag = cuttag
        self.fixFit = fixFit
        self.expectedRuns = expectedRuns
        self.fitValues = fitValues
        self.fitDiffs = fitDiffs
        self.passPretag = passPretag
        self.passPretagUncert = passPretagUncert
        self.typeis =  typeis
        
        self.isWmass = False
        self.isTopmass = False
        self.dontFit = True
        self.fixFit = False
        self.SF = -1.
        self.SF_sd = -1.
        self.MCeff = -1.
        self.Dataeff = -1.
        self.jms =    [0., 0.]
        self.jmr =    [0., 0.]
        self.scaleW = [0., 0.]
        #self.passPosttag = []
        #self.passPosttagUncert = []
        self.ptBs =  array.array('d', [200., 300., 400., 500., 800., 900., 1000.,1100.])
        self.nptBs = len(self.ptBs) - 1
        if self.isstage >=11 :
            self.hpeak = ROOT.TH1F("hpeak", " ;p_{T} of SD subjet 0 (GeV); JMS ",  self.nptBs, self.ptBs) 
            self.hwidth = ROOT.TH1F("hwidth", " ;p_{T} of SD subjet 0 (GeV); JMR ", self.nptBs, self.ptBs)
            self.hNpassDataPre  = ROOT.TH1F("hNpassDataPre", " ;p_{T} of SD subjet 0 (GeV); # Integral(mean+- sigma) pre tag ", self.nptBs, self.ptBs)
            self.hNpassDataPost  = ROOT.TH1F("hNpassDataPost", " ;p_{T} of SD subjet 0 (GeV); # Integral(mean+- sigma) post tag ", self.nptBs, self.ptBs)
            self.hNpassMCPre  = ROOT.TH1F("hNpassMCPre", " ;p_{T} of SD subjet 0 (GeV); # Integral(mean+- sigma) pre tag ", self.nptBs, self.ptBs)
            self.hNpassMCPost  = ROOT.TH1F("hNpassMCPost", " ;p_{T} of SD subjet 0 (GeV); # Integral(mean+- sigma) post tag ", self.nptBs, self.ptBs)
            self.hSFs  = ROOT.TH1F("hSFs", " ;p_{T} of SD subjet 0 (GeV); # data/mc [Integral(mean+- sigma) post/pre ", self.nptBs, self.ptBs)


        ROOT.gStyle.SetOptStat(000000)
        self.c1 = ROOT.TCanvas("c" + str(self.isstage), "c" + str(self.isstage),1,1,745,701)
        self.c1.SetHighLightColor(2)
        self.c1.Range(0,0,1,1)
        self.c1.SetFillColor(0)
        self.c1.SetBorderMode(0)
        self.c1.SetBorderSize(2)
        self.c1.SetTickx(1)
        self.c1.SetTicky(1)
        self.c1.SetLeftMargin(0.14)
        self.c1.SetRightMargin(0.04)
        self.c1.SetTopMargin(0.08)
        self.c1.SetBottomMargin(0.15)
        self.c1.SetFrameFillStyle(0)
        self.c1.SetFrameBorderMode(0)
        
        self.pad1 = ROOT.TPad("pad" + str(self.isstage), "pad" + str(self.isstage),0,0.3333333,1,1)
        self.pad1.Draw()
        self.pad1.cd()
        #self.pad2.Range(-0.1792683,-1.370091,1.10122,1.899)
        self.pad1.SetFillColor(0)
        self.pad1.SetBorderMode(0)
        self.pad1.SetBorderSize(2)
        self.pad1.SetTickx(1)
        self.pad1.SetTicky(1)
        self.pad1.SetLeftMargin(0.14)
        self.pad1.SetRightMargin(0.04)
        self.pad1.SetTopMargin(0.12)
        self.pad1.SetBottomMargin(0.01)
        self.pad1.SetFrameFillStyle(0)
        self.pad1.SetFrameBorderMode(0)
       

        HistoTitle = HistoTitles[self.histoName][0]
        rangeMin = HistoTitles[self.histoName][1]
        rangeMax = HistoTitles[self.histoName][2]
        print("X axis range is {} to {}".format(rangeMin, rangeMax))
        self.histofAlldata.GetXaxis().SetRangeUser( rangeMin, rangeMax )
        self.histofAlldata.SetMaximum(self.y_max * self.histofAlldata.GetMaximum() )
        self.histofAlldata.SetMinimum(0.0001 )
        self.histofAlldata.GetYaxis().SetTitle("Events")
        self.histofAlldata.GetYaxis().SetTitleSize(0.065)
        self.histofAlldata.GetYaxis().SetTitleOffset(0.9) ## 0.7)
        self.histofAlldata.GetYaxis().SetLabelSize(0.04)
        self.histofAlldata.SetLineColor(1)
        self.histofAlldata.SetFillColor(1)
        self.histofAlldata.SetFillStyle(0)
        self.histofAlldata.SetLineWidth(2)
        self.histofAlldata.SetMarkerStyle(20)
        self.histofAlldata.SetMarkerSize(0.8)
        self.histofAlldata.SetMarkerColor(1)


        self.histofAlldata.GetXaxis().SetNdivisions(506)
        self.histofAlldata.GetXaxis().SetLabelFont(42)
        self.histofAlldata.GetXaxis().SetLabelSize(0.5)
        self.histofAlldata.GetXaxis().SetTitleSize(0.0475)
        self.histofAlldata.GetXaxis().SetTickLength(0.045)
        self.histofAlldata.GetXaxis().SetTitleOffset(1.15)
        self.histofAlldata.GetXaxis().SetTitleFont(42)
        self.histofAlldata.GetXaxis().SetTitle("")

        self.histofAlldata.GetYaxis().SetTitle("Events")
        self.histofAlldata.GetYaxis().SetNdivisions(506)
        self.histofAlldata.GetYaxis().SetLabelFont(42)
        self.histofAlldata.GetYaxis().SetLabelSize(0.06375)
        self.histofAlldata.GetYaxis().SetTitleSize(0.06225)
        self.histofAlldata.GetYaxis().SetTitleOffset(0.9)
        self.histofAlldata.GetYaxis().SetTitleFont(42)
        #self.histofAlldata.SetXTitle(HistoTitle +" , Stage "+str(self.isstage))

        self.fitter_mc = None
        self.fitter_data = None

        self.histofAlldata.Draw("e x0")
        
        if self.expectedRuns != None :
            self.expectedRuns.SetMarkerStyle(20)
            self.expectedRuns.SetMarkerSize(0.8)
            self.expectedRuns.SetMarkerColor(6)
            self.expectedRuns.GetXaxis().SetRangeUser( rangeMin, rangeMax )
            self.expectedRuns.Draw("same")
        else:    
            self.histofAllMC.GetXaxis().SetRangeUser( rangeMin, rangeMax )          
            self.histofAllMC.SetFillStyle(3144)#3019)
            self.histofAllMC.SetFillColor(ROOT.kGray+1)
            self.histofAllMC.Draw("E2 same")
            self.mcStack.Draw("hist same")
            self.histofAlldata.Draw("e x0 same")
        self.minn = 0.
        self.maxx = 0.     
        rangenum = 17
        if self.typeis: rangenum = 15
        #fittingLimits = [ [minAvg, minAvg, minAvg, minAvg, minAvg, minAvg, minAvg ] , [maxAvg, maxAvg, maxAvg, maxAvg, maxAvg, maxAvg, maxAvg ] ]
        self.ipt = None  
        print("Histname is {}".format(self.histoName)   )
        noFitList = ['LeptonPtHist', 'LeptonEtaHist', 'METPtHist', 'HTLepHist', 'WeightHist',
                     'RunNumberHist', 'AK8PuppiSDPtResponse', 'AK8SDPtResponse', 'AK8SDPuppiptGenptResponse',
                     'AK8SDPuppimassSDCHSmassResponse', 'AK8SDPuppiMasswithPuppiCorrvsSDPuppiMassResponse', 'AK8MSDRawHist',
                     'AK8PtHist', 'AK8HTHist','AK8SDPtHist','AK8PuppiSDPtHist','AK8PuppiPtHist', 'AK8PuppiSDPtResponse', 'AK8SDPtResponse',
                     'AK8SDSJ0PtHist', 'AK8EtaHist','AK8puppitau21Hist','AK8puppitau32Hist', 'AK8SDRhoRatioHist', 'LeptonPtHist','LeptonEtaHist',
                     'METPtHist','HTLepHist','Iso2DHist','AK4BdiscHist'
                    ]       
                    
                    
                    
        if ( self.isWmass and self.isstage == (14 or 13 or 15) and self.typeis) or ( self.isWmass and self.isstage ==( 17 or 15)and not self.typeis) or ( self.isTopmass and self.isstage ==( 14 or 13) and not self.typeis ) :
            print("rangenum is {}".format(self.isstage))
            if self.histoName in noFitList:
                print("Histo is in the noFitList.")
                self.dontFit = True
            else :
                self.dontFit = False
                ### Fit these histos to a Gaussian and save mean and std dev for later use
                self.histofAlldata.Draw("e same x0")

                if self.typeis:
                        self.isWmass = True
                        self.minn = 55.
                        self.maxx = 115.
                        print("Type 2 W mass fit range [{0},{1}]".format(self.minn,self.maxx ))
                else:   
                    if (self.histoName.find("SDSJ")== -1 ) :
                        self.minn = 110.
                        self.maxx = 250.
                        self.isTopmass = True
                        print("Type 1 Top mass fit range [{0},{1}]".format(self.minn,self.maxx ))
                    else :
                        self.minn = 55.
                        self.maxx = 115.
                        self.isWmass = True
                        print("Type 1 W mass fit range [{0},{1}]".format(self.minn,self.maxx ))

            self.ptIs = 0.
            self.binIs = "200toInf"
            self.thePtBins = ["200To300","300To400","400To500","500To800"]    
            self.thePtIs = ["250","350","450","550"]    
            for iptbin, ptbin in enumerate(self.thePtBins):
                if not self.histoName.find( ptbin) == -1 :
                    self.ipt = iptbin 
                    self.binIs =  ptbin
                    self.ptIs = self.thePtIs[iptbin]   
                    print("The Pt bin is {}".format(ptbin))


            ibin = self.hpeak.GetXaxis().FindBin(self.ptIs)
            if self.dontFit == False:
                print( "Fitting range is from {0:2.2f} to {1:2.2f} GeV".format(self.minn, self.maxx ) )

                self.fitter_data = ROOT.TF1("fitter_data"+ str(self.isstage), "gaus", self.minn , self.maxx )                

                self.fitter_mc = ROOT.TF1("fitter_mc"+ str(self.isstage), "gaus", self.minn , self.maxx )   
                histofAlldata.GetXaxis().SetTitle("")
                self.fitter_data.SetTitle("")
                self.fitter_mc.SetTitle("")
                self.histofAllMC.SetTitle("")
                if ( self.isWmass and self.isstage == 14 and self.typeis) or ( self.isWmass and self.isstage == 17 and not self.typeis) or ( self.isTopmass and self.isstage == 14 and not self.typeis ) :
                    self.fixFit = True
                    ROOT.gStyle.SetOptStat(000000)
                    histofAlldata.SetTitleOffset(1.4)
                    histofAlldata.GetXaxis().SetTitle("")
                    self.fitter_data.SetTitle("")
                    self.fitter_mc.SetTitle("")
                    self.histofAllMC.SetTitle("")
                    data_meanval = self.fitValues[1][0]
                    data_sigmaval = self.fitValues[1][1] 
                    mc_meanval = self.fitValues[1][2]
                    mc_sigmaval = self.fitValues[1][3] 
                    print("Fixing Fit in data (mc) to mean {0:2.2f}({1:2.2f}) and width {2:2.2f}({3:2.2f}) ".format(data_meanval, mc_meanval, data_sigmaval, mc_sigmaval  ))
                    self.fitter_data.FixParameter(1, data_meanval)
                    self.fitter_data.FixParameter(2, data_sigmaval)
                    self.fitter_mc.FixParameter(1, mc_meanval)
                    self.fitter_mc.FixParameter(2, mc_sigmaval)                    

                self.fitter_data.SetLineColor(1)
                self.fitter_data.SetLineWidth(2)
                self.fitter_data.SetLineStyle(2)
                self.fitter_mc.SetLineColor(4)
                self.fitter_mc.SetLineWidth(2)
                self.fitter_mc.SetLineStyle(4) 
                self.fitter_mc.GetXaxis().SetRangeUser( rangeMin, rangeMax )          
                self.fitter_data.GetXaxis().SetRangeUser( rangeMin, rangeMax )          

                if self.fixFit :
                    self.histofAlldata.Fit(self.fitter_data,'R' )
                    self.histofAllMC.Fit(self.fitter_mc,'R' )
                    
                else :
                    self.histofAlldata.Fit(self.fitter_data,'R' )
                    self.histofAllMC.Fit(self.fitter_mc,'R' )
                    
                self.mcStack.Draw("hist same")
                self.fitter_data.Draw("same")
                self.fitter_mc.Draw("same")

                self.histofAlldata.Draw("e same x0")
                amp_data    = self.fitter_data.GetParameter(0)
                eamp_data   = self.fitter_data.GetParError(0) 
                mean_data   = self.fitter_data.GetParameter(1)
                emean_data  = self.fitter_data.GetParError(1) 
                width_data  = self.fitter_data.GetParameter(2)
                ewidth_data = self.fitter_data.GetParError(2) 

                print( 'Combined: amp_data {0:6.3}, eamp_data {1:6.3}, mean_data {2:6.3},emean_data {3:6.3}, width_data {4:6.3}, ewidth_data {5:6.3}  '.format(amp_data , eamp_data , mean_data, emean_data,  width_data, ewidth_data   ) )

                amp_mc    = self.fitter_mc.GetParameter(0)
                eamp_mc   = self.fitter_mc.GetParError(0) 
                mean_mc   = self.fitter_mc.GetParameter(1)
                emean_mc  = self.fitter_mc.GetParError(1) 
                width_mc  = self.fitter_mc.GetParameter(2)
                ewidth_mc = self.fitter_mc.GetParError(2) 
                      
                print( 'MC : amp_mc {0:6.3}, eamp_mc {1:6.3}, mean_mc {2:6.3},emean_mc {3:6.3}, width_mc {4:6.3}, ewidth_mc {5:6.3}  '.format(amp_mc , eamp_mc , emean_mc, emean_mc,  width_mc, ewidth_mc   )       )
                
                self.mcAxis = self.histofAllMC.GetXaxis()
                self.dataAxis = self.histofAlldata.GetXaxis()

                binSizeData = self.histofAlldata.GetBinWidth(0)
                binSizeMC = self.histofAllMC.GetBinWidth(0) 

                print("Bin size in data {0:1.2f} and MC  {1:1.2f}".format(binSizeData, binSizeMC ) )
                #print("self.fitDiffs[2][0] {}".format(self.fitDiffs[2][0]))
                self.bins = [self.dataAxis.FindBin(self.fitDiffs[2][0]), self.dataAxis.FindBin(self.fitDiffs[2][1]), self.mcAxis.FindBin(self.fitDiffs[2][2]), self.mcAxis.FindBin(self.fitDiffs[2][3]) ] # data low high, mc low high

                
                print("stage {0:1.2f} isWmass  {1:}".format(self.isstage, self.isWmass ) )

                if  ( self.isWmass and self.isstage == 13 and self.typeis) or ( self.isWmass and self.isstage == 15 and not self.typeis ) or ( self.isTopmass and self.isstage == 13 and not self.typeis  ) : ### Save the means and sigmas of the pre-tau21 mass cut distribution
                    self.fitValues[1][0] = mean_data
                    self.fitValues[1][1] = width_data
                    self.fitValues[1][2] = mean_mc
                    self.fitValues[1][3] = width_mc
                    
                    self.fitDiffs[1][0] = self.fitValues[1][0] - self.fitValues[1][1]
                    self.fitDiffs[1][1] = self.fitValues[1][0] + self.fitValues[1][1]
                    self.fitDiffs[1][2] = self.fitValues[1][2] - self.fitValues[1][3]
                    self.fitDiffs[1][3] = self.fitValues[1][2] + self.fitValues[1][3]
                    print("self.fitDiffs[1][0] {}".format(self.fitDiffs[1][0]))
                    self.bins = [self.dataAxis.FindBin(self.fitDiffs[1][0]), self.dataAxis.FindBin(self.fitDiffs[1][1]), self.mcAxis.FindBin(self.fitDiffs[1][2]), self.mcAxis.FindBin(self.fitDiffs[1][3]) ] # data low high, mc low high
                    self.passPretag = [self.histofAlldata.Integral(self.bins[0], self.bins[1]  ), self.histofAllMC.Integral(self.bins[2] , self.bins[3]  )] # data, mc
                    self.passPretagUncert = [ math.sqrt( self.passPretag[0] ) , math.sqrt( self.passPretag[1] ) ] # data, mc
                    
                    ibin = self.hNpassDataPre.GetXaxis().FindBin(self.ptIs )
                    self.hNpassDataPre.SetBinContent(ibin, self.passPretag[0])
                    print("self.histofAlldata.Integral   {0:4.3f} (self.bins[0]   {1} , self.bins[1]  {2} )".format(self.histofAlldata.Integral(self.bins[0], self.bins[1]  ), self.bins[0], self.bins[1] ))

                    self.hNpassMCPre.SetBinContent(ibin, self.passPretag[1])
                    print("self.hNpassMCPre {} in bin {}".format(self.passPretag[1] , ibin ) )

                    self.hNpassDataPre.SetBinError(ibin, self.passPretagUncert[0]) 
                    self.hNpassMCPre.SetBinError(ibin, self.passPretagUncert[1])

                    
                if  ( self.isWmass and self.isstage == 14 and self.typeis) or ( self.isWmass and self.isstage == 17 and not self.typeis ) or ( self.isTopmass and self.isstage == 14 and not self.typeis ): ### Save the means and sigmas of the tau21 cut distribution
                    self.fitValues[2][0] = mean_data
                    self.fitValues[2][1] = width_data
                    self.fitValues[2][2] =  mean_mc
                    self.fitValues[2][3] = width_mc    
                    
                    self.fitDiffs[2][0] = self.fitValues[1][0] - self.fitValues[1][1]
                    self.fitDiffs[2][1] = self.fitValues[1][0] + self.fitValues[1][1]
                    self.fitDiffs[2][2] = self.fitValues[1][2] - self.fitValues[1][3]
                    self.fitDiffs[2][3] = self.fitValues[1][2] + self.fitValues[1][3]
                    print("self.fitDiffs[2][0] {}".format(self.fitDiffs[2][0]))
                    self.bins = [self.dataAxis.FindBin(self.fitDiffs[2][0]), self.dataAxis.FindBin(self.fitDiffs[2][1]), self.mcAxis.FindBin(self.fitDiffs[2][2]), self.mcAxis.FindBin(self.fitDiffs[2][3]) ] # data low high, mc low high
                    self.passPosttag = [self.histofAlldata.Integral(self.bins[0], self.bins[1]  ), self.histofAllMC.Integral(self.bins[2] , self.bins[3]  )] # data, mc
                    self.passPosttagUncert = [ math.sqrt( self.passPosttag[0] ) , math.sqrt( self.passPosttag[1] ) ] # data, mc

                    if mean_mc > 0. : 
                        self.jms[0] = mean_data / mean_mc
                        self.jms[1] = 0.
                        if self.jms[0] > 0.1:
                            self.jms[1] = self.jms[0] * math.sqrt( (emean_data/mean_data)**2 + (emean_mc/mean_mc)**2 )
                    if width_mc > 0. :
                        self.jmr[0] = width_data / width_mc
                        self.jmr[1] = 0.
                        if self.jmr[0] > 0.1:
                            self.jmr[1] = self.jmr[0] * math.sqrt( (ewidth_data/width_data)**2 + (ewidth_mc/width_mc)**2 )
                            
                    
                    self.hpeak.SetBinContent(ibin, self.jms[0] ) 
                    self.hwidth.SetBinContent(ibin, self.jmr[0] )
                    self.hpeak.SetBinError(ibin, self.jms[1])   
                    self.hwidth.SetBinError(ibin,  self.jmr[1])
                    
                    ibin = self.hNpassDataPost.GetXaxis().FindBin(self.ptIs )
                    self.hNpassDataPost.SetBinContent(ibin, self.passPosttag[0])
                    print("self.hNpassDataPost {} in bin {}".format(self.passPosttag[0] , ibin ) )

                    self.hNpassMCPost.SetBinContent(ibin, self.passPosttag[1])
                    print("self.hNpassMCPost {} in bin {}".format(self.passPosttag[1] , ibin ) )

                    self.hNpassDataPost.SetBinError(ibin, self.passPosttagUncert[0]) 
                    self.hNpassMCPost.SetBinError(ibin, self.passPosttagUncert[1])
                    
                    if float(self.passPretag[1]) > 0.1 :
                        self.MCeff = ( float(self.passPosttag[1]) / float(self.passPretag[1]) )
                        #self.MCeff  = 1./self.MCeff 
                    if (self.passPretag[0] > 0.1 and self.passPretag[1] > 0.1 and float(self.passPretag[0]) > 0.1 and  self.MCeff > 0.1) :
                        print( "self.MCeff {} datapre {} datapost {}".format(self.MCeff, self.passPretag[0], self.passPosttag[0]))
                        self.Dataeff = ( float(self.passPosttag[0]) / float(self.passPretag[0]) ) 
                        #self.Dataeff = 1./self.Dataeff
                        self.SF =  self.Dataeff/self.MCeff
                        #self.SF_sd = self.SF * math.sqrt(   (+ float(self.passPosttag[0]) - float(self.passPretag[0]) ) / ( float(self.passPosttag[0]) * float(self.passPretag[0]) )  + (float(self.passPosttag[1]) - float(self.passPretag[1])) / (float(self.passPosttag[1]) * float(self.passPretag[1]))  )

                        self.SF_sd = self.SF * math.sqrt(   (- float(self.passPosttag[0]) + float(self.passPretag[0]) ) / ( float(self.passPosttag[0]) * float(self.passPretag[0]) )  + (-float(self.passPosttag[1]) + float(self.passPretag[1])) / (float(self.passPosttag[1]) * float(self.passPretag[1]))  )
                        print( "............................................")
                        print( "             SCALE FACTOR                   ")
                        print( "............................................")
                        print( "pt Bin :  " + str(self.binIs))
                        if self.isTopmass:
                            print( "Preliminary Top tagging SF : {0:3.3f} #pm {1:3.3f}".format(  self.SF, self.SF_sd))
                        else:
                            print( "Preliminary W tagging SF from subjet w : {0:3.3f} #pm {1:3.3f}".format(  self.SF, self.SF_sd))
                        print( "Data efficiency for this  bin {0:3.3f}".format(  self.Dataeff ))
                        print( "MC efficiency for this  bin {0:3.3f}".format(self.MCeff))

                        print( "............................................")
                        ibin = self.hSFs.GetXaxis().FindBin(self.ptIs)
                        self.hSFs.SetBinContent(ibin, self.SF )
                        self.hSFs.SetBinError(ibin, self.SF_sd)
                    else :
                        ibin = self.hSFs.GetXaxis().FindBin(self.ptIs)
                        self.hSFs.SetBinContent(ibin, 0.0 )
                    
        self.words = ROOT.TLatex(0.14,0.916,"#font[62]{CMS} #font[52]{Preliminary}")
        self.words.SetNDC()
        self.words.SetTextFont(42)
        self.words.SetTextSize(0.0725)
        self.words.SetLineWidth(2)
        self.words.Draw()
        
        self.words1 = ROOT.TLatex(0.9,0.916,"%2.2f fb^{-1} (13 TeV)"%(self.lumi))
        self.words1.SetNDC()
        self.words1.SetTextAlign(31)
        self.words1.SetTextFont(42)
        self.words1.SetTextSize(0.0725)
        self.words1.SetLineWidth(2)
        self.words1.Draw()
        
        self.words2 = ROOT.TLatex(0.92, 0.34,"%s"%(self.cuttag))
        self.words2.SetNDC()
        self.words2.SetTextAlign(31)
        self.words2.SetTextFont(42)
        self.words2.SetTextSize(0.03725)
        self.words2.SetLineWidth(1)
        self.words2.Draw()
                
        self.leg = ROOT.TLegend(0.68,0.4,0.80,0.84)
        self.leg.SetFillColor(0)
        self.leg.SetBorderSize(0)
        self.leg.SetTextSize(0.026)

        if self.expectedRuns != None :
            self.leg.AddEntry( self.histofAlldata, str(self.tagg), 'p')
            self.leg.AddEntry( self.expectedRuns  , 'Expected Data', 'p')
        else :
            if self.otherttbar == True :
                self.leg.AddEntry( self.httbar, 't#bar{t} #scale[0.6]{(80X Powheg + Pythia 8) Tune CUETP8M2T4}', 'f')
            else:
                self.leg.AddEntry( self.httbar, 't#bar{t} #scale[0.6]{(80X Powheg + Pythia 8) Tune CUETP8M1}', 'f')
            #if options.allMC :
            self.leg.SetTextSize(0.036)
            self.leg.AddEntry( self.hST, 'Single Top', 'f')
            self.leg.AddEntry( self.hwjets, 'W+jets', 'f')
            self.leg.AddEntry( self.hQCD, 'QCD', 'f')
            self.leg.AddEntry( self.histofAlldata, str(self.tagg), 'p')
            if ( self.isWmass and self.isstage >= 15 ) and ( self.isTopmass and self.isstage >= 13 )  :
                self.leg.AddEntry( self.fitter_mc  , 'MC Fit eff {0:3.3f}'.format(self.MCeff), 'l')
                self.leg.AddEntry( self.fitter_data  , 'Data Fit eff {0:3.3f}'.format(self.Dataeff), 'l') 
                if ( self.isWmass and self.isstage == 15 ) and ( self.isTopmass and self.isstage == 13 )  :      
                    self.leg.AddEntry( self.fitter_data  , 'Data/MC SF {0:3.3f} #pm {1:3.3f}'.format(self.SF, self.SF_sd), '')         

        self.leg.Draw()
        self.pad1.Modified()
        self.c1.cd()
        
        print("Making pad2")
        self.pad2 = ROOT.TPad("pad" + str(self.isstage), "pad" + str(self.isstage),0,0, 1, 0.33333) #0.3333333,1,1)
        self.pad2.Draw()
        self.pad2.cd()
        #self.pad2.Range(-0.1792683,-1.370091,1.10122,1.899)
        self.pad2.SetFillColor(0)
        self.pad2.SetBorderMode(0)
        self.pad2.SetBorderSize(2)
        self.pad2.SetTickx(1)
        self.pad2.SetTicky(1)
        self.pad2.SetLeftMargin(0.14)
        self.pad2.SetRightMargin(0.04)
        self.pad2.SetTopMargin(0)
        self.pad2.SetBottomMargin(0.45)
        self.pad2.SetFrameFillStyle(0)
        self.pad2.SetFrameBorderMode(0)
        self.pad2.SetFrameFillStyle(0)
        self.pad2.SetFrameBorderMode(0)

        self.hRatio = self.histofAlldata2.Clone('self.hRatio')
        self.hData = self.histofAlldata.Clone('self.hData')
        self.hMC = self.histofAllMC.Clone('self.hMC')
                
        hRatioBinWidth = self.histofAlldata2.GetBinWidth(0)
        hRationBins =  self.histofAlldata2.GetSize()
        print("hRatio has {} bins of size {}".format(hRationBins, hRatioBinWidth))        
        #self.hRatio.SetName('self.hRatio')
        self.hRatio.Sumw2()
        self.hRatio.SetStats(0)
        #if options.drawOnlyQCD :
        #    self.hRatio.Divide(hQCD)#(tempMC2)
        #else :
        hmcBinWidth = self.histofAllMC2.GetBinWidth(0)
        hmcnBins =  self.histofAllMC2.GetSize()
        print("histofAllMC has {} bins of size {}".format(hmcnBins, hmcBinWidth))    
        if self.expectedRuns != None :     
            self.hRatio.Divide(self.expectedRuns)
        else :     
            self.hRatio.Divide(self.histofAllMC2)            
        self.hRatio.Sumw2()
        self.hRatio.SetStats(0)
        
        self.hRatio.GetYaxis().SetRangeUser(0.01,1.99)   #(-1.01, 2.99)#
        self.hRatio.GetXaxis().SetRangeUser( rangeMin, rangeMax  )
        self.hRatio.GetXaxis().SetTitle(  HistoTitle +" , Stage "+str(self.isstage)  )


        self.hRatio.SetFillColor(1)
        self.hRatio.SetFillStyle(0)
        self.hRatio.SetLineWidth(2)
        self.hRatio.SetLineColor(1)
        self.hRatio.SetMarkerStyle(20)
        self.hRatio.SetMarkerSize(0.8)
        self.hRatio.GetXaxis().SetNdivisions(506)
        self.hRatio.GetXaxis().SetLabelFont(42)
        self.hRatio.GetXaxis().SetLabelOffset(0.015)
        self.hRatio.GetXaxis().SetLabelSize(0.1275)
        self.hRatio.GetXaxis().SetTitleSize(0.12)
        self.hRatio.GetXaxis().SetTickLength(0.09)
        self.hRatio.GetXaxis().SetTitleOffset(1.35)
        self.hRatio.GetXaxis().SetTitleFont(42)
        self.hRatio.GetYaxis().SetTitle("#frac{Data}{MC}")
        #self.hRatio.GetYaxis().CenterTitle(true)
        self.hRatio.GetYaxis().SetNdivisions(304)
        self.hRatio.GetYaxis().SetLabelFont(42)
        self.hRatio.GetYaxis().SetLabelSize(0.1275)
        self.hRatio.GetYaxis().SetTitleSize(0.121)
        self.hRatio.GetYaxis().SetTickLength(0.045)
        self.hRatio.GetYaxis().SetTitleOffset(0.415)
        self.hRatio.GetYaxis().SetTitleFont(42)

        self.hRatio.Draw("lepe0")

        self.lineup = ROOT.TF1("lineup", "1.5", -7000, 7000)
        self.lineup.SetLineColor(1)
        self.lineup.SetLineStyle(2)
        self.lineup.SetLineWidth(2)
        self.lineup.Draw("same")
        self.hRatio.Draw("e same x0")

        self.line = ROOT.TF1("line", "1", -7000, 7000)
        self.line.SetLineColor(1)
        self.line.SetLineStyle(1)
        self.line.SetLineWidth(3)
        self.line.Draw("same")
        self.hRatio.Draw("e same x0")

        self.lined = ROOT.TF1("lined", "0.5", -7000, 7000)
        self.lined.SetLineColor(1)
        self.lined.SetLineStyle(2)
        self.lined.SetLineWidth(2)
        self.lined.Draw("same")
        self.hRatio.Draw("e same x0")
        ROOT.gPad.RedrawAxis()
         
        self.pad2.Modified()
        self.c1.cd()
        self.c1.Modified()
        
        self.c1.cd()
        self.c1.SetSelected(self.c1)   

    #@staticmethod    
    def GetPlotCanvas( self ) :
        self.c1.Update()
        return self.c1  
    #@staticmethod
    def GetJMSHist(self) :
        return self.hpeak
    #@staticmethod
    def GetJMRHist(self) :
        return self.hwidth
    #@staticmethod
    def GetDataPostHist(self) :
        return self.hNpassDataPost
    #@staticmethod
    def GetDataPreHist(self) :
        return self.hNpassDataPre
    #@staticmethod
    def GetMCPreHist(self) :
        return self.hNpassMCPre
    #@staticmethod
    def GetMCPostHist(self) :
        return self.hNpassMCPost
    #@staticmethod
    def GetSFHist(self) :
        return self.hSFs
    #@staticmethod
    def GetFitValues( self ):
        return self.fitValues
    #@staticmethod
    def GetFitDiffs( self ):    
        return self.fitDiffs
    #@staticmethod
    def GetpassPretagUncert( self ):    
        return self.passPretagUncert
    #@staticmethod
    def GetpassPretag( self ):    
        return self.passPretag
    #@staticmethod
    def ResetHists( self) :
        self.hpeak.SetDirectory(0)
        self.hwidth.SetDirectory(0) 
        self.hNpassDataPre.SetDirectory(0) 
        self.hNpassDataPost.SetDirectory(0) 
        self.hNpassMCPre.SetDirectory(0) 
        self.hNpassMCPost.SetDirectory(0)   
        self.hSFs.SetDirectory(0)   

        return None
'''
             ) 
                ## Only fit the histos of SD jet mass in later stages of selection
                if (iHisto <17 and iHisto > 12 )  and self.isstage >= (options.nstages-2) : 
                    tempMC.Draw("axis same")
                    fitter_mc.Draw("same")
                    if not options.noData:
                        tempdata.Draw("axis same")
                        fitter_data.Draw("same")

                hdata.Draw("e same x0")


                if options.verbose : 
                    print "Setting X axis range to ({0}  ,  {1})".format(xAxisrange[iHisto][0] , xAxisrange[iHisto][1] )
                    if not options.noData:
                        print "Setting Y axis range to ({0}  ,  {1})".format(0. ,y_max_scale * hdata.GetMaximum() )
            if iHisto != 11:
 



            c1.Print("./plots_Nov10/" + options.hist + str(self.isstage) + typeIs + MCs + CorrIs + ".pdf", "pdf")
'''
#set the tdr style
#tdrstyle.setTDRStyle()
