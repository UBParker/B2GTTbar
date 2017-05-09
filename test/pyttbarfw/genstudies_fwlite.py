#! /usr/bin/env python

# Adapted from the example script  unittest_cmstt.py

import ROOT
import sys
from DataFormats.FWLite import Events, Handle

from optparse import OptionParser

parser = OptionParser()

parser.add_option('--infile', type='string', action='store',
                  dest='infile',
                  default = "root://cmsxrootd.fnal.gov//store/mc/RunIISpring16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/premix_withHLT_80X_mcRun2_asymptotic_v14-v1/00000/0446C8BC-A197-E611-8481-6CC2173BC120.root",
                  help='Input file string')

parser.add_option('--v', type='string', action='store',
                  dest='verbose',
                  default = 1,
                  help='verbose: 1 is everything, 2 is W info only ...')

parser.add_option('--m', type='float', action='store',
                  dest='maxevents',
                  default = 10000,
                  help='Max # of events to process')

(options, args) = parser.parse_args()
argv = []



files = [  #"root://cmseos.fnal.gov///store/user/jdolen/B2G2016/ZprimeToTT_M-3000_W-30_TuneCUETP8M1_13TeV-madgraphMLM_RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_MINIAOD.root",
           options.infile ,
           #root://cmsxrootd.fnal.gov//
        ]
events = Events (files)

h_vertices = Handle("std::vector<reco::Vertex>")
l_vertices =  ("offlineSlimmedPrimaryVertices")

h_ak8Jets =  Handle ("std::vector<pat::Jet>")        #   SD + PUPPI AK8 info not stored but 4-vector is  equal to sum of 2 subjets
l_ak8Jets =  ("slimmedJetsAK8")      # ("selectedPatJetsAK8PFPuppi")

#h_ak8SubJets =  Handle ("std::vector<pat::Jet>")
#l_ak8SubJets =         ("slimmedJetsAK8PFPuppiSoftDropPacked", "SubJets" )

#h_ak4Jets =  Handle ("std::vector<pat::Jet>")
#l_ak4Jets =         ("slimmedJetsPuppi" )

#h_MET  = Handle ("std::vector<pat::MET>")
#l_MET  =        ("slimmedMETsPuppi")

#h_Electron  = Handle ("std::vector<pat::Electron>")
#l_Electron  =        ("slimmedElectrons")

#h_Muon  = Handle ("std::vector<pat::Muon>")
#l_Muon  =        ("slimmedMuons")

h_GenParticle  = Handle ("std::vector<reco::GenParticle>")
l_GenParticle  =        ("prunedGenParticles")

ievent = 0
for event in events:
  if options.maxevents > 0 :
    if (options.maxevents == ievent ): break
    # Get events with good primary vertices
    event.getByLabel (l_vertices, h_vertices)
    PV = None
    if len(vertices) == 0 or vertices[0].ndof() < 4 :
      continue
    else:
      PV = vertices[0]

    event.getByLabel (l_ak8Jets, h_ak8Jets)
    #event.getByLabel (l_ak8SubJets, h_ak8SubJets)
    #event.getByLabel (l_ak4Jets, h_ak4Jets)
    #event.getByLabel (l_MET, h_MET)
    #event.getByLabel (l_Electron, h_Electron)
    #event.getByLabel (l_Muon, h_Muon)
    event.getByLabel (l_GenParticle, h_GenParticle)
    #print"AK8 jets product is {}".format(h_ak8Jets.product())
    vertices = h_vertices.product() 
    ak8Jets  = h_ak8Jets.product()
    #ak8SubJets = h_ak8SubJets.product()
    #ak4Jets = h_ak4Jets.product()
    #met = h_MET.product()
    #electrons = h_Electron.product()
    #muons = h_Muon.product()
    genParticles = h_GenParticle.product()

    ### Save the 4-vector of Reco level objects
    hadtopCand_p4 = None #ROOT.TLorentzVector()
    bCand_p4 = None      #ROOT.TLorentzVector()
    WCand_p4 = None      #ROOT.TLorentzVector() 
    ### W cand is most massive SD subjet of hadronic top candidate AK8 jet

    ### Particle Counts
    ngenParticles = 0   

    nTops = 0
    nWs   = 0
    nBs   = 0
    nWd1s = 0
    nWd2s = 0

    ### Save 4-vectors of the gen particles
    topQuark_p4 = ROOT.TLorentzVector()
    bt_p4 = ROOT.TLorentzVector() # Gen b quark from top decay
    Wt_p4 = ROOT.TLorentzVector() # Gen W boson from top decay
    Wtd1_p4 = ROOT.TLorentzVector() # Gen quark daughter 1 of W boson from top decay
    Wtd2_p4 = ROOT.TLorentzVector() # Gen quark daughter 2 of W boson from top decay
    Wtd1_id = -300.  # PDG ID of Gen quark daughter 1
    Wtd2_id = -300.
    tophadronic = None
    topleptonic = None  

    antitopQuark_p4 = ROOT.TLorentzVector()
    bat_p4 = ROOT.TLorentzVector() # Gen b quark from antitop decay
    Wat_p4 = ROOT.TLorentzVector()
    Watd1_p4 = ROOT.TLorentzVector() # Gen quark daughter 1 of W boson from top decay
    Watd2_p4 = ROOT.TLorentzVector() # Gen quark daughter 2 of W boson from top decay
    Watd1_id = -300.
    Watd2_id = -300.
    antitophadronic = None
    antitopleptonic = None  

    ### Save the channel for this event : Hadronic, leptonic or semileptonic
    GenTruth_hadronic = None
    GenTruth_leptonic = None
    GenTruth_semileptonic = None

    ### Loop over all pruned gen particles and find the 4-vectors of the top, W, B and W daughters
    for particle in  genParticles :
      ngenParticles +=1
      ### Get all the info on the gen particle
      PDGid        = particle.pdgId()
      statusIs    = particle.status()
      nDau      = particle.numberOfDaughters()
      px     = particle.px()
      py     = particle.py()
      pz     = particle.pz()
      energy      = particle.energy()
      mass      = particle.mass()
      pt     = particle.pt()
      eta    = particle.eta()
      phi    = particle.phi()

      ### Get the tops which decay to W + b and record information
      if nDau == 2 : 
        if PDGid==6 :
          topQuark_p4.SetPxPyPzE( px, py, pz, energy ); 
          if options.verbose: print"....Gen Top with two daughters --- pt {0:2.0f} status {1:3.0f} # of Daughters {2:3.0f} eta {3:2.2f} phi {4:2.2f}".format(pt, statusIs, nDau, eta, phi )
        
          ### Loop over daughters to find W and b by their PDG IDs
          for daught in xrange(nDau):
            if ( abs(particle.daughter( daught ).pdgId())==5 ) :  bt_p4.SetPxPyPzE( particle.daughter( daught ).px(), particle.daughter( daught ).py(), particle.daughter( daught ).pz(), particle.daughter( daught ).energy() )
            if ( abs(particle.daughter( daught ).pdgId())==24 ) : Wt_p4.SetPxPyPzE( particle.daughter( daught ).px(), particle.daughter( daught ).py(), particle.daughter( daught ).pz(), particle.daughter( daught ).energy() )
            if options.verbose: print"......top daughter ID {} pt {} ".format( particle.daughter( daught ).pdgId(), particle.daughter( daught ).pt() )
        elif PDGid==-6 :
          antitopQuark_p4.SetPxPyPzE( px, py, pz, energy ); 
          if options.verbose: print"....Gen antiTop with two daughters --- pt {0:2.0f} status {1:3.0f} # of Daughters {2:3.0f} eta {3:2.2f} phi {4:2.2f}".format(pt, statusIs, nDau, eta, phi )
        
          ### Loop over daughters to find W and b by their PDG IDs
          for daught in xrange(nDau):
            if ( abs(particle.daughter( daught ).pdgId())==5 ) :  bat_p4.SetPxPyPzE( particle.daughter( daught ).px(), particle.daughter( daught ).py(), particle.daughter( daught ).pz(), particle.daughter( daught ).energy() )
            if ( abs(particle.daughter( daught ).pdgId())==24 ) : Wat_p4.SetPxPyPzE( particle.daughter( daught ).px(), particle.daughter( daught ).py(), particle.daughter( daught ).pz(), particle.daughter( daught ).energy() )
            if options.verbose: print"......antiTop daughter ID {} pt {} ".format( particle.daughter( daught ).pdgId(), particle.daughter( daught ).pt() )
        ### Get the Ws which decay - record their daughter information
        ### W+
        elif PDGid==24 :
          if options.verbose: print"....W+ with 2 daughters  id {0} statusIs {1} ndau {2} pt {3:2.2f} eta {4:2.2f} phi {5:2.2f}".format(PDGid, statusIs, nDau, pt, eta, phi)
          if options.verbose: print"......W+ dd0 ID {} ndau {} ".format(particle.daughter( 0 ).pdgId(), particle.daughter( 0 ).numberOfDaughters())
          if options.verbose: print"......W+ dd1 ID {} ndau {} ".format(particle.daughter( 1 ).pdgId(), particle.daughter( 1 ).numberOfDaughters())
          Wtd1_p4.SetPxPyPzE( particle.daughter( 0 ).px(), particle.daughter( 0 ).py(), particle.daughter( 0 ).pz(), particle.daughter( 0 ).energy() )
          Wtd2_p4.SetPxPyPzE( particle.daughter( 1 ).px(), particle.daughter( 1 ).py(), particle.daughter( 1 ).pz(), particle.daughter( 1 ).energy() )
          if ( abs( particle.daughter( 0 ).pdgId() ) < 6 and abs( particle.daughter( 1 ).pdgId() ) < 6): tophadronic = True
          if ( abs( particle.daughter( 0 ).pdgId() ) <= 18 and abs( particle.daughter( 0 ).pdgId() ) >= 11): topleptonic = True  
          Wtd1_id = particle.daughter( 0 ).pdgId()
          Wtd2_id = particle.daughter( 1 ).pdgId()
        ### W-
        elif PDGid==-24 :
          if options.verbose: print"....W- with 2 daughters  id {0} statusIs {1} ndau {2} pt {3:2.2f} eta {4:2.2f} phi {5:2.2f}".format(PDGid, statusIs, nDau, pt, eta, phi)
          if options.verbose: print"......W- dd0 ID {} ndau {} ".format(particle.daughter( 0 ).pdgId(), particle.daughter( 0 ).numberOfDaughters())
          if options.verbose: print"......W- dd1 ID {} ndau {} ".format(particle.daughter( 1 ).pdgId(), particle.daughter( 1 ).numberOfDaughters())
          Watd1_p4.SetPxPyPzE( particle.daughter( 0 ).px(), particle.daughter( 0 ).py(), particle.daughter( 0 ).pz(), particle.daughter( 0 ).energy() )
          Watd2_p4.SetPxPyPzE( particle.daughter( 1 ).px(), particle.daughter( 1 ).py(), particle.daughter( 1 ).pz(), particle.daughter( 1 ).energy() )
          if ( abs( particle.daughter( 0 ).pdgId() ) < 6 and abs( particle.daughter( 1 ).pdgId() ) < 6) : antitophadronic = True 
          if ( abs( particle.daughter( 0 ).pdgId() ) <= 18 and abs( particle.daughter( 0 ).pdgId() ) >= 11):  antitopleptonic = True  
          Watd1_id = particle.daughter( 0 ).pdgId()
          Watd2_id = particle.daughter( 1 ).pdgId()
        
    ### End genParticle loop

    if (tophadronic  and antitophadronic)      : GenTruth_hadronic     = True
    if (tophadronic  and not antitophadronic)  : GenTruth_semileptonic = True
    if ( not tophadronic and antitophadronic)  : GenTruth_semileptonic = True

    ### Save 4-vectores of all ak8s and 2 SD subjets
    ak8_p4 = []
    sj_p4 = [] 

    ### The 2 subjets of the AK8 where "close" has a smaller dR with the AK8 jet axis
    sjcloseak8_p4 = None
    sjfarak8_p4 = None

    ### For the semi-leptonic decays (including hadronic too for now) find the reco level top , W and b candidates
    if GenTruth_semileptonic or GenTruth_hadronic:

      ### Loop over the AK8 jets and save their 4-vectors if pt > 400 GeV
      jet_p4 = None
      goodJets = 0
      for i, jet in enumerate(ak8Jets):
        ### Ensure a boosted topology with pt cut 
        if jet.pt()* jet.jecFactor('Uncorrected') < 400. : continue 
        print"........Reco AK8 jet of Pt {0:2.2f} > 400 GeV".format(jet.pt())         
        jet_p4= ROOT.TLorentzVector()
        jet_p4.SetPtEtaPhiM(jet.pt(), jet.eta(), jet.phi(), jet.mass() ) 
        ak8_p4.append(jet_p4)
        goodJets +=1
        ### If a boosted AK8 exists, loop over it's SoftDrop subjets
        tempSJ_p4 = ROOT.TLorentzVector()
        Subjets = jet.subjets('SoftDrop')
        for iw, sj in enumerate( Subjets ) :
          tempSJ_p4.SetPtEtaPhiM(sj.pt(), sj.eta(), sj.phi(), sj.mass() )
          dR_sj_ak8 = tempSJ_p4.DeltaR(jet_p4)
          print"..........Puppi SoftDrop subjet number {0} of pt {1:2.2f} (raw pt {2:2.2f}), eta  {3:2.2f}, mass  {4:2.2f} dR(subjet, AK8) {5:2.2f} ".format(iw, sj.pt(), sj.pt()*sj.jecFactor('Uncorrected'), sj.eta(), sj.mass(), dR_sj_ak8)
          sj_p4.append(tempSJ_p4)

      print"...... {} AK8 jets with pt > 400 GeV in this event".format(len(ak8_p4))
      print"...... {} AK8 SoftDrop Subjets within AK8s of pt > 400 GeV in this event".format(len(sj_p4))
      ### Only look at events where there is at least 1 boosted AK8 with 2 subjets
      if len(ak8_p4) > 0 and len(sj_p4) >1 :
        ### Determine which of the subjet is closest to the AK8 axis 
        dRMin_ak8_sj0  = 1000.
        dRMin2_ak8_sj0 = 1000.
        for isjet, sjet in enumerate(sj_p4):
          if isjet <= 1:
            if ak8_p4[0].DeltaR(sjet) < dRMin_ak8_sj0  : 
              dRMin_ak8_sj0 = ak8_p4[0].DeltaR(sjet)
              sjcloseak8_p4 = ROOT.TLorentzVector()
              sjcloseak8_p4 = sjet
              print"..............Subjet {0} is dR {1:2.2f} from the AK8".format(isjet, ak8_p4[0].DeltaR(sjet) )
            print"............Closest subjet is {} from the AK8".format(dRMin_ak8_sj0)
            for issjet, ssjet in enumerate(sj_p4):
              if issjet == isjet : continue
              if ( dRMin_ak8_sj0 < ak8_p4[0].DeltaR(sjet) < dRMin2_ak8_sj0)  :
                dRMin2_ak8_sj0 = ak8_p4[0].DeltaR(sjet)
                sjfarak8_p4 = ROOT.TLorentzVector()
                sjfarak8_p4 = ssjet
            print"Farthest subjet is {} from the AK8".format(dRMin2_ak8_sj0)  
          if isjet > 1:
            print"..............More than 2 SoftDrop subjets!!!!!!!!!"

    if sjcloseak8_p4 != None and sjfarak8_p4  != None:
      hadtopCand_p4 = ROOT.TLorentzVector()
      bCand_p4 = ROOT.TLorentzVector()
      WCand_p4 = ROOT.TLorentzVector()                 
      ### Higher mass subjet is W candidate
      if sjcloseak8_p4.M() > sjfarak8_p4.M() :
        WCand_p4.SetPtEtaPhiM(sjcloseak8_p4.Pt(), sjcloseak8_p4.Eta(), sjcloseak8_p4.Phi(), sjcloseak8_p4.M() )
        bCand_p4.SetPtEtaPhiM(sjfarak8_p4.Pt(), sjfarak8_p4.Eta(), sjfarak8_p4.Phi(), sjfarak8_p4.M() )
      else :
        bCand_p4.SetPtEtaPhiM(sjcloseak8_p4.Pt(), sjcloseak8_p4.Eta(), sjcloseak8_p4.Phi(), sjcloseak8_p4.M() )
        WCand_p4.SetPtEtaPhiM(sjfarak8_p4.Pt(), sjfarak8_p4.Eta(), sjfarak8_p4.Phi(), sjfarak8_p4.M() )
      print"......W candidate PUPPI + SD subjet of pt {0:2.2f} and mass {1:2.2f}".format(WCand_p4.Perp() , WCand_p4.M())
      print"......b quark candidate PUPPI + SD subjet of pt {0:2.2f} and mass {1:2.2f}".format(bCand_p4.Perp() , bCand_p4.M())
      hadtopCand_p4 = bCand_p4 + WCand_p4      ### Add 2 subjet P4s to get AK8 Puppi + SD 4-vector
      print"......Top candidate PUPPI + SD AK8 of pt {0:2.2f} and mass {1:2.2f}".format(hadtopCand_p4.Pt(), hadtopCand_p4.M())
        #if iak8.Pt() < 400. : continue ### To ensure a boosted topology

        #### We now have gen particles and reco subjets so we need DeltaRs btw them and then plot those dRs in 2D histos
    if  WCand_p4 != None and Wtd1_p4 != None :       
      dR_WCand_Wtd1 = WCand_p4.DeltaR(Wtd1_p4 )
      print"dR btw W candidate subjet of pt {0:2.2f} from ak8 of pt {1:2.2f} and W daugter quark 1 (from top ) of pt {2:2.2f} is {3:2.2f}".format(WCand_p4.Pt(), hadtopCand_p4.Pt(), Wtd1_p4.Pt(), dR_WCand_Wtd1 )
      dR_WCand_Wtd2 = WCand_p4.DeltaR(Wtd2_p4 )
      print"dR btw W candidate subjet of pt {0:2.2f} from ak8 of pt {1:2.2f} and W daugter quark 2 (from top ) of pt {2:2.2f} is {3:2.2f}".format(WCand_p4.Pt(), hadtopCand_p4.Pt(), Wtd2_p4.Pt(), dR_WCand_Wtd2 )

      dR_WCand_Watd1 = WCand_p4.DeltaR(Watd1_p4 )
      print"dR btw W candidate subjet of pt {0:2.2f} from ak8 of pt {1:2.2f} and W daugter quark 1 (from antitop ) of pt {2:2.2f} is {3:2.2f}".format(WCand_p4.Pt(), hadtopCand_p4.Pt(), Watd1_p4.Pt(), dR_WCand_Watd1 )
      dR_WCand_Watd2 = WCand_p4.DeltaR(Watd2_p4 )
      print"dR btw W candidate subjet of pt {0:2.2f} from ak8 of pt {1:2.2f} and W daugter quark 2 (from antitop ) of pt {2:2.2f} is {3:2.2f}".format(WCand_p4.Pt(), hadtopCand_p4.Pt(), Watd2_p4.Pt(), dR_WCand_Watd2 )

      dR_WCand_bat = WCand_p4.DeltaR(bat_p4 )
      print"dR btw W candidate subjet of pt {0:2.2f} from ak8 of pt {1:2.2f} and b quark (from antitop) of pt {2:2.2f} is {3:2.2f}".format(WCand_p4.Pt(), hadtopCand_p4.Pt(), bat_p4.Pt(), dR_WCand_bat )
      dR_WCand_bt = WCand_p4.DeltaR(bt_p4 )
      print"dR btw W candidate subjet of pt {0:2.2f} from ak8 of pt {1:2.2f} and b quark (from top) of pt {2:2.2f} is {3:2.2f}".format(WCand_p4.Pt(), hadtopCand_p4.Pt(), bt_p4.Pt(), dR_WCand_bt )


    ievent +=1
    ### End Event Loop
