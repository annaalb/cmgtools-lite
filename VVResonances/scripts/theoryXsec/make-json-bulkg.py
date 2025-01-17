import json, sys
from array import array
import ROOT
from ROOT import *

############## gluon fusion ##############
fin = ROOT.TFile.Open('BulkGWW.root','READ')
graph = fin.Get('gtheory')

xsec = {}

for i in range(graph.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graph.GetPoint(i,x,y)
 xsec[str(int(x*1000))] = {}

for i in range(graph.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graph.GetPoint(i,x,y)
 xsec[str(int(x*1000))]["BRWW"] = y
 xsec[str(int(x*1000))]["sigma"] = 1.0

fin.Close()

fin = ROOT.TFile.Open('BulkGZZ.root','READ')
graph = fin.Get('gtheory')

for i in range(graph.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graph.GetPoint(i,x,y)
 xsec[str(int(x*1000))]["BRZZ"] = y

fin.Close()

f=open("BulkG.json","w")
json.dump(xsec,f)
f.close()




############## VBF ##############
fin = ROOT.TFile.Open('VBF_BulkGWW.root','READ')
graph = fin.Get('gtheory')

xsec = {}

for i in range(graph.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graph.GetPoint(i,x,y)
 xsec[str(int(x*1000))] = {}

for i in range(graph.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graph.GetPoint(i,x,y)
 xsec[str(int(x*1000))]["BRWW"] = y
 xsec[str(int(x*1000))]["sigma"] = 1.0

fin.Close()

fin = ROOT.TFile.Open('VBF_BulkGZZ.root','READ')
graph = fin.Get('gtheory')

for i in range(graph.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graph.GetPoint(i,x,y)
 xsec[str(int(x*1000))]["BRZZ"] = y

fin.Close()

f=open("VBF_BulkG.json","w")
json.dump(xsec,f)
f.close()
