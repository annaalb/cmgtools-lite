#!/bin/env python
import ROOT
import json
import math
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from time import sleep
import optparse, sys
from collections import defaultdict
from  CMGTools.VVResonances.plotting.CMS_lumi import *
from array import array
   
ROOT.gROOT.SetBatch(True)

path = "../plots/"

def beautify(h1,color,linestyle=1,markerstyle=8):
    h1.SetLineColor(color)
    h1.SetMarkerColor(color)
    # h1.SetFillColor(color)                                                                                                                                                                                                                  
    h1.SetLineWidth(3)
    h1.SetLineStyle(linestyle)
    h1.SetMarkerStyle(markerstyle)
    h1.SetMarkerSize(1.5)


def getLegend(x1=0.2,y1=0.71,x2=0.45,y2=0.88):
#def getLegend(x1=0.70010112,y1=0.693362,x2=0.90202143,y2=0.829833):
  legend = ROOT.TLegend(x1,y1,x2,y2)
  legend.SetTextSize(0.035)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetMargin(0.35)
  return legend
  
def getCanvasPaper(cname):
        ROOT.gStyle.SetOptStat(0)

        H_ref = 600
        W_ref = 600
        W = W_ref
        H  = H_ref
        iPeriod = 0
        # references for T, B, L, R
        T = 0.08*H_ref
        B = 0.15*H_ref
        L = 0.15*W_ref
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
        legend = getLegend()

        pt = ROOT.TPaveText(0.1746231,0.6031469,0.5251256,0.7517483,"NDC")
        pt.SetTextFont(42)
        pt.SetTextSize(0.04)
        pt.SetTextAlign(12)
        pt.SetFillColor(0)
        pt.SetBorderSize(0)
        pt.SetFillStyle(0)

        return canvas, legend, pt
parser = optparse.OptionParser()

parser.add_option("-v","--var",dest="var",help="mVV or mJ",default='mVV')
parser.add_option("-l","--leg",dest="leg",help="l1 or l2",default='l1')
parser.add_option("-p","--period",dest="period",help="2016 or 2017 or 2018",default='2016')
parser.add_option("-c","--category",dest="category",help="VV_HPHP or VV_HPLP or VH_HPHP etc",default='VV_HPLP')
parser.add_option("-s","--signal",dest="signal",help="signal",default='BulkGWW')
parser.add_option("-f","--folder",dest="folder",help="input directory",default='')
parser.add_option("-n","--name",dest="name",help="specify a label for the output file name",default='All')

postfix = "Jet 1 "
(options,args) = parser.parse_args()
if options.leg == "l2" !=-1: postfix = "Jet 2 "
purity  = options.category


#inFileName = options.file
#massPoints = [1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]
massPoints = [1200,1400,1600,1800,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000]
#massPoints = [1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000,5200]
varName = {'mVV':'M_{VV} (GeV)','mJ':'%ssoftdrop mass (GeV)'%postfix}
varBins = {'mVV':'[37,1000,5500]','mJ':'[80,55,215]'}
w=ROOT.RooWorkspace("w","w")
w.factory(options.var+varBins[options.var])
w.var(options.var).SetTitle(varName[options.var])
colors= []
colors.append(["#f9c677","#f9d077","#f9f577","#ffd300","#f9fe77","#f9fe64","#f9fe43","#f9fe17"]*3)
colors.append(["#fee0d2","#fcbba1","#fc9272","#ef3b2c","#ef3b2c","#cb181d","#a50f15","#67000d"]*3) 
colors.append(["#e5f5e0","#c7e9c0","#a1d99b","#41ab5d","#41ab5d","#238b45","#006d2c","#00441b"]*3) 
colors.append(["#02fefe","#02e5fe","#02d7fe","#4292c6","#02b5fe","#02a8fe","#0282fe","#0300fc"]*3)  
colors.append(["#e6a3e1","#d987e6","#ce5ce0","#822391","#8526bd","#9b20e3","#a87eed","#8649eb"]*3)  
colors.append(["#45444B","#6B6974","#807D8D","#8F8BA2","#A39EBB","#AEA7D1","#B2A9E2","#B2A6F5"]*3)

colorsyears= {'2016': "#4292c6",'2017': "#41ab5d",'2018':"#ef3b2c", 'Run2': "#17202A"}
markeryears={'2016':8, '2017':25,'2018':22,'Run2':32}

def doTagging(signal,legend,year,colorindex,inputdir,decay):
    marker=[20,22,24,21,25,22,26,23,32]
    color=[1,425,12,2,4,7]
    purities=["HPHtag","HPVtag","LPHtag","LPVtag","NPVtag"]
    n = len(massPoints)
    decayleaf = " "
    if decay == "Hbb":
        decayleaf = "mergedHbbTruth"
    elif decay == "Hcc":
        decayleaf = "mergedHccTruth"
    elif decay == "Hgg":
        decayleaf = "mergedHggTruth"
    elif decay == "HVV4q":
        decayleaf = "mergedHVV4qTruth"
    elif decay == "HVVlep":
        decayleaf = "mergedHVVlepTruth"
    else:
        print " no decay leaf update!!"
    gr = {}
    j=0
    data = [] 
    c1,leg,pt = getCanvasPaper("c1")
    c1.Draw()

    for purity in purities:
        print " working on ",purity
        
        #gr[purity]
        markerd={}
        colord={}
        mass, perc = array( 'd' ), array( 'd' )
        for m in massPoints : 
            mass.append(m)
            filename= inputdir+"/"+signal+"_narrow_"+str(m)+"_"+year+".root"
            print " filename ",filename
            r_file = ROOT.TFile(filename,"READ")
            tree = r_file.Get("signalregion")
            t1 = ROOT.gROOT.FindObject('t1')
            if t1: t1.Delete()
            t2 = ROOT.gROOT.FindObject('t2')
            if t2: t2.Delete()
            h1 = ROOT.gROOT.FindObject('h1')
            if h1: h1.Delete()
            h2 = ROOT.gROOT.FindObject('h2')
            if h2: h2.Delete()
            print " * ",decayleaf
            tot = ROOT.TH1F("tot","tot",5,0,5)
            tree.Draw("jj_l1_jetTag>>t1(5,0,5)","jj_l1_"+decayleaf+"==1","goff")            
            t1 = ROOT.gROOT.FindObject('t1')
            tree.Draw("jj_l2_jetTag>>t2(5,0,5)","jj_l2_"+decayleaf+"==1","goff")            
            t2 = ROOT.gROOT.FindObject('t2')
            if t1:
                tot.Add(t1)
            if t2:
                tot.Add(t2)
            print " tot ",tot.GetEntries()
            total = tot.GetEntries()
            if tot.GetEntries() == 0: 
                total = -1
            h = ROOT.TH1F("h","h",1,0,1)
            tree.Draw("jj_l1_jetTag>>h1(1,0,1)","jj_l1_"+decayleaf+"==1&&(strstr(jj_l1_jetTag,\"%s\"))"%purity,"goff")
            h1 = ROOT.gROOT.FindObject('h1')
            tree.Draw("jj_l2_jetTag>>h2(1,0,1)","jj_l2_"+decayleaf+"==1&&(strstr(jj_l2_jetTag,\"%s\"))"%purity,"goff")
            h2 = ROOT.gROOT.FindObject('h2')
            print h1.GetEntries()
            if h1:
                h.Add(h1)
            if h2:
                h.Add(h2)
            print float(h.GetEntries())/float(total)*100
            perc.append(float(h.GetEntries())/float(total)*100)
        graph = ROOT.TGraph( n, mass, perc )
        gr[purity]= graph

        gr[purity].SetLineColor(color[j])
        gr[purity].SetLineStyle(2)
        gr[purity].SetLineWidth(2)
        gr[purity].SetMarkerColor(color[j])
        gr[purity].SetMarkerStyle(marker[j])
        

        gr[purity].GetYaxis().SetTitle("[%]")
        gr[purity].GetXaxis().SetTitle("m_{X} [GeV]")
        gr[purity].GetYaxis().SetTitleOffset(1.3)
        gr[purity].GetYaxis().SetNdivisions(4,5,0)
        gr[purity].GetXaxis().SetNdivisions(3,5,0)
        gr[purity].SetMinimum(0.)
        gr[purity].SetMaximum(100.)
        gr[purity].GetXaxis().SetLimits(1000.,8500.)
        gr[purity].GetXaxis().SetTitleSize(0.055)
        gr[purity].GetYaxis().SetTitleSize(0.055)
        gr[purity].GetYaxis().SetLabelSize(0.04)
        gr[purity].GetXaxis().SetLabelSize(0.04)
        data.append(gr[purity])        
        leg.AddEntry(gr[purity],purity, "LP")
        j=j+1


    data[0].Draw("AC")
    for i,(g) in enumerate(data):
        print " print ",i,g
        #g.GetXaxis().SetRangeUser(1000.,8500.)
        g.Draw("PLsame")

        #gr[purity][year].Draw("APL")
        #gr[purity][year].Draw("PL")
          
        
    leg.Draw("same")

    
    pt2 = ROOT.TPaveText(0.7,0.87,0.8,0.9,"NDC")
    pt2.SetTextFont(42)
    pt2.SetTextSize(0.04)
    pt2.SetTextAlign(12)
    pt2.SetFillColor(0)
    pt2.SetBorderSize(0)
    pt2.SetFillStyle(0)
    pt2.AddText(legend)
    pt2.Draw()
    

    pt3 = ROOT.TPaveText(0.7,0.75,0.8,0.87,"NDC")
    pt3.SetTextFont(42)
    pt3.SetTextSize(0.04)
    pt3.SetTextAlign(12)
    pt3.SetFillColor(0)
    pt3.SetBorderSize(0)
    pt3.SetFillStyle(0)
    pt3.AddText(decay)
    pt3.Draw()
    
      
    name = path+"TagHinc_%s_%s_%s_%s"  %(year,options.name,signal,decay)
    c1.SaveAs(name+".png")
    c1.SaveAs(name+".pdf" )
    c1.SaveAs(name+".C"   )
    c1.SaveAs(name+".root")


def doDecay(signal,legend,year,colorindex,inputdir):
    marker=[20,22,24,21,25,22,26,23,32]
    color=[1,425,12,2,4,7]
    decays = ["mergedHbbTruth","mergedHccTruth","mergedHggTruth","mergedHVV4qTruth","mergedHVVlepTruth"]
    n = len(massPoints)
    gr = {}
    j=0
    data = [] 
    c1,leg,pt = getCanvasPaper("c1")
    c1.Draw()

    for decayleaf in decays:
        print " working on ",decayleaf
        
        #gr[decayleaf]
        markerd={}
        colord={}
        mass, perc = array( 'd' ), array( 'd' )
        for m in massPoints : 
            mass.append(m)
            filename= inputdir+"/"+signal+"_narrow_"+str(m)+"_"+year+".root"
            print " filename ",filename
            r_file = ROOT.TFile(filename,"READ")
            tree = r_file.Get("signalregion")
            t1 = ROOT.gROOT.FindObject('t1')
            if t1: t1.Delete()
            t2 = ROOT.gROOT.FindObject('t2')
            if t2: t2.Delete()
            h1 = ROOT.gROOT.FindObject('h1')
            if h1: h1.Delete()
            h2 = ROOT.gROOT.FindObject('h2')
            if h2: h2.Delete()
            print " * ",decayleaf
            tot = ROOT.TH1F("tot","tot",1,0,1)
            tree.Draw("evt>>t1(1,0,1)","jj_l1_mergedHbbTruth==1||jj_l1_mergedHccTruth==1||jj_l1_mergedHggTruth==1||jj_l1_mergedHVV4qTruth==1||jj_l1_mergedHVVlepTruth==1","goff")
            t1 = ROOT.gROOT.FindObject('t1')
            tree.Draw("evt>>t2(1,0,1)","jj_l2_mergedHbbTruth==1||jj_l2_mergedHccTruth==1||jj_l2_mergedHggTruth==1||jj_l2_mergedHVV4qTruth==1||jj_l2_mergedHVVlepTruth==1","goff")  
            t2 = ROOT.gROOT.FindObject('t2')
            if t1:
                tot.Add(t1)
            if t2:
                tot.Add(t2)
            print " tot ",tot.GetEntries()
            total = tot.GetEntries()
            if tot.GetEntries() == 0: 
                total = -1
            h = ROOT.TH1F("h","h",1,0,1)
            tree.Draw("evt>>h1(1,0,1)","jj_l1_"+decayleaf+"==1","goff")
            h1 = ROOT.gROOT.FindObject('h1')
            tree.Draw("evt>>h2(1,0,1)","jj_l2_"+decayleaf+"==1","goff")
            h2 = ROOT.gROOT.FindObject('h2')
            print h1.GetEntries()
            if h1:
                h.Add(h1)
            if h2:
                h.Add(h2)
            print float(h.GetEntries())/float(total)*100
            perc.append(float(h.GetEntries())/float(total)*100)
        graph = ROOT.TGraph( n, mass, perc )
        gr[decayleaf]= graph

        gr[decayleaf].SetLineColor(color[j])
        gr[decayleaf].SetLineStyle(2)
        gr[decayleaf].SetLineWidth(2)
        gr[decayleaf].SetMarkerColor(color[j])
        gr[decayleaf].SetMarkerStyle(marker[j])
        

        gr[decayleaf].GetYaxis().SetTitle("[%]")
        gr[decayleaf].GetXaxis().SetTitle("m_{X} [GeV]")
        gr[decayleaf].GetYaxis().SetTitleOffset(1.3)
        gr[decayleaf].GetYaxis().SetNdivisions(4,5,0)
        gr[decayleaf].GetXaxis().SetNdivisions(3,5,0)
        gr[decayleaf].SetMinimum(0.)
        gr[decayleaf].SetMaximum(100.)
        gr[decayleaf].GetXaxis().SetLimits(1000.,8500.)
        gr[decayleaf].GetXaxis().SetTitleSize(0.055)
        gr[decayleaf].GetYaxis().SetTitleSize(0.055)
        gr[decayleaf].GetYaxis().SetLabelSize(0.04)
        gr[decayleaf].GetXaxis().SetLabelSize(0.04)
        data.append(gr[decayleaf])        
        leg.AddEntry(gr[decayleaf],decayleaf, "LP")
        j=j+1


    data[0].Draw("AC")
    for i,(g) in enumerate(data):
        print " print ",i,g
        #g.GetXaxis().SetRangeUser(1000.,8500.)
        g.Draw("PLsame")

        #gr[decayleaf][year].Draw("APL")
        #gr[decayleaf][year].Draw("PL")
          
        
    leg.Draw("same")

    
    pt2 = ROOT.TPaveText(0.7,0.87,0.8,0.9,"NDC")
    pt2.SetTextFont(42)
    pt2.SetTextSize(0.04)
    pt2.SetTextAlign(12)
    pt2.SetFillColor(0)
    pt2.SetBorderSize(0)
    pt2.SetFillStyle(0)
    pt2.AddText(legend)
    pt2.Draw()
    

    pt3 = ROOT.TPaveText(0.7,0.75,0.8,0.87,"NDC")
    pt3.SetTextFont(42)
    pt3.SetTextSize(0.04)
    pt3.SetTextAlign(12)
    pt3.SetFillColor(0)
    pt3.SetBorderSize(0)
    pt3.SetFillStyle(0)
    pt3.AddText("jet1 == H or jet 2 == H")
    pt3.Draw()
    
      
    name = path+"PercHinc_%s_%s_%s"  %(year,options.name,signal)
    c1.SaveAs(name+".png")
    c1.SaveAs(name+".pdf" )
    c1.SaveAs(name+".C"   )
    c1.SaveAs(name+".root")
    
    





                
if __name__ == '__main__':

    inputdir = "migrationunc/"
    signals=["ZprimeToZhToZhadhinc","VBF_ZprimeToZhToZhadhinc","WprimeToWhToWhadhinc","VBF_WprimeToWhToWhadhinc"]
    legs = ["Z'#rightarrow ZHinc","VBF Z'#rightarrow ZHinc","W'#rightarrow WHinc","VBF W'#rightarrow WHinc"]
    decays = ["Hbb","Hcc","Hgg","HVV4q","HVVlep"]
    years = ["2016","2017","2018"]
    for i in range(len(signals)):
      print i
      print signals[i]
      print legs[i]
      for j in range(len(decays)):
          for year in years:
              doTagging(signals[i],legs[i],year,i,inputdir,decays[j])
              doDecay(signals[i],legs[i],year,i,inputdir)
  
