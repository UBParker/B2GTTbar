# For each MC sample the cross section, number of events and color list is saved here.
import ROOT
# ttbar
# wjets
# ST
# QCD

xs_ttbar = [831.76]
nev_ttbar = [92925926.]
ttbar_colors = [ROOT.kGreen+1 ]
ttbar_names = [""]

xs_wjets = [
1629.87,  #1345.,     #100To200  
435.6,    #359.7,     #200To400  
59.27,    #48.91,     #400To600  
14.58,    #12.05,     #600To800  
6.656,    #5.501,     #800To1200 
1.608,    #1.329,     #1200To2500
0.039,    #0.03216,   #2500ToInf 
]

nev_wjets = [
10231928., #100To200        CORRECT
4963240.,  #200To400  # fix this: update to new numbers BEFORE crab report
1963464.,  #400To600 
3722395.,  #600To800
1540477.,  #800To1200 
246737.,  #1200To2500
253561.,   #2500ToInf 
]

wjets_colors = [   ROOT.kWhite,ROOT.kRed - 9, ROOT.kRed - 7, ROOT.kRed - 4, ROOT.kRed, ROOT.kRed +1, ROOT.kRed +2   ]

wjets_names = [ "100", "200", "400", "600", "800", "1200", "2500" ]

# fix this : get new event yeilds
xs_ST = [
136.02*0.322,     #ST t-channel top  
80.95*0.322 ,     #ST t-channel antitop   
35.6,     #ST tW top  xsec given for top + antitop https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_Wt
35.6,     #ST tW antitop                         
3.36 , # 47.13,     #ST s-channel  CONSIDERING only leptonic decays https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
]

nev_ST = [                                     
32808300.,     #ST t-channel top 
19825855.,     #ST t-channel antitop  
998400.,     #ST tW top     
985000.,     #ST tW antitop                         
1000000.,     #ST s-channel  
]


ST_colors = [  ROOT.kWhite,ROOT.kCyan - 9, ROOT.kCyan - 7, ROOT.kCyan - 4, ROOT.kCyan  ]

ST_names = ["t-channel_top", "tchannel-antitop", "tW-top", "tW_antitop", "schannel" ]

nev_QCD = [
82073090., #100 Ht binned
18523829., #200
16830696., #300
19199088.,#500
15621634., #700
4980387., #1000
3846616., #1500
1960245., #2000
]

xs_QCD = [
27990000., 
1712000.,
347700.,
32100.,
6831.,
1207.,
119.9,
25.24
]

QCD_colors = [ ROOT.kRed + 7, ROOT.kRed + 3,  ROOT.kOrange + 2, ROOT.kYellow + 6 ,ROOT.kYellow + 1 , ROOT.kGreen + 2, ROOT.kCyan + 6, ROOT.kCyan+1 ] #, ROOT.kBlue + 2, ROOT.kBlue + 6, ROOT.kMagenta + 2, ROOT.kMagenta + 7 ]

QCD_names = ["Ht100", "Ht200", "Ht300", "Ht500", "Ht700", "Ht1000", "Ht1500", "Ht2000" ]
