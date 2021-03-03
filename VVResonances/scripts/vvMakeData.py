#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from math import log
import os, sys, re, optparse,pickle,shutil,json
ROOT.v5.TFormula.SetMaxima(10000) #otherwise we get an error that the TFormula called by the TTree draw has too many operators when running on the CR
sys.path.insert(0, "../interactive/")
import cuts


parser = optparse.OptionParser()
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield",default='')
parser.add_option("-o","--output",dest="output",help="Output ROOT",default='')
parser.add_option("-v","--vars",dest="vars",help="variables seprataed by comma",default='')
parser.add_option("-b","--bins",dest="bins",help="bins per dimension separated by comma",default='')
parser.add_option("-m","--min",dest="mins",help="minimum separated by comma",default='')
parser.add_option("-M","--max",dest="maxes",help="maximum separated by comma",default='')
parser.add_option("-d","--isData",dest="data",type=int,help="isData",default=1)
parser.add_option("-f","--factors",dest="factors",type=str,help="factor",default="1")
parser.add_option("-n","--name",dest="name",help="name",default="histo")
parser.add_option("--binsMVV",dest="binsMVV",help="use special binning",default="")
parser.add_option("-t","--triggerweight",dest="triggerW",action="store_true",help="Use trigger weights",default=False)

(options,args) = parser.parse_args()
#define output dictionary

samples={}

def getBinning(binsMVV):
    l=[]
    if binsMVV!="":
        s = binsMVV.split(",")
        for w in s:
            l.append(int(w))
    return l

sampleTypes=options.samples.split(',')

dataPlotters=[]

print "args[0] "+str(args[0])
try: year=str(args[0]).split("/")[-2]
except: year=options.output.split("_")[1]
print "year ",year
print "now working with cuts "
ctx = cuts.cuts("init_VV_VH.json",year,"dijetbins_random")
print "lumi for year "+year+" = ",ctx.lumi[year]
luminosity = ctx.lumi[year]/ctx.lumi["Run2"]
if options.output.find("1617") !=-1 :luminosity = ctx.lumi[year]/ctx.lumi["1617"]
if options.output.find("Run2") ==-1 or options.output.find("1617") ==-1 or options.name.find("data")!=-1 : luminosity = 1
print " lumi rewight ",luminosity

for filename in os.listdir(args[0]):
    if filename.find(".")==-1:
        print "in "+str(filename)+"the separator . was not found. -> continue!"
        continue
    for sampleType in sampleTypes:
        if filename.find(sampleType)!=-1:
            fnameParts=filename.split('.')
            fname=fnameParts[0]
            ext=fnameParts[1]
            if ext.find("root") ==-1:
                continue
            dataPlotters.append(TreePlotter(args[0]+'/'+fname+'.root','AnalysisTree'))
            if options.data==0 or options.data==2:
                dataPlotters[-1].setupFromFile(args[0]+'/'+fname+'.pck')
                dataPlotters[-1].addCorrectionFactor('xsec','tree')
                genweight='genWeight'
                if (year == "2017" or year == "2018") and fname.find("TT") !=-1:  genweight='genWeight_LO'
                dataPlotters[-1].addCorrectionFactor(genweight,'tree')
                dataPlotters[-1].addCorrectionFactor('puWeight','tree')
                dataPlotters[-1].addCorrectionFactor(luminosity,'flat')
                if fname.find("QCD_Pt_") !=-1 or fname.find("QCD_HT") !=-1:
                    print "going to apply spikekiller for ",fname
                    dataPlotters[-1].addCorrectionFactor('b_spikekiller','tree')
                if options.triggerW:
                    print "Using triggerweights! Are you sure?"
                    dataPlotters[-1].addCorrectionFactor('triggerWeight','tree')	
                if fname.find("TT") !=-1:
                    print "applying top pt reweight"
                    dataPlotters[-1].addCorrectionFactor('TopPTWeight','tree')
                if fname.find("Jets") !=-1 or fname.find("TT")!=-1:
                    print "applying tagging SF"
                    dataPlotters[-1].addFriend("all","../interactive/migrationunc/"+fname+"_"+year+".root")
                    dataPlotters[-1].addCorrectionFactor("all.SF",'tree')
                if fname.find("Jets") !=-1:
                    print "applying k factors "
                    dataPlotters[-1].addCorrectionFactor("kfactor",'tree')
                if fname.find("Jets") !=-1 or  fname.find("TT")!=-1 or fname.find("QCD") !=-1:
                    print "applying L1 prefiring weights "
                    dataPlotters[-1].addCorrectionFactor("L1prefWeight",'tree')

data=MergedPlotter(dataPlotters)


pvars=options.vars.split(',')
pmins=options.mins.split(',')
pmaxes=options.maxes.split(',')
pbins=options.bins.split(',')

if len(pvars)==1:
    histo=data.drawTH1(pvars[0],options.cut,"1",int(pbins[0]),float(pmins[0]),float(pmaxes[0]))


if len(pvars)==2:
    histo=data.drawTH2(pvars[1]+":"+pvars[0],options.cut,"1",int(pbins[0]),float(pmins[0]),float(pmaxes[0]),int(pbins[1]),float(pmins[1]),float(pmaxes[1]))

if len(pvars)==3:
    binning = getBinning(options.binsMVV)
    print "z ",pvars[2], "y ", pvars[1], "x ", pvars[0]
    print "binsz ",int(pbins[2])," minz ", float(pmins[2])," maxz ", float(pmaxes[2])
    print "binsy ",int(pbins[1])," miny ", float(pmins[1])," maxy ", float(pmaxes[1])
    print "binsx ",int(pbins[0])," minx ", float(pmins[0])," maxx ", float(pmaxes[0])
    if options.binsMVV=="":
        histo=data.drawTH3(pvars[2]+":"+pvars[1]+":"+pvars[0],options.cut,"1",int(pbins[0]),float(pmins[0]),float(pmaxes[0]),int(pbins[1]),float(pmins[1]),float(pmaxes[1]),int(pbins[2]),float(pmins[2]),float(pmaxes[2]))
    else:
        binsx=[]
        for i in range(0,int(pbins[0])+1):
            binsx.append(float(pmins[0])+i*(float(pmaxes[0])-float(pmins[0]))/int(pbins[0]))
        histo=data.drawTH3Binned(pvars[2]+":"+pvars[1]+":"+pvars[0],options.cut,"1",array('f',binsx),array('f',binsx),array('f',binning))

F=ROOT.TFile(options.output,"RECREATE")
F.cd()
histo.Write(options.name)
F.Close()



