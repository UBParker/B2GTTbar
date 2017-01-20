#! /usr/bin/env python

import ROOT

class B2GSelectSemiLepTTbar_Type1( ) :
    """
    Selects semileptonic ttbar events with widely separated top quarks.
    This selects type 2 top events with traditional lepton isolation.
    """
    def __init__(self, options, tree, lepsel ):
        self.tau21Cut = options.tau21Cut
        self.Subjettau21Cut = self.tau21Cut
        self.tau32Cut = options.tau32Cut
        self.bdiscmin = options.bdiscmin
        self.ignoreTrig = options.ignoreTrig
        self.verbose = options.verbose

        self.infile = options.infile
        if self.verbose : print "The infile is : {}".format(self.infile)

        self.nstages = 8
        
        self.tree = tree
        self.lepsel = lepsel
        self.passed = [False] * self.nstages
        self.passedCount = [0] * self.nstages


        # Stage 0 (10)- Pass Leptonic Selection

        # Stage 1 (11)- AK8 Jet Pt and eta cut
        self.AK8PtCut = 400.
        self.AK8EtaCut = 2.4

        # Stage 2 (12) - AK4 Jet bdisc cut
        # see self.bdiscmin above

        # Stage 3 (13) - AK8 Jet tau32 cut
        #  see self.tau32Cut above

        # Stage 4 (14) - AK8 SD Jet mass cut
        self.minAK8Mass = 110.
        self.maxAK8Mass = 210.

        # Stage 5 (15) - AK8 SD Subjet 0 mass cut
        self.minAK8sjMass = 55.
        self.maxAK8sjMass = 115.

        #Stage 6 (16) - AK8 SD Subjt 0 tau21 cut
        # see self.tau21Cut above

        #Stage 7 (17) - AK8 SD subjet 1 bdisc cut
        # see self.bdiscmin above

        # Cached class member variables for plotting

        self.ak8JetP4 = None
        self.ak8JetP4Raw = None

        self.ak8SDJetP4 = None
        self.ak8SDJetP4Raw = None

        self.ak8PuppiJetP4 = None
        self.ak8PuppiJetP4Raw = None

        self.ak8PuppiSDJetP4 = None
        self.ak8PuppiSDJetP4Raw = None

        self.puppitau32 = None
        self.puppitau21 = None
        self.tau32      = None
        self.tau21      = None

        self.ak8PuppiSDJetP4_Subjet0 = None
        self.ak8PuppiSDJetP4_Subjet1 = None
        self.ak8PuppiSDJetP4_Subjet0Raw = None
        self.ak8PuppiSDJetP4_Subjet1Raw = None
        '''
        self.ak8PuppiJet200 = None
        self.ak8PuppiSDJetP4200 =  None
        self.ak8PuppiSDJetP4_Subjet0M200 =  None
        self.ak8PuppiSDJetP4_Subjet1M200 =  None

        self.ak8PuppiJet300 = None
        self.ak8PuppiSDJetP4300 =  None
        self.ak8PuppiSDJetP4_Subjet0M300 =  None
        self.ak8PuppiSDJetP4_Subjet1M300 =  None

        self.ak8PuppiJet400 = None
        self.ak8PuppiSDJetP4400 =  None
        self.ak8PuppiSDJetP4_Subjet0M400 =  None
        self.ak8PuppiSDJetP4_Subjet1M400 =  None

        self.ak8PuppiJet500 = None
        self.ak8PuppiSDJetP4500 =  None
        self.ak8PuppiSDJetP4_Subjet0M500 =  None
        self.ak8PuppiSDJetP4_Subjet1M500 =  None

        self.ak8PuppiJet600 = None
        self.ak8PuppiSDJetP4600 =  None
        self.ak8PuppiSDJetP4_Subjet0M600 =  None
        self.ak8PuppiSDJetP4_Subjet1M600 =  None
        '''
        self.ak4Jet = None
        self.ak4JetBdisc = None        

        self.ak8SDsubjet0tau1 = None
        self.ak8SDsubjet0tau2 = None
        self.ak8SDsubjet0tau21 = None

        self.SDptPuppipt = None
        self.SDptGenpt = None
        self.ak8JetHT = None
        self.SDRhoRatio = None
 
        self.ak8Jet_Ptbins = [200, 300, 400, 500, 800, 1000]


        ### PUPPI jet mass corrections

        self.finCor1 = ROOT.TFile.Open( "./puppiCorr.root","READ")
        self.puppisd_corrGEN      = self.finCor1.Get("puppiJECcorr_gen")
        self.puppisd_corrRECO_cen = self.finCor1.Get("puppiJECcorr_reco_0eta1v3")
        self.puppisd_corrRECO_for = self.finCor1.Get("puppiJECcorr_reco_1v3eta2v5")


        ### Flag to distinguish data from MC
        self.itIsData = None
        theFileIs = self.infile
        if theFileIs.find("un2016")== -1 : 
            self.itIsData = False
            self.PtSmear = None
            self.PuppiPtSmear = None
            if self.verbose :  
                print "MC : Event and PU weights != 1"

        else : 
            self.itIsData = True   
            self.PtSmear = 1.0  
            self.PuppiPtSmear = 1.0             
            if self.verbose : print "DATA : weights = 1" 
    """
        This is the "select" function that does the work for the event selection. If you have any complicated
        stuff to do, do it here and create a class member variable to cache the results. 
    """
    def select( self ) :

        self.PuppiCorr = None
        self.Corr = None
        self.CorrL2L3 = None
        self.CorrL2L3SD = None
        self.PtSmear = None
        self.PuppiPtSmear = None


        self.PuppiCorr = self.tree.JetPuppiCorrFactor[0]
        self.Corr = self.tree.JetCorrFactor[0]
        self.CorrL2L3 = self.tree.JetSDptCorrL23[0]
        self.CorrL2L3SD = self.tree.JetSDmassCorrL23[0]
        if self.itIsData :
            self.PtSmear = 1.
            self.PuppiPtSmear = 1.
        else:
            self.PtSmear = self.tree.JetPtSmearFactor[0]
            self.PuppiPtSmear = self.tree.JetPuppiPtSmearFactor[0]


            
        self.ak8JetP4 = None
        self.ak8JetP4Raw = None

        self.ak8SDJetP4 = None
        self.ak8SDJetP4Raw = None

        self.ak8PuppiJetP4 = None
        self.ak8PuppiJetP4Raw = None

        self.ak8PuppiSDJetP4 = None
        self.ak8PuppiSDJetP4Raw = None

        self.puppitau32 = None
        self.puppitau21 = None
        self.tau32      = None
        self.tau21      = None

        self.ak8PuppiSDJetP4_Subjet0 = None
        self.ak8PuppiSDJetP4_Subjet1 = None
        self.ak8PuppiSDJetP4_Subjet0Raw = None
        self.ak8PuppiSDJetP4_Subjet1Raw = None       

        self.ak4Jet = None
        self.ak4JetBdisc = None 

        self.ak8SDsubjet0tau1 = None
        self.ak8SDsubjet0tau2 = None
        self.ak8SDsubjet0tau21 = None

        self.ak8JetHT = 0.0
        self.SDRhoRatio = None

        self.SDptPuppipt = None
        self.SDptGenpt = None

        self.ak4Jet = ROOT.TLorentzVector( )        
        self.ak4Jet.SetPtEtaPhiM( self.tree.AK4_dRminLep_Pt[0],
                                  self.tree.AK4_dRminLep_Eta[0],
                                  self.tree.AK4_dRminLep_Phi[0],
                                  self.tree.AK4_dRminLep_Mass[0] )
        self.ak4JetBdisc = self.tree.AK4_dRminLep_Bdisc[0]

        self.ak8JetP4 = ROOT.TLorentzVector()
        self.ak8JetP4.SetPtEtaPhiM( self.tree.JetPt[0],
                                  self.tree.JetEta[0],
                                  self.tree.JetPhi[0],
                                  self.tree.JetMass[0] )   

        self.ak8JetP4Raw =   self.ak8JetP4
        self.ak8JetP4 =   self.ak8JetP4 * self.Corr
        if self.ak8JetP4Raw != None :
            self.ak8_m = self.CorrPUPPIMass( self.ak8JetP4Raw.Perp() , self.ak8JetP4Raw.Eta(), self.ak8JetP4Raw.M()  )
            self.ak8JetHT =         self.ak8JetHT + self.ak8JetP4.Perp()
        self.ak8PuppiJetP4 = ROOT.TLorentzVector()
        self.ak8PuppiJetP4.SetPtEtaPhiM( self.tree.JetPuppiPt[0],
                                  self.tree.JetPuppiEta[0],
                                  self.tree.JetPuppiPhi[0],
                                  self.tree.JetPuppiMass[0] )        
        self.ak8PuppiJetP4Raw =   self.ak8PuppiJetP4
        self.ak8PuppiJetP4 =   self.ak8PuppiJetP4 * self.PuppiCorr
        if self.ak8PuppiJetP4Raw != None :
            self.ak8_Puppim = self.CorrPUPPIMass( self.ak8PuppiJetP4Raw.Perp() , self.ak8PuppiJetP4Raw.Eta(), self.ak8PuppiJetP4Raw.M()  )

        self.ak8SDJetP4 = ROOT.TLorentzVector()
        self.ak8SDJetP4.SetPtEtaPhiM( self.tree.JetSDptRaw[0],
                                  self.tree.JetSDetaRaw[0],
                                  self.tree.JetSDphiRaw[0],
                                  self.tree.JetSDmassRaw[0] )        
        self.ak8SDJetP4Raw =   self.ak8SDJetP4
        self.ak8SDJetP4 =   self.ak8SDJetP4 * self.Corr
        if self.ak8SDJetP4Raw != None :
            self.ak8_SDm = self.ak8SDJetP4.M()
            # Pt Responses
            self.SDptGenpt = float(self.ak8SDJetP4.Perp())  / float(self.ak8JetP4.Perp() ) 
            if self.ak8PuppiJetP4Raw != None :
                self.SDptPuppipt = float(self.ak8SDJetP4.Perp())  / float(self.ak8PuppiJetP4.Perp() ) 
        self.ak8PuppiSDJetP4_Subjet0 = ROOT.TLorentzVector()
        self.ak8PuppiSDJetP4_Subjet0.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0],
                                            self.tree.JetPuppiSDsubjet0eta[0], 
                                            self.tree.JetPuppiSDsubjet0phi[0], 
                                            self.tree.JetPuppiSDsubjet0mass[0] )
        self.ak8PuppiSDJetP4_Subjet0Raw =   self.ak8PuppiSDJetP4_Subjet0 
        self.ak8PuppiSDJetP4_Subjet0 =   self.ak8PuppiSDJetP4_Subjet0  * self.PuppiCorr
        if self.ak8PuppiSDJetP4_Subjet0 != None :
            self.ak8PuppiSD_subjet0_m = self.CorrPUPPIMass( 
                                                           self.ak8PuppiSDJetP4_Subjet0Raw.Perp(), 
                                                           self.ak8PuppiSDJetP4_Subjet0Raw.Eta(), 
                                                           self.ak8PuppiSDJetP4_Subjet0Raw.M()       )

        self.ak8PuppiSDJetP4_Subjet1 = ROOT.TLorentzVector()
        self.ak8PuppiSDJetP4_Subjet1.SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0],
                                            self.tree.JetPuppiSDsubjet1eta[0], 
                                            self.tree.JetPuppiSDsubjet1phi[0],
                                            self.tree.JetPuppiSDsubjet1mass[0] )
        self.ak8PuppiSDJetP4_Subjet1Raw =   self.ak8PuppiSDJetP4_Subjet1 
        self.ak8PuppiSDJetP4_Subjet1 =   self.ak8PuppiSDJetP4_Subjet1 * self.PuppiCorr
        self.ak8PuppiSDsubjet1Bdisc = self.tree.JetPuppiSDsubjet1bdisc[0]

        self.ak8PuppiSDJetP4 =  self.ak8PuppiSDJetP4_Subjet0 +  self.ak8PuppiSDJetP4_Subjet1
        self.ak8PuppiSDJetP4Raw =   self.ak8PuppiSDJetP4
        self.ak8PuppiSDJetP4 =   self.ak8PuppiSDJetP4 * self.PuppiCorr
        if self.ak8PuppiSDJetP4Raw !=None :
            if self.ak8PuppiSDJetP4.Perp() > 0.001 :
                self.SDRhoRatio = pow( self.ak8PuppiSDJetP4.M() / (self.ak8PuppiSDJetP4.Perp()*0.8) , 2)
            self.ak8PuppiSD_m = self.CorrPUPPIMass( 
                                                   self.ak8PuppiSDJetP4Raw.Perp(),
                                                   self.ak8PuppiSDJetP4Raw.Eta(),
                                                   self.ak8PuppiSDJetP4Raw.M()  )

        if self.ak8PuppiSDJetP4_Subjet0Raw !=None :
            self.ak8SDsj0_m = self.CorrPUPPIMass( 
                                                 self.ak8PuppiSDJetP4_Subjet0Raw.Perp(),
                                                 self.ak8PuppiSDJetP4_Subjet0Raw.Eta(),
                                                 self.ak8PuppiSDJetP4_Subjet0Raw.M()  )

        self.ak8PuppiJetP4_m = self.CorrPUPPIMass( self.ak8PuppiJetP4Raw.Perp() , self.ak8PuppiJetP4Raw.Eta(), self.ak8PuppiJetP4Raw.M()  )

        self.ak8SDsj0_m = self.CorrPUPPIMass( self.ak8PuppiSDJetP4_Subjet0Raw.Perp() , self.ak8PuppiSDJetP4_Subjet0Raw.Eta(), self.ak8PuppiSDJetP4_Subjet0Raw.M()  )

        self.ak8SDsj1_m = self.CorrPUPPIMass( self.ak8PuppiSDJetP4_Subjet1Raw.Perp() , self.ak8PuppiSDJetP4_Subjet1Raw.Eta(), self.ak8PuppiSDJetP4_Subjet1Raw.M()  )

        self.ak8Jet_Ptbins = [200, 300, 400, 500, 800, 1000]
        
        self.ak8PuppiJetP4_Binned = [ROOT.TLorentzVector()] * len(self.ak8Jet_Ptbins)
        self.ak8PuppiSDJetP4_Binned = [ROOT.TLorentzVector()] * len(self.ak8Jet_Ptbins)
        self.ak8PuppiSDJetP4Subjet0_Binned = [ROOT.TLorentzVector()] * len(self.ak8Jet_Ptbins)
        self.ak8PuppiSDJetP4Subjet1_Binned = [ROOT.TLorentzVector()] * len(self.ak8Jet_Ptbins)
        self.ak8PuppiSDJetP4Subjet0PuppiCorrMass_Binned = [0.] * len(self.ak8Jet_Ptbins)
        self.ak8PuppiSDJetP4Subjet1PuppiCorrMass_Binned = [0.] * len(self.ak8Jet_Ptbins)


        for iptbin, ptbin in enumerate(self.ak8Jet_Ptbins) :
            if ptbin <  1000.:
                if (  ptbin < self.ak8PuppiSDJetP4_Subjet0.Perp() < self.ak8Jet_Ptbins[iptbin+1] ) :
                    self.ak8PuppiJetP4_Binned[iptbin].SetPtEtaPhiM( self.tree.JetPuppiPt[0], self.tree.JetPuppiEta[0], self.tree.JetPuppiPhi[0], self.tree.JetPuppiMass[0] ) 
                    self.ak8PuppiSDJetP4Subjet0_Binned[iptbin].SetPtEtaPhiM( self.tree.JetPuppiSDsubjet0pt[0], self.tree.JetPuppiSDsubjet0eta[0], self.tree.JetPuppiSDsubjet0phi[0], self.tree.JetPuppiSDsubjet0mass[0] )
                    self.ak8PuppiSDJetP4Subjet1_Binned[iptbin].SetPtEtaPhiM( self.tree.JetPuppiSDsubjet1pt[0], self.tree.JetPuppiSDsubjet1eta[0], self.tree.JetPuppiSDsubjet1phi[0], self.tree.JetPuppiSDsubjet1mass[0] )
                    self.ak8PuppiSDJetP4_Binned[iptbin] =  self.ak8PuppiSDJetP4Subjet0_Binned[iptbin] + self.ak8PuppiSDJetP4Subjet1_Binned[iptbin]
                    ak8SDsj0_m =  self.CorrPUPPIMass( self.tree.JetPuppiSDsubjet0pt[0]* self.PuppiCorr,
                                                        self.tree.JetPuppiSDsubjet0eta[0],
                                                        self.tree.JetPuppiSDsubjet0mass[0] )
                    self.ak8PuppiSDJetP4Subjet0PuppiCorrMass_Binned[iptbin] = ak8SDsj0_m
                    ak8SDsj1_m =  self.CorrPUPPIMass( self.tree.JetPuppiSDsubjet1pt[0]* self.PuppiCorr,
                                                        self.tree.JetPuppiSDsubjet1eta[0],
                                                        self.tree.JetPuppiSDsubjet1mass[0] )
                    self.ak8PuppiSDJetP4Subjet1PuppiCorrMass_Binned[iptbin] = ak8SDsj1_m


        self.puppitau32 = self.tree.JetPuppiTau32[0]
        self.puppitau21 = self.tree.JetPuppiTau21[0]
        self.tau32      = self.tree.JetTau32[0]
        self.tau21      = self.tree.JetTau21[0]

        self.ak8SDsubjet0tau1 = self.tree.JetSDsubjet0tau1[0]
        self.ak8SDsubjet0tau2 = self.tree.JetSDsubjet0tau2[0]

        self.ak8SDsubjet0tau21 = 1.0
        if self.ak8SDsubjet0tau1 > 0.001:
            self.ak8SDsubjet0tau21 = self.ak8SDsubjet0tau2 / self.ak8SDsubjet0tau1
            #if self.verbose : print "SD subjet 0 tau21 is: {0:2.2f}".format(self.ak8SDsubjet0tau21)            

        # Work the cut flow
        self.passedCount = [0] * self.nstages
        self.passed = [False] * self.nstages
        self.passed[0] = self.lepsel.passed[ len(self.lepsel.passed) - 1]


        if not self.passed[0] : return self.passed
        self.passedCount[0] += 1
        if self.verbose : print "Stage 10 : Event passed leptonic selection"

        if not (self.ak8JetP4.Perp() > self.AK8PtCut and abs(self.ak8JetP4.Eta()) < self.AK8EtaCut ) : return self.passed
        self.passed[1] = True
        self.passedCount[1] += 1
        if self.verbose : print "Stage 11 : AK8 Pt  {0:2.2f}* smear{1:2.2f}  > ( {2:2.2f} GeV) and eta {3:2.2f} < ( {4:2.2f} )".format( 
                                                                                                                   self.ak8JetP4.Perp(),
                                                                                                                         self.PtSmear,
                                                                                                                        self.AK8PtCut,
                                                                                                                    self.ak8JetP4.Eta(),
                                                                                                                       self.AK8EtaCut)
        if not ( self.ak4JetBdisc >  self.bdiscmin  ) : return self.passed
        self.passed[2] = True
        self.passedCount[2] += 1
        if self.verbose : print "Stage 12 :AK4 bdisc {0:2.2f}  > ( {1:2.2f} ) ".format(  self.ak4JetBdisc , self.bdiscmin )
        
        if not ( self.minAK8Mass < self.ak8_SDm < self.maxAK8Mass ) : return self.passed
        self.passed[3] = True
        self.passedCount[3] += 1
        if self.verbose : print "Stage 13: AK8 SD mass  ({0:2.2f}) < {1:2.2f} GeV < ({2:2.2f})  [For comparison SD Puppi mass after puppi corr is  {2:2.2f} ]".format(  self.minAK8Mass , self.ak8SDJetP4.M() , self.maxAK8Mass, self.ak8PuppiSD_m)



        if not ( self.puppitau32 < self.tau32Cut ) : return self.passed
        self.passed[4] = True
        self.passedCount[4] += 1
        if self.verbose : print "Stage 14: AK8 tau32  {0:2.2f}  < ( {1:2.2f} ) [For comparison puppi tau32 is  {2:2.2f} ]".format(  self.tau32 , self.tau32Cut, self.puppitau32)



        #W tag the SD subjet 0 fix this: later see if bdisc is higher for subjet 0 or 1
        if self.verbose : print "Mass of SD subjet 0 before puppi corr is: {0:2.2f}".format( float(self.ak8PuppiSDJetP4_Subjet0.M()))
        if not ( self.minAK8sjMass <  self.ak8PuppiSD_subjet0_m  <  self.maxAK8sjMass) : return self.passed
        self.passed[5] = True
        self.passedCount[5] += 1
        if self.verbose : print "Stage 15: AK8 SD subjet 0 mass  ({0}) < {1:2.2f} GeV < ({2})  [mass is after puppi mass corr]".format( self.minAK8sjMass ,  self.ak8PuppiSD_subjet0_m  , self.maxAK8sjMass)

        #if self.verbose : print "mass of sd subjet 0 after puppi corr in bin 200-300 {0:2.3f}, 300-400 {1:2.3f}, 400-500 {2:2.3f}, 500-800 {3:2.3f}".format(self.ak8SDsj0_m200,self.ak8SDsj0_m300,self.ak8SDsj0_m400,self.ak8SDsj0_m500)


        if self.verbose :print " tau21 of SD subjet 0 is: {0:2.2f}".format( float( self.ak8SDsubjet0tau21) )
        if not ( self.ak8SDsubjet0tau21 < self.tau21Cut ) : return self.passed
        self.passed[6] = True
        self.passedCount[6] += 1
        if self.verbose : print "Stage 16: AK8 SD subjet 0 tau21  {0:2.2f}  < ( {1} ) ".format( self.ak8SDsubjet0tau21 , self.tau21Cut )

        if self.verbose :print "Bdisc of SD subjet 1 is: {0:2.2f}".format( float( self.ak8PuppiSDsubjet1Bdisc) )
        if not ( self.ak8PuppiSDsubjet1Bdisc >  self.bdiscmin ) : return self.passed
        self.passed[7] = True
        self.passedCount[7] += 1
        if self.verbose : 
            print "Stage 17: Bdisc of SD subjet 1 {0:2.2f}  < ( {1} ) ".format( float( self.ak8PuppiSDsubjet1Bdisc) ,   self.Subjettau21Cut )



        return self.passed


    def CorrPUPPIMass(self, puppiptcorr, puppieta, puppimRaw) : #{ Adapted from https://github.com/thaarres/PuppiSoftdropMassCorr

        if puppimRaw < 0.0001 : return 0.0
        self.genCorr  = 1.
        self.recoCorr = 1.
        self.totalWeight = 1.

        self.genCorr =  self.puppisd_corrGEN.Eval(     puppiptcorr )
    
        if (abs(puppieta) <=1.3 ): self.recoCorr = self.puppisd_corrRECO_cen.Eval(    puppiptcorr)
        if (abs(puppieta) > 1.3 ): self.recoCorr = self.puppisd_corrRECO_for.Eval(    puppiptcorr)
        self.totalWeight = self.genCorr * self.recoCorr
        self.puppim = self.totalWeight * puppimRaw
        #if 0. <puppimRaw<0.1 :
        #if self.verbose : print "Puppi mass corr is {0:2.2f} for jet of Raw mass {1:2.2f} and new mass {2:2.2f}".format(self.totalWeight ,puppimRaw, self.puppim)
        return self.puppim
        #}                  


  
