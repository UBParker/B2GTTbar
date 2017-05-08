#! /usr/bin/env python

# python unittest_cmstt.py

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

h_ak8Jets =  Handle ("std::vector<pat::Jet>")
l_ak8Jets =         ("slimmedJetsAK8PFPuppiSoftDropPacked", "SubJets" )

h_ak4Jets =  Handle ("std::vector<pat::Jet>")
l_ak4Jets =         ("slimmedJetsPuppi" )

h_MET  = Handle ("std::vector<pat::MET>")
l_MET  =        ("slimmedMETsPuppi")

h_Electron  = Handle ("std::vector<pat::Electron>")
l_Electron  =        ("slimmedElectrons")

h_Muon  = Handle ("std::vector<pat::Muon>")
l_Muon  =        ("slimmedMuons")

h_GenParticle  = Handle ("std::vector<reco::GenParticle>")
l_GenParticle  =        ("prunedGenParticles")

ievent = 0
for event in events:
  if options.maxevents > 0 :
    if (options.maxevents == ievent ): break

    event.getByLabel (l_ak8Jets, h_ak8Jets)
    event.getByLabel (l_ak4Jets, h_ak4Jets)
    event.getByLabel (l_MET, h_MET)
    event.getByLabel (l_Electron, h_Electron)
    event.getByLabel (l_Muon, h_Muon)
    event.getByLabel (l_GenParticle, h_GenParticle)
    #print"AK8 jets product is {}".format(h_ak8Jets.product())
    ak8Jets = h_ak8Jets.product()
    #ak8Subjets = h_ak8Jets.product()[1]
    ak4Jets = h_ak4Jets.product()
    met = h_MET.product()
    electrons = h_Electron.product()
    muons = h_Muon.product()
    genParticles = h_GenParticle.product()

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
        elif PDGid==24:
          if options.verbose: print"....W+ with 2 daughters  id "+id+" status "+status+" ndau "+nDau+" pt "+pt+" eta "+eta+" phi "+phi
          if options.verbose: print"......dd0 "+particle.daughter( 0 ).pdgId()+" ndau "+particle.daughter( 0 ).numberOfDaughters()
          if options.verbose: print"......dd1 "+particle.daughter( 1 ).pdgId()+" ndau "+particle.daughter( 1 ).numberOfDaughters()
          Wtd1_p4.SetPxPyPzE( particle.daughter( 0 ).px(), particle.daughter( 0 ).py(), particle.daughter( 0 ).pz(), particle.daughter( 0 ).energy() )
          Wtd2_p4.SetPxPyPzE( particle.daughter( 1 ).px(), particle.daughter( 1 ).py(), particle.daughter( 1 ).pz(), particle.daughter( 1 ).energy() )
          if ( abs( particle.daughter( 0 ).pdgId() ) < 6 and abs( particle.daughter( 1 ).pdgId() ) < 6): tophadronic = true
          if ( abs( particle.daughter( 0 ).pdgId() ) <= 18 and abs( particle.daughter( 0 ).pdgId() ) >= 11): topleptonic = true  
          Wtd1_id = particle.daughter( 0 ).pdgId()
          Wtd2_id = particle.daughter( 1 ).pdgId()
        ### W-
        elif PDGid==-24:
          if options.verbose: print"....W- with 2 daughters  id "+id+" status "+status+" ndau "+nDau+" pt "+pt+" eta "+eta+" phi "+phi
          if options.verbose: print"......dd0 "+particle.daughter( 0 ).pdgId()+" ndau "+particle.daughter( 0 ).numberOfDaughters()
          if options.verbose: print"......dd1 "+particle.daughter( 1 ).pdgId()+" ndau "+particle.daughter( 1 ).numberOfDaughters()
          Watd1_p4.SetPxPyPzE( particle.daughter( 0 ).px(), particle.daughter( 0 ).py(), particle.daughter( 0 ).pz(), particle.daughter( 0 ).energy() )
          Watd2_p4.SetPxPyPzE( particle.daughter( 1 ).px(), particle.daughter( 1 ).py(), particle.daughter( 1 ).pz(), particle.daughter( 1 ).energy() )
          if ( abs( particle.daughter( 0 ).pdgId() ) < 6 and abs( particle.daughter( 1 ).pdgId() ) < 6) : antitophadronic = true 
          if ( abs( particle.daughter( 0 ).pdgId() ) <= 18 and abs( particle.daughter( 0 ).pdgId() ) >= 11):  antitopleptonic = true  
          Watd1_id = particle.daughter( 0 ).pdgId()
          Watd2_id = particle.daughter( 1 ).pdgId()
        
      ### End genParticle loop

    ievent +=1
    ### End Event Loop
