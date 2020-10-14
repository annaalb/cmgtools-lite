#!/usr/bin/env python
import sys, os
import json
import ROOT
class DatacardTools():

 def __init__(self,scales,scalesHiggs,vtag_pt_dependence,lumi_unc,sfQCD,pseudodata,outlabel,doCorrelation=True,fitvjetsmjj=False):
  
  self.scales=scales
  self.vtag_pt_dependence=vtag_pt_dependence
  self.lumi_unc = lumi_unc
  self.sfQCD = sfQCD
  self.pseudodata = pseudodata
  self.outlabel = outlabel
  self.scalesHiggs=scalesHiggs
  self.doCorrelation= doCorrelation
  self.fitvjetsmjj = fitvjetsmjj
 

 def AddSignal(self,card,dataset,category,sig,resultsDir,ncontrib):
      print "sig ",sig
      if sig.find('primeW') != -1:
       if sig.find('VprimeWV')!= -1 or sig.find('ZprimeWW')!= -1:
        sig1 = 'ZprimeWW'
        card.addMVVSignalParametricShape("%s_MVV"%sig1,"MJJ",resultsDir+"/JJ_%s_%s_MVV.json"%(sig1,dataset),{'CMS_scale_j':1},{'CMS_res_j':1.0})
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq1"%sig1,"MJ1" ,resultsDir+"/JJ_%s_%s_MJrandom_"%(sig1,dataset)+"NP.json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq2"%sig1,"MJ2" ,resultsDir+"/JJ_%s_%s_MJrandom_"%(sig1,dataset)+"NP.json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
        card.addParametricYieldHVTBR("%s"%sig1,ncontrib-1,resultsDir+"/JJ_%s_%s_"%(sig1,dataset)+category+"_yield.json","../scripts/theoryXsec/HVTB.json","CX0(pb)","BRWW",1000.,'CMS_tau21_PtDependence',self.vtag_pt_dependence[dataset][category],1.0)
        card.product3D("%s"%sig1,"%s_Wqq1"%sig1,"%s_Wqq2"%sig1,"%s_MVV"%sig1)
       if sig.find('VprimeWV')!= -1 or sig.find('WprimeWZ')!= -1:
        sig2 = 'WprimeWZ'
        card.addMVVSignalParametricShape("%s_MVV"%sig,"MJJ",resultsDir+"/JJ_%s_%s_MVV.json"%(sig,dataset),{'CMS_scale_j':1},{'CMS_res_j':1.0},self.doCorrelation)

        card.addMJJSignalParametricShapeNOEXP("%s_Wqq1_c1"%sig,"MJ1" ,resultsDir+"/JJ_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq2_c1"%sig,"MJ2" ,resultsDir+"/JJ_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
        if self.doCorrelation:
            print "doing correlation"
            card.product("%s_Wqq_c1"%sig,"%s_Wqq1_c1"%sig,"%s_Wqq2_c1"%sig)
            card.conditionalProduct("%s_c1"%sig,"%s_MVV"%sig,"MJ1,MJ2","%s_Wqq_c1"%sig)
        else:
            print "no MVV correlation"
            card.product3D("%s_c1"%sig,"%s_Wqq1_c1"%sig,"%s_Wqq2_c1"%sig,"%s_MVV"%sig)

        card.addMJJSignalParametricShapeNOEXP("%s_Wqq1_c2"%sig,"MJ1" ,resultsDir+"/JJ_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq2_c2"%sig,"MJ2" ,resultsDir+"/JJ_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
        if self.doCorrelation:
            print "doing correlation"
            card.product("%s_Wqq_c2"%sig,"%s_Wqq1_c2"%sig,"%s_Wqq2_c2"%sig)
            card.conditionalProduct("%s_c2"%sig,"%s_MVV"%sig,"MJ1,MJ2","%s_Wqq_c2"%sig)
        else:
            card.product3D("%s_c2"%sig,"%s_Wqq1_c2"%sig,"%s_Wqq2_c2"%sig,"%s_MVV"%sig)

        card.sumSimple("%s"%sig,"%s_c1"%sig,"%s_c2"%sig,"0.5")
       
        if self.outlabel.find("sigOnly")==-1:
         card.addParametricYieldHVTBR("%s"%sig2,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig2,dataset)+category+"_yield.json","../scripts/theoryXsec/HVTB.json","CX+(pb),CX-(pb)","BRWZ",1000.,'CMS_tau21_PtDependence',self.vtag_pt_dependence[dataset][category],1.0)
        else:
           card.addParametricYieldHVTBR("%s"%sig2,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig2,dataset)+category+"_yield.json","../scripts/theoryXsec/HVTB.json","CX+(pb),CX-(pb)","BRWZ",1000.,'CMS_tau21_PtDependence',self.vtag_pt_dependence[dataset][category],500.0)
        
        
      if sig.find('BulkG')!= -1:
       #NB since the signals are scaled by xsec BulkG = BulkGWW + BulkGZZ, they need to be rescaled accordingly when producing the limit plot!!! 
       if sig.find('BulkGVV') != -1 or sig.find('BulkGWW')!= -1:
        sig1 = 'BulkGWW'
        card.addMVVSignalParametricShape("%s_MVV"%sig1,"MJJ",resultsDir+"/JJ_%s_%s_MVV.json"%(sig1,dataset),{'CMS_scale_j':1},{'CMS_res_j':1.0})
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq1"%sig1,"MJ1" ,resultsDir+"/JJ_%s_%s_MJrandom_"%(sig1,dataset)+"NP.json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq2"%sig1,"MJ2" ,resultsDir+"/JJ_%s_%s_MJrandom_"%(sig1,dataset)+"NP.json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
        card.addParametricYieldHVTBR("%s"%sig1,ncontrib-1,resultsDir+"/JJ_%s_%s_"%(sig1,dataset)+category+"_yield.json","../scripts/theoryXsec/BulkG.json","sigma","BRWW",1000.,'CMS_tau21_PtDependence',self.vtag_pt_dependence[dataset][category],1.0)
        card.product3D("%s"%sig1,"%s_Wqq1"%sig1,"%s_Wqq2"%sig1,"%s_MVV"%sig1)
       if sig.find('BulkGVV')!= -1 or sig.find('BulkGZZ')!= -1:
        sig2 = 'BulkGZZ'
        card.addMVVSignalParametricShape("%s_MVV"%sig2,"MJJ",resultsDir+"/JJ_%s_%s_MVV.json"%(sig2,dataset),{'CMS_scale_j':1},{'CMS_res_j':1.0})
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq1"%sig2,"MJ1" ,resultsDir+"/JJ_%s_%s_MJrandom_"%(sig2,dataset)+"NP.json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq2"%sig2,"MJ2" ,resultsDir+"/JJ_%s_%s_MJrandom_"%(sig2,dataset)+"NP.json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
        card.addParametricYieldHVTBR("%s"%sig2,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig2,dataset)+category+"_yield.json","../scripts/theoryXsec/BulkG.json","sigma","BRZZ",1000.,'CMS_tau21_PtDependence',self.vtag_pt_dependence[dataset][category],1.0)
        card.product3D("%s"%sig2,"%s_Wqq1"%sig2,"%s_Wqq2"%sig2,"%s_MVV"%sig2)

       
      if sig.find("H")!=-1:
       card.addMVVSignalParametricShape("%s_MVV"%sig,"MJJ",resultsDir+"/JJ_%s_%s_MVV.json"%(sig,dataset),{'CMS_scale_j':1},{'CMS_res_j':1.0},self.doCorrelation)


       card.addMJJSignalParametricShapeHiggs("%s_Wqq1_c1"%sig,"MJ1" ,resultsDir+"/JJ_Hjet_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_j':1},{'CMS_res_j':1.0},self.scalesHiggs[dataset])
       card.addMJJSignalParametricShapeNOEXP("%s_Wqq2_c1"%sig,"MJ2" ,resultsDir+"/JJ_Vjet_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
       if self.doCorrelation:
        print "doing correlation"
        card.product("%s_Wqq_c1"%sig,"%s_Wqq1_c1"%sig,"%s_Wqq2_c1"%sig)
        card.conditionalProduct("%s_c1"%sig,"%s_MVV"%sig,"MJ1,MJ2","%s_Wqq_c1"%sig)
       else:
        print "no MVV correlation"
        card.product3D("%s_c1"%sig,"%s_Wqq1_c1"%sig,"%s_Wqq2_c1"%sig,"%s_MVV"%sig)
       
       card.addMJJSignalParametricShapeHiggs("%s_Wqq2_c2"%sig,"MJ2" ,resultsDir+"/JJ_Hjet_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_j':1},{'CMS_res_j':1.0},self.scalesHiggs[dataset])
       card.addMJJSignalParametricShapeNOEXP("%s_Wqq1_c2"%sig,"MJ1" ,resultsDir+"/JJ_Vjet_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
       if self.doCorrelation:
        print "doing correlation"
        card.product("%s_Wqq_c2"%sig,"%s_Wqq1_c2"%sig,"%s_Wqq2_c2"%sig)
        card.conditionalProduct("%s_c2"%sig,"%s_MVV"%sig,"MJ1,MJ2","%s_Wqq_c2"%sig)
       else:
        card.product3D("%s_c2"%sig,"%s_Wqq1_c2"%sig,"%s_Wqq2_c2"%sig,"%s_MVV"%sig)
       
       card.sumSimple("%s"%sig,"%s_c1"%sig,"%s_c2"%sig,"0.5")
       
       if self.outlabel.find("sigOnly")==-1:
          card.addParametricYieldWithUncertainty("%s"%sig,ncontrib,resultsDir+"/JJ_%s_%s_%s_yield.json"%(sig,dataset,category),1,'CMS_tau21_PtDependence',self.vtag_pt_dependence[dataset][category],1.0)
       else:
           card.addParametricYieldWithUncertainty("%s"%sig,ncontrib,resultsDir+"/JJ_%s_%s_%s_yield.json"%(sig,dataset,category),1,'CMS_tau21_PtDependence',self.vtag_pt_dependence[dataset][category],500.)


 #default implementation not working
 def AddTTBackground(self,card,dataset,category,rootFileMVV,rootFileNorm,resultsDir,ncontrib):
       print "add TT+jets background"  

       card.addMJJTTJetsParametricShape("TTJets_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.addMJJTTJetsParametricShape("TTJets_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.addHistoShapeFromFile("TTJets_mjj",["MJJ"],rootFileMVV,"histo_nominal",['PT:CMS_VV_JJ_TTJets_PTZ_'+category,'OPT:CMS_VV_JJ_TTJets_OPTZ_'+category],False,0)       
       card.conditionalProduct3('TTJets','TTJets_mjj','TTJets_mjetRes_l1','TTJets_mjetRes_l2','MJJ',tag1="",tag2="",tag3="")
       
       print "outlabel "+self.outlabel
       if self.pseudodata=="" or self.pseudodata=="Vjets":
           card.addFixedYieldFromFile('TTJets',ncontrib,rootFileNorm,"TTJets")
       elif self.outlabel.find("sigOnly")!=-1 or self.outlabel.find("sigonly")!=-1:
           print "add small yield"
           card.addFixedYieldFromFile('TTJets',ncontrib,rootFileNorm,"TTJets",0.000001)
       else:
           card.addFixedYieldFromFile('TTJets',ncontrib,rootFileNorm,"TTJets")
           
 #new implementation: split in 3 contributions W+W, T+T, nonRes+nonRes
 def AddTTBackground2(self,card,dataset,category,rootFileMVV,rootFileNorm,resultsDir,ncontrib):
       print "add TT+jets background"  
 
       #load mJJ - assume same for the three contributions (preliminary)
       card.addHistoShapeFromFile("TTJets_mjj",["MJJ"],rootFileMVV,"histo_nominal",['PT:CMS_VV_JJ_TTJets_PTZ_'+category,'OPT:CMS_VV_JJ_TTJets_OPTZ_'+category],False,0)       

       # W+W PDF
       card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.conditionalProduct3('TTJetsW','TTJets_mjj','TTJetsW_mjetRes_l1','TTJetsW_mjetRes_l2','MJJ',tag1="",tag2="",tag3="")

       #T+T PDF
       card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.conditionalProduct3('TTJetsTop','TTJets_mjj','TTJetsTop_mjetRes_l1','TTJetsTop_mjetRes_l2','MJJ',tag1="",tag2="",tag3="")

       #nonRes+nonRes PDF
       card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.conditionalProduct3('TTJetsNonRes','TTJets_mjj','TTJetsNonRes_mjetRes_l1','TTJetsNonRes_mjetRes_l2','MJJ',tag1="",tag2="",tag3="")
       
       print "outlabel "+self.outlabel
       if self.pseudodata=="" or self.pseudodata=="Vjets":
           card.addFixedYieldFromFile('TTJets',ncontrib,rootFileNorm,"TTJets")
       elif self.outlabel.find("sigOnly")!=-1 or self.outlabel.find("sigonly")!=-1:
           print "add small yield"
           card.addFixedYieldFromFile('TTJets',ncontrib,rootFileNorm,"TTJets",0.000001)
       else:
           card.addFixedYieldFromFile('TTJetsW',ncontrib,rootFileNorm,"TTJets")
           card.addFixedYieldFromFile('TTJetsTop',ncontrib+1,rootFileNorm,"TTJets")
           card.addFixedYieldFromFile('TTJetsNonRes',ncontrib+2,rootFileNorm,"TTJets")
           
           
           
 
 #new implementation: split in 6 contributions W+W, T+T, nonRes+nonRes, nonRes+T, nonres+W, resT+resW
 def AddTTBackground3(self,card,dataset,category,rootFileMVV,rootFileNorm,resultsDir,ncontrib,uncertainty,normjson):
    print "add TT+jets background"  
    contrib =["resT","resW","nonresT","resTnonresT","resWnonresT","resTresW"]
    mappdf = {"resT":"TTJetsTop","resW":"TTJetsW","nonresT":"TTJetsNonRes","resTnonresT":"TTJetsTNonResT","resWnonresT":"TTJetsWNonResT","resTresW":"TTJetsResWResT"}
    #uncjsonfile=open(resultsDir+"/JJ_"+dataset+"_TTJets_MjjUnc_"+category+".json")
    uncjsonfile=open(resultsDir+"/JJ_"+dataset+"_TTJets_MjjUnc_NP.json")
    unc = json.load(uncjsonfile)
    allunc = []
    for i in range(0,len(contrib)):
     allunc.append(unc[contrib[i]])
    print " allunc ",allunc
    maxunc = max(allunc)
    print " max unc is ",maxunc

    for i in range(0,len(contrib)):
     if self.pseudodata.find("ttbar")!=-1:

       #load mJJ - assume same for the three contributions (preliminary)
       #jsonfile = resultsDir+"/JJ_"+contrib[i]+dataset+"_TTJets_MVV_"+category+".json"
       jsonfile = resultsDir+"/JJ_"+contrib[i]+dataset+"_TTJets_MVV_NP.json"
       print "load parametrisation for MVV ttbar contributions ",jsonfile,contrib[i]
       #card.addMVVMinorBkgParametricShape("TTJets"+contrib[i]+"_mjj",["MJJ"],jsonfile,[uncertainty[0].replace("TTJets",mappdf[contrib[i]])+"_"+category,unc[contrib[i]]])
       card.addMVVMinorBkgParametricShape("TTJets"+contrib[i]+"_mjj",["MJJ"],jsonfile,[uncertainty[0].replace("TTJets",mappdf[contrib[i]]),unc[contrib[i]]])

       #print "load ", rootFileMVV[contrib[i]], " for ttbar contribution"
       #f = ROOT.TFile(rootFileMVV[contrib[i]],"READ")
       #card.addHistoShapeFromFile("TTJets"+contrib[i]+"_mjj",["MJJ"],rootFileMVV[contrib[i]],"histo_nominal",["PT:CMS_VV_JJ_TTJets_PTZ_"+category],False,0)       
     else:
      jsonfile = resultsDir+"/JJ_"+contrib[i]+dataset+"_TTJets_MVV_NP.json"
      slopejson= normjson.replace("Norm","NormSlopes")
      print "load parametrisation for MVV ttbar contributions ",jsonfile,contrib[i],slopejson
      #card.addMVVMinorBkgParametricShape("TTJets"+contrib[i]+"_mjj",["MJJ"],jsonfile,[uncertainty[0].replace("TTJets",mappdf[contrib[i]])+"_"+category,unc[contrib[i]]])
      #card.addMVVMinorBkgParametricShape("TTJets"+contrib[i]+"_mjj",["MJJ"],jsonfile,[uncertainty[0].replace("TTJets",mappdf[contrib[i]]),unc[contrib[i]]],slopejson)
      # have only one slope variation for all 6 contributions, the largest
      card.addMVVMinorBkgParametricShape("TTJets"+contrib[i]+"_mjj",["MJJ"],jsonfile,[uncertainty[0],maxunc],slopejson)


    card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    
    card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    
    card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    '''
    print " testing uncorrelated mjet unc"
    card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj_W_'+category:1.},{'CMS_res_prunedj_W_'+category:1.},self.scales[dataset])#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj_W_'+category:1.},{'CMS_res_prunedj_W_'+category:1.},self.scales[dataset])#,{'CMS_f_g1':1.},{'CMS_f_res':1.})

    card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj_T_'+category:1.},{'CMS_res_prunedj_T_'+category:1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj_T_'+category:1.},{'CMS_res_prunedj_T_'+category:1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})

    card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj_'+category:1.},{'CMS_res_prunedj_'+category:1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj_'+category:1.},{'CMS_res_prunedj_'+category:1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    '''
    # built final PDFs:
    # W+W PDF
    card.conditionalProduct3('TTJetsW','TTJetsresW_mjj','TTJetsW_mjetRes_l1','TTJetsW_mjetRes_l2','MJJ')

    #T+T PDF
    card.conditionalProduct3('TTJetsTop','TTJetsresT_mjj','TTJetsTop_mjetRes_l1','TTJetsTop_mjetRes_l2','MJJ')


    #nonRes+nonRes PDF
    card.conditionalProduct3('TTJetsNonRes','TTJetsnonresT_mjj','TTJetsNonRes_mjetRes_l1','TTJetsNonRes_mjetRes_l2','MJJ')
    
    #resT + nonresT
    card.conditionalProduct3('TTJetsTnonresT','TTJetsresTnonresT_mjj','TTJetsTop_mjetRes_l1','TTJetsNonRes_mjetRes_l2','MJJ')
    #nonresT + resT
    card.conditionalProduct3('TTJetsnonresTresT','TTJetsresTnonresT_mjj','TTJetsNonRes_mjetRes_l1','TTJetsTop_mjetRes_l2','MJJ')
    card.sumPdf('TTJetsTNonResT','TTJetsTnonresT','TTJetsnonresTresT',"CMS_ratio_const")
        
    #resW + nonresT
    card.conditionalProduct3('TTJetsWnonresT','TTJetsresWnonresT_mjj','TTJetsW_mjetRes_l1','TTJetsNonRes_mjetRes_l2','MJJ')
    #nonresT + resW
    card.conditionalProduct3('TTJetsnonresTresW','TTJetsresWnonresT_mjj','TTJetsNonRes_mjetRes_l1','TTJetsW_mjetRes_l2','MJJ')
    card.sumPdf('TTJetsWNonResT','TTJetsWnonresT','TTJetsnonresTresW',"CMS_ratio_const")
    
    #resW + resT
    card.conditionalProduct3('TTJetsresWresT','TTJetsresTresW_mjj','TTJetsW_mjetRes_l1','TTJetsTop_mjetRes_l2','MJJ')
    #resT + resW 
    card.conditionalProduct3('TTJetsresTresW','TTJetsresTresW_mjj','TTJetsTop_mjetRes_l1','TTJetsW_mjetRes_l2','MJJ')
    card.sumPdf('TTJetsResWResT','TTJetsresWresT','TTJetsresTresW',"CMS_ratio_const")
    
       
    print "outlabel "+self.outlabel
    if self.outlabel.find("sigOnly")!=-1 or self.outlabel.find("sigonly")!=-1:
        print "add small yield"
        card.addFixedYieldFromFile('TTJetsW',ncontrib,rootFileNorm["resW"],"TTJetsW",0.000001)
        card.addFixedYieldFromFile('TTJetsTop',ncontrib+1,rootFileNorm["resT"],"TTJetsTop",0.000001)
        card.addFixedYieldFromFile('TTJetsNonRes',ncontrib+2,rootFileNorm["nonresT"],"TTJetsNonRes",0.000001)
        card.addFixedYieldFromFile('TTJetsTnonresT',ncontrib+3,rootFileNorm["resTnonresT"],"TTJetsTnonresT",0.000001/2.)
        card.addFixedYieldFromFile('TTJetsnonresTresT',ncontrib+4,rootFileNorm["resTnonresT"],"TTJetsnonresTresT",0.000001/2.)
        card.addFixedYieldFromFile('TTJetsWnonresT',ncontrib+5,rootFileNorm["resWnonresT"],"TTJetsWnonresT",0.000001/2.)
        card.addFixedYieldFromFile('TTJetsnonresTresW',ncontrib+6,rootFileNorm["resWnonresT"],"TTJetsnonresTresW",0.000001/2.)
    elif self.pseudodata.find("ttbar")!=-1: 
	card.addFixedYieldFromFile('TTJetsW',ncontrib,rootFileNorm["resW"],"TTJets")
        card.addFixedYieldFromFile('TTJetsTop',ncontrib+1,rootFileNorm["resT"],"TTJets")
        card.addFixedYieldFromFile('TTJetsNonRes',ncontrib+2,rootFileNorm["nonresT"],"TTJets")
        card.addFixedYieldFromFile('TTJetsWNonResT',ncontrib+3,rootFileNorm["resWnonresT"],"TTJets")
        card.addFixedYieldFromFile('TTJetsResWResT',ncontrib+4,rootFileNorm["resWresT"],"TTJets")
        card.addFixedYieldFromFile('TTJetsTNonResT',ncontrib+5,rootFileNorm["resTnonresT"],"TTJets")
    else:
        norm = open(normjson,"r")
        norms = json.load(norm)
        mappdf = {"resT":"TTJetsTop","resW":"TTJetsW","nonresT":"TTJetsNonRes","resTnonresT":"TTJetsTNonResT","resWnonresT":"TTJetsWNonResT","resTresW":"TTJetsResWResT"}
        for i in range(0,len(contrib)):
            card.addYield(mappdf[contrib[i]],ncontrib+i,norms[contrib[i]])
	          
 def AddWResBackground(self,card,dataset,category,rootFileMVV,rootFileNorm,resultsDir,ncontrib,uncertainty=[]):
       print "add Wres background"  
       sys.path.append(resultsDir)
       module_name = 'JJ_WJets_%s'%category
       module = __import__(module_name)  
       print module_name
       # W+jets 
       if self.fitvjetsmjj == True:
        card.addMVVMinorBkgParametricShape("Wjets_mjj",["MJJ"],rootFileMVV,uncertainty)
       else:
        card.addHistoShapeFromFile("Wjets_mjj_c1",["MJJ"],rootFileMVV,"histo_nominal",['PT:CMS_VV_JJ_Wjets_PTZ_'+category,'OPT:CMS_VV_JJ_Wjets_OPTZ_'+category],False,0)
       card.addMJJSignalShapeNOEXP("Wjets_mjetRes_l1","MJ1","",getattr(module,'Wjets_TTbar_%s_Res'%category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
       card.addGaussianShape("Wjets_mjetNonRes_l2","MJ2",getattr(module,'Wjets_TTbar_%s_nonRes'%category))
       if self.fitvjetsmjj == True:
        card.product3D("Wjets_c2","Wjets_mjetRes_l2","Wjets_mjetNonRes_l1","Wjets_mjj")
       else:
        card.product3D("Wjets_c1","Wjets_mjetRes_l1","Wjets_mjetNonRes_l2","Wjets_mjj_c1")
      
       # jets + W
       if self.fitvjetsmjj == False:
        card.addHistoShapeFromFile("Wjets_mjj_c2",["MJJ"],rootFileMVV,"histo_nominal",['PT:CMS_VV_JJ_Wjets_PTZ_'+category,'OPT:CMS_VV_JJ_Wjets_OPTZ_'+category],False,0)
       card.addMJJSignalShapeNOEXP("Wjets_mjetRes_l2","MJ2","",getattr(module,'Wjets_TTbar_%s_Res'%category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
       card.addGaussianShape("Wjets_mjetNonRes_l1","MJ1",getattr(module,'Wjets_TTbar_%s_nonRes'%category))
       if self.fitvjetsmjj == True:
        card.product3D("Wjets_c2","Wjets_mjetRes_l2","Wjets_mjetNonRes_l1","Wjets_mjj")
       else:
        card.product3D("Wjets_c2","Wjets_mjetRes_l2","Wjets_mjetNonRes_l1","Wjets_mjj_c2")
       card.sumPdf('Wjets',"Wjets_c1","Wjets_c2","CMS_ratio_Wjets_"+category)
     
       print "outlabel "+self.outlabel
       if self.pseudodata=="" or self.pseudodata=="Vjets":
           card.addFixedYieldFromFile('Wjets',ncontrib,rootFileNorm,"WJets")
       elif self.outlabel.find("sigOnly")!=-1 or self.outlabel.find("sigonly")!=-1 or self.pseudodata.find("ttbar")!=-1:
           print "add small yield"
           card.addFixedYieldFromFile('Wjets',ncontrib,rootFileNorm,"WJets",0.000001)
       else:
           card.addFixedYieldFromFile('Wjets',ncontrib,rootFileNorm,"WJets")

 def AddZResBackground(self,card,dataset,category,rootFileMVV,rootFileNorm,resultsDir,ncontrib,uncertainty=[]):
       print "add Zres background"
       sys.path.append(resultsDir)
       module_name = 'JJ_WJets_%s'%category
       module = __import__(module_name)   
            
       # Z+jets 
       if self.fitvjetsmjj == True:
        #card.addMVVMinorBkgParametricShape("Zjets_mjj_c1",["MJJ"],rootFileMVV,uncertainty)
        card.addMVVMinorBkgParametricShape("Zjets_mjj",["MJJ"],rootFileMVV,uncertainty)
       else:
        card.addHistoShapeFromFile("Zjets_mjj_c1",["MJJ"],rootFileMVV,"histo_nominal",['PT:CMS_VV_JJ_Zjets_PTZ_'+category,'OPT:CMS_VV_JJ_Zjets_OPTZ_'+category],False,0)
       card.addMJJSignalShapeNOEXP("Zjets_mjetRes_l1","MJ1","",getattr(module,'Zjets_%s_Res'%category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
       card.addGaussianShape("Zjets_mjetNonRes_l2","MJ2",getattr(module,'Zjets_%s_nonRes'%category))
       if self.fitvjetsmjj == True:
        card.product3D("Zjets_c1","Zjets_mjetRes_l1","Zjets_mjetNonRes_l2","Zjets_mjj")
       else:
        card.product3D("Zjets_c1","Zjets_mjetRes_l1","Zjets_mjetNonRes_l2","Zjets_mjj_c1")
           
       # jets + Z
       if self.fitvjetsmjj == False:
        card.addHistoShapeFromFile("Zjets_mjj_c2",["MJJ"],rootFileMVV,"histo_nominal",['PT:CMS_VV_JJ_Zjets_PTZ_'+category,'OPT:CMS_VV_JJ_Zjets_OPTZ_'+category],False,0)
       card.addMJJSignalShapeNOEXP("Zjets_mjetRes_l2","MJ2","",getattr(module,'Zjets_%s_Res'%category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales[dataset])
       card.addGaussianShape("Zjets_mjetNonRes_l1","MJ1",getattr(module,'Zjets_%s_nonRes'%category))
       if self.fitvjetsmjj == True:
        card.product3D("Zjets_c2","Zjets_mjetRes_l2","Zjets_mjetNonRes_l1","Zjets_mjj")
       else:
        card.product3D("Zjets_c2","Zjets_mjetRes_l2","Zjets_mjetNonRes_l1","Zjets_mjj_c2")
       card.sumPdf('Zjets',"Zjets_c1","Zjets_c2","CMS_ratio_Zjets_"+category)
      
       if self.pseudodata=="" or self.pseudodata=="Vjets":
             card.addFixedYieldFromFile('Zjets',ncontrib,rootFileNorm,"ZJets") 
       elif self.outlabel.find("sigOnly")!=-1 or self.outlabel.find("sigonly")!=-1 or self.pseudodata.find("ttbar")!=-1:
           card.addFixedYieldFromFile('Zjets',ncontrib,rootFileNorm,"ZJets",0.000001)
       else:
             card.addFixedYieldFromFile('Zjets',ncontrib,rootFileNorm,"ZJets") 
       print "stop Zres background"
   
 def AddNonResBackground(self,card,dataset,category,rootFile3DPDF,rootFileNorm,ncontrib):
      
      card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile3DPDF,"histo",['PT:CMS_VV_JJ_nonRes_PT_'+category,'OPT:CMS_VV_JJ_nonRes_OPT_'+category,'OPT3:CMS_VV_JJ_nonRes_OPT3_'+category,'altshape:CMS_VV_JJ_nonRes_altshape_'+category,'altshape2:CMS_VV_JJ_nonRes_altshape2_'+category],False,0) ,    
          
      if self.outlabel.find("sigonly")!=-1 or self.outlabel.find("sigOnly")!=-1 or self.pseudodata.find("ttbar")!=-1:
          card.addFixedYieldFromFile("nonRes",ncontrib,rootFileNorm,"nonRes",0.0000000000001)
      else:
          card.addFixedYieldFromFile("nonRes",ncontrib,rootFileNorm,"nonRes",self.sfQCD)
 
 def AddData(self,card,fileData,histoName,scaleData):
  
      card.importBinnedData(fileData,histoName,["MJ1","MJ2","MJJ"],'data_obs',scaleData)
 
 #with old implementation 
 def AddTTSystematics(self,card,sig,dataset,category):
    card.addSystematic("CMS_f_g1","param",[0.0,0.02])
    card.addSystematic("CMS_f_res","param",[0.0,0.08])
    card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJets':1.2})  
    card.addSystematic("CMS_VV_JJ_TTJets_PTZ_"+category,"param",[0,0.1]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJets_OPTZ_"+category,"param",[0,0.1]) #0.333
   
 #with new implementation
 def AddTTSystematics2(self,card,sig,dataset,category,resultsDir):
    card.addSystematic("CMS_f_g1","param",[0.0,0.02])
    card.addSystematic("CMS_f_res","param",[0.0,0.08])
    card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJetsW':1.2,'TTJetsTop':1.2,'TTJetsNonRes':1.2})  
    card.addSystematic("CMS_VV_JJ_TTJets_PTZ_"+category,"param",[0,0.1]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJets_OPTZ_"+category,"param",[0,0.1]) #0.333

    f=open(resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category))
    info=json.load(f)
    card.addSystematic("TTresW_frac","rateParam", "{formula}".format(formula=info['f_g1'].replace('MJJ','@0')),"JJ_{category}_13TeV_{year}".format(category=category,year=dataset), "TTJetsW",'MJJ')
    card.addSystematic("TTres_frac","rateParam", "{formula}".format(formula=info['f_res'].replace('MJJ','@0')),"JJ_{category}_13TeV_{year}".format(category=category,year=dataset), "TTJetsW",'MJJ')
    card.addSystematic("TTresT_frac","rateParam", "(@0*(1-@1))","JJ_{category}_13TeV_{year}".format(category=category,year=dataset), "TTJetsTop",'TTres_frac,TTresW_frac')
    card.addSystematic("TTnonres_frac","rateParam", "(1-@0)","JJ_{category}_13TeV_{year}".format(category=category,year=dataset), "TTJetsNonRes",'TTres_frac')

 #with old implementation 
 def AddTTSystematics3(self,card,sig,dataset,category):
    card.addSystematic("CMS_f_g1","param",[0.0,0.02])
    card.addSystematic("CMS_f_res","param",[0.0,0.08])
    #   card.addSystematic("CMS_scale_prunedj_top","param",[0.0,0.02])
    #    card.addSystematic("CMS_res_prunedj_top","param",[0.0,0.08])
    card.addSystematic("CMS_scale_prunedj","param",[0.0,0.02])
    card.addSystematic("CMS_res_prunedj","param",[0.0,0.08])
    card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJetsW':1.2,'TTJetsTop':1.2,'TTJetsNonRes':1.2,'TTJetsWNonResT':1.2,'TTJetsResWResT':1.2,'TTJetsTNonResT':1.2})  
    #card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJets':1.2})  
    card.addSystematic("CMS_VV_JJ_TTJetsTop_PTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsTop_OPTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsW_PTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsW_OPTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsNonRes_PTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsNonRes_OPTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsTnonresT_PTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsTnonresT_OPTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsWnonresT_PTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsWnonresT_OPTZ_"+category,"param",[0,0.333]) #0.333
    
 def AddTTSystematics4(self,card,extra_uncertainty,dataset,category):
    card.addSystematic("CMS_f_g1","param",[0.0,0.02])
    card.addSystematic("CMS_f_res","param",[0.0,0.08])
    #card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJets':1.2})
    card.addSystematic("CMS_scale_prunedj","param",[0.0,0.02])
    card.addSystematic("CMS_res_prunedj","param",[0.0,0.08])
    '''
    print "decorrelateeeeeeeee "
    card.addSystematic("CMS_scale_prunedj_"+category,"param",[0.0,0.3])
    card.addSystematic("CMS_res_prunedj_"+category,"param",[0.0,0.3])
    card.addSystematic("CMS_scale_prunedj_W_"+category,"param",[0.0,0.3])
    card.addSystematic("CMS_res_prunedj_W_"+category,"param",[0.0,0.3])
    card.addSystematic("CMS_scale_prunedj_T_"+category,"param",[0.0,0.3])
    card.addSystematic("CMS_res_prunedj_T_"+category,"param",[0.0,0.3])
    '''
    contrib =["resT","resW","nonresT","resTnonresT","resWnonresT","resTresW"]
    mappdf = {"resT":"TTJetsTop","resW":"TTJetsW","nonresT":"TTJetsNonRes","resTnonresT":"TTJetsTNonResT","resWnonresT":"TTJetsWNonResT","resTresW":"TTJetsResWResT"}
    #uncjsonfile=open('results_'+dataset+"/JJ_"+dataset+"_TTJets_MjjUnc_"+category+".json")
    uncjsonfile=open('results_'+dataset+"/JJ_"+dataset+"_TTJets_MjjUnc_NP.json")
    unc = json.load(uncjsonfile)
    allunc = []
    for i in range(0,len(contrib)):
       allunc.append(unc[contrib[i]])

    #card.addSystematic("CMS_scale_prunedj_top","param",[0.0,0.02])
    #card.addSystematic("CMS_res_prunedj_top","param",[0.0,0.08])
    if self.pseudodata.find("ttbar")==-1:
        #card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJetsW':1.2,'TTJetsTop':1.2,'TTJetsNonRes':1.2,'TTJetsWNonResT':1.2,'TTJetsResWResT':1.2,'TTJetsTNonResT':1.2}) 
        card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJetsW':1.05,'TTJetsTop':1.05,'TTJetsNonRes':1.05,'TTJetsWNonResT':1.05,'TTJetsResWResT':1.05,'TTJetsTNonResT':1.05}) 
        #card.addSystematic(extra_uncertainty[0],"param",[0.0,extra_uncertainty[1]])
        #card.addSystematic(extra_uncertainty[0].replace("TTJets",mappdf[contrib[i]])+"_"+category,"param",[0.0,float("{:.3f}".format(unc[contrib[i]]))])
        card.addSystematic(extra_uncertainty[0],"param",[0.0,float("{:.3f}".format(max(allunc)))])
    else:
        for i in range(0,len(contrib)):
         #card.addSystematic(extra_uncertainty[0].replace("TTJets",mappdf[contrib[i]])+"_"+category,"param",[0.0,float("{:.3f}".format(unc[contrib[i]]))])
         card.addSystematic("CMS_VV_JJ_"+mappdf[contrib[i]]+"_norm","lnN",{mappdf[contrib[i]]:3.2})
         card.addSystematic(extra_uncertainty[0].replace("TTJets",mappdf[contrib[i]]),"param",[0.0,float("{:.3f}".format(unc[contrib[i]]))])
    
       
 def AddSigSystematics(self,card,sig,dataset,category,correlate):

      card.addSystematic("CMS_scale_prunedj","param",[0.0,0.02])
      card.addSystematic("CMS_res_prunedj","param",[0.0,0.08])
      card.addSystematic("CMS_scale_j","param",[0.0,0.012])
      card.addSystematic("CMS_res_j","param",[0.0,0.08])

      card.addSystematic("CMS_pdf","lnN",{'%s'%sig:1.01})    
      if correlate:
       card.addSystematic("CMS_lumi","lnN",{'%s'%sig:self.lumi_unc[dataset],"Wjets":self.lumi_unc[dataset],"Zjets":self.lumi_unc[dataset],
                                            'TTJetsW':self.lumi_unc[dataset],'TTJetsTop':self.lumi_unc[dataset],'TTJetsNonRes':self.lumi_unc[dataset],'TTJetsWNonResT':self.lumi_unc[dataset],'TTJetsResWResT':self.lumi_unc[dataset],'TTJetsTNonResT':self.lumi_unc[dataset]})   
      else: 
       card.addSystematic("CMS_lumi","lnN",{'%s'%sig:self.lumi_unc[dataset]})
      
    
 def AddTaggingSystematics(self,card,signal,dataset,p,jsonfile): 
     with open(jsonfile) as json_file:
        data = json.load(json_file)
     sig = signal
     if signal.find('Zprime')!=-1 and signal.find("ZH")!=-1: sig = "ZprimeToZh" 
     if signal.find('Zprime')!=-1 and signal.find("WW")!=-1: sig = "ZprimeToWW"
     if signal.find('Wprime')!=-1 and signal.find("WH")!=-1: sig = "WprimeToWh" 
     if signal.find('Wprime')!=-1 and signal.find("WZ")!=-1: sig = "WprimeToWZ"
     if signal.find('BulkGWW')!=-1 : sig = "BulkGravToWW" 
     if signal.find('BulkGZZ')!=-1 : sig = "BulkGravToZZ"
     uncup   = data[sig+"_"+dataset+"_CMS_VV_JJ_DeepJet_Htag_eff"][p+"_up"]
     uncdown = data[sig+"_"+dataset+"_CMS_VV_JJ_DeepJet_Htag_eff"][p+"_down"]
     card.addSystematic("CMS_VV_JJ_DeepJet_Htag_eff","lnN",{'%s'%signal: str(uncup)+"/"+ str(uncdown),'Wjets': str(uncup)+"/"+ str(uncdown),'Zjets': str(uncup)+"/"+ str(uncdown)})
     uncup   = data[sig+"_"+dataset+"_CMS_VV_JJ_DeepJet_Vtag_eff"][p+"_up"]
     uncdown = data[sig+"_"+dataset+"_CMS_VV_JJ_DeepJet_Vtag_eff"][p+"_down"]
     card.addSystematic("CMS_VV_JJ_DeepJet_Vtag_eff","lnN",{'%s'%signal: str(uncup)+"/"+ str(uncdown),'Wjets': str(uncup)+"/"+ str(uncdown),'Zjets': str(uncup)+"/"+ str(uncdown)})
     
     
 def AddResBackgroundSystematics(self,card,category,extra_uncertainty=[]):
 
       card.addSystematic("CMS_VV_JJ_Wjets_norm","lnN",{'Wjets':1.05})
       card.addSystematic("CMS_VV_JJ_Zjets_norm","lnN",{'Zjets':1.05}) 
       if self.fitvjetsmjj == True:
        card.addSystematic(extra_uncertainty[0],"param",[0.0,extra_uncertainty[1]])
        card.addSystematic(extra_uncertainty[2],"param",[0.0,extra_uncertainty[3]])
       else:
        card.addSystematic("CMS_VV_JJ_Wjets_PTZ_"+category,"param",[0,0.1]) #0.333
        card.addSystematic("CMS_VV_JJ_Wjets_OPTZ_"+category,"param",[0,0.1]) #0.333
        card.addSystematic("CMS_VV_JJ_Zjets_PTZ_"+category,"param",[0,0.1]) #0.333
        card.addSystematic("CMS_VV_JJ_Zjets_OPTZ_"+category,"param",[0,0.1]) #0.333
       

 def AddNonResBackgroundSystematics(self,card,category):

      card.addSystematic("CMS_VV_JJ_nonRes_norm","lnN",{'nonRes':1.5})
      
      card.addSystematic("CMS_VV_JJ_nonRes_PT_"+category,"param",[0.0,0.666])
      card.addSystematic("CMS_VV_JJ_nonRes_OPT_"+category,"param",[0.0,0.333])
      card.addSystematic('CMS_VV_JJ_nonRes_altshape2_'+category,"param",[0.0,0.333])  
      card.addSystematic('CMS_VV_JJ_nonRes_altshape_'+category,"param",[0.0,0.333])
      card.addSystematic("CMS_VV_JJ_nonRes_OPT3_"+category,"param",[1.0,0.333])
