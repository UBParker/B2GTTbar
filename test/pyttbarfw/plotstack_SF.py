import ROOT
import array as array
 
endstring1 =  '5db659f' #'605c442'
endstring2 = 'Commit' + endstring1

plotstack_outfiles = [
    ROOT.TFile('./plotstack_Commit5db659f/plotstack_outfile_0AK8MSDSJ0Pt200To300Hist_Commit5db659f.root'),
    ROOT.TFile('./plotstack_Commit5db659f/plotstack_outfile_0AK8MSDSJ0Pt300To400Hist_Commit5db659f.root'),
    ROOT.TFile('./plotstack_Commit5db659f/plotstack_outfile_0AK8MSDSJ0Pt400To500Hist_Commit5db659f.root'),
    ROOT.TFile('./plotstack_Commit5db659f/plotstack_outfile_0AK8MSDSJ0Pt500To800Hist_Commit5db659f.root')
    ]

thePtBins = ["200To300","300To400","400To500","500To800"]    
ptIs = ["250","350","450","550"]    

plotstack_outfile_hists1 = [
    "hpeak0AK8MSDSJ0Pt",
    "hwidth0AK8MSDSJ0Pt",
    "hSFs0AK8MSDSJ0Pt"
    ]
    
plotstack_outfile_hists2 = [
    "HistMuon16",
    "HistElectron16"
    ]
ptBs =  array.array('d', [200., 300., 400., 500., 800., 900., 1000.,1100.])
nptBs = len(ptBs) - 1

histsTocombine = [
    ROOT.TH1F("hpeak", " ;p_{T} of SD subjet 0 (GeV); JMS ",  nptBs, ptBs) ,
    ROOT.TH1F("hwidth", " ;p_{T} of SD subjet 0 (GeV); JMR ", nptBs, ptBs) ,
    ROOT.TH1F("hSFs", " ;p_{T} of SD subjet 0 (GeV); # data/mc [Integral(mean+- sigma) post/pre ", nptBs, ptBs) ]
histName = [
    "JMS",
    "JMR",
    "SF"]
canvas = [
    ROOT.TCanvas("cJMS", "cJMS",1,1,745,701),
    ROOT.TCanvas("cJMR", "cJMR",1,1,745,701),
    ROOT.TCanvas("cSF", "cSF",1,1,745,701)]
    
    
print("WARNING: The bin error is not yet set for JMR or JMS!!")

for ifile, filee in enumerate(plotstack_outfiles):
    print("Opening file {}".format(filee))
    for ihist, hist in enumerate(histsTocombine): 
        htemp = filee.Get(plotstack_outfile_hists1[ihist]+thePtBins[ifile]+ plotstack_outfile_hists2[0])
        #print("htemp is {}".format(htemp))
        ibin = 1 #hist.GetXaxis().FindBin(ptIs[ifile])
        #print("ibin is {}".format(ibin))
        tempVal =     htemp.GetBinContent(ibin)
        tempValU =     htemp.GetBinError(ibin)

        print("{0} is {1:2.3f} +/- {2:2.3f}".format(histName[ihist], tempVal, tempValU ))
        ibins = hist.GetXaxis().FindBin(ptBs[ifile])
        hist.SetBinContent(ibins, tempVal )
        hist.SetBinError(ibins, tempValU ) ### FIX THIS, SET REAL ERROR
        
        
for ihist, hist in enumerate(histsTocombine): 

    ROOT.gStyle.SetOptStat(00000000)
    c1 = canvas[ihist]
    c1.SetHighLightColor(2)
    c1.Range(0,0,1,1)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetBorderSize(2)
    c1.SetTickx(1)
    c1.SetTicky(1)
    c1.SetLeftMargin(0.14)
    c1.SetRightMargin(0.04)
    c1.SetTopMargin(0.08)
    c1.SetBottomMargin(0.15)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)

    pad1 = ROOT.TPad("pad" + str(ihist), "pad" + str(ihist),0,0,1,1)
    pad1.Draw()
    pad1.cd()
    #self.pad2.Range(-0.1792683,-1.370091,1.10122,1.899)
    pad1.SetFillColor(0)
    pad1.SetBorderMode(0)
    pad1.SetBorderSize(2)
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad1.SetLeftMargin(0.14)
    pad1.SetRightMargin(0.04)
    pad1.SetTopMargin(0.12)
    pad1.SetBottomMargin(0.14)
    pad1.SetFrameFillStyle(0)
    pad1.SetFrameBorderMode(0)


    hist.SetMaximum(1.3 )
    hist.SetMinimum(0.7 )
    hist.GetYaxis().SetTitle("Data/MC tau21< 0.55 efficiency Scale Factor")
    hist.GetYaxis().SetTitleOffset(1.) ## 0.7)
    hist.GetYaxis().SetLabelSize(0.03)
    hist.GetYaxis().SetNdivisions(506)
    hist.GetYaxis().SetLabelFont(42)
    hist.GetYaxis().SetTitleSize(0.04225)
    hist.GetYaxis().SetTitleFont(42)
    
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(1)
    hist.SetMarkerColor(1)
    
    
    hist.GetXaxis().SetRangeUser( 0, 800 )
    hist.GetXaxis().SetNdivisions(506)
    hist.GetXaxis().SetLabelFont(42)
    hist.GetXaxis().SetLabelSize(0.03)
    hist.GetXaxis().SetTitleSize(0.0275)
    hist.GetXaxis().SetTickLength(0.045)
    hist.GetXaxis().SetTitleOffset(1.15)
    hist.GetXaxis().SetTitleFont(42)
    hist.GetXaxis().SetTitle("Pt of Soft Drop subjet 0 of mass [50,120] (GeV)")


    #hist.SetXTitle(HistoTitle +" , Stage "+str(self.isstage))


    hist.Draw("EX0")

    c1.cd()
    c1.Modified()
    c1.Update()
    c1.Print("./plotstack_"+ str(endstring2)+ "/" + histName[ihist]+ "_plot.pdf", "pdf")
    c1.Print("./plotstack_"+ str(endstring2)+ "/" + histName[ihist]+ "_plot.png", "png")
