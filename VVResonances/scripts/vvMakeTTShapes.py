#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json, copy
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.v5.TFormula.SetMaxima(10000) #otherwise we get an error that the TFormula called by the TTree draw has too many operators when running on the CR
from time import sleep
from  CMGTools.VVResonances.plotting.CMS_lumi import *
parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="outname",default='')
parser.add_option("-m","--min",dest="mini",type=float,help="min MJJ",default=40)
parser.add_option("-M","--max",dest="maxi",type=float,help="max MJJ",default=160)
parser.add_option("--store",dest="store",type=str,help="store fitted parameters in this file",default="")
parser.add_option("--corrFactor",dest="corrFactor",type=float,help="add correction factor xsec",default=1.)
# parser.add_option("-f","--fix",dest="fixPars",help="Fixed parameters",default="c_1:430.")
parser.add_option("-f","--fix",dest="fixPars",help="Fixed parameters",default="1")
parser.add_option("--minMVV","--minMVV",dest="minMVV",type=float,help="mVV variable",default=1)
parser.add_option("--maxMVV","--maxMVV",dest="maxMVV",type=float, help="mVV variable",default=1)
parser.add_option("--binsMVV",dest="binsMVV",help="use special binning",default="")
parser.add_option("-t","--triggerweight",dest="triggerW",action="store_true",help="Use trigger weights",default=False)
(options,args) = parser.parse_args()


debug_out = "debug_TT/"
if not os.path.exists(debug_out): 
  os.system('mkdir '+debug_out)

def getPaveText(x1=0.15,y1=0.15,x2=0.25,y2=0.35):
  addInfo = ROOT.TPaveText(x1,y1,x2,y2,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)
  return addInfo
      
def getCanvasPaper(cname):
 ROOT.gStyle.SetOptStat(0)

 H_ref = 700 
 W_ref = 600 
 W = W_ref
 H  = H_ref
 T = 0.08*H_ref
 B = 0.12*H_ref
 L = 0.14*W_ref
 R = 0.04*W_ref
 canvas = ROOT.TCanvas(cname,cname,50,50,W,H)
 canvas.SetFillColor(0)
 canvas.SetBorderMode(0)
 canvas.SetFrameFillStyle(0)
 canvas.SetFrameBorderMode(0)
 canvas.SetLeftMargin( L/W )
 canvas.SetRightMargin( R/W )
 canvas.SetTopMargin( T/H )
 canvas.SetBottomMargin( B/H )
 canvas.SetTickx()
 canvas.SetTicky()

 pt = ROOT.TPaveText(0.1746231,0.7331469,0.5251256,0.7817483,"NDC")
 pt.SetTextFont(42)
 pt.SetTextSize(0.04)
 pt.SetTextAlign(12)
 pt.SetFillColor(0)
 pt.SetBorderSize(0)
 pt.SetFillStyle(0)
 
 return canvas, pt
 
def drawFromJson(jsonfile,category,outname):
  evalPoints = [1150,1200,1300,1400,1500,2000,2500,3000,3500,5500]
  fitter=Fitter(['MJ[80,55,215]'])
  fitter.erfexp2Gaus('model','MJ')
  var = fitter.w.var('MJJ')
  frame = fitter.w.var('MJ').frame()
  with open(jsonfile) as jsonFile:
    j = json.load(jsonFile)
    leg = ROOT.TLegend(0.1746231, 0.43, 0.5251256, 0.73)
    leg.SetBorderSize(0)
    c, pt =getCanvasPaper('ttMJ')
    
    for i,MJJ in enumerate(evalPoints):
      fitter.w.var("c_0")   .setVal( eval(j["c_0"   ]) );  fitter.w.var("c_0")   .setConstant(ROOT.kTRUE)
      fitter.w.var("c_1")   .setVal( eval(j["c_1"   ]) );  fitter.w.var("c_1")   .setConstant(ROOT.kTRUE)
      fitter.w.var("c_2")   .setVal( eval(j["c_2"   ]) );  fitter.w.var("c_2")   .setConstant(ROOT.kTRUE)
      fitter.w.var("f_g1")  .setVal( eval(j["f_g1"  ]) );  fitter.w.var("f_g1")  .setConstant(ROOT.kTRUE)
      fitter.w.var("f_res") .setVal( eval(j["f_res" ]) );  fitter.w.var("f_res") .setConstant(ROOT.kTRUE)
      fitter.w.var("mean1") .setVal( eval(j["mean1" ]) );  fitter.w.var("mean1") .setConstant(ROOT.kTRUE)
      fitter.w.var("mean2") .setVal( eval(j["mean2" ]) );  fitter.w.var("mean2") .setConstant(ROOT.kTRUE)
      fitter.w.var("sigma1").setVal( eval(j["sigma1"]) );  fitter.w.var("sigma1").setConstant(ROOT.kTRUE)
      fitter.w.var("sigma2").setVal( eval(j["sigma2"]) );  fitter.w.var("sigma2").setConstant(ROOT.kTRUE)
      
      fitter.w.pdf('model').plotOn(frame, ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colors[i])),ROOT.RooFit.Name(str(MJJ)))
      leg.AddEntry(frame.findObject(str(MJJ)), "%.1f TeV" %(MJJ/1000.), "L")
    frame.Draw()
    frame.SetTitle("")
    frame.GetYaxis().SetTitle("A.U")
    frame.GetXaxis().SetTitle("M_{jet} (GeV)")
    frame.GetYaxis().SetNdivisions(4,5,0)
    frame.SetMaximum(0.06)
    cmslabel_sim_prelim(c,'sim',11)
    leg.Draw('same')
    pt.AddText(category)

    pt.Draw()
    c.SaveAs(outname,"RECREATE")

def doClosure(histos,xaxis,jsonfile,category):
  coarse_bins_low  = [2,6,11]
  coarse_bins_high = [4,8,79]
  
  i = -1
  for h,xax in zip(histos,xaxis):
    for binL,binH in zip(coarse_bins_low,coarse_bins_high):
      i +=1
      
      c, pt =getCanvasPaper('ttMJ')
      leg = ROOT.TLegend(0.1746231, 0.33, 0.5251256, 0.63)
      leg.SetBorderSize(0)
      
      tmp = h.ProjectionY("binL%i_binH%i"%(binL,binH),binL,binH)
      tmp.Draw()
      
      projX = h.ProjectionX()
      mjjbinL = int(projX.GetBinLowEdge(binL))
      mjjbinH = int(projX.GetBinLowEdge(binH)+projX.GetBinWidth(binH))
      MJJ = int((mjjbinH+mjjbinL)/2)

      fitter=Fitter(['MJ'])
      fitter.importBinnedData(tmp,['MJ'],'data')
      fitter.erfexp2Gaus('model','MJ')
      
      with open(jsonfile) as jsonFile:
        j = json.load(jsonFile)
      
      fitter.w.var("c_0")   .setVal( eval(j["c_0"   ]) ); print eval(j["c_0"   ])
      fitter.w.var("c_1")   .setVal( eval(j["c_1"   ]) ); print eval(j["c_1"   ])
      fitter.w.var("c_2")   .setVal( eval(j["c_2"   ]) ); print eval(j["c_2"   ])
      fitter.w.var("f_g1")  .setVal( eval(j["f_g1"  ]) ); print eval(j["f_g1"  ])
      fitter.w.var("f_res") .setVal( eval(j["f_res" ]) ); print eval(j["f_res" ])
      fitter.w.var("mean1") .setVal( eval(j["mean1" ]) ); print eval(j["mean1" ])
      fitter.w.var("mean2") .setVal( eval(j["mean2" ]) ); print eval(j["mean2" ])
      fitter.w.var("sigma1").setVal( eval(j["sigma1"]) ); print eval(j["sigma1"])
      fitter.w.var("sigma2").setVal( eval(j["sigma2"]) ); print eval(j["sigma2"])
      
      fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Save(1)]) #55,140 works well with fitting only the resonant part 
      fitter.projection_ratioplot("model","data","MJ","debug_TT/%s_closure_%s_binL%s_binH%s.pdf"%(options.output,xax.replace("{","").replace("}",""),mjjbinL,mjjbinH),0,False,"%s (GeV)"%xax,options.output.split("_")[-2]+" "+options.output.split("_")[-1],55,215)
    
def getMean(h2,binL,binH):
  nbins = h2.GetYaxis().GetNbins()
  h1 = h2.ProjectionX("",0,nbins)
  h1.GetXaxis().SetRange(binL,binH)
  return h1.GetMean() 
  
def getFileList():
  samples={}
  samplenames = options.sample.split(",")
  for filename in os.listdir(args[0]):
    if filename.find("root") ==-1:
      continue
    for samplename in samplenames:
      if not (filename.find(samplename)!=-1):
        continue
      fnameParts=filename.split('.')
      try:
        fname=filename.split('.')[0]
        samples[fname] = fname
        print 'Fitting ttbar using file(s) ',filename
      except AssertionError as error:
          print(error)
          print('Root files does not have proper . separator')
  if len(samples) == 0:
    raise Exception('No input files found for samplename(s) {}'.format(options.sample))
  return samples

def getPlotters(samples_in):
  plotters_ = []
  for name in samples_in.keys():
    plotters_.append(TreePlotter(args[0]+'/'+samples[name]+'.root','AnalysisTree'))
    plotters_[-1].setupFromFile(args[0]+'/'+samples[name]+'.pck')
    plotters_[-1].addCorrectionFactor('xsec','tree')
    plotters_[-1].addCorrectionFactor('genWeight','tree')
    plotters_[-1].addCorrectionFactor('puWeight','tree')
    print "applying top pt reweight"
    plotters_[-1].addCorrectionFactor('TopPTWeight','tree')
    if options.triggerW: 
      plotters_[-1].addCorrectionFactor('triggerWeight','tree')	
    plotters_[-1].addCorrectionFactor(options.corrFactor,'flat')
  return plotters_
  
def get2DHist(plts, lumi_):
  mergedPlotter = MergedPlotter(plts)
  histo2D_l1 = mergedPlotter.drawTH2("jj_l1_softDrop_mass:jj_LV_mass",options.cut,"1",80,options.minMVV,options.maxMVV,80,options.mini,options.maxi) #y:x
  histo2D_l2 = mergedPlotter.drawTH2("jj_l2_softDrop_mass:jj_LV_mass",options.cut,"1",80,options.minMVV,options.maxMVV,80,options.mini,options.maxi)  
  histo2D    = copy.deepcopy(histo2D_l1)
  histo2D.Add(histo2D_l2)
  histo2D.Scale(float(lumi_))
  histo2D_l1.Scale(float(lumi_))
  histo2D_l2.Scale(float(lumi_))
  c, pt = getCanvasPaper('2D')
  histo2D.Draw("COLZ")
  addInfo = getPaveText(x1=0.71,y1=0.15,x2=0.81,y2=0.35)
  addInfo.AddText(options.output.split("_")[-2]+" "+options.output.split("_")[-1])
  addInfo.Draw()
  histo2D.GetXaxis().SetTitle("m_{jj}")
  histo2D.GetYaxis().SetTitle("m_{j}")
  cmslabel_sim_prelim(c,'sim',12)
  c.SaveAs(debug_out+"/%s_2D.pdf"%options.output)
  return histo2D_l1,histo2D_l2,histo2D

def doFit(th1_projY,mjj_mean,mjj_error,N):
  
  fitter=Fitter(['x'])
  fitter.erfexp2Gaus('model','x')
  projY.Rebin(2)
  if N == 0:
    fitter.w.var("c_0").setVal(-5.8573e-02)
    fitter.w.var("c_1").setVal(350.) #offset
    fitter.w.var("c_2").setVal(1.0707e+02) #width
    fitter.w.var("f_g1").setVal(7.8678e-02)
    fitter.w.var("f_res").setVal(5.9669e-01)
    fitter.w.var("mean1").setVal(8.1225e+01)
    fitter.w.var("mean2").setVal(1.7409e+02)
    fitter.w.var("sigma1").setVal(6.7507e+00)
    fitter.w.var("sigma2").setVal(1.3369e+01)

    fitter.w.var("c_0")   .setMax(0.2)
    fitter.w.var("c_1")   .setMin(100) #offset
    fitter.w.var("c_2")   .setMin(50) #width
    fitter.w.var("f_g1")  .setMin(0.05)
    fitter.w.var("f_res") .setMin(0.1)
    fitter.w.var("mean1") .setMin(75.)
    fitter.w.var("mean2") .setMin(160.)
    fitter.w.var("sigma1").setMin(5)
    fitter.w.var("sigma2").setMin(8)

    fitter.w.var("c_0")   .setMin(-0.20)
    fitter.w.var("c_1")   .setMax(600) #offset
    fitter.w.var("c_2")   .setMax(200) #width
    fitter.w.var("f_g1")  .setMax(0.9)
    fitter.w.var("f_res") .setMax(0.9)
    fitter.w.var("mean1") .setMax(90)
    fitter.w.var("mean2") .setMax(180)
    fitter.w.var("sigma1").setMax(9.)
    fitter.w.var("sigma2").setMax(16.)
    
    
    fitter.importBinnedData(projY,['x'],'data_full')
    fitter.fit('model','data_full',[ROOT.RooFit.SumW2Error(False),ROOT.RooFit.Save(1),ROOT.RooFit.Range(options.mini,options.maxi),ROOT.RooFit.Minimizer('Minuit2','migrad'), ROOT.RooFit.Extended(True)],requireConvergence=False) #55,140 works well with fitting only the resonant part
    fitter.projection_ratioplot("model","data_full","x","%s/%s_fullMjjSpectra.pdf"%(debug_out,options.output),0,False,"m_{jet} (GeV)",options.output.split("_")[-2]+" "+options.output.split("_")[-1])

  else:
    for var,graph in graphs.iteritems():
      yvalues = graphs[var].GetY()
      yvalues = [yvalues[index] for index in xrange(graphs[var].GetN())]
      print"For %s: Setting starting values of fit to values from previous bin:%f"%(var,yvalues[-1])
      fitter.w.var(var).setVal(yvalues[-1])
      
  if options.fixPars!="1":
    fixedPars =options.fixPars.split(',')
    if len(fixedPars) > 0:
      print "   - Fix parameters: ", fixedPars
    for par in fixedPars:
      parVal = par.split(':')
      fitter.w.var(parVal[0]).setVal(float(parVal[1]))
      fitter.w.var(parVal[0]).setConstant(1)
  th1_projY.Rebin(2)
  fitter.importBinnedData(th1_projY,['x'],'data')
  fitter.fit('model','data',[ROOT.RooFit.SumW2Error(False),ROOT.RooFit.Save(1),ROOT.RooFit.Range(options.mini,options.maxi),ROOT.RooFit.Minimizer('Minuit2','migrad'), ROOT.RooFit.Extended(True)],requireConvergence=False) #Set SumW2 false for cov matrix to converge, see https://root-forum.cern.ch/t/covqual-with-sumw2error/17662/6
  fitter.projection_ratioplot("model","data","x","%s/%s_%s.pdf"%(debug_out,options.output,th1_projY.GetName()),0,False,"m_{jet} (GeV)",options.output.split("_")[-2]+" "+options.output.split("_")[-1],options.mini,options.maxi)
  
  for var,graph in graphs.iteritems():
      value,error=fitter.fetch(var)
      graph.SetPoint(N,mjj_mean,value)
      graph.SetPointError(N,0.0,error) #No error x
      # graph.SetPointError(N,mjj_error,error) #error x is number of bins in mVV
      
  fitter.delete()    

def doParametrizations(graphs,ff):
  ranges = {}
  ranges["c_0"   ]= [-0.2,0.2]
  ranges["c_1"   ]= [100.,600.]
  ranges["c_2"   ]= [40.,200.]
  ranges["f_g1"  ]= [0.,0.8]
  ranges["f_res" ]= [0.0,0.9]
  ranges["mean1" ]= [77.,87.]
  ranges["mean2" ]= [160.,190.]
  ranges["sigma1"]= [0.,12.]
  ranges["sigma2"]= [6.,20.]
  
  inits = {}
  inits["c_0"   ]= [0.,9.7E07,3]
  inits["c_1"   ]= [350.,0.,0.]
  inits["c_2"   ]= [98.,-4E14,4.]
  inits["f_g1"  ]= [0.,3.4E16,5]
  inits["f_res" ]= [0.,-5.3E16,5]
  inits["mean1" ]= [81.,1.4E18,5]
  inits["mean2" ]= [176.,-1.6E19,5]
  inits["sigma1"]= [6,9.7E16,5,12.]
  inits["sigma2"]= [13.,2.5E15,5]
  
  

  titles = {}
  titles["c_0"   ] = "c_{0} (ErfExp)"   
  titles["c_1"   ] = "c_{1} (ErfExp)"   
  titles["c_2"   ] = "c_{2} (ErfExp)"   
  titles["f_g1"  ] = "F(Gauss_{W}, Gauss_{t})"  
  titles["f_res" ] = "F(res., non-res.)" 
  titles["mean1" ] = "<m>_{W}" 
  titles["mean2" ] = "<m>_{t}" 
  titles["sigma1"] = "#sigma_{W}"
  titles["sigma2"] = "#sigma_{t}"

  parametrisation = "[0]+[1]*pow(x,-[2])"

  ff.cd()
  parametrizations = {}
  for var,graph in graphs.iteritems():
    func=ROOT.TF1(var+"_func",parametrisation,options.minMVV,options.maxMVV)
    func.SetParameters(graph.Eval(options.minMVV), inits[var][1],inits[var][2])
    r = graph.Fit(func,"S R M","",options.minMVV,options.maxMVV)
    graph.Write(var)
    func.Write(var+"_func")
    c = ROOT.TCanvas()
    colors = ["#4292c6","#41ab5d","#ef3b2c","#ffd300","#D02090","#fdae61","#abd9e9","#2c7bb6"]
    mstyle = [8,4]
    graph.SetLineWidth(3)
    graph.SetLineStyle(1)
    graph.SetMarkerStyle(8)
    graph.Draw("APE")
    graph.GetXaxis().SetRangeUser(options.minMVV,options.maxMVV)
    graph.GetYaxis().SetRangeUser(ranges[var][0],ranges[var][1])
    graph.GetXaxis().SetTitle("M_{jj}")
    graph.GetYaxis().SetTitle(titles[var])
    cmslabel_sim_prelim(c,'sim',11)
    leg = ROOT.TLegend(0.55, 0.75, 0.85, 0.85)
    ROOT.SetOwnership(leg, False)
    leg.SetBorderSize(0)
    leg.AddEntry(graph, titles[var], "")
    leg.SetTextSize(0.04)
    leg.Draw()
    
    pavePars = ( [ int(func.GetParameter(i)) for i in range(func.GetNpar()) ])
    paveStr='y(x)=A+B#timesx^{-C}'
    paveStr1='A=%i'%(pavePars[0])
    paveStr2='B=%.2g'  %(pavePars[1])
    paveStr3='C=%i'  %(pavePars[2])
    
    addInfo = getPaveText()
    addInfo.AddText(options.output.split("_")[-2]+" "+options.output.split("_")[-1])
    addInfo.AddText(paveStr)
    addInfo.AddText(paveStr1)
    addInfo.AddText(paveStr2)
    addInfo.AddText(paveStr3)
    addInfo.Draw()
        
    c.SaveAs(debug_out+options.output+"_"+var+".pdf")
    
    fittedPars = ( [ func.GetParameter(i) for i in range(func.GetNpar()) ])
    st='(0+({}+{}*pow(MJJ,-{})))'.format(*fittedPars)
    parametrizations[var] = st
  return parametrizations
              
  
if __name__ == "__main__":
  
  graphs={'mean1':ROOT.TGraphErrors(),'sigma1':ROOT.TGraphErrors(),'mean2':ROOT.TGraphErrors(),'sigma2':ROOT.TGraphErrors(),'f_g1':ROOT.TGraphErrors(),'f_res':ROOT.TGraphErrors(),
            'c_0':ROOT.TGraphErrors(),'c_1':ROOT.TGraphErrors(),'c_2':ROOT.TGraphErrors()}
  
  lumi = args[1]
  samples = getFileList()
  plotters = getPlotters(samples)
  h2D_l1,h2D_l2,h2D = get2DHist(plotters,lumi)
  tmpfile = ROOT.TFile("testTT.root","RECREATE")
  
  coarse_bins_low  = [1,3,5,7,7,7]
  coarse_bins_high = [2,4,6,79,79,79]
  projX = h2D.ProjectionX()
  projY = h2D.ProjectionY()
  for bin in range(0,len(coarse_bins_low)):
    binL = float(projX.GetBinLowEdge(coarse_bins_low[bin]))
    binH = float(projX.GetBinLowEdge(coarse_bins_high[bin])+projX.GetBinWidth(coarse_bins_high[bin]))
    mjj_mean = getMean(h2D,coarse_bins_low[bin],coarse_bins_high[bin])
    mjj_error = (binH-binL)/2
    if bin == (len(coarse_bins_low)-2):
      mjj_mean = options.maxMVV-mjj_mean
    if bin == (len(coarse_bins_low)-1):
      mjj_mean = options.maxMVV
    tmp = h2D.ProjectionY("mjjmean%i_binL%i_binH%i"%(mjj_mean,binL,binH),coarse_bins_low[bin],coarse_bins_high[bin])
    doFit(tmp,mjj_mean,mjj_error,bin)
    tmpfile.cd()
    tmp.Write()
  tmpfile.cd()
  h2D.Write("h2D")
  h2D_l1.Write("h2D_l1")
  h2D_l2.Write("h2D_l2")
  for name,graph in graphs.iteritems():
      graph.Write(name)
  tmpfile.Close()
  ff=ROOT.TFile(debug_out+options.output+".root","RECREATE")
  parametrizations = doParametrizations(graphs,ff)
  ff.Close()
  f=open(options.output+".json","w")
  json.dump(parametrizations,f)
  f.close()
  print "Output name is %s" %options.output+".json"
  
  colors = ["#CD3700","#EE4000","#FF4500","#CD4F39","#EE5C42","#EE6A50","#FF7256","#FA8072","#FFA07A","#EEB4B4"]*3
  jsonfile_ = options.output+".json"
  category = options.output.split("_")[-2]+" "+options.output.split("_")[-1]
  drawFromJson(jsonfile_, category,debug_out+options.output+"_draw_from_json.pdf")
  doClosure([h2D_l1,h2D_l2],['m_{jet1}','m_{jet2}'],jsonfile_, category)
  
  
  
  
