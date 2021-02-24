import json, sys, math
from array import array
import ROOT
import pandas as pd

def get_theo_map(sqrts,model=""):

   V_mass = array('d',[])

   brs = {}
   index = {}

   mapping = ["M0","M+","BRWW","BRZh","BRWZ","BRWh","CX+(pb)","CX0(pb)","CX-(pb)"]

   for m in xrange(0,len(mapping)):
      if mapping[m] != "M0" and mapping[m] != "M+":
   	 brs[mapping[m]] = array('d',[])
   	 #print mapping[m]

   f = open('xsect_HVT%s_%sTeV.txt'%(model,sqrts),'r')
   for line in f:
      brDict = line.split(",")
      for d in xrange(0,len(brDict)):
   	 if brDict[d].find('\n') != -1:
   	    brDict[d] = brDict[d].split('\n')[0]
   	 for m in xrange(0,len(mapping)):
   	    if brDict[d] == mapping[m]:
   	       index[mapping[m]] = d
   	       #print "%s %i" %(mapping[m],d)
	    
   f.close()

   f = open('xsect_HVT%s_%sTeV.txt'%(model,sqrts),'r')
   for line in f:
      if line.find('M0') != -1: continue
      brDict = line.split(",")  	    
      V_mass.append(float(brDict[index['M0']]))
      for m in xrange(0,len(mapping)):
   	 if mapping[m] != "M0" and mapping[m] != "M+":
   	    brs[mapping[m]].append(float(brDict[index[mapping[m]]]))

   f.close()

   return [brs,V_mass]



print "########## Make json files for DY production mode ############"
thMap13 = get_theo_map("13","B")
xsecMap13 = thMap13[0]
mass = thMap13[1]

fdict = {}
for k,m in enumerate(mass):
 fdict[str(int(m))] = {}
 for i,v in xsecMap13.iteritems():
  fdict[str(int(m))][i] = v[k]

f=open("HVTB.json","w")
json.dump(fdict,f)
f.close()

############ add uncertainties for DY production mode #############
# from https://gitlab.cern.ch/cms-b2g/diboson-combination/combination-2016/-/blob/master/theory.py#L27-32
THEORY = {}
THEORY['W'] = {}
THEORY['W']['QCD'] = {800: [0.026, -0.026], 900: [0.033, -0.031], 1000: [0.039, -0.037], 1100: [0.044, -0.041], 1200: [0.049, -0.045], 1300: [0.054, -0.049], 1400: [0.058, -0.053], 1500: [0.062, -0.056], 1600: [0.066, -0.059], 1700: [0.070, -0.062], 1800: [0.074, -0.065], 1900: [0.077, -0.068], 2000: [0.080, -0.071], 2100: [0.084, -0.073], 2200: [0.087, -0.076], 2300: [0.090, -0.078], 2400: [0.093, -0.081], 2500: [0.097, -0.083], 2600: [0.100, -0.086], 2700: [0.103, -0.088], 2800: [0.106, -0.090], 2900: [0.109, -0.093], 3000: [0.112, -0.095], 3100: [0.115, -0.097], 3200: [0.117, -0.099], 3300: [0.120, -0.101], 3400: [0.123, -0.103], 3500: [0.126, -0.105], 3600: [0.128, -0.107], 3700: [0.130, -0.109], 3800: [0.133, -0.110], 3900: [0.135, -0.112], 4000: [0.137, -0.114], 4100: [0.139, -0.115], 4200: [0.140, -0.116], 4300: [0.142, -0.117], 4400: [0.144, -0.118], 4500: [0.145, -0.119], 4600: [0.145, -0.119], 4700: [0.145, -0.119], 4800: [0.145, -0.119], 4900: [0.145, -0.119], 5000: [0.145, -0.119], 5100: [0.145, -0.119], 5200: [0.145, -0.119], 5300: [0.145, -0.119], 5400: [0.145, -0.119], 5500: [0.145, -0.119], 5600: [0.145, -0.119], 5700: [0.145, -0.119], 5800: [0.145, -0.119], 5900: [0.145, -0.119], 6000: [0.145, -0.119]}
THEORY['W']['PDF'] = {800: [0.062, -0.062], 900: [0.064, -0.064], 1000: [0.066, -0.066], 1100: [0.068, -0.068], 1200: [0.070, -0.070], 1300: [0.072, -0.072], 1400: [0.074, -0.074], 1500: [0.077, -0.077], 1600: [0.081, -0.081], 1700: [0.083, -0.083], 1800: [0.085, -0.085], 1900: [0.089, -0.089], 2000: [0.093, -0.093], 2100: [0.098, -0.098], 2200: [0.104, -0.104], 2300: [0.109, -0.109], 2400: [0.114, -0.114], 2500: [0.120, -0.120], 2600: [0.128, -0.128], 2700: [0.136, -0.136], 2800: [0.144, -0.144], 2900: [0.152, -0.152], 3000: [0.160, -0.160], 3100: [0.174, -0.174], 3200: [0.188, -0.188], 3300: [0.202, -0.202], 3400: [0.216, -0.216], 3500: [0.230, -0.230], 3600: [0.258, -0.258], 3700: [0.285, -0.285], 3800: [0.313, -0.313], 3900: [0.340, -0.340], 4000: [0.368, -0.368], 4100: [0.408, -0.408], 4200: [0.448, -0.448], 4300: [0.488, -0.488], 4400: [0.529, -0.529], 4500: [0.569, -0.569], 4600: [0.569, -0.569], 4700: [0.569, -0.569], 4800: [0.569, -0.569], 4900: [0.569, -0.569], 5000: [0.569, -0.569], 5100: [0.569, -0.569], 5200: [0.569, -0.569], 5300: [0.569, -0.569], 5400: [0.569, -0.569], 5500: [0.569, -0.569], 5600: [0.569, -0.569], 5700: [0.569, -0.569], 5800: [0.569, -0.569], 5900: [0.569, -0.569], 6000: [0.569, -0.569]}
THEORY['Z'] = {}
THEORY['Z']['QCD'] = {800: [0.027, -0.026], 900: [0.033, -0.032], 1000: [0.040, -0.037], 1100: [0.045, -0.042], 1200: [0.050, -0.046], 1300: [0.054, -0.050], 1400: [0.059, -0.053], 1500: [0.063, -0.056], 1600: [0.067, -0.060], 1700: [0.070, -0.062], 1800: [0.074, -0.065], 1900: [0.077, -0.068], 2000: [0.080, -0.070], 2100: [0.083, -0.072], 2200: [0.086, -0.075], 2300: [0.089, -0.077], 2400: [0.091, -0.079], 2500: [0.094, -0.082], 2600: [0.097, -0.084], 2700: [0.099, -0.085], 2800: [0.102, -0.087], 2900: [0.104, -0.089], 3000: [0.107, -0.091], 3100: [0.109, -0.093], 3200: [0.112, -0.095], 3300: [0.114, -0.097], 3400: [0.116, -0.098], 3500: [0.119, -0.100], 3600: [0.121, -0.102], 3700: [0.123, -0.103], 3800: [0.125, -0.105], 3900: [0.127, -0.107], 4000: [0.130, -0.108], 4100: [0.131, -0.109], 4200: [0.133, -0.111], 4300: [0.135, -0.112], 4400: [0.137, -0.113], 4500: [0.138, -0.115], 4600: [0.138, -0.115], 4700: [0.138, -0.115], 4800: [0.138, -0.115], 4900: [0.138, -0.115], 5000: [0.138, -0.115], 5100: [0.138, -0.115], 5200: [0.138, -0.115], 5300: [0.138, -0.115], 5400: [0.138, -0.115], 5500: [0.138, -0.115], 5600: [0.138, -0.115], 5700: [0.138, -0.115], 5800: [0.138, -0.115], 5900: [0.138, -0.115], 6000: [0.138, -0.115]}
THEORY['Z']['PDF'] = {800: [0.062, -0.062], 900: [0.065, -0.065], 1000: [0.067, -0.067], 1100: [0.068, -0.068], 1200: [0.069, -0.069], 1300: [0.073, -0.073], 1400: [0.077, -0.077], 1500: [0.079, -0.079], 1600: [0.081, -0.081], 1700: [0.085, -0.085], 1800: [0.089, -0.089], 1900: [0.092, -0.092], 2000: [0.095, -0.095], 2100: [0.100, -0.100], 2200: [0.105, -0.105], 2300: [0.110, -0.110], 2400: [0.115, -0.115], 2500: [0.120, -0.120], 2600: [0.128, -0.128], 2700: [0.135, -0.135], 2800: [0.143, -0.143], 2900: [0.150, -0.150], 3000: [0.157, -0.157], 3100: [0.169, -0.169], 3200: [0.181, -0.181], 3300: [0.192, -0.192], 3400: [0.204, -0.204], 3500: [0.215, -0.215], 3600: [0.230, -0.230], 3700: [0.246, -0.246], 3800: [0.261, -0.261], 3900: [0.276, -0.276], 4000: [0.291, -0.291], 4100: [0.314, -0.314], 4200: [0.337, -0.337], 4300: [0.360, -0.360], 4400: [0.383, -0.383], 4500: [0.406, -0.406], 4600: [0.406, -0.406], 4700: [0.406, -0.406], 4800: [0.406, -0.406], 4900: [0.406, -0.406], 5000: [0.406, -0.406], 5100: [0.406, -0.406], 5200: [0.406, -0.406], 5300: [0.406, -0.406], 5400: [0.406, -0.406], 5500: [0.406, -0.406], 5600: [0.406, -0.406], 5700: [0.406, -0.406], 5800: [0.406, -0.406], 5900: [0.406, -0.406], 6000: [0.406, -0.406]}

print "############ make root files DY Z'->ZH #############"
yTH = array('d',[])
yTHDown = array('d',[])
yTHUp = array('d',[])
yTHUncs = array('d',[])
x = array('d',[])
x_uncs = array('d',[])
for i,m in enumerate(mass):
  x.append(m/1000.)
  x_uncs.append(m/1000.)
  yTH.append(fdict[str(int(m))]['CX0(pb)']*fdict[str(int(m))]['BRZh'])
  yTHUp.append(fdict[str(int(m))]['CX0(pb)']*(1.+math.hypot(THEORY['Z']['QCD'][m][0], THEORY['Z']['PDF'][m][0]))*fdict[str(int(m))]['BRZh'])
  yTHDown.append(fdict[str(int(m))]['CX0(pb)']*(1.-math.hypot(math.fabs(THEORY['Z']['QCD'][m][1]), math.fabs(THEORY['Z']['PDF'][m][1])))*fdict[str(int(m))]['BRZh'])
  yTHUncs.append(fdict[str(int(m))]['CX0(pb)']*(1.+math.hypot(THEORY['Z']['QCD'][m][0], THEORY['Z']['PDF'][m][0]))*fdict[str(int(m))]['BRZh'])

for m in xrange(len(mass), 0, -1):
  x_uncs.append(mass[m-1]/1000.)
  yTHUncs.append(yTHDown[m-1])
  
fout = ROOT.TFile.Open('ZprimeZH.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
graphTHUP = ROOT.TGraph(len(x),x,yTHUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(x),x,yTHDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(x_uncs),x_uncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()

print "############ make root files DY Z'->WW #############"
yTH = array('d',[])
yTHDown = array('d',[])
yTHUp = array('d',[])
yTHUncs = array('d',[])
for i,m in enumerate(mass):
  yTH.append(fdict[str(int(m))]['CX0(pb)']*fdict[str(int(m))]['BRWW'])
  yTHUp.append(fdict[str(int(m))]['CX0(pb)']*(1.+math.hypot(THEORY['Z']['QCD'][m][0], THEORY['Z']['PDF'][m][0]))*fdict[str(int(m))]['BRWW'])
  yTHDown.append(fdict[str(int(m))]['CX0(pb)']*(1.-math.hypot(math.fabs(THEORY['Z']['QCD'][m][1]), math.fabs(THEORY['Z']['PDF'][m][1])))*fdict[str(int(m))]['BRWW'])
  yTHUncs.append(fdict[str(int(m))]['CX0(pb)']*(1.+math.hypot(THEORY['Z']['QCD'][m][0], THEORY['Z']['PDF'][m][0]))*fdict[str(int(m))]['BRWW'])

for m in xrange(len(mass), 0, -1): yTHUncs.append(yTHDown[m-1])
  
fout = ROOT.TFile.Open('ZprimeWW.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
graphTHUP = ROOT.TGraph(len(x),x,yTHUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(x),x,yTHDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(x_uncs),x_uncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()

print "############ make root files DY W'->WZ #############"
yTH = array('d',[])
yTHDown = array('d',[])
yTHUp = array('d',[])
yTHUncs = array('d',[])
for i,m in enumerate(mass):
  yTH.append( (fdict[str(int(m))]['CX+(pb)']+fdict[str(int(m))]['CX-(pb)'])*fdict[str(int(m))]['BRWZ'])
  yTHUp.append((fdict[str(int(m))]['CX+(pb)']+fdict[str(int(m))]['CX-(pb)'])*(1.+math.hypot(THEORY['W']['QCD'][m][0], THEORY['W']['PDF'][m][0]))*fdict[str(int(m))]['BRWZ'])
  yTHDown.append((fdict[str(int(m))]['CX+(pb)']+fdict[str(int(m))]['CX-(pb)'])*(1.-math.hypot(math.fabs(THEORY['W']['QCD'][m][1]), math.fabs(THEORY['W']['PDF'][m][1])))*fdict[str(int(m))]['BRWZ'])
  yTHUncs.append((fdict[str(int(m))]['CX+(pb)']+fdict[str(int(m))]['CX-(pb)'])*(1.+math.hypot(THEORY['W']['QCD'][m][0], THEORY['W']['PDF'][m][0]))*fdict[str(int(m))]['BRWZ'])

for m in xrange(len(mass), 0, -1): yTHUncs.append(yTHDown[m-1])  

fout = ROOT.TFile.Open('WprimeWZ.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
graphTHUP = ROOT.TGraph(len(x),x,yTHUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(x),x,yTHDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(x_uncs),x_uncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()

print "############ make root files DY W'->WH #############"
yTH = array('d',[])
yTHDown = array('d',[])
yTHUp = array('d',[])
yTHUncs = array('d',[])
for i,m in enumerate(mass):
  yTH.append( (fdict[str(int(m))]['CX+(pb)']+fdict[str(int(m))]['CX-(pb)'])*fdict[str(int(m))]['BRWh'])
  yTHUp.append((fdict[str(int(m))]['CX+(pb)']+fdict[str(int(m))]['CX-(pb)'])*(1.+math.hypot(THEORY['W']['QCD'][m][0], THEORY['W']['PDF'][m][0]))*fdict[str(int(m))]['BRWh'])
  yTHDown.append((fdict[str(int(m))]['CX+(pb)']+fdict[str(int(m))]['CX-(pb)'])*(1.-math.hypot(math.fabs(THEORY['W']['QCD'][m][1]), math.fabs(THEORY['W']['PDF'][m][1])))*fdict[str(int(m))]['BRWh'])
  yTHUncs.append((fdict[str(int(m))]['CX+(pb)']+fdict[str(int(m))]['CX-(pb)'])*(1.+math.hypot(THEORY['W']['QCD'][m][0], THEORY['W']['PDF'][m][0]))*fdict[str(int(m))]['BRWh'])

for m in xrange(len(mass), 0, -1): yTHUncs.append(yTHDown[m-1])    

fout = ROOT.TFile.Open('WprimeWH.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
graphTHUP = ROOT.TGraph(len(x),x,yTHUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(x),x,yTHDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(x_uncs),x_uncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()

print "############ make json files for VBF production mode #############"
df = pd.read_csv('HVTC.csv') 

mass = df['M'].values
xsec_zpr = df['Zprime_cH1'].values
xsec_zpr_up = df['Zprime Up'].values
xsec_zpr_down = df['Zprime Down'].values
br_zpr_ww = df['BrZprimeToWW'].values
br_zpr_zh = df['BrZprimeToZH'].values
xsec_wpr = df['Wprime_cH1'].values
xsec_wpr_up = df['Wprime Up'].values
xsec_wpr_down = df['Wprime Down'].values
br_wpr_wz = df['BrWprimeToWZ'].values
br_wpr_wh = df['BrWprimeToWH'].values

fdict = {}
for i,m in enumerate(mass):
 fdict[str(int(m))] = {}
 fdict[str(int(m))]['Zprime_cH1'] = xsec_zpr[i]
 fdict[str(int(m))]['Zprime_cH1_Up'] = xsec_zpr[i]*(1.+xsec_zpr_up[i]/100.)
 fdict[str(int(m))]['Zprime_cH1_Down'] = xsec_zpr[i]*(1.-math.fabs(xsec_zpr_down[i])/100.)
 fdict[str(int(m))]['BRWW'] = br_zpr_ww[i]
 fdict[str(int(m))]['BRZh'] = br_zpr_zh[i]
 fdict[str(int(m))]['Wprime_cH1'] = xsec_wpr[i]
 fdict[str(int(m))]['Wprime_cH1_Up'] = xsec_wpr[i]*(1.+xsec_wpr_up[i]/100.)
 fdict[str(int(m))]['Wprime_cH1_Down'] = xsec_wpr[i]*(1.-math.fabs(xsec_wpr_down[i])/100.)
 fdict[str(int(m))]['BRWh'] = br_wpr_wh[i]
 fdict[str(int(m))]['BRWZ'] = br_wpr_wz[i]
 
f=open("HVTC.json","w")
json.dump(fdict,f)
f.close() 

print "############ make root files VBF Z'->ZH #############"
yTH = array('d',[])
yTHDown = array('d',[])
yTHUp = array('d',[])
yTHUncs = array('d',[])
x = array('d',[])
x_uncs = array('d',[])
for i,m in enumerate(mass):
  x.append(m/1000.)
  x_uncs.append(m/1000.)
  yTH.append(fdict[str(int(m))]['Zprime_cH1']*fdict[str(int(m))]['BRZh'])
  yTHUp.append(fdict[str(int(m))]['Zprime_cH1_Up']*fdict[str(int(m))]['BRZh'])
  yTHDown.append(fdict[str(int(m))]['Zprime_cH1_Down']*fdict[str(int(m))]['BRZh'])
  yTHUncs.append(fdict[str(int(m))]['Zprime_cH1_Up']*fdict[str(int(m))]['BRZh'])

for m in xrange(len(mass), 0, -1):
  x_uncs.append(mass[m-1]/1000.)
  yTHUncs.append(yTHDown[m-1])
  
fout = ROOT.TFile.Open('HVTC_ZprimeZH.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
graphTHUP = ROOT.TGraph(len(x),x,yTHUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(x),x,yTHDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(x_uncs),x_uncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()

print "############ make root files VBF Z'->WW #############"
yTH = array('d',[])
yTHDown = array('d',[])
yTHUp = array('d',[])
yTHUncs = array('d',[])
for i,m in enumerate(mass):
  yTH.append(fdict[str(int(m))]['Zprime_cH1']*fdict[str(int(m))]['BRWW'])
  yTHUp.append(fdict[str(int(m))]['Zprime_cH1_Up']*fdict[str(int(m))]['BRWW'])
  yTHDown.append(fdict[str(int(m))]['Zprime_cH1_Down']*fdict[str(int(m))]['BRWW'])
  yTHUncs.append(fdict[str(int(m))]['Zprime_cH1_Up']*fdict[str(int(m))]['BRWW'])

for m in xrange(len(mass), 0, -1): yTHUncs.append(yTHDown[m-1])

fout = ROOT.TFile.Open('HVTC_ZprimeWW.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
graphTHUP = ROOT.TGraph(len(x),x,yTHUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(x),x,yTHDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(x_uncs),x_uncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()

print "############ make root files VBF W'->WZ #############"

yTH = array('d',[])
yTHDown = array('d',[])
yTHUp = array('d',[])
yTHUncs = array('d',[])
for i,m in enumerate(mass):
  yTH.append(fdict[str(int(m))]['Wprime_cH1']*fdict[str(int(m))]['BRWZ'])
  yTHUp.append(fdict[str(int(m))]['Wprime_cH1_Up']*fdict[str(int(m))]['BRWZ'])
  yTHDown.append(fdict[str(int(m))]['Wprime_cH1_Down']*fdict[str(int(m))]['BRWZ'])
  yTHUncs.append(fdict[str(int(m))]['Wprime_cH1_Up']*fdict[str(int(m))]['BRWZ'])

for m in xrange(len(mass), 0, -1): yTHUncs.append(yTHDown[m-1])

fout = ROOT.TFile.Open('HVTC_WprimeWZ.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
graphTHUP = ROOT.TGraph(len(x),x,yTHUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(x),x,yTHDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(x_uncs),x_uncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()

print "############ make root files VBF W'->WH #############"
yTH = array('d',[])
yTHDown = array('d',[])
yTHUp = array('d',[])
yTHUncs = array('d',[])
for i,m in enumerate(mass):
  yTH.append(fdict[str(int(m))]['Wprime_cH1']*fdict[str(int(m))]['BRWh'])
  yTHUp.append(fdict[str(int(m))]['Wprime_cH1_Up']*fdict[str(int(m))]['BRWh'])
  yTHDown.append(fdict[str(int(m))]['Wprime_cH1_Down']*fdict[str(int(m))]['BRWh'])
  yTHUncs.append(fdict[str(int(m))]['Wprime_cH1_Up']*fdict[str(int(m))]['BRWh'])

for m in xrange(len(mass), 0, -1): yTHUncs.append(yTHDown[m-1])

fout = ROOT.TFile.Open('HVTC_WprimeWH.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
graphTHUP = ROOT.TGraph(len(x),x,yTHUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(x),x,yTHDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(x_uncs),x_uncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()
