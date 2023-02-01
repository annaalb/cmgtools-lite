#python make-control-plots-submit.py 2016 None True _jobs
import ROOT
from ROOT import *
import os, time, pickle, sys, optparse
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
import CMS_lumi, tdrstyle
tdrstyle.setTDRStyle()
ROOT.v5.TFormula.SetMaxima(10000)

def makeSubmitFileCondor(exe,jobname,jobflavour,localinput=False,cmst3=False):
    print "make options file for condor job submission "
    submitfile = open("submit.sub","w")
    submitfile.write("should_transfer_files = YES\n")
    submitfile.write("when_to_transfer_output = ON_EXIT\n")
    submitfile.write('transfer_output_files = ""\n')
    submitfile.write("executable  = "+exe+"\n")

    if localinput:
      submitfile.write("arguments             = $(ClusterID) $(ProcId)\n")
    else:
     #submitfile.write("Proxy_filename = x509up_%s\n"%os.getenv("USER"))
     #submitfile.write("Proxy_path = %s/$(Proxy_filename)\n"%os.getenv("HOME"))
     submitfile.write("Proxy_filename = myproxy\n")
     submitfile.write("Proxy_path = %s/private/proxy/$(Proxy_filename)\n"%os.getenv("HOME"))
     submitfile.write("transfer_input_files = $(Proxy_path)\n")
     submitfile.write("arguments             = $(Proxy_path) $(ClusterID) $(ProcId)\n")

    submitfile.write("output                = "+jobname+".$(ClusterId).$(ProcId).out\n")
    submitfile.write("error                 = "+jobname+".$(ClusterId).$(ProcId).err\n")
    submitfile.write("log                   = "+jobname+".$(ClusterId).log\n")
    submitfile.write('+JobFlavour           = "'+jobflavour+'"\n')
    if cmst3:
     submitfile.write("+AccountingGroup = group_u_CMST3.all\n")
    submitfile.write("queue")
    submitfile.close()

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

 if 'Wprime' in sampleName or 'Bulk' in sampleName or 'Zprime' in sampleName or 'Radion' in sampleName or 'Qstar' in sampleName or 'ALP' in sampleName: return True
 else: return False

def GetTotalHisto(sample):

  f16 = ROOT.TFile.Open('%s/control_plots_2016%s/h_%s_%s.root'%(outdir,label,sample,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_16 = getattr(f16, 'h_%s'%sample)
  h_16.SetName('h_%s_2016'%sample)
  f17 = ROOT.TFile.Open('%s/control_plots_2017%s/h_%s_%s.root'%(outdir,label,sample,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_17 = getattr(f17, 'h_%s'%sample)
  h_17.SetName('h_%s_2017'%sample)
  f18 = ROOT.TFile.Open('%s/control_plots_2018%s/h_%s_%s.root'%(outdir,label,sample,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_18 = getattr(f18, 'h_%s'%sample)
  h_18.SetName('h_%s_2018'%sample)

  h_ = h_16.Clone('h_%s'%sample)
  h_.SetDirectory(0)
  h_.Add(h_17)
  h_.Add(h_18)

  print sample,h_.Integral()

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

def MakeHist(var,settings,jobid,samplesDir, samplesDirALP,cut,outdir,year,lumi,doVBF,doInclusive,loadHistos,unblind):

 print "======================================================="
 print "make histos for variable:",settings['titleX'],"jobid",jobid
 print "======================================================="

 if not loadHistos:
  histos_data = []

  i = 0
  for f in os.listdir(samplesDir):
   if 'JetHT' in f and '.root' in f:
    tf = ROOT.TFile.Open(samplesDir+"/"+f,'READ')
    tree = tf.AnalysisTree
    ROOT.gROOT.cd()
    htemp = ROOT.gROOT.FindObject("htemp")
    if htemp: htemp.Delete()
    print "Draw histo for file",f
    tree.Draw("%s>>htemp_%i(%i,%f,%f)"%(var,i+1,settings['binsX'],settings['minX'],settings['maxX']), cut)
    htemp = ROOT.gROOT.FindObject("htemp_%i"%(i+1))
    histos_data.append(htemp)
    tf.Close()
    i+=1

  h_data = ROOT.TH1F("h_data","h_data",settings['binsX'],settings['minX'],settings['maxX'])
  h_data.SetLineWidth(2)
  h_data.SetLineColor(ROOT.kBlack)
  h_data.SetMarkerStyle(20)
  h_data.SetMarkerColor(ROOT.kBlack)
  for h in histos_data: h_data.Add(h)
  c_data = ROOT.TCanvas('c_data','c_data')
  c_data.cd()
  if 'jj_LV_mass' in var or 'ZHbbvsQCD' in var or 'WvsQCD' in var or var=='jj_l1_pt' or var=='jj_l2_pt' or var=='vbf_jj_l1_pt' or var=='vbf_jj_l2_pt':c_data.SetLogy()
  h_data.Draw("PE0")
  h_data.SaveAs('%s/control_plots_%s%s/h_data_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
  c_data.SaveAs('%s/control_plots_%s%s/h_data_%s.png'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fdata = ROOT.TFile.Open('%s/control_plots_%s%s/h_data_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_data = fdata.h_data

 mc_samples = []
 mc_folders = []
 signal_legend = ["G #rightarrow ZZ","ALP #rightarrow ZZ"]

 if year == '2016':
  mc_samples = ['WW','WZ','ZZ','_HToBB_','WJetsToQQ','ZJetsToQQ','TT_Mtt','QCD_Pt_','QCD_HT','QCD_Pt-','ZprimeToZhToZhadhbb_narrow_2000','WprimeToWZToWhadZhad_narrow_2000','BulkGravToZZToZhadZhad_narrow_2000','BulkGravToWW_narrow_2000', 'ALPtoZZ']
  mc_folders = [samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir, samplesDirALP]
 elif year == '2017':
  mc_samples = ['WW','WZ','ZZ','_HToBB_','WJetsToQQ','ZJetsToQQ','TT_Mtt','QCD_Pt_','QCD_HT','QCD_Pt-','ZprimeToZhToZhadhbb_narrow_2000','WprimeToWZToWhadZhad_narrow_2000','BulkGravToZZToZhadZhad_narrow_2000','BulkGravToWW_narrow_2000', 'ALPtoZZ']
  mc_folders = [samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir, samplesDirALP]
 elif year == '2018':
  mc_samples = ['WW','WZ','ZZ','_HToBB_','WJetsToQQ','ZJetsToQQ','TT_Mtt','QCD_Pt_','QCD_HT','QCD_Pt-','ZprimeToZhToZhadhbb_narrow_2000','WprimeToWZToWhadZhad_narrow_2000','BulkGravToZZToZhadZhad_narrow_2000','BulkGravToWW_narrow_2000', 'ALPtoZZ']
  mc_folders = [samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir,samplesDir, samplesDirALP]

 if doVBF:
  mc_samples[-4] = 'VBF_ZprimeToZhToZhadhbb_narrow_2000'
  mc_samples[-3] = 'VBF_WprimeToWZ_narrow_2000'
  mc_samples[-2] = 'VBF_BulkGravToZZ_narrow_2000'
  mc_samples[-1] = 'VBF_BulkGravToWW_narrow_2000'#'VBF_BulkGravToWW_narrow_2000'

 histos_mc = {}

 for i,s in enumerate(mc_samples):

  if loadHistos and not isSignal(s): continue

  histos_mc[s] = []

  for f in os.listdir(mc_folders[i]):
   if not '.root' in f: continue
   if not s in f: continue
   if not doVBF and 'VBF' in f: continue
   if (s == 'WZ' or s=='WW' or s=='ZZ') and isSignal(f): continue

   fpck=open(mc_folders[i]+"/"+f.replace('.root','.pck'))
   dpck=pickle.load(fpck)
   weightinv = float(dpck['events'])

   tf = ROOT.TFile.Open(mc_folders[i]+"/"+f,'READ')
   tree = tf.AnalysisTree
   ROOT.gROOT.cd()
   htemp = ROOT.gROOT.FindObject("htemp")
   if htemp: htemp.Delete()
   print "Draw histo for file",f
   if 'QCD_Pt_' in f or 'QCD_HT' in f:
    tree.Draw("%s>>htemp_%s(%i,%f,%f)"%(var,f.replace('.root',''),settings['binsX'],settings['minX'],settings['maxX']), '(genWeight*xsec*puWeight*%.10f)*'%(lumi*1./weightinv)+cut+"*(b_spikekiller==1)");
   elif 'TT_Mtt' in f: tree.Draw("%s>>htemp_%s(%i,%f,%f)"%(var,f.replace('.root',''),settings['binsX'],settings['minX'],settings['maxX']), '(TopPTWeight*genWeight*xsec*puWeight*%.10f)*'%(lumi*1./weightinv)+cut);
   else: tree.Draw("%s>>htemp_%s(%i,%f,%f)"%(var,f.replace('.root',''),settings['binsX'],settings['minX'],settings['maxX']), '(genWeight*xsec*puWeight*%.10f)*'%(lumi*1./weightinv)+cut);
   htemp = ROOT.gROOT.FindObject("htemp_%s"%(f.replace('.root','')))
   histos_mc[s].append(htemp)
   tf.Close()

 if not loadHistos:
  h_smvvvh = ROOT.TH1F("h_smvvvh","h_smvvvh",settings['binsX'],settings['minX'],settings['maxX'])
  h_smvvvh.SetLineWidth(2)
  h_smvvvh.SetLineColor(ROOT.kBlack)
  h_smvvvh.SetFillColor(15)
  for h in histos_mc['_HToBB_']: h_smvvvh.Add(h)
  for h in histos_mc['WW']: h_smvvvh.Add(h)
  for h in histos_mc['WZ']: h_smvvvh.Add(h)
  for h in histos_mc['ZZ']: h_smvvvh.Add(h)
  c_smvvvh = ROOT.TCanvas('c_smvvvh','c_smvvvh')
  c_smvvvh.cd()
  if 'jj_LV_mass' in var or 'ZHbbvsQCD' in var or 'WvsQCD' in var or var=='jj_l1_pt' or var=='jj_l2_pt' or var=='vbf_jj_l1_pt' or var=='vbf_jj_l2_pt':c_smvvvh.SetLogy()
  h_smvvvh.Draw("HIST")
  h_smvvvh.SaveAs('%s/control_plots_%s%s/h_smvvvh_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
  c_smvvvh.SaveAs('%s/control_plots_%s%s/h_smvvvh_%s.png'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fsmvvvh = ROOT.TFile.Open('%s/control_plots_%s%s/h_smvvvh_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_smvvvh = fsmvvvh.h_smvvvh

 if not loadHistos:
  h_wjets = ROOT.TH1F("h_wjets","h_wjets",settings['binsX'],settings['minX'],settings['maxX'])
  h_wjets.SetLineWidth(2)
  h_wjets.SetLineColor(ROOT.kBlack)
  h_wjets.SetFillColor(ROOT.kRed-7)
  for h in histos_mc['WJetsToQQ']: h_wjets.Add(h)
  c_wjets = ROOT.TCanvas('c_wjets','c_wjets')
  c_wjets.cd()
  if 'jj_LV_mass' in var or 'ZHbbvsQCD' in var or 'WvsQCD' in var or var=='jj_l1_pt' or var=='jj_l2_pt' or var=='vbf_jj_l1_pt' or var=='vbf_jj_l2_pt':c_wjets.SetLogy()
  h_wjets.Draw("HIST")
  h_wjets.SaveAs('%s/control_plots_%s%s/h_wjets_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
  c_wjets.SaveAs('%s/control_plots_%s%s/h_wjets_%s.png'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fwjets = ROOT.TFile.Open('%s/control_plots_%s%s/h_wjets_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_wjets = fwjets.h_wjets

 if not loadHistos:
  h_zjets = ROOT.TH1F("h_zjets","h_zjets",settings['binsX'],settings['minX'],settings['maxX'])
  h_zjets.SetLineWidth(2)
  h_zjets.SetLineColor(ROOT.kBlack)
  h_zjets.SetFillColor(ROOT.kBlue-7)
  for h in histos_mc['ZJetsToQQ']: h_zjets.Add(h)
  c_zjets = ROOT.TCanvas('c_zjets','c_zjets')
  c_zjets.cd()
  if 'jj_LV_mass' in var or 'ZHbbvsQCD' in var or 'WvsQCD' in var or var=='jj_l1_pt' or var=='jj_l2_pt' or var=='vbf_jj_l1_pt' or var=='vbf_jj_l2_pt':c_zjets.SetLogy()
  h_zjets.Draw("HIST")
  h_zjets.SaveAs('%s/control_plots_%s%s/h_zjets_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
  c_zjets.SaveAs('%s/control_plots_%s%s/h_zjets_%s.png'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fzjets = ROOT.TFile.Open('%s/control_plots_%s%s/h_zjets_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_zjets = fzjets.h_zjets

 if not loadHistos:
  h_tt = ROOT.TH1F("h_tt","h_tt",settings['binsX'],settings['minX'],settings['maxX'])
  h_tt.SetLineWidth(2)
  h_tt.SetLineColor(ROOT.kBlack)
  h_tt.SetFillColor(ROOT.kTeal+2)
  for h in histos_mc['TT_Mtt']: h_tt.Add(h)
  c_tt = ROOT.TCanvas('c_tt','c_tt')
  c_tt.cd()
  if 'jj_LV_mass' in var or 'MassDecorrelated' in var or var=='jj_l1_pt' or var=='jj_l2_pt' or var=='vbf_jj_l1_pt' or var=='vbf_jj_l2_pt':c_tt.SetLogy()
  h_tt.Draw("HIST")
  h_tt.SaveAs('%s/control_plots_%s%s/h_tt_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
  c_tt.SaveAs('%s/control_plots_%s%s/h_tt_%s.png'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  ftt = ROOT.TFile.Open('%s/control_plots_%s%s/h_tt_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_tt = ftt.h_tt

 sf_qcd = 1.0
 if not loadHistos:
  h_qcd = ROOT.TH1F("h_qcd","h_qcd",settings['binsX'],settings['minX'],settings['maxX'])
  h_qcd.SetLineWidth(2)
  h_qcd.SetLineColor(ROOT.kBlack)
  h_qcd.SetFillColor(ROOT.kMagenta-10)
  htemps = {}
  for h in histos_mc['QCD_Pt_']:
    h_qcd.Add(h)
  sf_qcd = (h_data.Integral()-h_wjets.Integral()-h_zjets.Integral()-h_tt.Integral()-h_smvvvh.Integral())/h_qcd.Integral()
  print "Use scale factor for pythia8",sf_qcd
  c_qcd = ROOT.TCanvas('c_qcd','c_qcd')
  c_qcd.cd()
  if 'jj_LV_mass' in var or 'ZHbbvsQCD' in var or 'WvsQCD' in var or var=='jj_l1_pt' or var=='jj_l2_pt' or var=='vbf_jj_l1_pt' or var=='vbf_jj_l2_pt':c_qcd.SetLogy()
  h_qcd.Scale(sf_qcd)
  h_qcd.Draw("HIST")
  h_qcd.SaveAs('%s/control_plots_%s%s/h_qcd_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
  c_qcd.SaveAs('%s/control_plots_%s%s/h_qcd_%s.png'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fqcd = ROOT.TFile.Open('%s/control_plots_%s%s/h_qcd_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_qcd = fqcd.h_qcd

 sf_qcd_mg = 1.0
 if not loadHistos:
  h_qcd_mg = ROOT.TH1F("h_qcd_mg","h_qcd_mg",settings['binsX'],settings['minX'],settings['maxX'])
  h_qcd_mg.SetLineWidth(2)
  h_qcd_mg.SetLineStyle(2)
  h_qcd_mg.SetLineColor(ROOT.kBlack)
  for h in histos_mc['QCD_HT']: h_qcd_mg.Add(h)
  sf_qcd_mg = (h_data.Integral()-h_wjets.Integral()-h_zjets.Integral()-h_tt.Integral()-h_smvvvh.Integral())/h_qcd_mg.Integral()
  print "Use scale factor for madgraph",sf_qcd_mg
  c_qcd_mg = ROOT.TCanvas('c_qcd_mg','c_qcd_mg')
  c_qcd_mg.cd()
  if 'jj_LV_mass' in var or 'ZHbbvsQCD' in var or 'WvsQCD' in var or var=='jj_l1_pt' or var=='jj_l2_pt' or var=='vbf_jj_l1_pt' or var=='vbf_jj_l2_pt':c_qcd_mg.SetLogy()
  h_qcd_mg.Scale(sf_qcd_mg)
  h_qcd_mg.Draw("HIST")
  h_qcd_mg.SaveAs('%s/control_plots_%s%s/h_qcd_mg_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
  c_qcd_mg.SaveAs('%s/control_plots_%s%s/h_qcd_mg_%s.png'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fqcd_mg = ROOT.TFile.Open('%s/control_plots_%s%s/h_qcd_mg_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_qcd_mg = fqcd_mg.h_qcd_mg

 sf_qcd_herw = 1.0
 if not loadHistos:
  h_qcd_herw = ROOT.TH1F("h_qcd_herw","h_qcd_herw",settings['binsX'],settings['minX'],settings['maxX'])
  h_qcd_herw.SetLineWidth(2)
  h_qcd_herw.SetLineStyle(2)
  h_qcd_herw.SetLineColor(ROOT.kBlack)
  h_qcd_herw.SetLineStyle(3)
  for h in histos_mc['QCD_Pt-']:
   h_qcd_herw.Add(h)
  sf_qcd_herw = (h_data.Integral()-h_wjets.Integral()-h_zjets.Integral()-h_tt.Integral()-h_smvvvh.Integral())/h_qcd_herw.Integral()
  print "Use scale factor for herwig",sf_qcd_herw
  c_qcd_herw = ROOT.TCanvas('c_qcd_herw','c_qcd_herw')
  c_qcd_herw.cd()
  if 'jj_LV_mass' in var or 'ZHbbvsQCD' in var or 'WvsQCD' in var or var=='jj_l1_pt' or var=='jj_l2_pt' or var=='vbf_jj_l1_pt' or var=='vbf_jj_l2_pt':c_qcd_herw.SetLogy()
  h_qcd_herw.Scale(sf_qcd_herw)
  h_qcd_herw.Draw("HIST")
  h_qcd_herw.SaveAs('%s/control_plots_%s%s/h_qcd_herw_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
  c_qcd_herw.SaveAs('%s/control_plots_%s%s/h_qcd_herw_%s.png'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 else:
  fqcd_herw = ROOT.TFile.Open('%s/control_plots_%s%s/h_qcd_herw_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')),'READ')
  h_qcd_herw = fqcd_herw.h_qcd_herw

 h_sig1 = ROOT.TH1F("h_sig1","h_sig1",settings['binsX'],settings['minX'],settings['maxX'])
 h_sig1.SetLineWidth(2)
 h_sig1.SetLineColor(ROOT.kOrange+1)
 for hk in histos_mc.keys():
  if 'BulkGravToZZ' in hk: h_sig1.Add(histos_mc[hk][0])
 h_sig1.Scale(settings['scaleSig'])
 h_sig1.SaveAs('%s/control_plots_%s%s/h_sig1_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))

 h_sig2 = ROOT.TH1F("h_sig2","h_sig2",settings['binsX'],settings['minX'],settings['maxX'])
 h_sig2.SetLineWidth(2)
 h_sig2.SetLineColor(ROOT.kGray+2)
 for hk in histos_mc.keys():
  if 'ALPtoZZ' in hk: h_sig2.Add(histos_mc[hk][0])
 h_sig2.Scale(settings['scaleSig'])
 h_sig2.SaveAs('%s/control_plots_%s%s/h_sig2_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))

 hstack = ROOT.THStack("hstack","hstack")
 hstack.Add(h_smvvvh)
 hstack.Add(h_tt)
 hstack.Add(h_zjets)
 hstack.Add(h_wjets)
 hstack.Add(h_qcd)

 leg1 = GetLegend(1)
 if unblind:
   leg1.AddEntry(h_data,'Data','PE')
 leg1.AddEntry(h_qcd,'QCD Pythia8','F')
 leg1.AddEntry(h_qcd_mg,'QCD MG+Pythia8','L')
 leg1.AddEntry(h_qcd_herw,'QCD Herwig++','L')
 leg1.AddEntry(h_wjets,'W+jets','F')
 leg1.AddEntry(h_zjets,'Z+jets','F')
 leg1.AddEntry(h_tt,'t#bar{t}','F')
 leg1.AddEntry(h_smvvvh,'VV+VH','F')

 leg2 = GetLegend(2)
 leg2.AddEntry(h_sig1,signal_legend[0],"L")
 leg2.AddEntry(h_sig2,signal_legend[1],"L")

 c = ROOT.TCanvas('c')
 pad1 = get_pad("pad1",lumi) #ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
 pad1.SetBottomMargin(0.01)
 pad1.SetTopMargin(0.1)
 if 'jj_LV_mass' in var or 'ZHbbvsQCD' in var or 'WvsQCD' in var or var=='jj_l1_pt' or var=='jj_l2_pt' or var=='vbf_jj_l1_pt' or var=='vbf_jj_l2_pt':pad1.SetLogy()
 pad1.Draw()
 pad1.cd()

 htotmc_mg = ROOT.TH1F("h_tot_mc_mg","h_tot_mc_mg",settings['binsX'],settings['minX'],settings['maxX'])
 htotmc_mg.Add(h_qcd_mg)
 htotmc_mg.Add(h_tt)
 htotmc_mg.Add(h_wjets)
 htotmc_mg.Add(h_zjets)
 htotmc_mg.Add(h_smvvvh)
 htotmc_mg.SetLineWidth(2)
 htotmc_mg.SetLineStyle(2)
 htotmc_mg.SetLineColor(ROOT.kBlack)

 htotmc_herw = ROOT.TH1F("h_tot_mc_herw","h_tot_mc_herw",settings['binsX'],settings['minX'],settings['maxX'])
 htotmc_herw.Add(h_qcd_herw)
 htotmc_herw.Add(h_tt)
 htotmc_herw.Add(h_wjets)
 htotmc_herw.Add(h_zjets)
 htotmc_herw.Add(h_smvvvh)
 htotmc_herw.SetLineWidth(2)
 htotmc_herw.SetLineStyle(2)
 htotmc_herw.SetLineColor(ROOT.kBlack)
 htotmc_herw.SetLineStyle(3)

 # h_data.Draw("PE")
 # h_data.GetXaxis().SetTitle(settings['titleX'])
 # h_data.GetYaxis().SetTitle('Events')
 # h_data.SetMinimum(0.005)
 # h_data.SetMaximum(h_data.GetMaximum()*settings['maxY'])
 hstack.Draw("HIST")
 hstack.GetXaxis().SetTitle(settings['titleX'])
 hstack.GetYaxis().SetTitle('Events')
 hstack.SetMinimum(0.005)
 hstack.SetMaximum(hstack.GetMaximum()*settings['maxY'])
 #hstack.Draw("HISTsame")
 htotmc_mg.Draw("HISTsame")
 htotmc_herw.Draw("HISTsame")
 #h_qcd_mg.Draw("HISTsame")
 #h_qcd_herw.Draw("HISTsame")
 if unblind:
   h_data.Draw("PEsame")
 h_sig1.Draw("HISTsame")
 h_sig2.Draw("HISTsame")
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
 if not doInclusive: pt.Draw()

 CMS_lumi.CMS_lumi(pad1, 4, 11)
 pad1.Modified()
 pad1.Update()
 pad1.RedrawAxis()
 c.Update()
 c.cd()

 pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
 pad2.SetTopMargin(0.01)
 pad2.SetBottomMargin(0.4)
 pad2.SetGridy()
 pad2.Draw()
 pad2.cd()

 ratiohist_mg = GetRatioHisto(h_data,htotmc_mg,"ratiohist_mg",0,2,settings['titleX'])
 for b in range(1,ratiohist_mg.GetNbinsX()+1): ratiohist_mg.SetBinError(b,0)
 if(not unblind):
   ratiohist_mg.Reset()
 ratiohist_mg.Draw("")
 ratiohist_mg.Draw("HISTsame")

 ratiohist_herw = GetRatioHisto(h_data,htotmc_herw,"ratiohist_herw",0,3,settings['titleX']) #GetRatioHisto(histoNum,histoDen,name,markerSize,lineStyle,titleX):
 for b in range(1,ratiohist_herw.GetNbinsX()+1): ratiohist_herw.SetBinError(b,0)
 if unblind:
   ratiohist_herw.Draw("HISTsame")

 htotmc = ROOT.TH1F("h_tot_mc","h_tot_mc",settings['binsX'],settings['minX'],settings['maxX'])
 htotmc.Add(h_qcd)
 htotmc.Add(h_tt)
 htotmc.Add(h_wjets)
 htotmc.Add(h_zjets)
 htotmc.Add(h_smvvvh)
 ratiohist = GetRatioHisto(h_data,htotmc,"ratiohist",1,1,settings['titleX'])
 if unblind:
   ratiohist.Draw("PEsame")

 pad2.Modified()
 pad2.Update()
 c.cd()
 c.Update()
 c.Modified()
 c.Update()
 c.cd()
 c.SetSelected(c)


 c.SaveAs('%s/control_plots_%s%s/h_final_%s.pdf'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 c.SaveAs('%s/control_plots_%s%s/h_final_%s.png'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 c.SaveAs('%s/control_plots_%s%s/h_final_%s.root'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
 c.SaveAs('%s/control_plots_%s%s/h_final_%s.C'%(outdir,year,label,settings['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))

 print "############### YIELDS ###########"
 print "Observed data:",h_data.Integral()
 print "W+jets:",h_wjets.Integral()
 print "Z+jets:",h_zjets.Integral()
 print "ttbar:",h_tt.Integral()
 print "QCD (pythia8):",h_qcd.Integral(),"( sf =",sf_qcd,")"
 print "QCD (mg+pythia8)",h_qcd_mg.Integral(),"( sf =",sf_qcd_mg,")"
 print "QCD (herwig)",h_qcd_herw.Integral(),"( sf =",sf_qcd_herw,")"

if __name__ == "__main__":

 #argc = len(sys.argv)
 #if (argc < 6):
 # print("ERROR: usage: python", str(sys.argv[0]), "<YEAR> <VAR> <SUBMITJOBS> <LOADHISTOS> <DOVBF> <LABEL>",)
 # raise SystemExit

 parser = optparse.OptionParser()
 parser.add_option("-y","--year",dest="year",default='2016',help="year (2016, 2017, 2018, ALL)")
 parser.add_option("-v","--var",dest="var", default='None',help="Plot one of the variables")
 parser.add_option("-s","--submit_jobs",dest="submit_jobs",action="store_true", help="Parallelize",default=False)
 parser.add_option("-H","--load_histos",dest="load_histos",action="store_true", help="Load already made histos",default=False)
 parser.add_option("--vbf","--vbf",dest="doVBF",action="store_true", help="Run VBF selections",default=False)
 parser.add_option("--incl","--incl",dest="inclusive",action="store_true", help="Run inclusive selections",default=False)
 parser.add_option("-l","--label",dest="label",help="Label for folders",default='')
 parser.add_option("-u","--unblind",dest="unblind",action="store_true", help="Plot with data",default=False)
 (options,args) = parser.parse_args()

 print options

 year = options.year
 whichVar = options.var
 submitJobs = options.submit_jobs
 label = options.label
 loadHistos = options.load_histos
 doVBF = options.doVBF
 doInclusive = options.inclusive
 unblind = options.unblind

 outdir = os.getcwd()
 samplesDir = year #'samples_'+year
 samplesDir2016 = '2016'
 samplesDir2017 = '2017'
 samplesDir2018 = '2018'
 samplesDirALP = 'ALPS_samples'

 import cuts
 ctx  = cuts.cuts("init_VV_VH.json","2016,2017,2018","dijetbins_random",True)

 print ""
 cut='*'.join([ctx.cuts['common_VV'],ctx.cuts['acceptance_loose']])

 vars = {
        'jj_LV_mass':{'minX':1126,'maxX':7126,'binsX':60,'titleX':'Dijet invariant mass [GeV]','scaleSig':0.0005,'maxY':100},
        'jj_l1_pt':{'minX':200,'maxX':3500,'binsX':66,'titleX':'Jet 1 p_{T} [GeV]','scaleSig':0.0001,'maxY':100},
	'jj_l2_pt':{'minX':200,'maxX':3500,'binsX':66,'titleX':'Jet 2 p_{T} [GeV]','scaleSig':0.0001,'maxY':100},
	'jj_l1_eta':{'minX':-2.4,'maxX':2.4,'binsX':48,'titleX':'Jet 1 #eta','scaleSig':30.,'maxY':1.7},
	'jj_l2_eta':{'minX':-2.4,'maxX':2.4,'binsX':48,'titleX':'Jet 2 #eta','scaleSig':30.,'maxY':1.7},
	'jj_l1_phi':{'minX':-3.2,'maxX':3.2,'binsX':32,'titleX':'Jet 1 #phi','scaleSig':25.,'maxY':2.0},
	'jj_l2_phi':{'minX':-3.2,'maxX':3.2,'binsX':32,'titleX':'Jet 2 #phi','scaleSig':25.,'maxY':2.0},
	'abs(jj_l1_eta-jj_l2_eta)':{'minX':0.0,'maxX':1.5,'binsX':15,'titleX':'#Delta#eta_{jj}','scaleSig':25.,'maxY':2.0},
	'jj_l1_softDrop_mass':{'minX':55,'maxX':215,'binsX':32,'titleX':'Jet 1 m_{SD} [GeV]','scaleSig':2.,'maxY':1.7}, #scaleSig = 10
	'jj_l2_softDrop_mass':{'minX':55,'maxX':215,'binsX':32,'titleX':'Jet 2 m_{SD} [GeV]','scaleSig':10.,'maxY':1.7}, #scaleSig = 10
        '(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))':{'minX':0.2,'maxX':1.25,'binsX':21,'titleX':'Jet 1 #tau_{21}^{DDT} [GeV]','scaleSig':40.,'maxY':1.7},
        '(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))':{'minX':0.2,'maxX':1.25,'binsX':21,'titleX':'Jet 2 #tau_{21}^{DDT} [GeV]','scaleSig':40.,'maxY':1.7},
	'jj_l1_MassDecorrelatedDeepBoosted_ZHbbvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} MD','scaleSig':0.05,'maxY':1500*100},
	'jj_l2_MassDecorrelatedDeepBoosted_ZHbbvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} MD','scaleSig':0.05,'maxY':1500*100},
	'jj_l1_MassDecorrelatedDeepBoosted_WvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} MD','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_MassDecorrelatedDeepBoosted_WvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} MD','scaleSig':0.05,'maxY':10000*100},
	#'jj_l1_DeepBoosted_ZHbbvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD}','scaleSig':0.05,'maxY':1500*100},
	#'jj_l2_DeepBoosted_ZHbbvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD}','scaleSig':0.05,'maxY':1500*100},
	#'jj_l1_DeepBoosted_WvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD}','scaleSig':0.05,'maxY':10000*100},
	#'jj_l2_DeepBoosted_WvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD}','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p02_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-2%','scaleSig':0.05,'maxY':100000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p02_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-2%','scaleSig':0.05,'maxY':100000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p03_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-3%','scaleSig':0.05,'maxY':100000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p03_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-3%','scaleSig':0.05,'maxY':100000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p05_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-5%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p05_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-5%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p10_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-10%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p10_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-10%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p15_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-15%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p15_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-15%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p20_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-20%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p20_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-20%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p30_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-30%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p30_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-30%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p50_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-50%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p50_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-50%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p02_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-2%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p02_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-2%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p03_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-3%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p03_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-3%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p05_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-5%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p05_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-5%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p10_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-10%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p10_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-10%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p15_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-15%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p15_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-15%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p20_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-20%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p20_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-20%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p30_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-30%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p30_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-30%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p50_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-50%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p50_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-50%','scaleSig':0.05,'maxY':10000*100},
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
	'jj_l1_MassDecorrelatedDeepBoosted_ZHbbvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} MD','scaleSig':0.05,'maxY':1500*100},
	'jj_l2_MassDecorrelatedDeepBoosted_ZHbbvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} MD','scaleSig':0.05,'maxY':1500*100},
	'jj_l1_MassDecorrelatedDeepBoosted_WvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} MD','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_MassDecorrelatedDeepBoosted_WvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} MD','scaleSig':0.05,'maxY':10000*100},
	#'jj_l1_DeepBoosted_ZHbbvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD}','scaleSig':0.05,'maxY':1500*100},
	#'jj_l2_DeepBoosted_ZHbbvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD}','scaleSig':0.05,'maxY':1500*100},
	#'jj_l1_DeepBoosted_WvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD}','scaleSig':0.05,'maxY':10000*100},
	#'jj_l2_DeepBoosted_WvsQCD':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD}','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p02_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-2%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p02_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-2%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p03_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-3%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p03_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-3%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p05_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-5%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p05_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-5%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p10_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-10%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p10_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-10%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p15_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-15%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p15_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-15%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p20_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-20%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p20_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-20%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p30_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-30%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p30_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-30%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_WvsQCD__0p50_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{WvsQCD} DDT-50%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_WvsQCD__0p50_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{WvsQCD} DDT-50%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p02_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-2%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p02_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-2%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p03_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-3%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p03_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-3%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p05_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-5%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p05_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-5%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p10_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-10%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p10_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-10%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p15_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-15%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p15_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-15%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p20_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-20%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p20_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-20%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p30_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-30%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p30_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-30%','scaleSig':0.05,'maxY':10000*100},
	'jj_l1_DeepBoosted_ZHbbvsQCD__0p50_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 1 deepAK8_{ZHbbvsQCD} DDT-50%','scaleSig':0.05,'maxY':10000*100},
	'jj_l2_DeepBoosted_ZHbbvsQCD__0p50_MD_default_161718':{'minX':0,'maxX':1,'binsX':20,'titleX':'Jet 2 deepAK8_{ZHbbvsQCD} DDT-50%','scaleSig':0.05,'maxY':10000*100},
	'abs(vbf_jj_l1_eta-vbf_jj_l2_eta)':{'minX':4.5,'maxX':10,'binsX':22,'titleX':'#Delta#eta_{jj}^{VBF}','scaleSig':10,'maxY':1.7},
	'vbf_jj_l1_eta':{'minX':-5.0,'maxX':5.0,'binsX':50,'titleX':'VBF jet 1 #eta','scaleSig':3,'maxY':2},
	'vbf_jj_l2_eta':{'minX':-5.0,'maxX':5.0,'binsX':50,'titleX':'VBF jet 2 #eta','scaleSig':3,'maxY':2},
	'vbf_jj_l1_phi':{'minX':-3.2,'maxX':3.2,'binsX':32,'titleX':'VBF jet 1 #phi','scaleSig':3,'maxY':2},
	'vbf_jj_l2_phi':{'minX':-3.2,'maxX':3.2,'binsX':32,'titleX':'VBF jet 2 #phi','scaleSig':3,'maxY':2},
	'vbf_jj_LV_mass':{'minX':800,'maxX':10000,'binsX':92,'titleX':'VBF jets invariant mass [GeV]','scaleSig':0.01,'maxY':100},
        'vbf_jj_l1_pt':{'minX':50,'maxX':1450,'binsX':56,'titleX':'VBF jet 1 p_{T} [GeV]','scaleSig':0.01,'maxY':100},
	'vbf_jj_l2_pt':{'minX':50,'maxX':750,'binsX':28,'titleX':'VBF jet 2 p_{T} [GeV]','scaleSig':0.01,'maxY':100},
  }
  cut='*'.join([ctx.cuts['common_VBF'],ctx.cuts['acceptance_loose']])

 if doInclusive: cut='*'.join([ctx.cuts['common_norho'],ctx.cuts['acceptance_loose']])

 print cut

 if year != 'ALL': lumi = ctx.lumi[options.year]
 else: lumi = ctx.lumi['2016'] + ctx.lumi['2017'] + ctx.lumi['2018']

 if not os.path.exists('%s/control_plots_%s%s'%(outdir,year,label)):
  os.mkdir('%s/control_plots_%s%s'%(outdir,year,label))
 else:
  print "DIRECTORY EXISTS"

 ###############################################
 if year != "ALL":

  if submitJobs: print "Submitting",len(vars.keys()),"jobs!"

  j=0
  for k,v in vars.iteritems():

   #if j<36:
   # j+=1
   # continue #VBF: 7 24 36

   if submitJobs==False:
    if k == whichVar or whichVar=="None":
     MakeHist(k,v,j+1,samplesDir, samplesDirALP,cut,outdir,year,lumi,doVBF,doInclusive,loadHistos,unblind)
   else:
    jobdir = 'controlplots'+options.year+"-"+str(j+1)+label
    if os.path.exists(jobdir):
      print "Job directory",jobdir,"already exists. Removing it ..."
      os.system('rm -rf %s'%jobdir)
    os.mkdir(jobdir)
    os.chdir(jobdir)

    cmssw_cmd = 'python {outdir}/make-control-plots-ALP.py -y {year} -v "{var}" -l {label}'.format(outdir=outdir,year=year,var=k,label=options.label)
    if doVBF: cmssw_cmd = 'python {outdir}/make-control-plots-ALP.py -y {year} -v "{var}" --vbf -l "{label}"'.format(outdir=outdir,year=year,var=k,label=options.label)
    if doInclusive: cmssw_cmd = 'python {outdir}/make-control-plots-ALP.py -y {year} -v "{var}" --incl -l "{label}"'.format(outdir=outdir,year=year,var=k,label=options.label)
    print(cmssw_cmd)

    with open('job.sh', 'w') as fout:
     fout.write("#!/bin/sh\n")
     fout.write("echo\n")
     fout.write("echo\n")
     fout.write("echo 'START---------------'\n")
     fout.write("echo 'WORKDIR ' ${PWD}\n")
     fout.write("source /afs/cern.ch/cms/cmsset_default.sh\n")
     fout.write("cd "+str(outdir)+"\n")
     fout.write("cmsenv\n")
     fout.write("export X509_USER_PROXY=$1\n")
     fout.write("echo $X509_USER_PROXY\n")
     fout.write("voms-proxy-info -all\n")
     fout.write("voms-proxy-info -all -file $1\n")
     fout.write("%s\n"%(cmssw_cmd))
     fout.write("echo 'STOP---------------'\n")
     fout.write("echo\n")
     fout.write("echo\n")
    os.system("chmod 755 job.sh")

    ###### sends bjobs ######
    makeSubmitFileCondor("job.sh","job","workday")
    os.system("condor_submit submit.sub")
    print "job nr " + str(j+1) + " submitted"

    os.chdir("../")
   j+=1


 ###############################################
 if year == 'ALL':

  for k,v in vars.iteritems():

   #if k == 'jj_l2_DeepBoosted_WvsQCD__0p03_MD_default_161718': continue
   #if k == 'vbf_jj_LV_mass': continue
   #if not 'vbf' in k: continue
   #if k=='vbf_jj_l2_pt': continue #data missing
   #if k == 'jj_l2_DeepBoosted_WvsQCD__0p03_MD_default_161718': continue

   print k
   if k != whichVar and whichVar != "None": continue

   print "======================================================="
   print "make histos for variable:",v['titleX']
   print "======================================================="

   h_data = GetTotalHisto('data')
   h_wjets = GetTotalHisto('wjets')
   h_zjets = GetTotalHisto('zjets')
   h_smvvvh = GetTotalHisto('smvvvh')
   h_tt = GetTotalHisto('tt')
   h_qcd = GetTotalHisto('qcd')
   h_qcd_mg = GetTotalHisto('qcd_mg')
   h_qcd_herw = GetTotalHisto('qcd_herw')
   h_sig1 = GetTotalHisto('sig1')
   h_sig2 = GetTotalHisto('sig2')

   hstack = ROOT.THStack("hstack","hstack");
   hstack.Add(h_smvvvh)
   hstack.Add(h_tt)
   hstack.Add(h_zjets)
   hstack.Add(h_wjets)
   hstack.Add(h_qcd)

   leg1 = GetLegend(1)
   if(unblind): leg1.AddEntry(h_data,'Data','PE')
   leg1.AddEntry(h_qcd,'QCD Pythia8','F')
   leg1.AddEntry(h_qcd_mg,'QCD MG+Pythia8','L')
   leg1.AddEntry(h_qcd_herw,'QCD Herwig++','L')
   leg1.AddEntry(h_wjets,'W+jets','F')
   leg1.AddEntry(h_zjets,'Z+jets','F')
   leg1.AddEntry(h_tt,'t#bar{t}','F')
   leg1.AddEntry(h_smvvvh,'VV+VH','F')

   leg2 = GetLegend(2)
   if not doVBF:leg2.AddEntry(h_sig1,"G #rightarrow ZZ","L")
   leg2.AddEntry(h_sig2,"ALP #rightarrow ZZ","L")

   c = ROOT.TCanvas('c')
   pad1 = get_pad("pad1",lumi) #ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
   pad1.SetBottomMargin(0.01)
   pad1.SetTopMargin(0.1)
   if 'jj_LV_mass' in k or 'ZHbbvsQCD' in k or 'WvsQCD' in k or k=='jj_l1_pt' or k=='jj_l2_pt' or k=='vbf_jj_l1_pt' or k=='vbf_jj_l2_pt':pad1.SetLogy()
   pad1.Draw()
   pad1.cd()

   htotmc_mg = ROOT.TH1F("h_tot_mc_mg","h_tot_mc_mg",v['binsX'],v['minX'],v['maxX'])
   htotmc_mg.Add(h_qcd_mg)
   htotmc_mg.Add(h_tt)
   htotmc_mg.Add(h_smvvvh)
   htotmc_mg.Add(h_wjets)
   htotmc_mg.Add(h_zjets)
   htotmc_mg.SetLineWidth(2)
   htotmc_mg.SetLineStyle(2)
   htotmc_mg.SetLineColor(ROOT.kBlack)
   htotmc_herw = ROOT.TH1F("h_tot_mc_herw","h_tot_mc_herw",v['binsX'],v['minX'],v['maxX'])
   htotmc_herw.Add(h_qcd_herw)
   htotmc_herw.Add(h_tt)
   htotmc_herw.Add(h_smvvvh)
   htotmc_herw.Add(h_wjets)
   htotmc_herw.Add(h_zjets)
   htotmc_herw.SetLineWidth(2)
   htotmc_herw.SetLineStyle(2)
   htotmc_herw.SetLineColor(ROOT.kBlack)
   htotmc_herw.SetLineStyle(3)

   if(not unblind):
     h_data.Reset()
   #h_data.Draw("PE")
   #h_data.GetXaxis().SetTitle(v['titleX'])
   # h_data.GetYaxis().SetTitle('Events')
   # h_data.SetMinimum(0.005)
   # h_data.SetMaximum(h_data.GetMaximum()*v['maxY'])

   hstack.Draw("HIST")
   hstack.GetXaxis().SetTitle(v['titleX'])
   hstack.GetYaxis().SetTitle('Events')
   hstack.SetMinimum(0.005)
   hstack.SetMaximum(hstack.GetMaximum()*v['maxY'])

   htotmc_mg.Draw("HISTsame")
   htotmc_herw.Draw("HISTsame")
   #h_qcd_mg.Draw("HISTsame")
   #h_qcd_herw.Draw("HISTsame")
   if(unblind): h_data.Draw("PEsame")
   if not doVBF: h_sig1.Draw("HISTsame")
   h_sig2.Draw("HISTsame")

   leg1.Draw()
   leg2.Draw()

   pt = ROOT.TPaveText(0.5334448,0.5121951,0.8929766,0.7735192,"NDC")
   pt.SetTextFont(62)
   pt.SetTextSize(0.04)
   pt.SetTextAlign(12)
   pt.SetFillColor(0)
   pt.SetBorderSize(0)
   pt.SetFillStyle(0)
   if doVBF: pt.AddText("VBF channel")
   else: pt.AddText("ggF/DY channel")
   if not doInclusive: pt.Draw()

   CMS_lumi.CMS_lumi(pad1, 4, 11)
   pad1.Modified()
   pad1.Update()
   pad1.RedrawAxis()
   c.Update()
   c.cd()

   pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
   pad2.SetTopMargin(0.01)
   pad2.SetBottomMargin(0.4)
   pad2.SetGridy()
   pad2.Draw()
   pad2.cd()

   ratiohist_mg = GetRatioHisto(h_data,htotmc_mg,"ratiohist_mg",0,2,v['titleX'])
   for b in range(1,ratiohist_mg.GetNbinsX()+1): ratiohist_mg.SetBinError(b,0)
   if(not unblind):
     ratiohist_mg.Reset()
   ratiohist_mg.Draw("")
   ratiohist_mg.Draw("HISTsame")

   ratiohist_herw = GetRatioHisto(h_data,htotmc_herw,"ratiohist_herw",0,3,v['titleX']) #GetRatioHisto(histoNum,histoDen,name,markerSize,lineStyle,titleX):
   for b in range(1,ratiohist_herw.GetNbinsX()+1): ratiohist_herw.SetBinError(b,0)
   if(unblind):
     ratiohist_herw.Draw("HISTsame")

   htotmc = ROOT.TH1F("h_tot_mc","h_tot_mc",v['binsX'],v['minX'],v['maxX'])
   htotmc.Add(h_qcd)
   htotmc.Add(h_tt)
   htotmc.Add(h_wjets)
   htotmc.Add(h_zjets)
   ratiohist = GetRatioHisto(h_data,htotmc,"ratiohist",1,1,v['titleX'])
   if(unblind):
    ratiohist.Draw("same")

   pad2.Modified()
   pad2.Update()
   c.cd()
   c.Update()
   c.Modified()
   c.Update()
   c.cd()
   c.SetSelected(c)

   c.SaveAs('%s/control_plots_%s%s/h_final_%s.pdf'%(outdir,year,label,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
   c.SaveAs('%s/control_plots_%s%s/h_final_%s.png'%(outdir,year,label,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
   c.SaveAs('%s/control_plots_%s%s/h_final_%s.root'%(outdir,year,label,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
   c.SaveAs('%s/control_plots_%s%s/h_final_%s.C'%(outdir,year,label,v['titleX'].replace(' ','_').replace('{','').replace('}','').replace('#','')))
