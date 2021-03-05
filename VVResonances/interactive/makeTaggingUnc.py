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

def loadJson(inputdir,signal,period):
    
    jsonname=inputdir+"/migrationunc_"+signal+"_"+period+".json"
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
    tagging=["Htag","Vtag"]
    category = options.categories.split(",")
    print category

    for tag in tagging:
        print "tag ",tag
        text_file = open("TaggingUncSIGNALS_"+tag+"_"+year+options.output+".txt", "w")

        for signal in signals:
            print " signal ",signal
            uncstring = signalstable[signal]
            unc = loadJson(inputdir,signal,year)
            for p in category:
                print " cat ",p
                uncup_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][p+"_up"]
                uncdown_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][p+"_down"]

                if tag == "Htag" and (p.find('VV_HPHP') !=-1 or p.find('VH_HPLP') !=-1 or p.find('VV_HPLP') !=-1):
                    if p.find('VV_HPHP') !=-1: ap = 'VH_HPHP'
                    if p.find('VH_HPLP') !=-1: ap = 'VH_LPHP'
                    if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
                    if p.find('VBF') !=-1 : ap = 'VBF_'+ap
                    uncdown_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_up"]
                    uncup_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_down"]
                elif tag == "Vtag" and (p.find('VH_LPHP')  !=-1 or p.find('VV_HPLP') !=-1 ):
                    if p.find('VH_LPHP') !=-1: ap = 'VV_HPHP'
                    if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
                    if p.find('VBF') !=-1 : ap = 'VBF_'+ap
                    uncdown_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_up"]
                    uncup_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_down"]

                uncstring= uncstring+" & "+str(uncdown_s)+"/"+ str(uncup_s)

            uncstring=uncstring+" \\\\ \n"
            print " uncstring ",uncstring
            text_file.write(uncstring)
        text_file.write("\\hline \n")

        for signal in signals:
            print " VBF signal ",signal
            uncstring = "VBF "+signalstable[signal]
            signal = "VBF_"+signal
            unc = loadJson(inputdir,signal,year)
            for p in category:
                print " cat ",p
                uncup_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][p+"_up"]
                uncdown_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][p+"_down"]
                if tag == "Htag" and (p.find('VV_HPHP') !=-1 or p.find('VH_HPLP') !=-1 or p.find('VV_HPLP') !=-1):
                    if p.find('VV_HPHP') !=-1: ap = 'VH_HPHP'
                    if p.find('VH_HPLP') !=-1: ap = 'VH_LPHP'
                    if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
                    if p.find('VBF') !=-1 : ap = 'VBF_'+ap
                    uncdown_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_up"]
                    uncup_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_down"]

                elif tag == "Vtag" and (p.find('VH_LPHP')  !=-1 or p.find('VV_HPLP') !=-1 ):
                    if p.find('VH_LPHP') !=-1: ap = 'VV_HPHP'
                    if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
                    if p.find('VBF') !=-1 : ap = 'VBF_'+ap
                    uncdown_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_up"]
                    uncup_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_down"]

                uncstring= uncstring+" & "+str(uncdown_s)+"/"+ str(uncup_s)
            uncstring=uncstring+" \\\\ \n"
            print " uncstring ",uncstring
            text_file.write(uncstring)



        text_file.write("*** VBF cat \n")
        print " VBF cat "
        
        for signal in signals:
            print " signal ",signal
            unc = loadJson(inputdir,signal,year)
            uncstring = signalstable[signal]
            for p in category:
                p = "VBF_"+p
                print " cat ",p
                uncup_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][p+"_up"]
                uncdown_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][p+"_down"]
                if tag == "Htag" and (p.find('VV_HPHP') !=-1 or p.find('VH_HPLP') !=-1 or p.find('VV_HPLP') !=-1):
                    if p.find('VV_HPHP') !=-1: ap = 'VH_HPHP'
                    if p.find('VH_HPLP') !=-1: ap = 'VH_LPHP'
                    if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
                    if p.find('VBF') !=-1 : ap = 'VBF_'+ap
                    uncdown_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_up"]
                    uncup_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_down"]

                elif tag == "Vtag" and (p.find('VH_LPHP')  !=-1 or p.find('VV_HPLP') !=-1 ):
                    if p.find('VH_LPHP') !=-1: ap = 'VV_HPHP'
                    if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
                    if p.find('VBF') !=-1 : ap = 'VBF_'+ap
                    uncdown_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_up"]
                    uncup_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_down"]

                uncstring= uncstring+" & "+str(uncdown_s)+"/"+ str(uncup_s)
            uncstring=uncstring+" \\\\ \n "
            print " uncstring ",uncstring
            text_file.write(uncstring)

        text_file.write("\\hline \n")



        for signal in signals:
            print " VBF signal ",signal
            uncstring = "VBF "+signalstable[signal]
            signal = "VBF_"+signal
            unc = loadJson(inputdir,signal,year)
            for p in category:
                p = "VBF_"+p
                print " cat ",p
                uncup_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][p+"_up"]
                uncdown_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][p+"_down"]
                if tag == "Htag" and (p.find('VV_HPHP') !=-1 or p.find('VH_HPLP') !=-1 or p.find('VV_HPLP') !=-1):
                    if p.find('VV_HPHP') !=-1: ap = 'VH_HPHP'
                    if p.find('VH_HPLP') !=-1: ap = 'VH_LPHP'
                    if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
                    if p.find('VBF') !=-1 : ap = 'VBF_'+ap
                    uncdown_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_up"]
                    uncup_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_down"]

                elif tag == "Vtag" and (p.find('VH_LPHP')  !=-1 or p.find('VV_HPLP') !=-1 ):
                    if p.find('VH_LPHP') !=-1: ap = 'VV_HPHP'
                    if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
                    if p.find('VBF') !=-1 : ap = 'VBF_'+ap
                    uncdown_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_up"]
                    uncup_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag+"_eff"][ap+"_down"]

                uncstring= uncstring+" & "+str(uncdown_s)+"/"+ str(uncup_s)

            uncstring=uncstring+" \\\\ \n "
            print " uncstring ",uncstring
            text_file.write(uncstring)



        text_file.close()

    
    # Now backgrounds!!
    print " ********* backgrounds "
    signals = ["WJets","ZJets","resT","resW","nonresT","resTnonresT","resWnonresT","resTresW"]
    signalsTag = {"Htag_eff":["WJets","ZJets","resW","resWnonresT","resTresW"],
                  "Vtag_eff":["WJets","ZJets","resW","resWnonresT","resTresW"],
                  "TOPtag_mistag":["resT","resTnonresT","resTresW"]}

    signalstable ={"WJets":"W+Jets","ZJets":"Z+Jets","resT":"\\ttbar (TT) ","resW":"\\ttbar (WW) ","nonresT":"\\ttbar (nonRes) ","resTnonresT":"\\ttbar(TnonRes)","resWnonresT":"\\ttbar (WnonRes)","resTresW":"\\ttbar (WT)"}

    tagging=["Htag_eff","Vtag_eff","TOPtag_mistag"]
    mappdf = {"resT":"TTJetsTop","resW":"TTJetsW","nonresT":"TTJetsNonRes","resTnonresT":"TTJetsTNonResT","resWnonresT":"TTJetsWNonResT","resTresW":"TTJetsResWResT"}


    for tag in tagging:
        print "tag ",tag
        text_file = open("TaggingUncBKG_"+tag+"_"+year+options.output+".txt", "w")
        text_file.write(tag+"\n")
        for signal in signals:
            print " signal ",signal
    
            uncstring = signalstable[signal]
            if signal not in signalsTag[tag]:
                print " signal ",signal," not in ",tag
                for p in category: 
                    uncstring=uncstring+" & - "
            else:
                if "Jets" not in signal:
                    unc = loadJson(inputdir,"TTJets",year)
                else:
                    unc = loadJson(inputdir,signal,year)

                for p in category:
                    print " cat ",p
                    if "Jets" in signal:
                        uncup_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag][signal+"."+p+"_up"]
                        uncdown_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag][signal+"."+p+"_down"]
                    else:
                        uncup_s   = unc["TTJets_CMS_VV_JJ_DeepJet_"+tag][mappdf[signal]+"."+p+"_up"]
                        uncdown_s = unc["TTJets_CMS_VV_JJ_DeepJet_"+tag][mappdf[signal]+"."+p+"_down"]

                    if tag == "Htag_eff" and (p.find('VV_HPHP') !=-1 or p.find('VH_HPLP') !=-1 or p.find('VV_HPLP') !=-1):
                        if p.find('VV_HPHP') !=-1: ap = 'VH_HPHP'
                        if p.find('VH_HPLP') !=-1: ap = 'VH_LPHP'
                        if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
                        if p.find('VBF') !=-1 : ap = 'VBF_'+ap
                        if "Jets" in signal:
                            uncdown_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag][signal+"."+ap+"_up"]
                            uncup_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag][signal+"."+ap+"_down"]
                        else:
                            uncdown_s   = unc["TTJets_CMS_VV_JJ_DeepJet_"+tag][mappdf[signal]+"."+ap+"_up"]
                            uncup_s = unc["TTJets_CMS_VV_JJ_DeepJet_"+tag][mappdf[signal]+"."+ap+"_down"]

                    elif tag == "Vtag_eff" and (p.find('VH_LPHP')  !=-1 or p.find('VV_HPLP') !=-1 ):
                        if p.find('VH_LPHP') !=-1: ap = 'VV_HPHP'
                        if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
                        if p.find('VBF') !=-1 : ap = 'VBF_'+ap
                        if "Jets" in signal:
                            uncdown_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag][signal+"."+ap+"_up"]
                            uncup_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag][signal+"."+ap+"_down"]
                        else:
                            uncdown_s   = unc["TTJets_CMS_VV_JJ_DeepJet_"+tag][mappdf[signal]+"."+ap+"_up"]
                            uncup_s = unc["TTJets_CMS_VV_JJ_DeepJet_"+tag][mappdf[signal]+"."+ap+"_down"]


                    uncstring= uncstring+" & "+str(uncdown_s)+"/"+ str(uncup_s)
                
            uncstring=uncstring+" \\\\ \n"
            print " uncstring ",uncstring
            text_file.write(uncstring)





        text_file.write("*** VBF cat \n")
        print " VBF cat "
        

        text_file.write("\\hline \n")

        for signal in signals:
            print " signal ",signal
    
            uncstring = signalstable[signal]
            if signal not in signalsTag[tag]: 
                for p in category:
                    uncstring=uncstring+" & - "
            else:
                if "Jets" not in signal:
                    unc = loadJson(inputdir,"TTJets",year)
                else:
                    unc = loadJson(inputdir,signal,year)

                for p in category:
                    print " VBF cat ",p
                    p = "VBF_"+p
                    if "Jets" in signal:
                        uncup_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag][signal+"."+p+"_up"]
                        uncdown_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag][signal+"."+p+"_down"]
                    else:
                        uncup_s   = unc["TTJets_CMS_VV_JJ_DeepJet_"+tag][mappdf[signal]+"."+p+"_up"]
                        uncdown_s = unc["TTJets_CMS_VV_JJ_DeepJet_"+tag][mappdf[signal]+"."+p+"_down"]

                    if tag == "Htag_eff" and (p.find('VV_HPHP') !=-1 or p.find('VH_HPLP') !=-1 or p.find('VV_HPLP') !=-1):
                        if p.find('VV_HPHP') !=-1: ap = 'VH_HPHP'
                        if p.find('VH_HPLP') !=-1: ap = 'VH_LPHP'
                        if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
                        if p.find('VBF') !=-1 : ap = 'VBF_'+ap
                        if "Jets" in signal:
                            uncdown_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag][signal+"."+ap+"_up"]
                            uncup_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag][signal+"."+ap+"_down"]
                        else:
                            uncdown_s   = unc["TTJets_CMS_VV_JJ_DeepJet_"+tag][mappdf[signal]+"."+ap+"_up"]
                            uncup_s = unc["TTJets_CMS_VV_JJ_DeepJet_"+tag][mappdf[signal]+"."+ap+"_down"]

                    elif tag == "Vtag_eff" and (p.find('VH_LPHP')  !=-1 or p.find('VV_HPLP') !=-1 ):
                        if p.find('VH_LPHP') !=-1: ap = 'VV_HPHP'
                        if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
                        if p.find('VBF') !=-1 : ap = 'VBF_'+ap
                        if "Jets" in signal:
                            uncdown_s   = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag][signal+"."+ap+"_up"]
                            uncup_s = unc[signal+"_CMS_VV_JJ_DeepJet_"+tag][signal+"."+ap+"_down"]
                        else:
                            uncdown_s   = unc["TTJets_CMS_VV_JJ_DeepJet_"+tag][mappdf[signal]+"."+ap+"_up"]
                            uncup_s = unc["TTJets_CMS_VV_JJ_DeepJet_"+tag][mappdf[signal]+"."+ap+"_down"]


                    uncstring= uncstring+" & "+str(uncdown_s)+"/"+ str(uncup_s)
                
            uncstring=uncstring+" \\\\ \n"
            print " uncstring ",uncstring
            text_file.write(uncstring)
                




        text_file.close()

