'''
# DONE Jan 24 : Add all possible histo names to HistoTitles

AK8SDPuppimassSDCHSmassResponse
AK8PuppiSDPtResponse
AK8SDPtResponse
AK8SDPuppiptGenptResponse
AK8SDPuppiMasswithPuppiCorrvsSDPuppiMassResponse

AK8MSDRawHist
AK8MSDPUPPIHist
AK8MSDCHSHist
AK8MSDHist
'''
      
HistoTitles =            {
                              "RunNumberHist" :  [ "Run Number" ,   271000. ,    286591. ],  
                              "WeightHist" :  [ "Weight used for filling" ,   -2. ,    2. ],  
                              "AK8PuppiSDPtResponse" :  [ "Response AK8/PUPPISD" ,   0., 500. ],  
                              "AK8SDPtResponse" :  [ "Response AK8/SD ",   0., 500. ],  
                              "AK8SDPuppiptGenptResponse" :  [ "Response AK8 SD Puppi/ AK8 jet pt",   0., 500. ],  
                              "AK8SDPuppimassSDCHSmassResponse" :  [ "Jet Mass (GeV); Response AK8 SD Puppi/ SD CHS jetMass (GeV)",   0., 500. ],  
                              "AK8SDPuppiMasswithPuppiCorrvsSDPuppiMassResponse" :  [ "Response AK8 mass after PUPPi corr/ AK8 mass JECs vs. SD puppi Mass GeV ",   0., 500. ],  
                              "AK8SDRhoRatioHist" :  [ "SD Rho ratio ",  0., 1.0 ],  
                              "AK8MSDHist" :  [ "AK8 Jet SD + PUPPI Mass + PUPPI corrections (GeV)" ,  0.0  ,   400. ],  
                              "AK8MSDRawHist" :  [ "AK8 Jet SD Mass RAW (GeV)" ,  0.0  ,   400. ],  
                              "AK8MSDPUPPIHist" :  [ "AK8 Jet SD + PUPPI Mass (GeV)" ,  0.0  ,   400. ],  
                              "AK8MSDCHSHist" :  [ "AK8 Jet SD + CHS Mass (GeV)" ,  0.0  ,   400. ],  
                              "AK8MSDSJ0Hist" : [ "Leading Subjet SD Mass (GeV)" , 39.0  ,   150. ],
                              "AK8MSDSJ0PtHist" : [ "Leading Subjet SD Pt (GeV)" , .0  ,   650. ],             
                              "AK8PtHist" : [ "AK8 Jet P_{T} (GeV)", 0.     ,  1000. ],
                              "AK8SDPtHist" : [ "AK8 SD Jet P_{T} (GeV)", 0.     ,  1000. ],
                              "AK8PuppiSDPtHist" : [ "AK8 PUPPI SD Jet P_{T} (GeV)", 0.     ,  1000. ],
                              "AK8PuppiPtHist" : [ "AK8 PUPPI Jet P_{T} (GeV)", 0.     ,  1000. ],
                              "AK8EtaHist" : [   "AK8 Jet #eta", -2.5   ,    2.5 ],
                              "AK8puppitau21Hist" : [ "AK8 puppi Jet #tau_{21}", 0.0    ,    1.0 ],
                              "AK8puppitau32Hist" : [ "AK8 puppi Jet #tau_{32}", 0.0    ,    1.0 ],
                              "AK8MHist" : [ "AK8 Jet Mass (GeV)", 0.0    ,   400. ],
                              "LeptonPtHist" : [ "Lepton P_{T} (GeV)", 0.0    ,   600. ],
                              "LeptonEtaHist" : [ "Lepton #eta", 2.5    ,  -2.5  ],
                              "METPtHist" : [ "Missing P_{T} (GeV)", 0.    ,   1000. ],
                              "HTLepHist" : [  "Lepton P_{T} + Missing P_{T} (GeV)", 0.     ,   700. ],
                              #"Iso2DHist" : [ "Lepton 2D isolation (#Delta R vs p_{T}^{REL} )", 0.     ,   400. ],
                              "AK4BdiscHist" : [ "CSVv2 B Disc", 0. , 1. ],
                              "AK8MSDSJ0Pt200To300Hist" : [ "(200<P_{t}<300) Subjet 0 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "AK8MSDSJ0Pt300To400Hist" : [  "(300<P_{t}<400) Subjet 0 SD Mass (GeV)",  0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "AK8MSDSJ0Pt400To500Hist" : [  "(400<P_{t}<500) Subjet 0 SD Mass (GeV)",  0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "AK8MSDSJ0Pt500To800Hist" : [  "(500<P_{t}<800) Subjet 0 SD Mass (GeV)",  0.    ,   150.  ], # TO-DO : [ move pt label elsewhere on canvas
                              "AK8MSDSJ1Pt200To300Hist" : [ "(200<P_{t}<300) Subjet 1 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "AK8MSDSJ1Pt300To400Hist" : [  "(300<P_{t}<400) Subjet 1 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "AK8MSDSJ1Pt400To500Hist" : [  "(400<P_{t}<500) Subjet 1 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "AK8MSDSJ1Pt500To800Hist" : [  "(500<P_{t}<800) Subjet 1 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MSDSJ0Pt200To300Hist" : [ "(200<P_{t}<300) Subjet 0 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MSDSJ0Pt300To400Hist" : [  "(300<P_{t}<400) Subjet 0 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MSDSJ0Pt400To500Hist" : [  "(400<P_{t}<500) Subjet 0 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MSDSJ0Pt500To800Hist" : [  "(500<P_{t}<800) Subjet 0 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MSDSJ1Pt200To300Hist" : [ "(200<P_{t}<300) Subjet 1 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MSDSJ1Pt300To400Hist" : [  "(300<P_{t}<400) Subjet 1 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MSDSJ1Pt400To500Hist" : [  "(400<P_{t}<500) Subjet 1 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MSDSJ1Pt500To800Hist" : [  "(500<P_{t}<800) Subjet 1 SD Mass (GeV)", 0.    ,   150. ], # TO-DO : [ move pt label elsewhere on canvas             
                              "AK8HTHist" : [ "AK8 Jet H_{T} (GeV)", 0.     ,  1000. ],
                              "AK8MPt200To300Hist" : [ "(200<P_{t}<300)  AK8 Jet Mass (GeV)", 0.    ,   400.   ], # TO-DO : [ move pt label elsewhere on canvas
                              "AK8MPt300To400Hist" : [ "(300<P_{t}<400)  AK8 Jet Mass (GeV)", 0.    ,   400.   ], # TO-DO : [ move pt label elsewhere on canvas
                              "AK8MPt400To500Hist" : [ "(400<P_{t}<500)  AK8 Jet Mass (GeV)", 0.    ,   400.   ],# TO-DO : [ move pt label elsewhere on canvas
                              "AK8MPt500To800Hist" : [ "(500<P_{t}<800)  AK8 Jet Mass (GeV)", 0.    ,   400.   ],# TO-DO : [ move pt label elsewhere on canvas
                              "AK8MSDPt200To300Hist" : [ "(200<P_{t}<300)  AK8 SD Jet Mass (GeV)", 0.    ,   400.   ],# TO-DO : [ move pt label elsewhere on canvas
                              "AK8MSDPt300To400Hist" : [  "(300<P_{t}<400)  AK8 SD Jet Mass (GeV)", 0.    ,   400.   ],# TO-DO : [ move pt label elsewhere on canvas
                              "AK8MSDPt400To500Hist" : [ "(400<P_{t}<500)  AK8 SD Jet Mass (GeV)", 0.    ,   400.   ],# TO-DO : [ move pt label elsewhere on canvas
                              "AK8MSDPt500To800Hist" : [ "(500<P_{t}<800)  AK8 SD Jet Mass (GeV)", 0.    ,   400.   ],# TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MPt200To300Hist" : [ "(200<P_{t}<300)  AK8 Jet Mass (GeV)", 0.    ,   400.   ], # TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MPt300To400Hist" : [ "(300<P_{t}<400)  AK8 Jet Mass (GeV)", 0.    ,   400.   ], # TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MPt400To500Hist" : [ "(400<P_{t}<500)  AK8 Jet Mass (GeV)", 0.    ,   400.   ],# TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MPt500To800Hist" : [ "(500<P_{t}<800)  AK8 Jet Mass (GeV)", 0.    ,   400.   ],# TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MSDPt200To300Hist" : [ "(200<P_{t}<300)  AK8 SD Jet Mass (GeV)", 0.    ,   400.   ],# TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MSDPt300To400Hist" : [  "(300<P_{t}<400)  AK8 SD Jet Mass (GeV)", 0.    ,   400.   ],# TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MSDPt400To500Hist" : [ "(400<P_{t}<500)  AK8 SD Jet Mass (GeV)", 0.    ,   400.   ],# TO-DO : [ move pt label elsewhere on canvas
                              "0AK8MSDPt500To800Hist" : [ "(500<P_{t}<800)  AK8 SD Jet Mass (GeV)", 0.    ,   400.   ],# TO-DO : [ move pt label elsewhere on canvas
                              }

                                 
                                 
                                 
                                
                                 
                                 
                                                
