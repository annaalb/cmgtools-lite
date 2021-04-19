#!/usr/bin/env python                                                                                                                                                                   
import ROOT
from array import array
import argparse
import os, sys, re, optparse,pickle,shutil,json, copy
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.v5.TFormula.SetMaxima(10000) #otherwise we get an error that the TFormula called by the TTree draw has too many operators when running on the CR                                    
from  CMGTools.VVResonances.plotting.CMS_lumi import *
#sys.path.insert(0, "../interactive/")                                                                                                                                                   
import cuts

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="outname",default='')
parser.add_option("-i","--inputdir",dest="inputdir",help="directory where the input files are stored",default="results_Run2")
parser.add_option("-p","--period",dest="period",help="2016 or 2017 or 2016,2017,2018",default="2016,2017,2018")
parser.add_option("-c","--categories",dest="categories",help="VV_HPHP etc",default="VH_HPHP,VV_HPHP,VH_LPHP,VH_HPLP,VV_HPLP")
parser.add_option("-v","--vbf",dest="vbf",help="make vbf?",action='store_true')

(options,args) = parser.parse_args()

def loadJson(inputdir,signal,cat,unc,case):
    
    jsonname=inputdir+"/"+unc+"_case"+case+"_"+signal+"_"+cat+".json"
    with open(jsonname) as jsonFile:
        print " opened json file ",jsonname
        j = json.load(jsonFile)
    #print j
    return j





if __name__ == "__main__":
    signals = ["RadionWW","RadionZZ","WprimeWZ","WprimeWHinc","ZprimeWW","ZprimeZHinc","BulkGWW","BulkGZZ"]
    signalstable ={"RadionWW":"Radion$\\to\\Wo\\Wo$","RadionZZ":"Radion$\\to\\Zo\\Zo$","WprimeWZ":"$\\Wpr\\to\\Wo\\Zo$ ","WprimeWHinc":"$\\Wpr\\to\\Wo\\Ho$" ,"ZprimeWW":"$\\Zprime\\to\\Wo\\Wo$","ZprimeZHinc":"$\\Zprime\\to\\Zo\\Ho$" ,"BulkGWW":"$\\BulkG\\to\\Wo\\Wo$","BulkGZZ":"$\\BulkG\\to\\Zo\\Zo$"}
    if options.period.find(",")!=-1 and len(options.period.split(",")) == 3:
        year = "Run2"
    else: year = options.period
    inputdir = options.inputdir
    tagging=["nonVBFcat","VBFcat"]
    unctype=["JES","JER"]
    category = options.categories.split(",")
    print category
    unc={}
    uncVBF={}

    text_file = open("JESJERUncSIGNALS_"+year+"_"+options.output+".txt", "w")

    #fixme : cycle on signal then the rest!

    case="1"
    for u in unctype:
        print " doing ",u
        for tag in tagging:
            print "tag ",tag

            unc[u] = loadJson(inputdir,"nonVBFsig","nonVBFcat",u,case)
            uncVBF[u] = loadJson(inputdir,"nonVBFsig","VBFcat",u,case)
            
    for signal in signals:
        print " signal ",signal

        for u in unctype:
            unc[u][signal]=round(abs(1-unc[u][signal])*100,1)
            uncVBF[u][signal]=round(abs(1-uncVBF[u][signal])*100,1)

        uncstring = signalstable[signal]+" & "+str(unc["JES"][signal])+" & "+str(uncVBF["JES"][signal])+" & "+str(unc["JER"][signal])+" & "+str(uncVBF["JER"][signal])+"\\\\ \n"
        print " uncstring ",uncstring
        text_file.write(uncstring)

    text_file.write("\\hline \n")

    for u in unctype:
        print " doing ",u
        for tag in tagging:
            print "tag ",tag

            unc[u] = loadJson(inputdir,"VBFsig","nonVBFcat",u,case)
            uncVBF[u] = loadJson(inputdir,"VBFsig","VBFcat",u,case)
            
    for signal in signals:

        for u in unctype:
            unc[u][signal]=round(abs(1-unc[u][signal])*100,1)
            uncVBF[u][signal]=round(abs(1-uncVBF[u][signal])*100,1)

        print " VBF signal ",signal
        uncstring = "VBF "+signalstable[signal]+" & "+str(unc["JES"][signal])+" & "+str(uncVBF["JES"][signal])+" & "+str(unc["JER"][signal])+" & "+str(uncVBF["JER"][signal])+"\\\\ \n"
        print " uncstring ",uncstring
        text_file.write(uncstring)


text_file.close()

