#find uhh2.AnalysisModuleRunner.Data.2016v3-* -size +1500c | xargs hadd SingleMuon_Run2016B_17Jul2018.root
import ROOT
from ROOT import *
import os, time, pickle, sys
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import CMS_lumi, tdrstyle
tdrstyle.setTDRStyle()

argc = len(sys.argv)
if (argc != 2):
 print("ERROR: usage: python", str(sys.argv[0]), "<YEAR>")
 raise SystemExit
	
year = str(sys.argv[1])
outdir = os.getcwd()
loadHistos = False
doVBF = True

def get_pad(name,lumi):

 #change the CMS_lumi variables (see CMS_lumi.py)
 CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
 CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
 CMS_lumi.lumi_13TeV = "%.1f fb^{-1}"%(lumi/1000.)
 CMS_lumi.writeExtraText = 1
 CMS_lumi.extraText = "Preliminary"
 CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

 iPos = 11
 if( iPos==0 ): CMS_lumi.relPosX = 0.14

 H_ref = 600 
 W_ref = 600 
 W = W_ref
 H  = H_ref

 iPeriod = 0
 iPeriod = 4
 # references for T, B, L, R
 T = 0.08*H_ref
 B = 0.12*H_ref 
 L = 0.12*W_ref
 R = 0.04*W_ref

 pad = ROOT.TPad(name, name, 0, 0.3, 1, 1.0)
 pad.SetFillColor(0)
 pad.SetBorderMode(0)
 pad.SetFrameFillStyle(0)
 pad.SetFrameBorderMode(0)
 #pad.SetLeftMargin( L/W )
 #pad.SetRightMargin( R/W )
 pad.SetTopMargin( T/H )
 #pad.SetBottomMargin( B/H )
 pad.SetTickx(0)
 pad.SetTicky(0)
 
 return pad

def isSignal(sampleName):
        
 if 'Wprime' in sampleName or 'Bulk' in sampleName or 'Zprime' in sampleName: return True
 else: return False

def GetTotalHisto(label):

  f16 = ROOT.TFile.Open('%s/control_plots_2016/h_%s_%s.root'%(outdir,label,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_16 = getattr(f16, 'h_%s'%label)
  h_16.SetName('h_%s_2016'%label) 
  f17 = ROOT.TFile.Open('%s/control_plots_2017/h_%s_%s.root'%(outdir,label,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_17 = getattr(f17, 'h_%s'%label)
  h_17.SetName('h_%s_2017'%label)  
  f18 = ROOT.TFile.Open('%s/control_plots_2018/h_%s_%s.root'%(outdir,label,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_18 = getattr(f18, 'h_%s'%label)
  h_18.SetName('h_%s_2018'%label) 

  h_ = h_16.Clone('h_%s'%label)
  h_.SetDirectory(0)
  h_.Add(h_17)
  h_.Add(h_18) 
  
  print label,h_.Integral()
  
  return h_

def GetLegend(which):

 if which == 1:
  l = ROOT.TLegend(0.73,0.49,0.91,0.89)
 else: 
  l = ROOT.TLegend(0.55,0.68,0.72,0.89)
  
 l.SetTextSize(0.04) #0.05
 l.SetBorderSize(0)
 l.SetLineColor(1)
 l.SetLineStyle(1)
 l.SetLineWidth(1)
 l.SetFillColor(0)
 l.SetFillStyle(0)
 l.SetTextFont(42)
 
 return l

def GetRatioHisto(histoNum,histoDen,name,markerSize,lineStyle,titleX):

 ratiohist = histoNum.Clone(name)
 ratiohist.Divide(histoDen)
 ratiohist.SetMarkerColor(1)
 ratiohist.SetMarkerSize(markerSize)
 ratiohist.SetLineColor(ROOT.kBlack)
 ratiohist.SetLineStyle(lineStyle)
 ratiohist.GetYaxis().SetTitle("Data/MC")
 ratiohist.GetXaxis().SetTitle(titleX)
 ratiohist.GetYaxis().SetRangeUser(0.2,1.8)
 ratiohist.SetNdivisions(505,"x")
 ratiohist.SetNdivisions(105,"y")
 ratiohist.GetXaxis().SetLabelSize(0.15)
 ratiohist.GetXaxis().SetTitleSize(0.15)
 ratiohist.GetXaxis().SetTitleOffset(1.2)
 ratiohist.GetYaxis().SetLabelSize(0.15)
 ratiohist.GetYaxis().SetTitleSize(0.15)
 ratiohist.GetYaxis().SetTitleOffset(0.4)
 ratiohist.GetYaxis().CenterTitle()
 return ratiohist

   
#ranges and binning
minMJ=55.0
maxMJ=215.0
binsMJ=80

minMVV=1126.
maxMVV=7126.
binsMVV=100

minMX=1000.0
maxMX=7000.0

catVtag = {}
catHtag = {}

# For retuned DDT tau 21, use this
'''
catVtag['HP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.43'
catVtag['HP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.43'
catVtag['LP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.43&&(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.79'
catVtag['LP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.43&&(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.79'
catVtag['NP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.79'
catVtag['NP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.79'
'''
catVtag['HP1'] = 'jj_l1_MassDecorrelatedDeepBoosted_WvsQCD>0.8'                                                                                                                                                                                                                 
catVtag['HP2'] = 'jj_l2_MassDecorrelatedDeepBoosted_WvsQCD>0.8'                                                                                                                                                                                                                 
catVtag['LP1'] = 'jj_l1_MassDecorrelatedDeepBoosted_WvsQCD<0.8&&jj_l1_MassDecorrelatedDeepBoosted_WvsQCD>0.5'                                                                                                                                                                   
catVtag['LP2'] = 'jj_l2_MassDecorrelatedDeepBoosted_WvsQCD<0.8&&jj_l2_MassDecorrelatedDeepBoosted_WvsQCD>0.5'                                                                                                                                                                  
catVtag['NP1'] = 'jj_l1_MassDecorrelatedDeepBoosted_WvsQCD<0.5'                                                                                                                                                                                                                 
catVtag['NP2'] = 'jj_l2_MassDecorrelatedDeepBoosted_WvsQCD<0.5' 

catHtag['HP1'] = '(jj_l1_MassDecorrelatedDeepBoosted_ZHbbvsQCD>0.8)'
catHtag['HP2'] = '(jj_l2_MassDecorrelatedDeepBoosted_ZHbbvsQCD>0.8)'
catHtag['LP1'] = '(jj_l1_MassDecorrelatedDeepBoosted_ZHbbvsQCD>0.5&&jj_l1_MassDecorrelatedDeepBoosted_ZHbbvsQCD<0.8)'
catHtag['LP2'] = '(jj_l2_MassDecorrelatedDeepBoosted_ZHbbvsQCD>0.5&&jj_l2_MassDecorrelatedDeepBoosted_ZHbbvsQCD<0.8)'
catHtag['NP1'] = '(jj_l1_MassDecorrelatedDeepBoosted_ZHbbvsQCD<0.5)'
catHtag['NP2'] = '(jj_l2_MassDecorrelatedDeepBoosted_ZHbbvsQCD<0.5)'

cuts={}

cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(passed_METfilters&&passed_PVfilter&&njj>0&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.&&!njj_vbf)' #with rho
if doVBF:
 cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(passed_METfilters&&passed_PVfilter&&njj>0&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.&&njj_vbf)' #with rho 
cuts['acceptance']= "(jj_LV_mass>{minMVV}&&jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ}&&jj_l2_softDrop_mass>{minMJ}&&jj_l2_softDrop_mass<{maxMJ})".format(minMVV=minMVV,minMJ=minMJ,maxMJ=maxMJ)

#signal regions
print "Use random sorting!"
cuts['VH_HPHP'] = '(' + '('+  '&&'.join([catVtag['HP1'],catHtag['HP2']]) + ')' + '||' + '(' + '&&'.join([catVtag['HP2'],catHtag['HP1']]) + ')' + ')'
cuts['VH_HPLP'] = '(' + '('+  '&&'.join([catVtag['HP1'],catHtag['LP2']]) + ')' + '||' + '(' + '&&'.join([catVtag['HP2'],catHtag['LP1']]) + ')' + ')'
cuts['VH_LPHP'] = '(' + '('+  '&&'.join([catVtag['LP1'],catHtag['HP2']]) + ')' + '||' + '(' + '&&'.join([catVtag['LP2'],catHtag['HP1']]) + ')' + ')'
cuts['VH_LPLP'] = '(' + '('+  '&&'.join([catVtag['LP1'],catHtag['LP2']]) + ')' + '||' + '(' + '&&'.join([catVtag['LP2'],catHtag['LP1']]) + ')' + ')'
cuts['VH_all'] =  '('+  '||'.join([cuts['VH_HPHP'],cuts['VH_HPLP'],cuts['VH_LPHP'],cuts['VH_LPLP']]) + ')'
#cuts['VV_HPHP'] = '(' + '!' + cuts['VH_all'] + '&&' + '(' + '&&'.join([catVtag['HP1'],catVtag['HP2']]) + ')' + ')'
#cuts['VV_HPLP'] = '(' + '!' + cuts['VH_all'] + '&&' + '(' + '('+  '&&'.join([catVtag['HP1'],catVtag['LP2']]) + ')' + '||' + '(' + '&&'.join([catVtag['HP2'],catVtag['LP1']]) + ')' + ')' + ')'
cuts['VV_HPHP'] = '('  +  '&&'.join([catVtag['HP1'],catVtag['HP2']]) + ')' 
cuts['VV_HPLP'] = '('  + '(' +  '&&'.join([catVtag['HP1'],catVtag['LP2']]) + ')' + '||' + '(' + '&&'.join([catVtag['HP2'],catVtag['LP1']]) + ')' + ')'

#validation regions --> we might need more of these here (control region of b-tagging?)
cuts['VV_LPLP'] = '(' + '&&'.join([catVtag['LP1'],catVtag['LP2']]) + ')'

#define variables to plot, ranges and histo formatting config
vars = {
        'jj_LV_mass':{'minX':1126,'maxX':7126,'binsX':60,'titleX':'Dijet invariant mass [GeV]','scaleSig':0.0005,'maxY':100},
        'jj_l1_pt':{'minX':200,'maxX':3500,'binsX':66,'titleX':'Jet 1 p_{T} [GeV]','scaleSig':0.0001,'maxY':100},
	'jj_l2_pt':{'minX':200,'maxX':3500,'binsX':66,'titleX':'Jet 2 p_{T} [GeV]','scaleSig':0.0001,'maxY':100},
	'jj_l1_eta':{'minX':-2.4,'maxX':2.4,'binsX':48,'titleX':'Jet 1 #eta','scaleSig':30.,'maxY':1.7},
	'jj_l2_eta':{'minX':-2.4,'maxX':2.4,'binsX':48,'titleX':'Jet 2 #eta','scaleSig':30.,'maxY':1.7},
	'jj_l1_phi':{'minX':-3.2,'maxX':3.2,'binsX':32,'titleX':'Jet 1 #phi','scaleSig':25.,'maxY':2.0},
	'jj_l2_phi':{'minX':-3.2,'maxX':3.2,'binsX':32,'titleX':'Jet 2 #phi','scaleSig':25.,'maxY':2.0},
	'abs(jj_l1_eta-jj_l2_eta)':{'minX':0.0,'maxX':1.5,'binsX':15,'titleX':'#Delta#eta_{jj}','scaleSig':25.,'maxY':2.0},
	'jj_l1_softDrop_mass':{'minX':55,'maxX':215,'binsX':32,'titleX':'Jet 1 m_{SD} [GeV]','scaleSig':10.,'maxY':1.7},
	'jj_l2_softDrop_mass':{'minX':55,'maxX':215,'binsX':32,'titleX':'Jet 2 m_{SD} [GeV]','scaleSig':10,'maxY':1.7},
        '(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))':{'minX':0.2,'maxX':1.25,'binsX':21,'titleX':'Jet 1 #tau_{21}^{DDT} [GeV]','scaleSig':40.,'maxY':1.7},
        '(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))':{'minX':0.2,'maxX':1.25,'binsX':21,'titleX':'Jet 2 #tau_{21}^{DDT} [GeV]','scaleSig':40.,'maxY':1.7},
	'jj_l1_MassDecorrelatedDeepBoosted_ZHbbvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8 ZHbbvsQCD','scaleSig':0.05,'maxY':1500*100},
	'jj_l2_MassDecorrelatedDeepBoosted_ZHbbvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8 ZHbbvsQCD','scaleSig':0.05,'maxY':1500*100},
	'jj_l1_MassDecorrelatedDeepBoosted_WvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8 WvsQCD','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_MassDecorrelatedDeepBoosted_WvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8 WvsQCD','scaleSig':0.05,'maxY':10000*100},
	'nVert':{'minX':0,'maxX':60,'binsX':60,'titleX':'Primary vertices','scaleSig':25.,'maxY':1.7},
	}

if doVBF:
 vars = { 
        'jj_LV_mass':{'minX':1126,'maxX':7126,'binsX':60,'titleX':'Dijet invariant mass [GeV]','scaleSig':0.005,'maxY':100},
        'jj_l1_pt':{'minX':200,'maxX':3500,'binsX':66,'titleX':'Jet 1 p_{T} [GeV]','scaleSig':0.001,'maxY':100},
	'jj_l2_pt':{'minX':200,'maxX':3500,'binsX':66,'titleX':'Jet 2 p_{T} [GeV]','scaleSig':0.001,'maxY':100},
	'jj_l1_eta':{'minX':-2.4,'maxX':2.4,'binsX':48,'titleX':'Jet 1 #eta','scaleSig':5.,'maxY':1.7},
	'jj_l2_eta':{'minX':-2.4,'maxX':2.4,'binsX':48,'titleX':'Jet 2 #eta','scaleSig':5.,'maxY':1.7},
	'jj_l1_phi':{'minX':-3.2,'maxX':3.2,'binsX':32,'titleX':'Jet 1 #phi','scaleSig':5.,'maxY':2},
	'jj_l2_phi':{'minX':-3.2,'maxX':3.2,'binsX':32,'titleX':'Jet 2 #phi','scaleSig':5.,'maxY':2},
	'abs(jj_l1_eta-jj_l2_eta)':{'minX':0.0,'maxX':1.5,'binsX':15,'titleX':'#Delta#eta_{jj}','scaleSig':8.,'maxY':2},
	'jj_l1_softDrop_mass':{'minX':55,'maxX':215,'binsX':32,'titleX':'Jet 1 m_{SD} [GeV]','scaleSig':1.5,'maxY':1.7},
	'jj_l2_softDrop_mass':{'minX':55,'maxX':215,'binsX':32,'titleX':'Jet 2 m_{SD} [GeV]','scaleSig':1.5,'maxY':1.7},
        '(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))':{'minX':0.2,'maxX':1.25,'binsX':21,'titleX':'Jet 1 #tau_{21}^{DDT} [GeV]','scaleSig':10.,'maxY':1.7},
        '(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))':{'minX':0.2,'maxX':1.25,'binsX':21,'titleX':'Jet 2 #tau_{21}^{DDT} [GeV]','scaleSig':10.,'maxY':1.7},
	'jj_l1_MassDecorrelatedDeepBoosted_ZHbbvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8 ZHbbvsQCD','scaleSig':0.05,'maxY':1500*100},
	'jj_l2_MassDecorrelatedDeepBoosted_ZHbbvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8 ZHbbvsQCD','scaleSig':0.05,'maxY':1500*100},
	'jj_l1_MassDecorrelatedDeepBoosted_WvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8 WvsQCD','scaleSig':0.05,'maxY':1500*100},
	'jj_l2_MassDecorrelatedDeepBoosted_WvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8 WvsQCD','scaleSig':0.05,'maxY':1500*100},
	'abs(vbf_jj_l1_eta-vbf_jj_l2_eta)':{'minX':4.5,'maxX':10,'binsX':22,'titleX':'#Delta#eta_{jj}^{VBF}','scaleSig':10,'maxY':1.7},
	'vbf_jj_l1_eta':{'minX':-5.0,'maxX':5.0,'binsX':50,'titleX':'VBF jet 1 #eta','scaleSig':3,'maxY':2},
	'vbf_jj_l2_eta':{'minX':-5.0,'maxX':5.0,'binsX':50,'titleX':'VBF jet 2 #eta','scaleSig':3,'maxY':2},  
	'vbf_jj_l1_phi':{'minX':-3.2,'maxX':3.2,'binsX':32,'titleX':'VBF jet 1 #phi','scaleSig':3,'maxY':2},
	'vbf_jj_l2_phi':{'minX':-3.2,'maxX':3.2,'binsX':32,'titleX':'VBF jet 2 #phi','scaleSig':3,'maxY':2},
	'vbf_jj_LV_mass':{'minX':800,'maxX':10000,'binsX':92,'titleX':'VBF jets invariant mass [GeV]','scaleSig':0.01,'maxY':100},
        'vbf_jj_l1_pt':{'minX':50,'maxX':1450,'binsX':56,'titleX':'VBF jet 1 p_{T} [GeV]','scaleSig':0.01,'maxY':100},
	'vbf_jj_l2_pt':{'minX':50,'maxX':750,'binsX':28,'titleX':'VBF jet 2 p_{T} [GeV]','scaleSig':0.01,'maxY':100},
 }

cut='*'.join([cuts['common'],cuts['acceptance']])

if year == '2016': lumi = 35.9*1000.
elif year == '2017': lumi = 41.5*1000.
elif year == '2018': lumi = 59.7*1000.  
elif year == 'ALL': lumi = 137.2*1000.

if not os.path.exists('%s/control_plots_%s'%(outdir,year)):
 os.mkdir('%s/control_plots_%s'%(outdir,year))
  
if year == 'ALL':

 for k,v in vars.iteritems():

  print "======================================================="
  print "make histos for variable:",v['titleX']
  print "======================================================="
    
  h_data = GetTotalHisto('data') 
  h_wjets = GetTotalHisto('wjets')  
  h_zjets = GetTotalHisto('zjets')  
  h_tt = GetTotalHisto('tt')  
  h_qcd = GetTotalHisto('qcd')
  h_qcd_mg = GetTotalHisto('qcd_mg')
  h_qcd_herw = GetTotalHisto('qcd_herw')
  h_sig1 = GetTotalHisto('sig1')
  h_sig2 = GetTotalHisto('sig2')
  h_sig3 = GetTotalHisto('sig3')
  h_sig4 = GetTotalHisto('sig4')

  hstack = ROOT.THStack("hstack","hstack");
  hstack.Add(h_tt)
  hstack.Add(h_zjets)
  hstack.Add(h_wjets)
  hstack.Add(h_qcd)

  leg1 = GetLegend(1)
  leg1.AddEntry(h_data,'Data','PE')
  leg1.AddEntry(h_qcd,'QCD Pythia8','F')
  leg1.AddEntry(h_qcd_mg,'QCD MG+Pythia8','L')
  leg1.AddEntry(h_qcd_herw,'QCD Herwig++','L')
  leg1.AddEntry(h_wjets,'W+jets','F')
  leg1.AddEntry(h_zjets,'Z+jets','F')
  leg1.AddEntry(h_tt,'t#bar{t}','F')

  leg2 = GetLegend(2)
  if not doVBF: leg2.AddEntry(h_sig1,"Z'#rightarrow ZH","L")
  leg2.AddEntry(h_sig2,"W'#rightarrow WZ","L")
  leg2.AddEntry(h_sig3,"G #rightarrow ZZ","L")
  leg2.AddEntry(h_sig4,"G #rightarrow WW","L")
 
  c = ROOT.TCanvas('c')
  pad1 = get_pad("pad1",lumi) #ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
  pad1.SetBottomMargin(0.01)    
  pad1.SetTopMargin(0.1) 
  if 'jj_LV_mass' in k or 'MassDecorrelated' in k or k=='jj_l1_pt' or k=='jj_l2_pt' or k=='vbf_jj_l1_pt' or k=='vbf_jj_l2_pt':pad1.SetLogy()
  pad1.Draw()
  pad1.cd()
 
  h_data.Draw("PE")
  h_data.GetXaxis().SetTitle(v['titleX'])
  h_data.GetYaxis().SetTitle('Events')
  h_data.SetMinimum(0.005)
  h_data.SetMaximum(h_data.GetMaximum()*v['maxY'])
  hstack.Draw("HISTsame")
  h_qcd_mg.Draw("HISTsame")
  h_qcd_herw.Draw("HISTsame")
  h_data.Draw("PEsame")
  if not doVBF: h_sig1.Draw("HISTsame")
  h_sig2.Draw("HISTsame")
  h_sig3.Draw("HISTsame")
  h_sig4.Draw("HISTsame")
  leg1.Draw()
  leg2.Draw()

  pt = ROOT.TPaveText(0.5334448,0.5121951,0.8929766,0.7735192,"NDC")
  pt.SetTextFont(62)
  pt.SetTextSize(0.04)
  pt.SetTextAlign(12)
  pt.SetFillColor(0)
  pt.SetBorderSize(0)
  pt.SetFillStyle(0)   
  if doVBF:
   pt.AddText("VBF channel")
  else:
   pt.AddText("ggF/DY channel")
  pt.Draw()
      
  CMS_lumi.CMS_lumi(pad1, 4, 11)
  pad1.Modified()
  pad1.Update()
  c.Update()
  c.cd()

  pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
  pad2.SetTopMargin(0.01)
  pad2.SetBottomMargin(0.4)
  pad2.SetGridy()
  pad2.Draw()
  pad2.cd()
 
  htotmc_mg = ROOT.TH1F("h_tot_mc_mg","h_tot_mc_mg",v['binsX'],v['minX'],v['maxX'])
  htotmc_mg.Add(h_qcd_mg)
  htotmc_mg.Add(h_tt)
  htotmc_mg.Add(h_wjets)
  htotmc_mg.Add(h_zjets)
  ratiohist_mg = GetRatioHisto(h_data,htotmc_mg,"ratiohist_mg",0,2,v['titleX'])
  for b in range(1,ratiohist_mg.GetNbinsX()+1): ratiohist_mg.SetBinError(b,0)
  ratiohist_mg.Draw("")
  ratiohist_mg.Draw("HISTsame")

  htotmc_herw = ROOT.TH1F("h_tot_mc_herw","h_tot_mc_herw",v['binsX'],v['minX'],v['maxX'])
  htotmc_herw.Add(h_qcd_herw)
  htotmc_herw.Add(h_tt)
  htotmc_herw.Add(h_wjets)
  htotmc_herw.Add(h_zjets)
  ratiohist_herw = GetRatioHisto(h_data,htotmc_herw,"ratiohist_herw",0,3,v['titleX']) #GetRatioHisto(histoNum,histoDen,name,markerSize,lineStyle,titleX):
  for b in range(1,ratiohist_herw.GetNbinsX()+1): ratiohist_herw.SetBinError(b,0)
  ratiohist_herw.Draw("HISTsame")
       
  htotmc = ROOT.TH1F("h_tot_mc","h_tot_mc",v['binsX'],v['minX'],v['maxX'])
  htotmc.Add(h_qcd)
  htotmc.Add(h_tt)
  htotmc.Add(h_wjets)
  htotmc.Add(h_zjets)
  ratiohist = GetRatioHisto(h_data,htotmc,"ratiohist",1,1,v['titleX'])
  ratiohist.Draw("same")

  pad2.Modified()
  pad2.Update()
  c.cd()
  c.Update()
  c.Modified()
  c.Update()
  c.cd()
  c.SetSelected(c)

  c.SaveAs('%s/control_plots_%s/h_final_%s.pdf'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))    
  c.SaveAs('%s/control_plots_%s/h_final_%s.png'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
  c.SaveAs('%s/control_plots_%s/h_final_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
  c.SaveAs('%s/control_plots_%s/h_final_%s.C'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 
 sys.exit()
          



for k,v in vars.iteritems():

 print "======================================================="
 print "make histos for variable:",v['titleX']
 print "======================================================="
 
 if not loadHistos: 
  histos_data = []

  i = 0
  directory='deepAK8V2/%s/'%year
  for f in os.listdir(directory):
   if 'JetHT' in f and '.root' in f:
    tf = ROOT.TFile.Open(directory+f,'READ')
    tree = tf.AnalysisTree
    ROOT.gROOT.cd()
    htemp = ROOT.gROOT.FindObject("htemp")
    if htemp: htemp.Delete()
    print "Draw histo for file",f
    tree.Draw("%s>>htemp_%i(%i,%f,%f)"%(k,i+1,v['binsX'],v['minX'],v['maxX']), cut);
    htemp = ROOT.gROOT.FindObject("htemp_%i"%(i+1))
    histos_data.append(htemp)
    tf.Close()
    i+=1

  h_data = ROOT.TH1F("h_data","h_data",v['binsX'],v['minX'],v['maxX'])
  h_data.SetLineWidth(2)
  h_data.SetLineColor(ROOT.kBlack)
  h_data.SetMarkerStyle(20)
  h_data.SetMarkerColor(ROOT.kBlack)
  for h in histos_data: h_data.Add(h)
  c_data = ROOT.TCanvas('c_data','c_data')
  c_data.cd()
  if 'jj_LV_mass' in k or 'MassDecorrelated' in k or k=='jj_l1_pt' or k=='jj_l2_pt' or k=='vbf_jj_l1_pt' or k=='vbf_jj_l2_pt':c_data.SetLogy()
  h_data.Draw("PE0")
  h_data.SaveAs('%s/control_plots_%s/h_data_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#',''))) 
  c_data.SaveAs('%s/control_plots_%s/h_data_%s.png'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fdata = ROOT.TFile.Open('%s/control_plots_%s/h_data_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_data = fdata.h_data
    
 mc_samples = []
 mc_folders = []
 
 if year == '2016':
  mc_samples = ['WJetsToQQ','ZJetsToQQ','TT','QCD_Pt_','QCD_HT','QCD_Pt-','ZprimeToZhToZhadhbb_narrow_2000','WprimeToWZToWhadZhad_narrow_2000','BulkGravToZZToZhadZhad_narrow_2000','BulkGravToWW_narrow_2000']
  mc_folders = ['2018','2018','2016','2016','2016','2016','2016','2016','2016','2016']
 elif year == '2017':
  mc_samples = ['WJetsToQQ','ZJetsToQQ','TT','QCD_Pt_','QCD_HT','QCD_Pt-','ZprimeToZhToZhadhbb_narrow_2000','WprimeToWZToWhadZhad_narrow_2000','BulkGravToZZToZhadZhad_narrow_2000','BulkGravToWW_narrow_2000']
  mc_folders = ['2018','2018','2017','2017','2017','2017','2016','2016','2016','2016']
 elif year == '2018':
  mc_samples = ['WJetsToQQ','ZJetsToQQ','TT','QCD_Pt_','QCD_HT','QCD_Pt-','ZprimeToZhToZhadhbb_narrow_2000','WprimeToWZToWhadZhad_narrow_2000','BulkGravToZZToZhadZhad_narrow_2000','BulkGravToWW_narrow_2000']
  mc_folders = ['2018','2018','2018','2018','2018','2018','2016','2016','2016','2016']
  
 if doVBF:
  mc_samples[6] = 'ZprimeToZhToZhadhbb_narrow_2000' #replace at some point with VBF version
  mc_samples[7] = 'VBF_WprimeToWZ_narrow_2000'
  mc_samples[8] = 'VBF_BulkGravToZZ_narrow_2000'
  mc_samples[9] = 'VBF_BulkGravToWW_narrow_2000'
       
 histos_mc = {}

 for i,s in enumerate(mc_samples):
  
  if loadHistos and not isSignal(s): continue  
  histos_mc[s] = []
  
  for f in os.listdir(mc_folders[i]):
   if not '.root' in f: continue
   if not s in f: continue
   if not doVBF and 'VBF' in f: continue
   
   fpck=open(mc_folders[i]+"/"+f.replace('.root','.pck'))
   dpck=pickle.load(fpck)
   weightinv = float(dpck['events'])
	
   tf = ROOT.TFile.Open(mc_folders[i]+"/"+f,'READ')
   tree = tf.AnalysisTree
   ROOT.gROOT.cd()
   htemp = ROOT.gROOT.FindObject("htemp")
   if htemp: htemp.Delete()
   print "Draw histo for file",f
   if f.find("QCD_Pt_") !=-1 or f.find("QCD_HT") !=-1:
    print "spike killer "
    if not 'part' in f: tree.Draw("%s>>htemp_%s(%i,%f,%f)"%(k,f.replace('.root',''),v['binsX'],v['minX'],v['maxX']), '(genWeight*xsec*puWeight*b_spikekiller*%f)*'%(lumi*1./weightinv)+cut);
    else: tree.Draw("%s>>htemp_%s(%i,%f,%f)"%(k,f.replace('.root',''),v['binsX'],v['minX'],v['maxX']), '(genWeight*xsec*puWeight*b_spikekiller*%f)*'%(lumi)+cut);
   else:
    if not 'part' in f: tree.Draw("%s>>htemp_%s(%i,%f,%f)"%(k,f.replace('.root',''),v['binsX'],v['minX'],v['maxX']), '(genWeight*xsec*puWeight*%f)*'%(lumi*1./weightinv)+cut);
    else: tree.Draw("%s>>htemp_%s(%i,%f,%f)"%(k,f.replace('.root',''),v['binsX'],v['minX'],v['maxX']), '(genWeight*xsec*puWeight*%f)*'%(lumi)+cut);
   htemp = ROOT.gROOT.FindObject("htemp_%s"%(f.replace('.root','')))
   histos_mc[s].append(htemp)
   tf.Close()
 
 if not loadHistos: 
  h_wjets = ROOT.TH1F("h_wjets","h_wjets",v['binsX'],v['minX'],v['maxX'])  
  h_wjets.SetLineWidth(2)
  h_wjets.SetLineColor(ROOT.kBlack)
  h_wjets.SetFillColor(ROOT.kRed-7)
  for h in histos_mc['WJetsToQQ']: h_wjets.Add(h)
  c_wjets = ROOT.TCanvas('c_wjets','c_wjets')
  c_wjets.cd()
  if 'jj_LV_mass' in k or 'MassDecorrelated' in k or k=='jj_l1_pt' or k=='jj_l2_pt' or k=='vbf_jj_l1_pt' or k=='vbf_jj_l2_pt':c_wjets.SetLogy()
  h_wjets.Draw("HIST")
  h_wjets.SaveAs('%s/control_plots_%s/h_wjets_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#',''))) 
  c_wjets.SaveAs('%s/control_plots_%s/h_wjets_%s.png'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fwjets = ROOT.TFile.Open('%s/control_plots_%s/h_wjets_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_wjets = fwjets.h_wjets
 
 if not loadHistos: 
  h_zjets = ROOT.TH1F("h_zjets","h_zjets",v['binsX'],v['minX'],v['maxX'])  
  h_zjets.SetLineWidth(2)
  h_zjets.SetLineColor(ROOT.kBlack)
  h_zjets.SetFillColor(ROOT.kBlue-7)
  for h in histos_mc['ZJetsToQQ']: h_zjets.Add(h)
  c_zjets = ROOT.TCanvas('c_zjets','c_zjets')
  c_zjets.cd()
  if 'jj_LV_mass' in k or 'MassDecorrelated' in k or k=='jj_l1_pt' or k=='jj_l2_pt' or k=='vbf_jj_l1_pt' or k=='vbf_jj_l2_pt':c_zjets.SetLogy()
  h_zjets.Draw("HIST")
  h_zjets.SaveAs('%s/control_plots_%s/h_zjets_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#',''))) 
  c_zjets.SaveAs('%s/control_plots_%s/h_zjets_%s.png'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fzjets = ROOT.TFile.Open('%s/control_plots_%s/h_zjets_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_zjets = fzjets.h_zjets
 
 if not loadHistos:  
  h_tt = ROOT.TH1F("h_tt","h_tt",v['binsX'],v['minX'],v['maxX'])
  h_tt.SetLineWidth(2)
  h_tt.SetLineColor(ROOT.kBlack)
  h_tt.SetFillColor(ROOT.kTeal+2)
  for h in histos_mc['TT']: h_tt.Add(h)
  c_tt = ROOT.TCanvas('c_tt','c_tt')
  c_tt.cd()
  if 'jj_LV_mass' in k or 'MassDecorrelated' in k or k=='jj_l1_pt' or k=='jj_l2_pt' or k=='vbf_jj_l1_pt' or k=='vbf_jj_l2_pt':c_tt.SetLogy()
  h_tt.Draw("HIST")
  h_tt.SaveAs('%s/control_plots_%s/h_tt_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#',''))) 
  c_tt.SaveAs('%s/control_plots_%s/h_tt_%s.png'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  ftt = ROOT.TFile.Open('%s/control_plots_%s/h_tt_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_tt = ftt.h_tt
   
 if not loadHistos:  
  h_qcd = ROOT.TH1F("h_qcd","h_qcd",v['binsX'],v['minX'],v['maxX'])
  h_qcd.SetLineWidth(2)
  h_qcd.SetLineColor(ROOT.kBlack)
  h_qcd.SetFillColor(ROOT.kMagenta-10)
  htemps = {}
  for h in histos_mc['QCD_Pt_']:
    h_qcd.Add(h)
  sf = (h_data.Integral()-h_wjets.Integral()-h_zjets.Integral()-h_tt.Integral())/h_qcd.Integral()
  print "Use scale factor for pythia8",sf
  c_qcd = ROOT.TCanvas('c_qcd','c_qcd')
  c_qcd.cd()
  if 'jj_LV_mass' in k or 'MassDecorrelated' in k or k=='jj_l1_pt' or k=='jj_l2_pt' or k=='vbf_jj_l1_pt' or k=='vbf_jj_l2_pt':c_qcd.SetLogy()
  h_qcd.Scale(sf)
  h_qcd.Draw("HIST")
  h_qcd.SaveAs('%s/control_plots_%s/h_qcd_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#',''))) 
  c_qcd.SaveAs('%s/control_plots_%s/h_qcd_%s.png'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fqcd = ROOT.TFile.Open('%s/control_plots_%s/h_qcd_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_qcd = fqcd.h_qcd

 if not loadHistos:   
  h_qcd_mg = ROOT.TH1F("h_qcd_mg","h_qcd_mg",v['binsX'],v['minX'],v['maxX'])
  h_qcd_mg.SetLineWidth(2)
  h_qcd_mg.SetLineStyle(2)
  h_qcd_mg.SetLineColor(ROOT.kBlack)
  for h in histos_mc['QCD_HT']: h_qcd_mg.Add(h)
  sf = (h_data.Integral()-h_wjets.Integral()-h_zjets.Integral()-h_tt.Integral())/h_qcd_mg.Integral()
  print "Use scale factor for madgraph",sf
  c_qcd_mg = ROOT.TCanvas('c_qcd_mg','c_qcd_mg')
  c_qcd_mg.cd()
  if 'jj_LV_mass' in k or 'MassDecorrelated' in k or k=='jj_l1_pt' or k=='jj_l2_pt' or k=='vbf_jj_l1_pt' or k=='vbf_jj_l2_pt':c_qcd_mg.SetLogy()
  h_qcd_mg.Scale(sf)
  h_qcd_mg.Draw("HIST")
  h_qcd_mg.SaveAs('%s/control_plots_%s/h_qcd_mg_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#',''))) 
  c_qcd_mg.SaveAs('%s/control_plots_%s/h_qcd_mg_%s.png'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fqcd_mg = ROOT.TFile.Open('%s/control_plots_%s/h_qcd_mg_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_qcd_mg = fqcd_mg.h_qcd_mg

 if not loadHistos:   
  h_qcd_herw = ROOT.TH1F("h_qcd_herw","h_qcd_herw",v['binsX'],v['minX'],v['maxX'])
  h_qcd_herw.SetLineWidth(2)
  h_qcd_herw.SetLineStyle(2)
  h_qcd_herw.SetLineColor(ROOT.kBlack)
  h_qcd_herw.SetLineStyle(3)
  for h in histos_mc['QCD_Pt-']: h_qcd_herw.Add(h)
  sf = (h_data.Integral()-h_wjets.Integral()-h_zjets.Integral()-h_tt.Integral())/h_qcd_herw.Integral()
  print "Use scale factor for herwig",sf
  c_qcd_herw = ROOT.TCanvas('c_qcd_herw','c_qcd_herw')
  c_qcd_herw.cd()
  if 'jj_LV_mass' in k or 'MassDecorrelated' in k or k=='jj_l1_pt' or k=='jj_l2_pt' or k=='vbf_jj_l1_pt' or k=='vbf_jj_l2_pt':c_qcd_herw.SetLogy()
  h_qcd_herw.Scale(sf)
  h_qcd_herw.Draw("HIST")
  h_qcd_herw.SaveAs('%s/control_plots_%s/h_qcd_herw_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#',''))) 
  c_qcd_herw.SaveAs('%s/control_plots_%s/h_qcd_herw_%s.png'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fqcd_herw = ROOT.TFile.Open('%s/control_plots_%s/h_qcd_herw_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_qcd_herw = fqcd_herw.h_qcd_herw
      
 h_sig1 = ROOT.TH1F("h_sig1","h_sig1",v['binsX'],v['minX'],v['maxX'])
 h_sig1.SetLineWidth(2)
 h_sig1.SetLineColor(ROOT.kPink+4)
 h_sig1.Add(histos_mc['ZprimeToZhToZhadhbb_narrow_2000'][0])
 if k=='jj_l1_eta' or k=='jj_l2_eta' or k=='vbf_jj_l1_eta' or k=='vbf_jj_l2_eta': h_sig1.Scale(30.)
 elif 'MassDecorrelated' in k: h_sig1.Scale(0.05)
 elif 'jj_LV_mass' in k: h_sig1.Scale(0.0005)
 elif k.find('softDrop') != -1: h_sig1.Scale(10)
 elif k=='jj_l1_pt' or k=='jj_l2_pt' or k=='vbf_jj_l1_pt' or k=='vbf_jj_l2_pt': h_sig1.Scale(0.0001)
 else: h_sig1.Scale(25.)
 h_sig1.SaveAs('%s/control_plots_%s/h_sig1_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#',''))) 
    
 h_sig2 = ROOT.TH1F("h_sig2","h_sig2",v['binsX'],v['minX'],v['maxX'])
 h_sig2.SetLineWidth(2)
 h_sig2.SetLineColor(ROOT.kAzure+10)
 for hk in histos_mc.keys():
  if 'WprimeToWZ' in hk: h_sig2.Add(histos_mc[hk][0])
 h_sig2.Scale(v['scaleSig'])
 h_sig2.SaveAs('%s/control_plots_%s/h_sig2_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#',''))) 
    
 h_sig3 = ROOT.TH1F("h_sig3","h_sig3",v['binsX'],v['minX'],v['maxX'])
 h_sig3.SetLineWidth(2)
 h_sig3.SetLineColor(ROOT.kOrange+1)
 for hk in histos_mc.keys():
  if 'BulkGravToZZ' in hk: h_sig3.Add(histos_mc[hk][0])
 h_sig3.Scale(v['scaleSig'])
 h_sig3.SaveAs('%s/control_plots_%s/h_sig3_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#',''))) 
  
 h_sig4 = ROOT.TH1F("h_sig4","h_sig4",v['binsX'],v['minX'],v['maxX'])
 h_sig4.SetLineWidth(2)
 h_sig4.SetLineColor(ROOT.kGray+2)
 for hk in histos_mc.keys():
  if 'BulkGravToWW' in hk: h_sig4.Add(histos_mc[hk][0])
 h_sig4.Scale(v['scaleSig'])
 h_sig4.SaveAs('%s/control_plots_%s/h_sig4_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#',''))) 
     
 hstack = ROOT.THStack("hstack","hstack");
 hstack.Add(h_tt)
 hstack.Add(h_zjets)
 hstack.Add(h_wjets)
 hstack.Add(h_qcd)
 
 leg1 = GetLegend(1)
 leg1.AddEntry(h_data,'Data','PE')
 leg1.AddEntry(h_qcd,'QCD Pythia8','F')
 leg1.AddEntry(h_qcd_mg,'QCD MG+Pythia8','L')
 leg1.AddEntry(h_qcd_herw,'QCD Herwig++','L')
 leg1.AddEntry(h_wjets,'W+jets','F')
 leg1.AddEntry(h_zjets,'Z+jets','F')
 leg1.AddEntry(h_tt,'t#bar{t}','F')

 leg2 = GetLegend(2)
 if not doVBF: leg2.AddEntry(h_sig1,"Z'#rightarrow ZH","L")
 leg2.AddEntry(h_sig2,"W'#rightarrow WZ","L")
 leg2.AddEntry(h_sig3,"G #rightarrow ZZ","L")
 leg2.AddEntry(h_sig4,"G #rightarrow WW","L")
 
 c = ROOT.TCanvas('c')
 pad1 = get_pad("pad1",lumi) #ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
 pad1.SetBottomMargin(0.01)    
 pad1.SetTopMargin(0.1) 
 if 'jj_LV_mass' in k or 'MassDecorrelated' in k or k=='jj_l1_pt' or k=='jj_l2_pt' or k=='vbf_jj_l1_pt' or k=='vbf_jj_l2_pt':pad1.SetLogy()
 pad1.Draw()
 pad1.cd()
 
 h_data.Draw("PE")
 h_data.GetXaxis().SetTitle(v['titleX'])
 h_data.GetYaxis().SetTitle('Events')
 h_data.SetMinimum(0.005)
 h_data.SetMaximum(h_data.GetMaximum()*v['maxY'])
 hstack.Draw("HISTsame")
 h_qcd_mg.Draw("HISTsame")
 h_qcd_herw.Draw("HISTsame")
 h_data.Draw("PEsame")
 if not doVBF: h_sig1.Draw("HISTsame")
 h_sig2.Draw("HISTsame")
 h_sig3.Draw("HISTsame")
 h_sig4.Draw("HISTsame")
 leg1.Draw()
 leg2.Draw()

 if doVBF:
  pt = ROOT.TPaveText(0.5334448,0.5121951,0.8929766,0.7735192,"NDC")
  pt.SetTextFont(62)
  pt.SetTextSize(0.04)
  pt.SetTextAlign(12)
  pt.SetFillColor(0)
  pt.SetBorderSize(0)
  pt.SetFillStyle(0)   
  pt.AddText("VBF channel")
 else:
  pt = ROOT.TPaveText(0.4983278,0.5121951,0.8578595,0.7735192,"NDC")
  pt.SetTextFont(62)
  pt.SetTextSize(0.04)
  pt.SetTextAlign(12)
  pt.SetFillColor(0)
  pt.SetBorderSize(0)
  pt.SetFillStyle(0)   
  pt.AddText("ggF/DY channel")
 pt.Draw()
   
 CMS_lumi.CMS_lumi(pad1, 4, 11)
 pad1.Modified()
 pad1.Update()
 c.Update()
 c.cd()

 pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
 pad2.SetTopMargin(0.01)
 pad2.SetBottomMargin(0.4)
 pad2.SetGridy()
 pad2.Draw()
 pad2.cd()

 htotmc_mg = ROOT.TH1F("h_tot_mc_mg","h_tot_mc_mg",v['binsX'],v['minX'],v['maxX'])
 htotmc_mg.Add(h_qcd_mg)
 htotmc_mg.Add(h_tt)
 htotmc_mg.Add(h_wjets)
 htotmc_mg.Add(h_zjets)
 ratiohist_mg = GetRatioHisto(h_data,htotmc_mg,"ratiohist_mg",0,2,v['titleX'])
 for b in range(1,ratiohist_mg.GetNbinsX()+1): ratiohist_mg.SetBinError(b,0)
 ratiohist_mg.Draw("")
 ratiohist_mg.Draw("HISTsame")

 htotmc_herw = ROOT.TH1F("h_tot_mc_herw","h_tot_mc_herw",v['binsX'],v['minX'],v['maxX'])
 htotmc_herw.Add(h_qcd_herw)
 htotmc_herw.Add(h_tt)
 htotmc_herw.Add(h_wjets)
 htotmc_herw.Add(h_zjets)
 ratiohist_herw = GetRatioHisto(h_data,htotmc_herw,"ratiohist_herw",0,3,v['titleX']) #GetRatioHisto(histoNum,histoDen,name,markerSize,lineStyle,titleX):
 for b in range(1,ratiohist_herw.GetNbinsX()+1): ratiohist_herw.SetBinError(b,0)
 ratiohist_herw.Draw("HISTsame")
       
 htotmc = ROOT.TH1F("h_tot_mc","h_tot_mc",v['binsX'],v['minX'],v['maxX'])
 htotmc.Add(h_qcd)
 htotmc.Add(h_tt)
 htotmc.Add(h_wjets)
 htotmc.Add(h_zjets)
 ratiohist = GetRatioHisto(h_data,htotmc,"ratiohist",1,1,v['titleX'])
 ratiohist.Draw()

 pad2.Modified()
 pad2.Update()
 c.cd()
 c.Update()
 c.Modified()
 c.Update()
 c.cd()
 c.SetSelected(c)

 c.SaveAs('%s/control_plots_%s/h_final_%s.pdf'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))    
 c.SaveAs('%s/control_plots_%s/h_final_%s.png'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 c.SaveAs('%s/control_plots_%s/h_final_%s.root'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 c.SaveAs('%s/control_plots_%s/h_final_%s.C'%(outdir,year,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))

