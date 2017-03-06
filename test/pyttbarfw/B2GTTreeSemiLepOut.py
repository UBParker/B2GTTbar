#! /usr/bin/env python
import ROOT
import array


class B2GTTreeSemiLepOut( ) :
    def __init__( self, options, dtype):
        self.dtype = dtype
        
        self.fout2 = ROOT.TFile.Open( './combinedTTrees80x/'+ self.dtype +'_combinedttree_80x_B2GTTreeV4.root', 'RECREATE')

        self.fout2.cd()

        self.TTreeSemiLept = ROOT.TTree("TreeSemiLept", "TreeSemiLept")
        ###
        ### Make a list of variables to add to our analysis
        ###
        self.variables = {
            'SemiLeptEventWeight':'f',
            'SemiLeptPUweight':'f',
            'FatJetMass':'f',
            'FatJetPt':'f',
            'FatJetMassSoftDrop':'f',
            'FatJetPtSoftDrop':'f',
            'FatJetTau1':'f',
            'FatJetTau2':'f',
            'FatJetTau3':'f',
            'FatJetTau32':'f',
            'FatJetTau21':'f',
            'FatJetSDbdiscW':'f',
            'FatJetSDsubjetWpt':'f',            
            'FatJetSDsubjetWEta':'f',
            'FatJetSDsubjetWPhi':'f',
            'FatJetSDsubjetWmass':'f',
            'FatJetSDsubjetWtau1':'f',
            'FatJetSDsubjetWtau2':'f',
            'FatJetSDsubjetWtau3':'f',
            'FatJetSDsubjetWtau21':'f',
            'FatJetSDsubjet_isRealW':'i',            
            'FatJetSDsubjet_isFakeW':'i',
            'FatJetSDsubjetBpt':'f',
            'FatJetSDsubjetBmass':'f',
            'FatJetSDbdiscB':'f',
            'LeptonType':'i',
            'LeptonEta':'f',
            'LeptonIso':'f',
            'LeptonPhi':'f',
            'LeptonPt':'f',
            'NearestAK4JetPt':'f',
            'AK4bDisc':'f',
            'SemiLepMETpt':'f',
            'SemiLeptRunNum':'i',
            'SemiLeptLumiBlock':'i',
            'SemiLeptEventNum':'i',
          }


        self.branchesArray = []
        for var in self.variables.iteritems() :
            self.branchesArray.append(array.array(var[1], [-1] ))
            self.TTreeSemiLept.Branch(var[0]  , self.branchesArray[i]     ,  str(var[0])+'/F'      )


    def fillTTree( self, options, variablesToFill = None ):
        self.variablesToFill = variablesToFill
        self.i = 0

        for var in self.variables.iteritems() :
            self.i +=1
            
            self.branchesArray[i] = self.variablesToFill[i]
            
            self.TTreeSemiLept.Fill()

    def WriteTTree( options):
        self.fout2.cd() 
        self.fout2.Write()
        self.fout2.Close()
