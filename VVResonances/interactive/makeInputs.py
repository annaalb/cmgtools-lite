from functions import *
from optparse import OptionParser
#from cuts import cuts, HPSF16, HPSF17, LPSF16, LPSF17, dijetbins, HCALbinsMVVSignal, minMJ,maxMJ,binsMJ, minMVV, maxMVV, binsMVV, minMX, maxMX, catVtag, catHtag
import cuts
import argparse
## import cuts of the analysis from separate file

# python makeInputs.py -p 2016 --run "detector" --batch False
# python makeInputs.py -p 2016 --run "signorm" --signal "ZprimeWW" --batch False
# python makeInputs.py -p 2016 --run "tt" --batch False
# python makeInputs.py -p 2016 --run "vjets" --batch False
# python makeInputs.py -p "2016,2017,2018"  --run "vjetsAll"
# python makeInputs.py -p "2016,2017,2018"  --run "vjetsfits"
# python makeInputs.py -p "2016,2017,2018"  --run "vjetskernel"
# python makeInputs.py -p "2016"  --run "vjetsSF"
# python makeInputs.py -p "2016,2017,2018"  --run "vjetsnorm"
# python makeInputs.py -p 2016 --run "qcdtemplates"
# python makeInputs.py -p 2016 --run "qcdkernel"
# python makeInputs.py -p "2016,2017,2018" --run "qcdkernel"  --single True
# python makeInputs.py -p 2016 --run "qcdnorm"
# python makeInputs.py -p 2016 --run "data"
# python makeInputs.py -p 2016 --run "pseudoNOVJETS"
# python makeInputs.py -p 2016 --run "pseudoVJETS"
# python makeInputs.py -p 2016 --run "pseudoTT"
# python makeInputs.py -p 2016 --run "pseudoALL" #to produce also the TT pseudodata

parser = OptionParser()
parser.add_option("-p","--period",dest="period",default="2016",help="run period")
parser.add_option("-s","--sorting",dest="sorting",help="b-tag or random sorting",default='random')
parser.add_option("-b","--binning",action="store_false",dest="binning",help="use dijet binning or not",default=True)
parser.add_option("--batch",action="store_false",dest="batch",help="submit to batch or not ",default=True)
parser.add_option("--trigg",action="store_true",dest="trigg",help="add trigger weights or not ",default=False)
parser.add_option("--run",dest="run",help="decide which parts of the code should be run right now possible optoins are: all : run everything, sigmvv: run signal mvv fit sigmj: run signal mj fit, signorm: run signal norm, vjets: run vjets, tt: run ttbar , qcdtemplates: run qcd templates, qcdkernel: run qcd kernel, qcdnorm: run qcd merge and norm, detector: run detector fit , data : run the data or pseudodata scripts ",default="all")
parser.add_option("--signal",dest="signal",default="BGWW",help="which signal do you want to run? options are BGWW, BGZZ, WprimeWZ, ZprimeWW, ZprimeZH, RWW, RZZ and VBF combination")
parser.add_option("--fitsmjj",dest="fitsmjj",default=False,action="store_true",help="True makes fits for mjj of vjets/tt, False uses hists")
parser.add_option("--fittempl",dest="fittempl",default=False,action="store_true",help="True derives templates for mjj of vjets/tt starting from a fit function in stead of smoothening, False uses default templates")
parser.add_option("--single",dest="single",default=False,help="set to True to merge kernels also for single years when processing full run2 data")
parser.add_option("--sendjobs",dest="sendjobs",default=True,help="make job list without submitting them (useful to only merge jobs if something was not finished")
parser.add_option("-c",dest="category",default="VH_HPHP,VH_HPLP,VH_LPHP,VV_HPHP,VV_HPLP",help="chose the category, e.g. NP or VV_HPHP")
parser.add_option("-t",dest="ttcontrib",default="resT,resW,nonresT,resTnonresT,resWnonresT,resTresW",help="chose the ttbar contribution you want to run on, e.g. resT")
parser.add_option("--vbf",dest="vbf",help="make vbf?",action='store_true')
parser.add_option("--vv",dest="vv",help="make VV only (no VHveto) ?",action='store_true',default=False)
parser.add_option("--tau",dest="tau",help="use tau21 ?",action='store_true')
parser.add_option("--four",dest="four",help="merge VH HPLP in VV HPLP ?",action='store_true')
parser.add_option("--kfactors",dest="kfactors",help="use combination of kfactors as V+Jets MVV alternative shapes?",action='store_true',default=False)
parser.add_option("-i","--inputdir",dest="inputdir",help="input direcory of all the files",default='results_Run2')
parser.add_option("--qcdsf",dest="qcdsf",help="Combine with rescale= True to rescale the QCD in pseudodata by a sf",default=1.8)
(options,args) = parser.parse_args()

widerMVV=True

jsonfile="init_VV_VH.json"

if options.vv == True:
    print " ^^^^^^^^^^^^^^ Running on VV only!!!! ^^^^^^^^^^^^^^^^"
    ctx  = cuts.cuts(jsonfile,options.period,options.sorting+"VVdijetbins",widerMVV)
    if options.tau == True:
        ctx  = cuts.cuts(jsonfile,options.period,options.sorting+"VVtaudijetbins",widerMVV)
elif options.four == True:
    print " ^^^^^^^^^^^^^^ Running with VH HPLP merged in VV HPLP ^^^^^^^^^^^^^^^^"
    ctx  = cuts.cuts(jsonfile,options.period,options.sorting+"4dijetbins",widerMVV)
else:
    ctx  = cuts.cuts(jsonfile,options.period,options.sorting+"dijetbins",widerMVV)
if options.binning==False: ctx  = cuts.cuts(jsonfile,int(options.period),options.sorting,widerMVV)

basedir=""
#basedir="deepAK8V2/"
print "options.period  ",options.period
period = options.period
samples=""
filePeriod=period
rescale=True #for pseudodata: set to True if you want to rescale QCD
if options.period.find(",")!=-1:
    period = options.period.split(',')
    filePeriod="Run2"
    if "2018" not in options.period: filePeriod = "1617"
    for year in period:
        print year
        if year==period[-1]: samples+=basedir+year+"/"
        else: samples+=basedir+year+"/,"
else: samples=basedir+period+"/"
# NB to use the DDT decorrelation method, the ntuples in /eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/deepAK8V2/ should be used

print "period ",period
print "sample ",samples

sorting = options.sorting

submitToBatch = options.batch #Set to true if you want to submit kernels + makeData to batch!
runParallel   = True #Set to true if you want to run all kernels in parallel! This will exit this script and you will have to run mergeKernelJobs when your jobs are done!

dijetBinning = options.binning
useTriggerWeights = options.trigg



addOption = ""
if useTriggerWeights:
    addOption = "-t"

#all categories
categories=options.category.split(",")

if options.vbf == True:
    for cat in options.category.split(","):
        categories.append("VBF_"+cat)

if options.category == "all": categories = ["VV_HPLP","VV_HPHP","VH_HPLP","VH_HPHP","VH_LPHP","VBF_VV_HPLP","VBF_VV_HPHP","VBF_VH_HPLP","VBF_VH_HPHP","VBF_VH_LPHP"]
if options.category == "VBF": categories = ["VBF_VV_HPLP","VBF_VV_HPHP","VBF_VH_HPLP","VBF_VH_HPHP","VBF_VH_LPHP"]
if options.category == "ggDY": categories = ["VV_HPLP","VV_HPHP","VH_HPLP","VH_HPHP","VH_LPHP"]
if options.category=="four": categories = ["VV_HPLP","VV_HPHP","VH_HPHP","VH_LPHP"]
if options.category=="fourvbf": categories = ["VV_HPLP","VV_HPHP","VH_HPHP","VH_LPHP","VBF_VV_HPLP","VBF_VV_HPHP","VBF_VH_HPHP","VBF_VH_LPHP"]

print " ********* running on categories: ",categories

#list of signal samples --> nb, radion and vbf samples to be added
BulkGravWWTemplate="BulkGravToWW_"
VBFBulkGravWWTemplate="VBF_BulkGravToWW_"
BulkGravZZTemplate="BulkGravToZZToZhadZhad_"
VBFBulkGravZZTemplate="VBF_BulkGravToZZ_"
ZprimeWWTemplate= "ZprimeToWW_"
VBFZprimeWWTemplate= "VBF_ZprimeToWW_"
ZprimeZHTemplate="ZprimeToZhToZhadhbb_"
VBFZprimeZHTemplate="VBF_ZprimeToZhToZhadhbb_"
ZprimeZHincTemplate="ZprimeToZhToZhadhinc_"
VBFZprimeZHincTemplate="VBF_ZprimeToZhToZhadhinc_"
WprimeWZTemplate= "WprimeToWZToWhadZhad_"
VBFWprimeWZTemplate= "VBF_WprimeToWZ_"
WprimeWHTemplate="WprimeToWhToWhadhbb_" #"WprimeToWhToWhadhbb_"
VBFWprimeWHTemplate="VBF_WprimeToWhToWhadhbb_" #"WprimeToWhToWhadhbb_"
WprimeWHincTemplate="WprimeToWhToWhadhinc_" #"WprimeToWhToWhadhbb_"
VBFWprimeWHincTemplate="VBF_WprimeToWhToWhadhinc_" #"WprimeToWhToWhadhbb_"
RadionWWTemplate="RadionToWW_"
VBFRadionWWTemplate="VBF_RadionToWW_"
RadionZZTemplate="RadionToZZ_"
VBFRadionZZTemplate="VBF_RadionToZZ_"

# use arbitrary cross section 0.001 so limits converge better
BRZZ=1.*0.001*0.6991*0.6991
BRZZincl=1.*0.001
BRWW=1.*0.001 #ZprimeWW and GBulkWW are inclusive
BRZH=1.*0.001*0.6991*0.584
BRZHinc=1.*0.001*0.6991
BRWZ=1.*0.001*0.6991*0.676
BRWZincl=1.*0.001
BRWH=1.*0.001*0.676*0.584
BRWHinc=1.*0.001*0.676

#data samples
dataTemplate="JetHT"

#background samples
#nonResTemplate="QCD_Pt-" #low stat herwig
#nonResTemplate="QCD_HT" #medium stat madgraph+pythia
nonResTemplate="QCD_Pt_" #high stat pythia8

STemplate= "ST_tW_antitop,ST_tW_top"
WWTemplate="SM_WWTo4Q"
TTemplate= "TT_Mtt-700to1000,TT_Mtt-1000toInf,ST_tW_antitop,ST_tW_top,SM_WWTo4Q"

WresTemplate= "WJetsToQQ_HT400to600,WJetsToQQ_HT600to800,WJetsToQQ_HT800toInf"
ZresTemplate= "ZJetsToQQ_HT400to600,ZJetsToQQ_HT600to800,ZJetsToQQ_HT800toInf"
resTemplate= "ZJetsToQQ_HT400to600,ZJetsToQQ_HT600to800,ZJetsToQQ_HT800toInf,WJetsToQQ_HT400to600,WJetsToQQ_HT600to800,WJetsToQQ_HT800toInf"
if options.tau:
    print " W jets + Ttbar together!! "
    WresTemplate=WresTemplate+",TT_Mtt-700to1000,TT_Mtt-1000toInf"
    resTemplate=resTemplate+",TT_Mtt-700to1000,TT_Mtt-1000toInf"
print " WresTemplate ",WresTemplate

#do not change the order here, add at the end instead
parameters = [ctx.cuts,ctx.minMVV,ctx.maxMVV,ctx.minMX,ctx.maxMX,ctx.binsMVV,ctx.HCALbinsMVV,samples,categories,ctx.minMJ,ctx.maxMJ,ctx.binsMJ,ctx.lumi,submitToBatch]
f = AllFunctions(parameters)


#parser.add_option("--signal",dest="signal",default="BGWW",help="which signal do you want to run? options are BGWW, BGZZ, WprimeWZ, ZprimeWW, ZprimeZH")
if options.run.find("all")!=-1 or options.run.find("sig")!=-1:
    if options.signal.find("ZprimeZH")!=-1 and not 'VBF' in options.signal and not 'inc' in options.signal:
        signal_inuse="ZprimeZH"
        signaltemplate_inuse=ZprimeZHTemplate
        xsec_inuse=BRZH
    elif options.signal.find("VBFZprimeZH")!=-1 and not 'inc' in options.signal:
        signal_inuse="VBF_ZprimeZH"
        signaltemplate_inuse=VBFZprimeZHTemplate
        xsec_inuse=BRZH
    elif options.signal.find("ZprimeZHinc")!=-1 and not 'VBF' in options.signal:
        signal_inuse="ZprimeZHinc"
        signaltemplate_inuse=ZprimeZHincTemplate
        xsec_inuse=BRZHinc
    elif options.signal.find("VBFZprimeZHinc")!=-1:
        signal_inuse="VBF_ZprimeZHinc"
        signaltemplate_inuse=VBFZprimeZHincTemplate
        xsec_inuse=BRZHinc
    elif options.signal.find("BGWW")!=-1 and not 'VBF' in options.signal:
        signal_inuse="BulkGWW"
        signaltemplate_inuse=BulkGravWWTemplate
        xsec_inuse=BRWW
    elif options.signal.find("VBFBGWW")!=-1:
        signal_inuse="VBF_BulkGWW"
        signaltemplate_inuse=VBFBulkGravWWTemplate
        xsec_inuse=BRWW
    elif options.signal.find("BGZZ")!=-1 and not 'VBF' in options.signal:
        signal_inuse="BulkGZZ"
        signaltemplate_inuse=BulkGravZZTemplate
        xsec_inuse=BRZZ
    elif options.signal.find("VBFBGZZ")!=-1:
        signal_inuse="VBF_BulkGZZ"
        signaltemplate_inuse=VBFBulkGravZZTemplate
        xsec_inuse=BRZZincl
    elif options.signal.find("ZprimeWW")!=-1 and not 'VBF' in options.signal:
        signal_inuse="ZprimeWW"
        signaltemplate_inuse=ZprimeWWTemplate
        xsec_inuse=BRWW
    elif options.signal.find("VBFZprimeWW")!=-1:
        signal_inuse="VBF_ZprimeWW"
        signaltemplate_inuse=VBFZprimeWWTemplate
        xsec_inuse=BRWW
    elif options.signal.find("WprimeWZ")!=-1 and not 'VBF' in options.signal:
        signal_inuse="WprimeWZ"
        signaltemplate_inuse=WprimeWZTemplate
        xsec_inuse=BRWZ
    elif options.signal.find("VBFWprimeWZ")!=-1:
        signal_inuse="VBF_WprimeWZ"
        signaltemplate_inuse=VBFWprimeWZTemplate
        xsec_inuse=BRWZincl
    elif options.signal.find("WprimeWH")!=-1 and not 'VBF' in options.signal and not 'inc' in options.signal:
        signal_inuse="WprimeWH"
        signaltemplate_inuse=WprimeWHTemplate
        xsec_inuse=BRWH
    elif options.signal.find("VBFWprimeWH")!=-1 and not 'inc' in options.signal:
        signal_inuse="VBF_WprimeWH"
        signaltemplate_inuse=VBFWprimeWHTemplate
        xsec_inuse=BRWH
    elif options.signal.find("WprimeWHinc")!=-1 and not 'VBF' in options.signal:
        signal_inuse="WprimeWHinc"
        signaltemplate_inuse=WprimeWHincTemplate
        xsec_inuse=BRWHinc
    elif options.signal.find("VBFWprimeWHinc")!=-1:
        signal_inuse="VBF_WprimeWHinc"
        signaltemplate_inuse=VBFWprimeWHincTemplate
        xsec_inuse=BRWHinc
    elif options.signal.find("RWW")!=-1 and not 'VBF' in options.signal:
        signal_inuse="RadionWW"
        signaltemplate_inuse=RadionWWTemplate
        xsec_inuse=BRWW
    elif options.signal.find("VBFRWW")!=-1:
        signal_inuse="VBF_RadionWW"
        signaltemplate_inuse=VBFRadionWWTemplate
        xsec_inuse=BRWW
    elif options.signal.find("RZZ")!=-1 and not 'VBF' in options.signal:
        signal_inuse="RadionZZ"
        signaltemplate_inuse=RadionZZTemplate
        xsec_inuse=BRZZincl
    elif options.signal.find("VBFRZZ")!=-1:
        signal_inuse="VBF_RadionZZ"
        signaltemplate_inuse=VBFRadionZZTemplate
        xsec_inuse=BRZZincl
    else:
        print "signal "+str(options.signal)+" not found!"
        sys.exit()


fixParsSig=ctx.fixParsSig

fixParsSigMVV=ctx.fixParsSigMVV


if options.run.find("all")!=-1 or options.run.find("sig")!=-1:
    print "run signal"
    if options.run.find("all")!=-1 or options.run.find("mj")!=-1:
        print "mj fit for signal "
        if sorting == "random":
            if signal_inuse.find("H")!=-1:
                f.makeSignalShapesMJ("JJ_Vjet_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,'random', fixParsSig[signal_inuse.replace('VBF_','')],"jj_random_mergedVTruth==1")
                if signal_inuse.find("inc")==-1:
                    f.makeSignalShapesMJ("JJ_Hjet_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,'random',fixParsSig[signal_inuse.replace('VBF_','')],"jj_random_mergedHbbTruth==1")
                else:
                    f.makeSignalShapesMJ("JJ_Hjet_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,'random',fixParsSig[signal_inuse.replace('VBF_','')],"jj_random_mergedHbbTruth==1||jj_random_mergedHccTruth==1||jj_random_mergedHggTruth==1||jj_random_mergedHVVTruth_4q==1||jj_random_mergedHVVTruth_lept==1")

            else:
                f.makeSignalShapesMJ("JJ_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,'random',fixParsSig[signal_inuse.replace('VBF_','')])
        else:
            if signal_inuse.find("H")!=-1:
                f.makeSignalShapesMJ("JJ_Vjet_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,'l1',fixParsSig[signal_inuse.replace('VBF_','')],"jj_l1_mergedVTruth==1")
                f.makeSignalShapesMJ("JJ_Vjet_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,'l2',fixParsSig[signal_inuse.replace('VBF_','')],"jj_l2_mergedVTruth==1")
                f.makeSignalShapesMJ("JJ_Hjet_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,'l1',fixParsSig[signal_inuse.replace('VBF_','')],"jj_l1_mergedHTruth==1")
                f.makeSignalShapesMJ("JJ_Hjet_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,'l2',fixParsSig[signal_inuse.replace('VBF_','')],"jj_l2_mergedHTruth==1")
            else:
                f.makeSignalShapesMJ("JJ_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,'l1',fixParsSig[signal_inuse.replace('VBF_','')])
                f.makeSignalShapesMJ("JJ_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,'l2',fixParsSig[signal_inuse.replace('VBF_','')])
    if options.run.find("all")!=-1 or options.run.find("mvv")!=-1:
        print "mjj fit for signal ",signal_inuse
        if signal_inuse.find("H")!=-1:
            f.makeSignalShapesMVV("JJ_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,fixParsSigMVV[signal_inuse.replace('VBF_','')],"( jj_l1_softDrop_mass <= 215 && jj_l1_softDrop_mass > 105 && jj_l2_softDrop_mass <= 105 && jj_l2_softDrop_mass > 55) || (jj_l2_softDrop_mass <= 215 && jj_l2_softDrop_mass > 105 && jj_l1_softDrop_mass <= 105 && jj_l1_softDrop_mass > 55) ")
        elif signal_inuse.find("WZ")!=-1:
            #f.makeSignalShapesMVV("JJ_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,fixParsSigMVV[signal_inuse],"(jj_l1_softDrop_mass <= 105 && jj_l1_softDrop_mass > 85 && jj_l2_softDrop_mass <= 85 && jj_l2_softDrop_mass >= 65) || (jj_l2_softDrop_mass <= 105 && jj_l2_softDrop_mass > 85 && jj_l1_softDrop_mass <= 85 && jj_l1_softDrop_mass >= 65)")
            f.makeSignalShapesMVV("JJ_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,fixParsSigMVV[signal_inuse.replace('VBF_','')],"1")
        else:
            f.makeSignalShapesMVV("JJ_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,fixParsSigMVV[signal_inuse.replace('VBF_','')],"1")
    if options.run.find("all")!=-1 or options.run.find("SF")!=-1:
        print " make SF "
        f.makeSF(signaltemplate_inuse,True,options.vv,options.four,options.tau)
    if options.run.find("all")!=-1 or options.run.find("MU")!=-1:
        print " make migration uncertainties "
        f.makeMigrationUnc(signaltemplate_inuse,str(signal_inuse),options.period,True,options.vv,options.four)
    if options.run.find("all")!=-1 or options.run.find("norm")!=-1:
        print "fit signal norm, DID YOU MAKE SF "
        f.makeSignalYields("JJ_"+str(signal_inuse)+"_"+filePeriod,signaltemplate_inuse,xsec_inuse,'"pol4"',options.tau) #'"[0]*TMath::Log10(x)"')
        #f.makeNormalizations("sigonly_M2000","JJ_"+filePeriod+"_"+str(signal_inuse),signaltemplate_inuse+"narrow_2000",0,ctx.cuts['nonres'],"sig")
        #f.makeNormalizations("sigonly_M4000","JJ_"+filePeriod+"_"+str(signal_inuse),signaltemplate_inuse+"narrow_4000",0,ctx.cuts['nonres'],"sig")

if options.run.find("all")!=-1 or options.run.find("detector")!=-1:
    print "make Detector response"
    f.makeDetectorResponse("nonRes","JJ_"+filePeriod,nonResTemplate,ctx.cuts['nonres'])

if options.run.find("all")!=-1 or options.run.find("qcd")!=-1:
    print "Make nonresonant QCD templates and normalization"
    if runParallel and submitToBatch:
        if options.run.find("all")!=-1 or options.run.find("templates")!=-1:
            wait = False
            print "ctx.cuts['nonres'] = ",ctx.cuts['nonres']
            f.makeBackgroundShapesMVVKernel("nonRes","JJ_"+filePeriod,nonResTemplate,ctx.cuts['nonres'],"1D",wait)
            f.makeBackgroundShapesMVVConditional("nonRes","JJ_"+filePeriod,nonResTemplate,'l1',ctx.cuts['nonres'],"2Dl1",wait)
            f.makeBackgroundShapesMVVConditional("nonRes","JJ_"+filePeriod,nonResTemplate,'l2',ctx.cuts['nonres'],"2Dl2",wait)
            print "Exiting system! When all jobs are finished, please run mergeKernelJobs below"
            sys.exit()
        elif options.run.find("all")!=-1 or options.run.find("kernel")!=-1:
            f.mergeKernelJobs("nonRes","JJ_"+filePeriod,options.single)
            print " calling merge Bckg shape"
	    f.mergeBackgroundShapes("nonRes","JJ_"+filePeriod,options.single)
    else:
        if options.run.find("all")!=-1 or options.run.find("templates")!=-1:
            wait = True
            f.makeBackgroundShapesMVVKernel("nonRes","JJ_"+filePeriod,nonResTemplate,ctx.cuts['nonres'],"1D",wait)
            f.makeBackgroundShapesMVVConditional("nonRes","JJ_"+filePeriod,nonResTemplate,'l1',ctx.cuts['nonres'],"2Dl1",wait)
            f.makeBackgroundShapesMVVConditional("nonRes","JJ_"+filePeriod,nonResTemplate,'l2',ctx.cuts['nonres'],"2Dl2",wait)
            f.mergeBackgroundShapes("nonRes","JJ_"+filePeriod)
    if options.run.find("all")!=-1 or options.run.find("norm")!=-1:
        f.makeNormalizations("nonRes","JJ_"+filePeriod,nonResTemplate,0,ctx.cuts['nonres'],"nRes",options.single,"",options.sendjobs,options.tau)



if options.run.find("all")!=-1 or options.run.find("vjets")!=-1:
    print "for V+jets"
    if options.run.find("all")!=-1 or options.run.find("fits")!=-1 or options.run.find("All")!=-1:
        print "first we fit"
        f.fitVJets("JJ_"+filePeriod+"_WJets",resTemplate,1.,1.)
    wait=False
    if options.batch == True : wait=True
    if options.run.find("all")!=-1 or options.run.find("kernel")!=-1 or options.run.find("All")!=-1:
        if options.fitsmjj == True:
            print "and then we fit mvv"
            f.makeMinorBkgShapesMVV("ZJets","JJ_"+filePeriod,ZresTemplate,ctx.cuts['nonres'],"Zjets",1.,1.)
            f.makeMinorBkgShapesMVV("WJets","JJ_"+filePeriod,WresTemplate,ctx.cuts['nonres'],"Wjets",1.,1.)
        else :
            print " did you run Detector response  for this period? otherwise the kernels steps will not work!"
            print "first kernel W"
            f.makeBackgroundShapesMVVKernel("WJets","JJ_"+filePeriod,WresTemplate,ctx.cuts['nonres'],"1DW",wait,1.,1.,options.sendjobs,options.fittempl,options.tau,options.kfactors)
            print "then kernel Z"
            f.makeBackgroundShapesMVVKernel("ZJets","JJ_"+filePeriod,ZresTemplate,ctx.cuts['nonres'],"1DZ",wait,1.,1.,options.sendjobs,options.fittempl,options.tau,options.kfactors)
    if options.run.find("all")!=-1 or options.run.find("SF")!=-1 or options.run.find("All")!=-1:
        #print "then SF W"
        #f.makeSF(WresTemplate,False,options.vv,options.four,options.tau)
        print "then SF Z"
        f.makeSF(ZresTemplate,False,options.vv,options.four,options.tau)
    if options.run.find("all")!=-1 or options.run.find("MU")!=-1 or options.run.find("All")!=-1:
        print "then migration uncertainties W"
        f.makeMigrationUnc(WresTemplate,"WJets",options.period,False,options.vv,options.four)
        print "then migration uncertainties Z"
        f.makeMigrationUnc(ZresTemplate,"ZJets",options.period,False,options.vv,options.four)
    if options.run.find("all")!=-1 or options.run.find("vjetsnorm")!=-1 or options.run.find("All")!=-1:
        print " DID YOU PRODUCE THE SF TREES?? "
        print "then norm W"
        f.makeNormalizations("WJets","JJ_"+filePeriod,WresTemplate,0,ctx.cuts['nonres'],"nResWJets",options.single,"1",options.sendjobs,options.tau) #,HPSF_vtag,LPSF_vtag)
        print "then norm Z"
        f.makeNormalizations("ZJets","JJ_"+filePeriod,ZresTemplate,0,ctx.cuts['nonres'],"nResZJets",options.single,"1",options.sendjobs,options.tau)



if options.run.find("all")!=-1 or options.run.find("tt")!=-1:
    if options.run.find("all")!=-1 or options.run.find("fit")!=-1 or options.run.find("ALL")!=-1:
        print "first we fit"
        f.fitTT   ("JJ_%s_TTJets"%(filePeriod),TTemplate,1.,)
    wait=False
    if options.batch == True : wait=True
    if options.run.find("all")!=-1 or options.run.find("SF")!=-1 or options.run.find("ALL")!=-1:
        print " Making SF "
        f.makeSF(TTemplate,False,options.vv,options.four,options.tau)
    if options.run.find("all")!=-1 or options.run.find("MU")!=-1 or options.run.find("ALL")!=-1:
        print " Making migration uncertainties "
        f.makeMigrationUnc(TTemplate,"TTJets",options.period,False,options.vv,options.four)
#    if options.run.find("all")!=-1 or options.run.find("norm")!=-1 or options.run.find("ALL")!=-1:
#        print "make norm for all contributions of ttbar together, DID YOU MAKE SF?"
#        f.makeNormalizations("TTJets","JJ_"+filePeriod,TTemplate,0,ctx.cuts['nonres'],"nResTT",options.single,"1",options.sendjobs)
#    if options.run.find("all")!=-1 or options.run.find("templates")!=-1 or options.run.find("ALL")!=-1:
#        f.makeBackgroundShapesMVVKernel("TTJets","JJ_"+filePeriod,TTemplate,ctx.cuts['nonres'],"1DTT",wait,1.,1.,options.sendjobs)
    contrib =options.ttcontrib.split(",") #["resT","resW","nonresT","resTnonresT","resWnonresT","resTresW"]
    for con in contrib:
        if options.run.find("all")!=-1 or options.run.find("templates")!=-1 or options.run.find("ALL")!=-1:
            print " ***************************         "+con+"      ******************************"
            if options.fitsmjj == True:
                f.makeMinorBkgShapesMVV("TTJets"+con,"JJ_"+filePeriod,TTemplate,ctx.cuts[con],con)
            else:
                f.makeBackgroundShapesMVVKernel("TTJets"+con,"JJ_"+filePeriod,TTemplate,ctx.cuts[con],"1DTT"+con,wait,1.,1.,options.sendjobs,options.fittempl)
        if options.run.find("all")!=-1 or options.run.find("norm")!=-1 or options.run.find("ALL")!=-1:
            print " ***************************         "+con+"      ******************************"
            print "make norm, DID YOU MAKE SF?"
            cutsTT=con
            if con == "" : cutsTT ='nonres'
            print " cutsTT ",cutsTT
            f.makeNormalizations("TTJets"+con,"JJ_"+filePeriod,TTemplate,0,ctx.cuts[cutsTT],"nResTT"+con,options.single,"1",options.sendjobs,options.tau)

if options.run.find("all")!=-1 or options.run.find("st")!=-1:
    wait=False
    if options.batch == True : wait=True
    if options.run.find("all")!=-1 or options.run.find("SF")!=-1 or options.run.find("ALL")!=-1:
        print " Making SF "
        f.makeSF(STemplate,False,options.vv)
    if options.run.find("all")!=-1 or options.run.find("MU")!=-1 or options.run.find("ALL")!=-1:
        print " Making migration uncertainties "
        f.makeMigrationUnc(STemplate,"STJets",options.period)
    if options.run.find("all")!=-1 or options.run.find("norm")!=-1 or options.run.find("ALL")!=-1:
        print "make norm for all contributions of ttbar together, DID YOU MAKE SF?"
        f.makeNormalizations("STJets","JJ_"+filePeriod,STemplate,0,ctx.cuts['nonres'],"nResST",options.single,"1",options.sendjobs)


if options.run.find("all")!=-1 or options.run.find("sm")!=-1:
    wait=False
    if options.batch == True : wait=True
    if options.run.find("all")!=-1 or options.run.find("SF")!=-1 or options.run.find("ALL")!=-1:
        print " Making SF "
        f.makeSF(WWTemplate,False,options.vv)
    if options.run.find("all")!=-1 or options.run.find("MU")!=-1 or options.run.find("ALL")!=-1:
        print " Making migration uncertainties "
        f.makeMigrationUnc(SMTemplate,"STJets",options.period)
    if options.run.find("all")!=-1 or options.run.find("norm")!=-1 or options.run.find("ALL")!=-1:
        print "make norm for all contributions of ttbar together, DID YOU MAKE SF?"
        f.makeNormalizations("WWJets","JJ_"+filePeriod,WWTemplate,0,ctx.cuts['nonres'],"nResWW",options.single,"1",options.sendjobs)

if options.run.find("all")!=-1 or options.run.find("data")!=-1:
    print " Do data "
    f.makeNormalizations("data","JJ_"+filePeriod,dataTemplate,1,'1',"normD",options.single,"1",options.sendjobs) #run on data. Currently run on pseudodata only (below)
if options.run.find("all")!=-1 or options.run.find("pseudoNOVJETS")!=-1:
    print " Do pseudodata without vjets"
    from modules.submitJobs import makePseudoData
    for p in categories: makePseudoData(options.inputdir+"/JJ_"+filePeriod+"_nonRes_%s.root"%p,options.inputdir+"/save_new_shapes_"+filePeriod+"_pythia_%s_3D.root"%p,"pythia","JJ_%s_PDnoVjets_%s.root"%(filePeriod,p),ctx.lumi[filePeriod])
if options.run.find("all")!=-1 or options.run.find("pseudoVJETS")!=-1:
    print " Do pseudodata with vjets: DID YOU PRODUCE THE WORKSPACE BEFORE???"
    from modules.submitJobs import makePseudoDataVjets
    for p in categories: makePseudoDataVjets(options.inputdir+"/JJ_"+filePeriod+"_nonRes_%s.root"%p,options.inputdir+"/save_new_shapes_"+filePeriod+"_pythia_%s_3D.root"%p,"pythia","JJ_%s_PDVjets_%s.root"%(filePeriod,p),ctx.lumi[filePeriod],options.inputdir+"/workspace_JJ_BulkGWW_"+p+"_13TeV_"+filePeriod+"_PrepPseudo.root",filePeriod,p)
if options.run.find("all")!=-1 or options.run.find("pseudoTT")!=-1:
    print " Do pseudodata with tt"
    from modules.submitJobs import makePseudoDataTT
    for p in categories: makePseudoDataTT(options.inputdir+"/JJ_"+filePeriod+"_TTJets_"+p+".root",
					  "JJ_%s_PDTT_%s.root"%(filePeriod,p),ctx.lumi[filePeriod],
                                          filePeriod,p)
if options.run.find("all")!=-1 or options.run.find("pseudoNOQCD")!=-1:
    print " Do pseudodata with vjets & tt: DID YOU PRODUCE THE WORKSPACE BEFORE???"
    from modules.submitJobs import makePseudoDataNoQCD
    for p in categories: makePseudoDataNoQCD(options.inputdir+"/JJ_"+filePeriod+"_TTJets_"+p+".root",
					       "JJ_%s_PDnoQCD_%s.root"%(filePeriod,p),ctx.lumi[filePeriod],
					       options.inputdir+"/workspace_JJ_BulkGWW_"+p+"_13TeV_"+filePeriod+"_PrepPseudo.root",
					       filePeriod,p)
if options.run.find("all")!=-1 or options.run.find("pseudoALL")!=-1:
    print " Do pseudodata with vjets & tt: DID YOU PRODUCE THE WORKSPACE BEFORE???"
    from modules.submitJobs import makePseudoDataVjetsTT
    for p in categories:
        print " making pseudodata for ",p
        ap = p
        if "VBF" in p: ap = p.replace("VBF_","")
        print " using shapes ",ap
        makePseudoDataVjetsTT(options.inputdir+"/JJ_"+filePeriod+"_nonRes_%s.root"%p,
                              options.inputdir+"/JJ_"+filePeriod+"_TTJets_"+p+".root",
                              options.inputdir+"/save_new_shapes_"+filePeriod+"_pythia_%s_3D.root"%ap,
                              "pythia","JJ_%s_PDALL_%s.root"%(filePeriod,p),ctx.lumi[filePeriod],
                              options.inputdir+"/workspace_JJ_BulkGWW_"+p+"_13TeV_"+filePeriod+"_PrepPseudo.root",
                              filePeriod,ap,rescale,options.qcdsf)

print " ########## I did everything I could! ###### "
