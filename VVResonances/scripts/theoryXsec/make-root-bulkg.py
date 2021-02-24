import json, sys, math
from array import array
import ROOT
from ROOT import *

print "********* Make G->WW cross section graphs***********"

yTH = array('d',[])
yTHUp = array('d',[])
yTHDown = array('d',[])
yTHUncs = array('d',[])
masses = array('d',[])
massesUncs = array('d',[])

Fxsec = open('GF_NLO_13TeV_ktilda_0p1.txt','r')
Fbr = open('Decay_short_extended.txt','r')
brs = Fbr.readlines()

for i,l in enumerate(Fxsec.readlines()):

 if i<2: continue
 #print l.split('\t')
 
 masses.append(float(l.split('\t')[0])/1000.)
 massesUncs.append(float(l.split('\t')[0])/1000.)
 
 br = float(brs[i].split('\t')[3])
 sigma = float(l.split('\t')[1])*math.pow(0.5/0.1,2)
 uncUp = 1.0 + float(l.split('\t')[6])/100.
 uncDown = 1.0 + float(l.split('\t')[7])/100.
 
 
 yTH.append(sigma*br)
 yTHUp.append(uncUp*sigma*br)
 yTHDown.append(uncDown*sigma*br)
 yTHUncs.append(uncUp*sigma*br)
 print "mass",masses[-1],"th",yTH[-1],"down",yTHDown[-1],"up",yTHUp[-1]

for m in xrange(len(masses), 0, -1):

  massesUncs.append(masses[m-1])
  yTHUncs.append(yTHDown[m-1])
  #print masses[m-1],yTHDown[m-1]

Fxsec.close()
Fbr.close()
 
fout = ROOT.TFile.Open('BulkGWW.root','RECREATE') 
graphTH = ROOT.TGraph(len(masses),masses,yTH)
graphTH.SetName('gtheory')
graphTH.Write()
graphTHUP = ROOT.TGraph(len(masses),masses,yTHUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(masses),masses,yTHDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(massesUncs),massesUncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()

print "********* Make G->ZZ cross section graphs***********"
yTH = array('d',[])
yTHUp = array('d',[])
yTHDown = array('d',[])
yTHUncs = array('d',[])
masses = array('d',[])
massesUncs = array('d',[])

Fxsec = open('GF_NLO_13TeV_ktilda_0p1.txt','r')
Fbr = open('Decay_short_extended.txt','r')
brs = Fbr.readlines()

for i,l in enumerate(Fxsec.readlines()):

 if i<2: continue
 #print l.split('\t')
 
 masses.append(float(l.split('\t')[0])/1000.)
 massesUncs.append(float(l.split('\t')[0])/1000.)
 
 br = float(brs[i].split('\t')[4])
 sigma = float(l.split('\t')[1])*math.pow(0.5/0.1,2)
 uncUp = 1.0 + float(l.split('\t')[6])/100.
 uncDown = 1.0 + float(l.split('\t')[7])/100.
 
 
 yTH.append(sigma*br)
 yTHUp.append(uncUp*sigma*br)
 yTHDown.append(uncDown*sigma*br)
 yTHUncs.append(uncUp*sigma*br)
 print "mass",masses[-1],"th",yTH[-1],"down",yTHDown[-1],"up",yTHUp[-1]

for m in xrange(len(masses), 0, -1):

  massesUncs.append(masses[m-1])
  yTHUncs.append(yTHDown[m-1])
  #print masses[m-1],yTHDown[m-1]

Fxsec.close()
Fbr.close()
 
fout = ROOT.TFile.Open('BulkGZZ.root','RECREATE') 
graphTH = ROOT.TGraph(len(masses),masses,yTH)
graphTH.SetName('gtheory')
graphTH.Write()
graphTHUP = ROOT.TGraph(len(masses),masses,yTHUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(masses),masses,yTHDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(massesUncs),massesUncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()

print "********* Make VBF G->WW cross section graphs***********"
yTH = array('d',[])
yTHUp = array('d',[])
yTHDown = array('d',[])
yTHUncs = array('d',[])
masses = array('d',[])
massesUncs = array('d',[])

Fxsec = open('Xjj_VBF_LO_13TeV_ktilda_0p1.txt','r')
Fbr = open('Decay_short_extended.txt','r')

for i,l in enumerate(Fxsec.readlines()):

 if i<2: continue
  
 Fbr = open('Decay_short_extended.txt','r')
 for j,ll in enumerate(Fbr.readlines()):
 
  if j < 2: continue
  
  if float(ll.split('\t')[0]) != float(l.split('\t')[0]): continue
 
  masses.append(float(l.split('\t')[0])/1000.)
  massesUncs.append(float(l.split('\t')[0])/1000.)
 
  br = float(ll.split('\t')[3])
  sigma = float(l.split('\t')[1])*math.pow(0.5/0.1,2)
  uncUp = 1.0 + float(l.split('\t')[5])/100.
  uncDown = 1.0 - float(l.split('\t')[5])/100.
  
  yTH.append(sigma*br)
  yTHUp.append(uncUp*sigma*br)
  yTHDown.append(uncDown*sigma*br)
  yTHUncs.append(uncUp*sigma*br)
  print "mass",masses[-1],"th",yTH[-1],"down",yTHDown[-1],"up",yTHUp[-1]

 Fbr.close()
 
for m in xrange(len(masses), 0, -1):

  massesUncs.append(masses[m-1])
  yTHUncs.append(yTHDown[m-1])
  #print masses[m-1],yTHDown[m-1]

Fxsec.close()
Fbr.close()
 
fout = ROOT.TFile.Open('VBF_BulkGWW.root','RECREATE') 
graphTH = ROOT.TGraph(len(masses),masses,yTH)
graphTH.SetName('gtheory')
graphTH.Write()
graphTHUP = ROOT.TGraph(len(masses),masses,yTHUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(masses),masses,yTHDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(massesUncs),massesUncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()

print "********* Make VBF G->ZZ cross section graphs***********"
yTH = array('d',[])
yTHUp = array('d',[])
yTHDown = array('d',[])
yTHUncs = array('d',[])
masses = array('d',[])
massesUncs = array('d',[])

Fxsec = open('Xjj_VBF_LO_13TeV_ktilda_0p1.txt','r')
Fbr = open('Decay_short_extended.txt','r')

for i,l in enumerate(Fxsec.readlines()):

 if i<2: continue
  
 Fbr = open('Decay_short_extended.txt','r')
 for j,ll in enumerate(Fbr.readlines()):
 
  if j < 2: continue
  
  if float(ll.split('\t')[0]) != float(l.split('\t')[0]): continue
 
  masses.append(float(l.split('\t')[0])/1000.)
  massesUncs.append(float(l.split('\t')[0])/1000.)
 
  br = float(ll.split('\t')[4])
  sigma = float(l.split('\t')[1])*math.pow(0.5/0.1,2)
  uncUp = 1.0 + float(l.split('\t')[5])/100.
  uncDown = 1.0 - float(l.split('\t')[5])/100.
  
  yTH.append(sigma*br)
  yTHUp.append(uncUp*sigma*br)
  yTHDown.append(uncDown*sigma*br)
  yTHUncs.append(uncUp*sigma*br)
  print "mass",masses[-1],"th",yTH[-1],"down",yTHDown[-1],"up",yTHUp[-1]

 Fbr.close()
 
for m in xrange(len(masses), 0, -1):

  massesUncs.append(masses[m-1])
  yTHUncs.append(yTHDown[m-1])
  #print masses[m-1],yTHDown[m-1]

Fxsec.close()
Fbr.close()
 
fout = ROOT.TFile.Open('VBF_BulkGZZ.root','RECREATE') 
graphTH = ROOT.TGraph(len(masses),masses,yTH)
graphTH.SetName('gtheory')
graphTH.Write()
graphTHUP = ROOT.TGraph(len(masses),masses,yTHUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(masses),masses,yTHDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(massesUncs),massesUncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()
