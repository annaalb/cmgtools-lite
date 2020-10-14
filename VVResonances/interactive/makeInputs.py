from functions import *
from optparse import OptionParser
#from cuts import cuts, HPSF16, HPSF17, LPSF16, LPSF17, dijetbins, HCALbinsMVVSignal, minMJ,maxMJ,binsMJ, minMVV, maxMVV, binsMVV, minMX, maxMX, catVtag, catHtag
import cuts

## import cuts of the analysis from separate file

# python makeInputs.py -p 2016 --run "detector"
# python makeInputs.py -p 2016 --run "signorm" --signal "ZprimeWW" --batch False 
# python makeInputs.py -p 2016 --run "tt" --batch False 
# python makeInputs.py -p 2016 --run "vjets" --batch False                                                                                                                                      
# python makeInputs.py -p 2016 --run "qcdtemplates"
# python makeInputs.py -p 2016 --run "qcdkernel"
# python makeInputs.py -p 2016 --run "qcdnorm"
# python makeInputs.py -p 2016 --run "data"
# python makeInputs.py -p 2016 --run "pseudoNOVJETS"
# python makeInputs.py -p 2016 --run "pseudoVJETS"
# python makeInputs.py -p 2016 --run "pseudoTT"
# python makeInputs.py -p 2016 --run "pseudoALL" #to produce also the TT pseudodata

parser = OptionParser()
parser.add_option("-p","--period",dest="period",type="int",default=2016,help="run period")
parser.add_option("-s","--sorting",dest="sorting",help="b-tag or random sorting",default='random')
parser.add_option("-b","--binning",action="store_false",dest="binning",help="use dijet binning or not",default=True)
parser.add_option("--batch",action="store_false",dest="batch",help="submit to batch or not ",default=True)
parser.add_option("--trigg",action="store_true",dest="trigg",help="add trigger weights or not ",default=False)
parser.add_option("--run",dest="run",help="decide which parts of the code should be run right now possible optoins are: all : run everything, sigmvv: run signal mvv fit sigmj: run signal mj fit, signorm: run signal norm, vjets: run vjets, tt: run ttbar , qcdtemplates: run qcd templates, qcdkernel: run qcd kernel, qcdnorm: run qcd merge and norm, detector: run detector fit , data : run the data or pseudodata scripts ",default="all")
parser.add_option("--signal",dest="signal",default="BGWW",help="which signal do you want to run? options are BulkGWW, BulkGZZ, WprimeWZ, ZprimeWW, ZprimeZH")
parser.add_option("--fitvjetsmjj",dest="fitvjetsmjj",default=False,action="store_true",help="True makes fits for mjj of vjets, False uses hists")


(options,args) = parser.parse_args()

widerMVV=False


ctx  = cuts.cuts("init_VV_VH.json",int(options.period),options.sorting+"dijetbins",widerMVV)
if options.binning==False: ctx  = cuts.cuts("init_VV_VH.json",int(options.period),options.sorting,widerMVV)

period = options.period
# NB to use the DDT decorrelation method, the ntuples in /eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/deepAK8V2/ should be used
samples= str(period)+"/" #for V+jets we use 2017 samples also for 2016 because the 2016 ones are buggy

sorting = options.sorting

submitToBatch = options.batch #Set to true if you want to submit kernels + makeData to batch!
runParallel   = True #Set to true if you want to run all kernels in parallel! This will exit this script and you will have to run mergeKernelJobs when your jobs are done! 

dijetBinning = options.binning
useTriggerWeights = options.trigg


    
addOption = ""
if useTriggerWeights: 
    addOption = "-t"
    
#all categories
#categories=['VH_HPHP','VH_LPHP','VV_HPHP'] #,'VBF_VV_HPHP','VBF_VV_HPLP']
categories=['VH_HPHP','VH_LPHP','VH_HPLP','VV_HPHP','VV_HPLP'] #,'VBF_VV_HPHP','VBF_VV_HPLP']
#categories=['VH_HPNP_control_region'] #,'VH_NPHP_control_region']
#categories=['VV_HPLP'] 
#categories=['NP']
       
#list of signal samples --> nb, radion and vbf samples to be added
BulkGravWWTemplate="BulkGravToWW_"
VBFBulkGravWWTemplate="VBF_BulkGravToWW_"
BulkGravZZTemplate="BulkGravToZZToZhadZhad_"
ZprimeWWTemplate= "ZprimeToWW_"
ZprimeZHTemplate="ZprimeToZhToZhadhbb_"
WprimeWZTemplate= "WprimeToWZToWhadZhad_"
WprimeWHTemplate="WprimeToWhToWhadhbb_" #"WprimeToWhToWhadhbb_"

# use arbitrary cross section 0.001 so limits converge better
BRZZ=1.*0.001*0.6991*0.6991
BRWW=1.*0.001 #ZprimeWW and GBulkWW are inclusive
BRZH=1.*0.001*0.6991*0.584
BRWZ=1.*0.001*0.6991*0.676
BRWH=1.*0.001*0.676*0.584

#data samples
dataTemplate="JetHT"

#background samples
#nonResTemplate="QCD_Pt-" #low stat herwig
#nonResTemplate="QCD_HT" #medium stat madgraph+pythia
nonResTemplate="QCD_Pt_" #high stat pythia8

if(period == 2016):
    TTemplate= "TT_Mtt-700to1000,TT_Mtt-1000toInf" #do we need a separate fit for ttbar?
else:
    TTemplate= "TTToHadronic" #do we need a separate fit for ttbar?
WresTemplate= "WJetsToQQ_HT400to600,WJetsToQQ_HT600to800,WJetsToQQ_HT800toInf"
ZresTemplate= "ZJetsToQQ_HT400to600,ZJetsToQQ_HT600to800,ZJetsToQQ_HT800toInf"
resTemplate= "ZJetsToQQ_HT400to600,ZJetsToQQ_HT600to800,ZJetsToQQ_HT800toInf,WJetsToQQ_HT400to600,WJetsToQQ_HT600to800,WJetsToQQ_HT800toInf"

      

#do not change the order here, add at the end instead
parameters = [ctx.cuts,ctx.minMVV,ctx.maxMVV,ctx.minMX,ctx.maxMX,ctx.binsMVV,ctx.HCALbinsMVV,samples,categories,ctx.minMJ,ctx.maxMJ,ctx.binsMJ,ctx.lumi,submitToBatch]   
f = AllFunctions(parameters)


#parser.add_option("--signal",dest="signal",default="BGWW",help="which signal do you want to run? options are BGWW, BGZZ, WprimeWZ, ZprimeWW, ZprimeZH")
if options.run.find("all")!=-1 or options.run.find("sig")!=-1:
    if options.signal.find("ZprimeZH")!=-1:
        signal_inuse="ZprimeZH"
        signaltemplate_inuse=ZprimeZHTemplate
        xsec_inuse=BRZH
    elif options.signal.find("BGWW")!=-1 and not 'VBF' in options.signal:
        signal_inuse="BulkGWW"
        signaltemplate_inuse=BulkGravWWTemplate
        xsec_inuse=BRWW
    elif options.signal.find("VBFBGWW")!=-1:
        signal_inuse="VBF_BulkGWW"
        signaltemplate_inuse=VBFBulkGravWWTemplate
        xsec_inuse=BRWW
    elif options.signal.find("BGZZ")!=-1:
        signal_inuse="BulkGZZ"
        signaltemplate_inuse=BulkGravZZTemplate
        xsec_inuse=BRZZ
    elif options.signal.find("ZprimeWW")!=-1:
        signal_inuse="ZprimeWW"
        signaltemplate_inuse=ZprimeWWTemplate
        xsec_inuse=BRWW
    elif options.signal.find("WprimeWZ")!=-1:
        signal_inuse="WprimeWZ"
        signaltemplate_inuse=WprimeWZTemplate
        xsec_inuse=BRWZ
    elif options.signal.find("WprimeWH")!=-1:
        signal_inuse="WprimeWH"
        signaltemplate_inuse=WprimeWHTemplate
        xsec_inuse=BRWH
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
                f.makeSignalShapesMJ("JJ_Vjet_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'random', fixParsSig[signal_inuse],"jj_random_mergedVTruth==1")
                f.makeSignalShapesMJ("JJ_Hjet_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'random',fixParsSig[signal_inuse],"jj_random_mergedHTruth==1")
            else:
                f.makeSignalShapesMJ("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'random',fixParsSig[signal_inuse.replace('VBF_','')]) 
        else:
            if signal_inuse.find("H")!=-1: 
                f.makeSignalShapesMJ("JJ_Vjet_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'l1',fixParsSig[signal_inuse],"jj_l1_mergedVTruth==1")
                f.makeSignalShapesMJ("JJ_Vjet_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'l2',fixParsSig[signal_inuse],"jj_l2_mergedVTruth==1")
                f.makeSignalShapesMJ("JJ_Hjet_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'l1',fixParsSig[signal_inuse],"jj_l1_mergedHTruth==1")
                f.makeSignalShapesMJ("JJ_Hjet_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'l2',fixParsSig[signal_inuse],"jj_l2_mergedHTruth==1")
            else:
                f.makeSignalShapesMJ("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'l1',fixParsSig[signal_inuse])
                f.makeSignalShapesMJ("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'l2',fixParsSig[signal_inuse])
    if options.run.find("all")!=-1 or options.run.find("mvv")!=-1:
        print "mjj fit for signal ",signal_inuse
        if signal_inuse.find("H")!=-1:
            f.makeSignalShapesMVV("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,fixParsSigMVV[signal_inuse],"( jj_l1_softDrop_mass <= 215 && jj_l1_softDrop_mass > 105 && jj_l2_softDrop_mass <= 105 && jj_l2_softDrop_mass > 55) || (jj_l2_softDrop_mass <= 215 && jj_l2_softDrop_mass > 105 && jj_l1_softDrop_mass <= 105 && jj_l1_softDrop_mass > 55) ")
        elif signal_inuse.find("WZ")!=-1:
            #f.makeSignalShapesMVV("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,fixParsSigMVV[signal_inuse],"(jj_l1_softDrop_mass <= 105 && jj_l1_softDrop_mass > 85 && jj_l2_softDrop_mass <= 85 && jj_l2_softDrop_mass >= 65) || (jj_l2_softDrop_mass <= 105 && jj_l2_softDrop_mass > 85 && jj_l1_softDrop_mass <= 85 && jj_l1_softDrop_mass >= 65)")
            f.makeSignalShapesMVV("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,fixParsSigMVV[signal_inuse],"1")
        else:
            f.makeSignalShapesMVV("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,fixParsSigMVV[signal_inuse.replace('VBF_','')],"1")
    

    if options.run.find("all")!=-1 or options.run.find("norm")!=-1:
        print "fit signal norm "
        f.makeSignalYields("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,xsec_inuse,{'VH_HPHP':ctx.HPSF_htag*ctx.HPSF_vtag,'VH_HPLP':ctx.HPSF_htag*ctx.LPSF_vtag,'VH_LPHP':ctx.HPSF_vtag*ctx.LPSF_htag,'VH_LPLP':ctx.LPSF_htag*ctx.LPSF_vtag,'VV_HPHP':ctx.HPSF_vtag*ctx.HPSF_vtag,'VV_HPLP':ctx.HPSF_vtag*ctx.LPSF_vtag,'VH_all':ctx.HPSF_vtag*ctx.HPSF_htag+ctx.HPSF_vtag*ctx.LPSF_htag,'VH_NPHP_control_region':1,'VH_HPNP_control_region':1,},"pol2")
        #f.makeNormalizations("sigonly_M2000","JJ_"+str(period)+"_"+str(signal_inuse),signaltemplate_inuse+"narrow_2000",0,ctx.cuts['nonres'],"sig")
        #f.makeNormalizations("sigonly_M4000","JJ_"+str(period)+"_"+str(signal_inuse),signaltemplate_inuse+"narrow_4000",0,ctx.cuts['nonres'],"sig")

if options.run.find("all")!=-1 or options.run.find("detector")!=-1:
    print "make Detector response"
    f.makeDetectorResponse("nonRes","JJ_"+str(period),nonResTemplate,ctx.cuts['nonres'])

if options.run.find("all")!=-1 or options.run.find("qcd")!=-1:
    print "Make nonresonant QCD templates and normalization"
    if runParallel and submitToBatch:
        if options.run.find("all")!=-1 or options.run.find("templates")!=-1:
            wait = False
            f.makeBackgroundShapesMVVKernel("nonRes","JJ_"+str(period),nonResTemplate,ctx.cuts['nonres'],"1D",wait)
            f.makeBackgroundShapesMVVConditional("nonRes","JJ_"+str(period),nonResTemplate,'l1',ctx.cuts['nonres'],"2Dl1",wait)
            f.makeBackgroundShapesMVVConditional("nonRes","JJ_"+str(period),nonResTemplate,'l2',ctx.cuts['nonres'],"2Dl2",wait)
            print "Exiting system! When all jobs are finished, please run mergeKernelJobs below"
            sys.exit()
        elif options.run.find("all")!=-1 or options.run.find("kernel")!=-1:
            f.mergeKernelJobs("nonRes","JJ_"+str(period))
	    f.mergeBackgroundShapes("nonRes","JJ_"+str(period))
    else:
        if options.run.find("all")!=-1 or options.run.find("templates")!=-1:
            wait = True
            f.makeBackgroundShapesMVVKernel("nonRes","JJ_"+str(period),nonResTemplate,ctx.cuts['nonres'],"1D",wait)
            f.makeBackgroundShapesMVVConditional("nonRes","JJ_"+str(period),nonResTemplate,'l1',ctx.cuts['nonres'],"2Dl1",wait)
            f.makeBackgroundShapesMVVConditional("nonRes","JJ_"+str(period),nonResTemplate,'l2',ctx.cuts['nonres'],"2Dl2",wait)
            f.mergeBackgroundShapes("nonRes","JJ_"+str(period))
    if options.run.find("all")!=-1 or options.run.find("norm")!=-1:
        f.makeNormalizations("nonRes","JJ_"+str(period),nonResTemplate,0,ctx.cuts['nonres'],"nRes")

if options.run.find("all")!=-1 or options.run.find("vjets")!=-1:    
    print "for V+jets"
    print "first we fit"
    f.fitVJets("JJ_WJets",resTemplate,1.,1.)
    if options.fitvjetsmjj == True:
        print "and then we fit mvv"
        f.makeMinorBkgShapesMVV("ZJets","JJ_"+str(period),ZresTemplate,ctx.cuts['nonres'],"Zjets",1.,1.)
        f.makeMinorBkgShapesMVV("WJets","JJ_"+str(period),WresTemplate,ctx.cuts['nonres'],"Wjets",1.,1.)
    else :
        print "first kernel W"
        f.makeBackgroundShapesMVVKernel("WJets","JJ_"+str(period),WresTemplate,ctx.cuts['nonres'],"1D",0,1.,1.)
        print "then kernel Z"
        f.makeBackgroundShapesMVVKernel("ZJets","JJ_"+str(period),ZresTemplate,ctx.cuts['nonres'],"1D",0,1.,1.)
    print "make norm W"
    f.makeNormalizations("WJets","JJ_"+str(period),WresTemplate,0,ctx.cuts['nonres'],"nRes","",ctx.HPSF_vtag,ctx.LPSF_vtag)
    print "then norm Z"
    f.makeNormalizations("ZJets","JJ_"+str(period),ZresTemplate,0,ctx.cuts['nonres'],"nRes","",ctx.HPSF_vtag,ctx.LPSF_vtag)
    


if options.run.find("all")!=-1 or options.run.find("tt")!=-1:
    f.fitTT   ("JJ_%s_TTJets"%(period),TTemplate,1.,)
    print "resT"
    f.makeMinorBkgShapesMVV("TTJets","JJ_resT"+str(period),TTemplate,ctx.cuts['resTT'],'resTT')
    f.makeNormalizations("TTJets","JJ_resT"+str(period),TTemplate,0,ctx.cuts['resTT'],"nRes","")
    print "resW"
    f.makeMinorBkgShapesMVV("TTJets","JJ_resW"+str(period),TTemplate,ctx.cuts['resTT_W'],'resW')
    f.makeNormalizations("TTJets","JJ_resW"+str(period),TTemplate,0,ctx.cuts['resTT_W'],"nRes","")
    print "nonres"
    f.makeMinorBkgShapesMVV("TTJets","JJ_nonresT"+str(period),TTemplate,ctx.cuts['nonresTT'],'nonresTT')
    f.makeNormalizations("TTJets","JJ_nonresT"+str(period),TTemplate,0,ctx.cuts['nonresTT'],"nRes","")
    print "resTresW"
    f.makeMinorBkgShapesMVV("TTJets","JJ_resTresW"+str(period),TTemplate,ctx.cuts['resTresW'],'resTresW')
    f.makeNormalizations("TTJets","JJ_resTresW"+str(period),TTemplate,0,ctx.cuts['resTresW'],"nRes","")
    print "resTnonresT"
    f.makeMinorBkgShapesMVV("TTJets","JJ_resTnonresT"+str(period),TTemplate,ctx.cuts['resTnonresT'],'resTnonresT')
    f.makeNormalizations("TTJets","JJ_resTnonresT"+str(period),TTemplate,0,ctx.cuts['resTnonresT'],"nRes","")
    print "resWnonresT"
    f.makeMinorBkgShapesMVV("TTJets","JJ_resWnonresT"+str(period),TTemplate,ctx.cuts['resWnonresT'],'resWnonresT')
    f.makeNormalizations("TTJets","JJ_resWnonresT"+str(period),TTemplate,0,ctx.cuts['resWnonresT'],"nRes","")
    print "make norm for all contributions of ttbar together"
    f.makeNormalizations("TTJets","JJ_"+str(period),TTemplate,0,ctx.cuts['nonres'],"nRes","")

if options.run.find("all")!=-1 or options.run.find("data")!=-1:
    print " Do data "
    f.makeNormalizations("data","JJ_"+str(period),dataTemplate,1,'1',"normD") #run on data. Currently run on pseudodata only (below)
if options.run.find("all")!=-1 or options.run.find("pseudoNOVJETS")!=-1:
    print " Do pseudodata without vjets"
    from modules.submitJobs import makePseudoData
    for p in categories: makePseudoData("JJ_"+str(period)+"_nonRes_%s.root"%p,"save_new_shapes_"+str(period)+"_pythia_%s_3D.root"%p,"pythia","JJ_PDnoVjets_%s.root"%p,ctx.lumi)
if options.run.find("all")!=-1 or options.run.find("pseudoVJETS")!=-1:
    print " Do pseudodata with vjets: DID YOU PRODUCE THE WORKSPACE BEFORE???"
    from modules.submitJobs import makePseudoDataVjets
    for p in categories: makePseudoDataVjets("results_"+str(period)+"/JJ_"+str(period)+"_nonRes_%s.root"%p,"results_"+str(period)+"/save_new_shapes_"+str(period)+"_pythia_%s_3D.root"%p,"pythia","JJ_PDVjets_%s.root"%p,ctx.lumi,"results_"+str(period)+"/workspace_JJ_BulkGWW_"+p+"_13TeV_"+str(period)+"_VjetsPrep.root",period,p)
if options.run.find("all")!=-1 or options.run.find("pseudoTT")!=-1:
    print " Do pseudodata with tt"
    from modules.submitJobs import makePseudoDataTT
    for p in categories: makePseudoDataTT("results_"+str(period)+"/JJ_"+str(period)+"_TTJets_"+p+".root",
					  "JJ_PDTT_%s.root"%p,ctx.lumi,
                                          period,p)
if options.run.find("all")!=-1 or options.run.find("pseudoNOQCD")!=-1:
    print " Do pseudodata with vjets & tt: DID YOU PRODUCE THE WORKSPACE BEFORE???"
    from modules.submitJobs import makePseudoDataNoQCD
    for p in categories: makePseudoDataNoQCD("results_"+str(period)+"/JJ_all_"+str(period)+"_TTJets_"+p+".root",
					       "JJ_PDnoQCD_%s.root"%p,ctx.lumi,
					       "results_"+str(period)+"/workspace_JJ_BulkGWW_"+p+"_13TeV_"+str(period)+"_PrepPseudo.root",
					       period,p)
if options.run.find("all")!=-1 or options.run.find("pseudoALL")!=-1:
    print " Do pseudodata with vjets & tt: DID YOU PRODUCE THE WORKSPACE BEFORE???"
    from modules.submitJobs import makePseudoDataVjetsTT
    for p in categories: makePseudoDataVjetsTT("results_"+str(period)+"/JJ_"+str(period)+"_nonRes_%s.root"%p,
                                               "results_"+str(period)+"/JJ_"+str(period)+"_TTJets_"+p+".root",
					       "results_"+str(period)+"/save_new_shapes_"+str(period)+"_pythia_%s_3D.root"%p,
					       "pythia","JJ_PDALL_%s.root"%p,ctx.lumi,
					       "results_"+str(period)+"/workspace_JJ_BulkGWW_"+p+"_13TeV_"+str(period)+"_PrepPseudo.root",
					       period,p)

print " ########## I did everything I could! ###### "
