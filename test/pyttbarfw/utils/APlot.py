import ROOT

from utils.HistoTitles import HistoTitles
import tdrstyle

class APlot () :
    
    def __init__(self, isstage = None , y_max = None, histofAlldata = None, histofAlldata2 = None, histofAllMC = None, histofAllMC2 = None, mcStack = None, httbar = None, hwjets = None, hST = None, hQCD = None, histoName = None, lumi = None, tagg = None, cuttag = None) :
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

        self.histofAlldata.GetXaxis().SetNdivisions(506)
        self.histofAlldata.GetXaxis().SetLabelFont(42)
        self.histofAlldata.GetXaxis().SetLabelSize(0)
        self.histofAlldata.GetXaxis().SetTitleSize(0.0475)
        self.histofAlldata.GetXaxis().SetTickLength(0.045)
        self.histofAlldata.GetXaxis().SetTitleOffset(1.15)
        self.histofAlldata.GetXaxis().SetTitleFont(42)
        self.histofAlldata.GetYaxis().SetTitle("Events")
        self.histofAlldata.GetYaxis().SetNdivisions(506)
        self.histofAlldata.GetYaxis().SetLabelFont(42)
        self.histofAlldata.GetYaxis().SetLabelSize(0.06375)
        self.histofAlldata.GetYaxis().SetTitleSize(0.06225)
        self.histofAlldata.GetYaxis().SetTitleOffset(0.9)
        self.histofAlldata.GetYaxis().SetTitleFont(42)
        #self.histofAlldata.SetXTitle(HistoTitle +" , Stage "+str(self.isstage))


        self.histofAlldata.Draw("e x0")

        #if options.drawOnlyQCD :
        #   hQCD_stack.Draw("hist same")
        #else :
        self.mcStack.Draw("hist same")
        
        self.histofAlldata.Draw("e same x0")

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
        self.leg.AddEntry( self.httbar, 't#bar{t} (80X Powheg + Pythia 8 )', 'f')
        #if options.allMC :
        self.leg.AddEntry( self.hST, 'Single Top', 'f')
        self.leg.AddEntry( self.hwjets, 'W+jets', 'f')
        self.leg.AddEntry( self.hQCD, 'QCD', 'f')
        self.leg.AddEntry( self.histofAlldata, str(self.tagg), 'p')
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
                if (iHisto <17 and iHisto > 12 )  and istage >= (options.nstages-2) : 
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
 



            c1.Print("./plots_Nov10/" + options.hist + str(istage) + typeIs + MCs + CorrIs + ".pdf", "pdf")
'''
#set the tdr style
#tdrstyle.setTDRStyle()
