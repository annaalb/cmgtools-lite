from tools.DatacardTools import *
import sys,os
import ROOT
import json
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
from optparse import OptionParser
import cuts

# produce workspace with ttbar only
# python makeCard.py -p "2016" --signal "BulkGWW" -c "VH_NPHP_control_region,VH_HPNP_control_region" --outlabel "_ttbar" --pseudodata "ttbar"
# produce the preparatory workspace to make the pseudodata with all workspace
# python makeCard.py -p "2016" --signal "BulkGWW" -c "VH_HPNP_control_region" --outlabel "_PrepPseudo" --pseudodata "PrepPseudo"
# produce the workspace with all backgrounds and pseudodata
# python makeCard.py -p "2016" --signal "BulkGWW" -c "VH_HPNP_control_region,VH_NPHP_control_region" --outlabel "_pseudodata" --pseudodata "True"
# produce the workspace with all backgrounds and data
# python makeCard.py -p "2016" --signal "BulkGWW" -c "VH_NPHP_control_region,VH_HPNP_control_region" --outlabel "_data" --pseudodata "False"

parser = OptionParser()
parser.add_option("-p","--period",dest="period",default="2016,2017",help="run period")
parser.add_option("--pseudodata",dest="pseudodata",help="make cards with real data(False option) or differen pseudodata sets: Vjets, ZprimeZH etc",default='')
parser.add_option("--signal",dest="signal",default="BulkGWW,BulkGZZ,ZprimeWW,ZprimeZH,WprimeWH,WprimeWZ",help="which signal do you want to run? options are BulkGWW, BulkGZZ, WprimeWZ, ZprimeWW, ZprimeZH")
parser.add_option("--outlabel",dest="outlabel",help="lebel for output workspaces for example sigonly_M4500",default='')
parser.add_option("-c","--category",dest="category",default="VV_HPLP,VV_HPHP,VH_HPLP,VH_HPHP,VH_LPHP",help="run period")
parser.add_option("-j","--jsonname",dest="jsonname",help="write the name of the output json file, the category will be automatically inserted",default='ttbarNorm')
parser.add_option("--fitvjetsmjj",dest="fitvjetsmjj",default=False,action="store_true",help="True makes fits for mjj of vjets, False uses hists")

(options,args) = parser.parse_args()



cmd='combineCards.py '



pseudodata = options.pseudodata

outlabel = options.outlabel

datasets= options.period.split(",")


purities= options.category.split(",")

signals = options.signal.split(",")

doVjets= True
sf_qcd=1.
if outlabel.find("sigonly")!=-1 or outlabel.find("qcdonly")!=-1: doVjets = False
if outlabel.find("sigonly")!=-1 or outlabel.find("Vjetsonly")!=-1: sf_qcd = 0.00001

resultsDir = {'2016':'results_2016','2017':'results_2017','2018':'results_2018'}#'2016':'ttbarmodeling''2016':'newmodel4GeV'

# vtag uncertainty is added through the migrationunc.json file 
# all other uncertainties and SF from one place: defined in init_VV_VH.json imported via the class defined in cuts.py
ctx16 = cuts.cuts("init_VV_VH.json",2016,"dijetbins_random")
ctx17 = cuts.cuts("init_VV_VH.json",2017,"dijetbins_random")
ctx18 = cuts.cuts("init_VV_VH.json",2018,"dijetbins_random")

lumi = {'2016':ctx16.lumi,'2017':ctx17.lumi, '2018':ctx18.lumi}
lumi_unc = {'2016':ctx16.lumi_unc,'2017':ctx17.lumi_unc, '2018':ctx18.lumi_unc}

if pseudodata == False:
  scales = {"2017" :[ctx17.W_HPmassscale,ctx17.W_LPmassscale], "2016":[ctx16.W_HPmassscale,ctx16.W_LPmassscale], "2018":[ctx18.W_HPmassscale,ctx18.W_LPmassscale]}
  scalesHiggs = {"2017" :[ctx17.H_HPmassscale,ctx17.H_LPmassscale], "2016":[ctx16.H_HPmassscale,ctx16.H_LPmassscale], "2018":[ctx18.H_HPmassscale,ctx18.H_LPmassscale]}

scales = {"2017" :[1,1], "2016":[1,1], "2018":[1,1]}
scalesHiggs = {"2017" :[1,1], "2016":[1,1], "2018":[1,1]}

vtag_pt_dependence = {'VV_HPHP':'((1+0.06*log(MH/2/300))*(1+0.06*log(MH/2/300)))','VV_HPLP':'((1+0.06*log(MH/2/300))*(1+0.07*log(MH/2/300)))','VH_HPHP':'1','VH_HPLP':'1','VH_LPHP':'1','VH_LPLP':'1'}

#quick fix to add VH !!!
vtag_pt_dependence = {"2016" : ctx16.vtag_pt_dependence,"2017" : ctx17.vtag_pt_dependence,"2018" : ctx18.vtag_pt_dependence}

doCorrelation = True 
Tools = DatacardTools(scales,scalesHiggs,vtag_pt_dependence,lumi_unc,sf_qcd,pseudodata,outlabel,doCorrelation,options.fitvjetsmjj)

for sig in signals:
  cmd ="combineCards.py"
  for dataset in datasets:
    cmd_combo="combineCards.py"
    for p in purities:

      ncontrib = 0
      
      cat='_'.join(['JJ',sig,p,'13TeV_'+dataset])
      card=DataCardMaker('',p,'13TeV_'+dataset,lumi[dataset],'JJ',cat)
      cmd=cmd+" "+cat.replace('_%s'%sig,'')+'=datacard_'+cat+'.txt '
      cmd_combo=cmd_combo+" "+cat.replace('_%s'%sig,'')+'=datacard_'+cat+'.txt '
      cardName='datacard_'+cat+'.txt '
      workspaceName='workspace_'+cat+outlabel+'.root'

      Tools.AddSignal(card,dataset,p,sig,resultsDir[dataset],ncontrib)
      ncontrib+=1
      print "##########################       including W/Z jets in datacard      ######################"
      rootFileNorm = resultsDir[dataset]+'/JJ_%s_WJets_%s.root'%(dataset,p)
      if options.fitvjetsmjj == True:
        rootFileMVV =  resultsDir[dataset]+'/JJ_%s_WJets_MVV_NP_Wjets'%dataset+'.json'
        Tools.AddWResBackground(card,dataset,p,rootFileMVV,rootFileNorm,resultsDir[dataset],ncontrib,["CMS_VV_JJ_WJets_slope",0.5])
      else:
        rootFileMVV = resultsDir[dataset]+'/JJ_%s_WJets_MVV_'%dataset+p+'.root'
        Tools.AddWResBackground(card,dataset,p,rootFileMVV,rootFileNorm,resultsDir[dataset],ncontrib)
      ncontrib+=1
      
      rootFileNorm = resultsDir[dataset]+"/JJ_%s_ZJets_%s.root"%(dataset,p)
      if options.fitvjetsmjj == True:
        rootFileMVV =  resultsDir[dataset]+'/JJ_%s_ZJets_MVV_NP_Zjets'%dataset+'.json'
        Tools.AddZResBackground(card,dataset,p,rootFileMVV,rootFileNorm,resultsDir[dataset],ncontrib,["CMS_VV_JJ_ZJets_slope",0.5])
      else:
        rootFileMVV = resultsDir[dataset]+'/JJ_%s_ZJets_MVV_'%dataset+p+'.root'
        Tools.AddZResBackground(card,dataset,p,rootFileMVV,rootFileNorm,resultsDir[dataset],ncontrib)
      ncontrib+=1
        
      print "including tt+jets in datacard"
      #rootFileMVV = {"resT":resultsDir[dataset]+'/JJ_resT'+dataset+'_TTJets_MVV_NP.root', "resW":resultsDir[dataset]+"/JJ_resW"+dataset+"_TTJets_MVV_NP.root","nonresT":resultsDir[dataset]+"/JJ_nonresT"+dataset+"_TTJets_MVV_NP.root","resTnonresT":resultsDir[dataset]+"/JJ_resTnonresT"+dataset+"_TTJets_MVV_NP.root","resWnonresT":resultsDir[dataset]+"/JJ_resWnonresT"+dataset+"_TTJets_MVV_NP.root","resTresW":resultsDir[dataset]+"/JJ_resTresW"+dataset+"_TTJets_MVV_NP.root"}
      rootFileMVV = {"resT":resultsDir[dataset]+'/JJ_resT'+dataset+'_TTJets_MVV_'+p+'.root', "resW":resultsDir[dataset]+"/JJ_resW"+dataset+"_TTJets_MVV_"+p+".root","nonresT":resultsDir[dataset]+"/JJ_nonresT"+dataset+"_TTJets_MVV_"+p+".root","resTnonresT":resultsDir[dataset]+"/JJ_resTnonresT"+dataset+"_TTJets_MVV_"+p+".root","resWnonresT":resultsDir[dataset]+"/JJ_resWnonresT"+dataset+"_TTJets_MVV_"+p+".root","resTresW":resultsDir[dataset]+"/JJ_resTresW"+dataset+"_TTJets_MVV_"+p+".root"}
      rootFileNorm = {"resT" : resultsDir[dataset]+'/JJ_resT'+dataset+'_TTJets_'+p+'.root', "resW": resultsDir[dataset]+'/JJ_resW'+dataset+'_TTJets_'+p+'.root',"nonresT" : resultsDir[dataset]+'/JJ_nonresT'+dataset+'_TTJets_'+p+'.root',"resTnonresT": resultsDir[dataset]+'/JJ_resTnonresT'+dataset+'_TTJets_'+p+'.root' , "resWnonresT": resultsDir[dataset]+'/JJ_resWnonresT'+dataset+'_TTJets_'+p+'.root',"resWresT": resultsDir[dataset]+'/JJ_resTresW'+dataset+'_TTJets_'+p+'.root'}
      jsonfileNorm = resultsDir[dataset]+'/'+options.jsonname+'_'+p+'.json'
      Tools.AddTTBackground3(card,dataset,p,rootFileMVV,rootFileNorm,resultsDir[dataset],ncontrib,["CMS_VV_JJ_TTJets_slope",0.5],jsonfileNorm)
      #rootFileMVV  = resultsDir[dataset]+'/JJ_'+dataset+'_TTJets_MVV_'+p+'.root'
      #rootFileNorm = resultsDir[dataset]+'/JJ_'+dataset+'_TTJets_'+p+'.root'
      #Tools.AddTTBackground2(card,dataset,p,rootFileMVV,rootFileNorm,resultsDir[dataset],ncontrib)
      #ncontrib+=1 --> with old implementation
      ncontrib+=6 #--> with new implementation
      #ncontrib+=3 #--> with new implementation

      print " including QCD in datacard"
      #rootFile3DPDF = resultsDir[dataset]+'/JJ_2016_nonRes_3D_VV_HPLP.root'
      rootFile3DPDF = resultsDir[dataset]+"/save_new_shapes_{year}_pythia_{purity}_3D.root".format(year=dataset,purity=p)#    save_new_shapes_%s_pythia_"%dataset+"_""VVVH_all"+"_3D.root"
      print "rootFile3DPDF ",rootFile3DPDF
      rootFileNorm = resultsDir[dataset]+"/JJ_%s_nonRes_"%dataset+p+".root"
      print "rootFileNorm ",rootFileNorm
      Tools.AddNonResBackground(card,dataset,p,rootFile3DPDF,rootFileNorm,ncontrib)

      print " including data or pseudodata in datacard"
      if pseudodata=="PrepPseudo":
        rootFileData = resultsDir[dataset]+"/JJ_%s_nonRes_3D_NP.root"%(dataset) #use this only to prepare workspace for making pseudo data with vjets
        histName="histo"
        scaleData=lumi[dataset]
      elif pseudodata=="True":
        print "Using pseudodata with all backgrounds (QCD, V+jets and tt+jets)"
        rootFileData = resultsDir[dataset]+"/JJ_PDALL_"+p+".root"
        histName="data"
        scaleData=1.0
      elif pseudodata=="ttjets":
        print "Using pseudodata with only tt+jets backgrounds"
        rootFileData = resultsDir[dataset]+"/JJ_TTJets_"+p+".root"
        histName="data_obs"
        scaleData=1.0
      elif pseudodata=="noqcd":
        print "Using pseudodata with only tt+jets backgrounds and no qcd"
        rootFileData = resultsDir[dataset]+"/JJ_PDnoQCD_"+p+".root"
        histName="data"
        scaleData=1.0
      elif pseudodata=="ttbar":
        print "Using pseudodata with only tt backgrounds"
        rootFileData = resultsDir[dataset]+"/JJ_PDTT_"+p+".root"
        histName="data"
        scaleData=1.0
      elif pseudodata==sig:
       rootFileData = resultsDir[dataset]+"/pseudodata_sigOnly_"+dataset+"_"+sig+"_"+p+"_"+"M"+outlabel.split("_M")[1]+".root"
       histName="data_obs" 
       scaleData=1.0
      elif pseudodata=="False":
        rootFileData = resultsDir[dataset]+"/JJ_"+dataset+"_data_"+p+".root" #resultsDir[dataset]+"/pseudo40/JJ_"+p+".root"
        histName="data"
        scaleData=1.0


      Tools.AddData(card,rootFileData,histName,scaleData)
      
      Tools.AddSigSystematics(card,sig,dataset,p,1)
      if options.fitvjetsmjj == True:
        Tools.AddResBackgroundSystematics(card,p,["CMS_VV_JJ_WJets_slope",0.2,"CMS_VV_JJ_ZJets_slope",0.2])
      else:
        Tools.AddResBackgroundSystematics(card,p)
      Tools.AddNonResBackgroundSystematics(card,p)
      #Tools.AddTaggingSystematics(card,sig,dataset,p,resultsDir[dataset]+'/migrationunc.json')
      Tools.AddTTSystematics4(card,["CMS_VV_JJ_TTJets_slope",0.05],dataset,p)
      #Tools.AddTTSystematics2(card,sig,dataset,p,resultsDir[dataset])
      card.makeCard()

      t2wcmd = "text2workspace.py %s -o %s"%(cardName,workspaceName)
      print t2wcmd
      os.system(t2wcmd)
    del card

    print "#####################################"

    #make combined 
    if len(purities)>1:
      print "#######     going to combine purity categories: ",purities    
      combo_card = cardName.replace("VV_HPHP","").replace("VV_HPLP","").replace("VV_LPLP","").replace("VH_HPHP","").replace("VH_HPLP","").replace("VH_LPHP","").replace("VH_HPNP_control_region","").replace("VH_NPHP_control_region","").replace("__","_VVVH_")
      combo_workspace = workspaceName.replace("VV_HPHP","").replace("VV_HPLP","").replace("VV_LPLP","").replace("VH_HPHP","").replace("VH_HPLP","").replace("VH_LPHP","").replace("VH_HPNP_control_region","").replace("VH_NPHP_control_region","").replace("__","_VVVH_")
      os.system('rm %s'%combo_card)
      cmd_combo+=' >> %s'%combo_card
      print cmd_combo
      os.system(cmd_combo)
      t2wcmd = "text2workspace.py %s -o %s"%(combo_card,combo_workspace)
      print t2wcmd
      os.system(t2wcmd)
      print "#####################################"

  if len(datasets)>1:   
    #make combine 2016+2017 card
    print "more than one year, making combined cards"
    combo_card = 'datacard_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","").replace('_2016','').replace('_2017','')+'.txt'
    combo_workspace = 'workspace_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","").replace('_2016','').replace('_2017','')+'.root'
    os.system('rm %s'%combo_card)
    cmd+=' >> %s'%combo_card
    print cmd
    os.system(cmd)
    t2wcmd = "text2workspace.py %s -o %s"%(combo_card,combo_workspace)
    print t2wcmd
    os.system(t2wcmd)

    


