import ROOT

from utils.HistoTitles import HistoTitles
import tdrstyle

class APlot () :
    
    def __init__(self, isstage = None , y_max = None, histofAlldata = None, histofAlldata2 = None, histofAllMC = None, histofAllMC2 = None, mcStack = None, httbar = None, hwjets = None, hST = None, hQCD = None, histoName = None, lumi = None, tagg = None, cuttag = None, fixFit = None, expectedRuns = None) :
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
        
        self.tagg = tagg
        self.cuttag = cuttag
        self.fixFit = fixFit
        self.expectedRuns = expectedRuns
        
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
        self.histofAlldata.SetTitle("")

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
        
            self.mcStack.Draw("hist same")
            self.histofAlldata.Draw("e same x0")
        self.minn = 0.
        self.maxx = 0.     
        rangenum = 17
        self.fitValues = [ ["Datamean", "Datasigma", "MCmean", "MCsigma"],[0.,0.,0.,0.],[0.,0.,0.,0.] ]
        self.fitDiffs = [ ["DataLowerBound", "DataHigherBound", "MCLowerBound", "MCHigherBound"],[0.,0.,0.,0.],[0.,0.,0.,0.] ]

        #fittingLimits = [ [minAvg, minAvg, minAvg, minAvg, minAvg, minAvg, minAvg ] , [maxAvg, maxAvg, maxAvg, maxAvg, maxAvg, maxAvg, maxAvg ] ]
        self.ipt = None          
        if  rangenum  -4 <self.isstage < rangenum  -1 :
            print("rangenum is {}".format(self.isstage))
            
            if (self.histoName.find("AK8MPt")== -1 ) and (self.histoName.find("AK8MSD")== -1 ) and self.expectedRuns == None: 
                self.histofAlldata.Draw("e same x0")
            else : 
                ### Fit these histos to a Gaussian and save mean and std dev for later use
                self.histofAlldata.Draw("e same x0")
            if (self.histoName.find("AK8MPt")== -1 ) :
                self.minn = 55.
                self.maxx = 115.
            elif (self.histoName.find("AK8MSD")== -1 ) :
                self.minn = 110.
                self.maxx = 210.
            self.thePtBins = ["200To300","300To400","400To500","500To800"]    
            for iptbin, ptbin in enumerate(self.thePtBins):
                if ptbin.find("200") ==-1 :
                    if ptbin.find("300To400") ==-1 :
                        if ptbin.find("400To500") ==-1 :
                            if ptbin.find("500To800") ==-1 :
                                self.minn = self.minn
                            else:
                                self.ipt = iptbin        

                        else:
                            self.ipt = iptbin        

                    else:
                        self.ipt = iptbin        
                else:
                    self.ipt = iptbin                  
                    
            print( "Fitting range is from {0:2.2f} to {1:2.2f} GeV".format(self.minn, self.maxx ) )

            self.fitter_data = ROOT.TF1("fitter_data", "gaus", self.minn , self.maxx )                

            self.fitter_mc = ROOT.TF1("fitter_mc", "gaus", self.minn , self.maxx )   
   
            if self.isstage > rangenum -3 and self.fixFit:
                ROOT.gStyle.SetOptStat(000000)
                histofAlldata.GetXaxis().SetTitle("")
                data_meanval = self.fitValues[1][0]
                data_sigmaval = self.fitValues[1][1] 
                mc_meanval = self.fitValues[1][2]
                mc_sigmaval = self.fitValues[1][3] 
                
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
            self.fitter_data.SetTitle("")
            self.fitter_mc.SetTitle("")

            if self.fixFit :
                self.histofAlldata.Fit(self.fitter_data,'B' )
                self.histofAllMC.Fit(self.fitter_mc,'B' )
                
            else :
                self.histofAlldata.Fit(self.fitter_data,'R' )
                self.histofAllMC.Fit(self.fitter_mc,'R' )

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

            if self.isstage == (rangenum -3 ) : ### Save the means and sigmas of the pre-tau21 mass cut distribution
                self.fitValues[1][0] = mean_data
                self.fitValues[1][1] = width_data
                self.fitValues[1][2] = mean_mc
                self.fitValues[1][3] = width_mc
                
                self.fitDiffs[1][0] = self.fitValues[1][0] - self.fitValues[1][1]
                self.fitDiffs[1][1] = self.fitValues[1][0] + self.fitValues[1][1]
                self.fitDiffs[1][2] = self.fitValues[1][2] - self.fitValues[1][3]
                self.fitDiffs[1][3] = self.fitValues[1][2] + self.fitValues[1][3]

            if self.isstage == (rangenum -2 ) : ### Save the means and sigmas of the tau21 cut distribution
                self.fitValues[2][0] = amp_data
                self.fitValues[2][1] = width_data
                self.fitValues[2][2] = amp_mc
                self.fitValues[2][3] = width_mc    
                
                self.fitDiffs[2][0] = self.fitValues[1][0] - self.fitValues[1][1]
                self.fitDiffs[2][1] = self.fitValues[1][0] + self.fitValues[1][1]
                self.fitDiffs[2][2] = self.fitValues[1][2] - self.fitValues[1][3]
                self.fitDiffs[2][3] = self.fitValues[1][2] + self.fitValues[1][3]
                            
            self.fitter_data.Draw("same")
            self.mcStack.SetTitle("")
            self.mcStack.Draw("hist same")
            self.histofAlldata.Draw("e same x0")
            self.fitter_mc.Draw("same")

            '''''
               
                    datalow = Datameans[ipt] - Datasigmas[ipt] 
                    datahigh = Datameans[ipt] + Datasigmas[ipt]

                    mudatalow = MuDatameans[ipt] - MuDatasigmas[ipt] 
                    mudatahigh = MuDatameans[ipt] + MuDatasigmas[ipt]

                    eldatalow = ElDatameans[ipt] - ElDatasigmas[ipt] 
                    eldatahigh = ElDatameans[ipt] + ElDatasigmas[ipt]

                mcAxis = mchist.GetXaxis()
                dataAxis = hdataT.GetXaxis()
                mudataAxis = hmudataT.GetXaxis()
                eldataAxis = heldataT.GetXaxis()

                bminmc = mcAxis.FindBin(mclow)
                bmaxmc = mcAxis.FindBin(mchigh)

                bmindata = hdataT.FindBin(datalow)
                bmaxdata = hdataT.FindBin(datahigh)



     mclow = MCmeans[ipt] - MCsigmas[ipt] 
                    mchigh = MCmeans[ipt] + MCsigmas[ipt] 

                    datalow = Datameans[ipt] - Datasigmas[ipt] 
                    datahigh = Datameans[ipt] + Datasigmas[ipt]

                    self.fitDiffs = [ ["DataLowerBound", "DataHigherBound", "MCLowerBound", "MCHigherBound"],[0.,0.,0.,0.],[0.,0.,0.,0.] ]

                    jms = [0., 0.]
                    jmr = [0., 0.]

                meanrat = 1.0
                meanrat_uncert = meanrat
                jms = 1.0
                jms_uncert = jms
                
                binSizeData = hdataT.GetBinWidth(0)
                binSizeMC = mchist.GetBinWidth(0) # was mchist

                print "Bin size in data {0:1.2f} and MC  {1:1.2f}".format(binSizeData, binSizeMC )
                mclow = 0. 
                mchigh = 0.

                datalow = 0.
                datahigh = 0.
                if ipt <=6 :
                    mclow = MCmeans[ipt] - MCsigmas[ipt] 
                    mchigh = MCmeans[ipt] + MCsigmas[ipt] 

                    datalow = Datameans[ipt] - Datasigmas[ipt] 
                    datahigh = Datameans[ipt] + Datasigmas[ipt]

                    mudatalow = MuDatameans[ipt] - MuDatasigmas[ipt] 
                    mudatahigh = MuDatameans[ipt] + MuDatasigmas[ipt]

                    eldatalow = ElDatameans[ipt] - ElDatasigmas[ipt] 
                    eldatahigh = ElDatameans[ipt] + ElDatasigmas[ipt]

                mcAxis = mchist.GetXaxis()
                dataAxis = hdataT.GetXaxis()
                mudataAxis = hmudataT.GetXaxis()
                eldataAxis = heldataT.GetXaxis()

                bminmc = mcAxis.FindBin(mclow)
                bmaxmc = mcAxis.FindBin(mchigh)

                bmindata = hdataT.FindBin(datalow)
                bmaxdata = hdataT.FindBin(datahigh)

                bminmudata = hmudataT.FindBin(mudatalow)
                bmaxmudata = hmudataT.FindBin(mudatahigh)

                bmineldata = heldataT.FindBin(eldatalow)
                bmaxeldata = heldataT.FindBin(eldatahigh)

                if ipt <=6:
                    if options.pre  :
                        nMCpre[ipt] = mchist.Integral(bminmc , bmaxmc  ) #/ binSizeMC
                        nDatapre[ipt] = hdataT.Integral(bmindata, bmaxdata  ) #/ binSizeData
                        nMuDatapre[ipt] = hmudataT.Integral(bminmudata, bmaxmudata  ) #/ binSizeData
                        nElDatapre[ipt] = heldataT.Integral(bmineldata, bmaxeldata  ) #/ binSizeData
                        nMCupre[ipt] =  math.sqrt( nMCpre[ipt] )   #mchist.IntegralError(bminmc , bmaxmc  ) / binSizeMC
                        nDataupre[ipt] = math.sqrt(nDatapre[ipt] ) #hdataT.IntegralError(bmindata, bmaxdata  ) / binSizeData
                        nMuDataupre[ipt] = math.sqrt(nMuDatapre[ipt] ) 
                        nElDataupre[ipt] = math.sqrt(nElDatapre[ipt] ) 
                    else :
                        nMCpost[ipt] = mchist.Integral(bminmc , bmaxmc  ) #/ binSizeMC
                        nDatapost[ipt] = hdataT.Integral(bmindata, bmaxdata  ) #/ binSizeData
                        nMuDatapost[ipt] = hmudataT.Integral(bminmudata, bmaxmudata  ) 
                        nElDatapost[ipt] = heldataT.Integral(bmineldata, bmaxeldata  ) 
                        nMCupost[ipt] =  math.sqrt( nMCpost[ipt] )  #mchist.IntegralError(bminmc , bmaxmc  ) / binSizeMC
                        nDataupost[ipt] = math.sqrt(nDatapost[ipt] )#hdataT.IntegralError(bmindata, bmaxdata  ) / binSizeData
                        nMuDataupost[ipt] = math.sqrt(nMuDatapost[ipt] )
                        nElDataupost[ipt] = math.sqrt(nElDatapost[ipt] )

                meanrat = 0.
                meanrat_uncert = 0.
                meanratel_uncert = 0.
                meanratel = 0.
                meanratmu = 0.
                meanratmu_uncert = 0.
                if mean_mc > 0. : 
                    meanrat = mean_data / mean_mc
                    meanrat_uncert = meanrat * math.sqrt( (emean_data/mean_data)**2 + (emean_mc/mean_mc)**2 )
                    if options.Mudata :
                        meanratmu = mmean_data / mean_mc
                        meanratmu_uncert = meanratmu * math.sqrt( (memean_data/mmean_data)**2 + (emean_mc/mean_mc)**2 )
                    if options.Eldata :
                        meanratel_uncert = 0.
                        meanratel = 0.
                        if  ( abs(Emean_data) > 0.01 ) and  ( abs(mean_mc) > 0.01 ) :
                            meanratel = Emean_data / mean_mc
                            meanratel_uncert = meanratel * math.sqrt( (Eemean_data/Emean_data)**2 + (emean_mc/mean_mc)**2 )
                jms = 0.
                jms_uncert = 0.
                jms_mu = 0.
                jms_mu_uncert = 0.
                jms_el = 0.
                jms_el_uncert = 0.
                if width_mc > 0. :
                    jms = width_data / width_mc
                    jms_uncert = jms * math.sqrt( (ewidth_data/width_data)**2 + (ewidth_mc/width_mc)**2 )
                    if options.Mudata :
                        jms_mu = mwidth_data / width_mc
                        jms_mu_uncert = jms_mu * math.sqrt( (mewidth_data/mwidth_data)**2 + (ewidth_mc/width_mc)**2 )
                    if options.Eldata :
                        jms_el = Ewidth_data / width_mc
                        jms_el_uncert =  0.0
                        if abs(Ewidth_data) > 0.0001 :
                            jms_el_uncert = jms_el * math.sqrt( (Eewidth_data/Ewidth_data)**2 + (ewidth_mc/width_mc)**2 )

                #print 'data_over_mc peak combined {0:6.3}, muon {1:6.3}, electron {2:6.3} '.format(meanrat, meanratmu, meanratel)
                #print '...........................................................'

                ibin = hpeak.GetXaxis().FindBin(pt)
                hpeak.SetBinContent(ibin, meanrat ) 
                hwidth.SetBinContent(ibin, jms )
                hpeak.SetBinError(ibin, meanrat_uncert)   
                hwidth.SetBinError(ibin, jms_uncert)

                if options.Mudata :
                    hpeakmu.SetBinContent(ibin, meanratmu ) 
                    hwidthmu.SetBinContent(ibin, jms_mu )
                    hpeakmu.SetBinError(ibin, meanratmu_uncert)   
                    hwidthmu.SetBinError(ibin, jms_mu_uncert)
                if options.Eldata :
                    hpeakel.SetBinContent(ibin, meanratel ) 
                    hwidthel.SetBinContent(ibin, jms_el )
                    hpeakel.SetBinError(ibin, meanratel_uncert)   
                    hwidthel.SetBinError(ibin, jms_el_uncert)

                if ipt <=6:
                    if options.pre :
                        ibin = hNpassDataPre.GetXaxis().FindBin(pt)
                        hNpassDataPre.SetBinContent(ibin, nDatapre[ipt])
                        hNpassMuDataPre.SetBinContent(ibin, nMuDatapre[ipt])
                        hNpassElDataPre.SetBinContent(ibin, nElDatapre[ipt])
                        hNpassMCPre.SetBinContent(ibin, nMCpre[ipt])
                        hNpassDataPre.SetBinError(ibin, nDataupre[ipt])
                        hNpassMuDataPre.SetBinError(ibin, nMuDataupre[ipt])
                        hNpassElDataPre.SetBinError(ibin, nElDataupre[ipt])
                        hNpassMCPre.SetBinError(ibin, nMCupre[ipt])
                        hmeanDataPre.SetBinContent(ibin, Datameans[ipt]) 
                        hmeanMuDataPre.SetBinContent(ibin, MuDatameans[ipt]) 
                        hmeanElDataPre.SetBinContent(ibin, ElDatameans[ipt]) 
                        hmeanMCPre.SetBinContent(ibin, MCmeans[ipt] )
                        hsigmaDataPre.SetBinContent(ibin, Datasigmas[ipt])
                        hsigmaMuDataPre.SetBinContent(ibin, MuDatasigmas[ipt])
                        hsigmaElDataPre.SetBinContent(ibin, ElDatasigmas[ipt])
                        hsigmaMCPre.SetBinContent(ibin,  MCsigmas[ipt] )
                    else :
                        ibin = hNpassDataPost.GetXaxis().FindBin(pt)
                        hNpassDataPost.SetBinContent(ibin, nDatapost[ipt])
                        hNpassMuDataPost.SetBinContent(ibin, nMuDatapost[ipt])
                        hNpassElDataPost.SetBinContent(ibin, nElDatapost[ipt])
                        hNpassMCPost.SetBinContent(ibin, nMCpost[ipt])
                        hNpassDataPost.SetBinError(ibin, nDataupost[ipt])
                        hNpassMuDataPost.SetBinError(ibin, nMuDataupost[ipt])
                        hNpassElDataPost.SetBinError(ibin, nElDataupost[ipt])
                        hNpassMCPost.SetBinError(ibin, nMCupost[ipt])


            '''


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
        
        self.words2 = ROOT.TLatex(0.8, 0.34,"%s"%(self.cuttag))
        self.words2.SetNDC()
        self.words2.SetTextAlign(31)
        self.words2.SetTextFont(42)
        self.words2.SetTextSize(0.03725)
        self.words2.SetLineWidth(1)
        self.words2.Draw()
                
        self.leg = ROOT.TLegend(0.63,0.4,0.78,0.84)
        self.leg.SetFillColor(0)
        self.leg.SetBorderSize(0)
        self.leg.SetTextSize(0.036)

        if self.expectedRuns != None :
            self.leg.AddEntry( self.histofAlldata, str(self.tagg), 'p')
            self.leg.AddEntry( self.expectedRuns  , 'Expected Data', 'p')
        else :
            self.leg.AddEntry( self.httbar, 't#bar{t} (80X Powheg + Pythia 8 )', 'f')
            #if options.allMC :
            self.leg.AddEntry( self.hST, 'Single Top', 'f')
            self.leg.AddEntry( self.hwjets, 'W+jets', 'f')
            self.leg.AddEntry( self.hQCD, 'QCD', 'f')
            self.leg.AddEntry( self.histofAlldata, str(self.tagg), 'p')
            self.leg.AddEntry( self.fitter_mc  , 'MC Fit', 'l')
            self.leg.AddEntry( self.fitter_data  , 'Data Fit', 'l')         
                
        self.leg.Draw()
        self.pad1.Modified()
        self.c1.Update()        
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
                 
'''
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
