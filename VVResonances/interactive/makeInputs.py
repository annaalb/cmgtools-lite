import ROOT
import os,sys

submitToBatch = False #Set to true if you want to submit kernels + makeData to batch!
runParallel   = False #Set to true if you want to run all kernels in parallel! This will exit this script and you will have to run mergeKernelJobs when your jobs are done! TODO! Add waitForBatchJobs also here?
 	
cat={}
# For standard tau 21, use this
# cat['HP1'] = 'jj_l1_tau2/jj_l1_tau1<0.35'
# cat['HP2'] = 'jj_l2_tau2/jj_l2_tau1<0.35'
# cat['LP1'] = 'jj_l1_tau2/jj_l1_tau1>0.35&&jj_l1_tau2/jj_l1_tau1<0.75'
# cat['LP2'] = 'jj_l2_tau2/jj_l2_tau1>0.35&&jj_l2_tau2/jj_l2_tau1<0.75'
# cat['NP1'] = 'jj_l1_tau2/jj_l1_tau1>0.75'
# cat['NP2'] = 'jj_l2_tau2/jj_l2_tau1>0.75'

# For standard DDT tau 21, use this
#cat['HP1'] = 'jj_l1_tau21_DDT<0.47'
#cat['HP2'] = 'jj_l2_tau21_DDT<0.47'
#cat['LP1'] = 'jj_l1_tau21_DDT>0.47&&jj_l1_tau21_DDT<0.88'
#cat['LP2'] = 'jj_l2_tau21_DDT>0.47&&jj_l2_tau21_DDT<0.88'
#cat['NP1'] = 'jj_l1_tau21_DDT>0.88'
#cat['NP2'] = 'jj_l2_tau21_DDT>0.88'

# For retuned DDT tau 21, use this
cat['HP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.57'
cat['HP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.57'
cat['LP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.57&&(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.98'
cat['LP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.57&&(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.98'
cat['NP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.98'
cat['NP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.98'


cuts={}

cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.)'

cuts['HPHP'] = '('+cat['HP1']+'&&'+cat['HP2']+')'
cuts['LPLP'] = '('+cat['LP1']+'&&'+cat['LP2']+')'
cuts['HPLP'] = '(('+cat['HP1']+'&&'+cat['LP2']+')||('+cat['LP1']+'&&'+cat['HP2']+'))'
cuts['NP'] = '(('+cat['LP1']+'&&'+cat['NP2']+')||('+cat['NP1']+'&&'+cat['LP2']+'))'

cuts['nonres'] = '1'

purities=['HPHP','HPLP','LPLP','NP']
purities=['HPHP']

BulkGravWWTemplate="BulkGravToWW_narrow"
BulkGravZZTemplate="BulkGravToZZToZhadZhad_narrow"
BRWW=1.*0.001
BRZZ=1.*0.001

dataTemplate="JetHT"
#nonResTemplate="QCD_Pt_" #high stat
nonResTemplate="QCD_Pt-" #low stat --> use this for tests
#nonResTemplate="Dijet" #to compare shapes

minMJ=55.0
maxMJ=215.0

minMVV=1000.0
maxMVV=5000.0

minMX=1200.0
maxMX=7000.0

binsMJ=80
binsMVV=100

cuts['acceptance']= "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV}&&jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ}&&jj_l2_softDrop_mass>{minMJ}&&jj_l2_softDrop_mass<{maxMJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJ=minMJ,maxMJ=maxMJ)
cuts['acceptanceGEN']='(jj_l1_gen_softDrop_mass>20&&jj_l2_gen_softDrop_mass>20&&jj_l1_gen_softDrop_mass<300&&jj_l2_gen_softDrop_mass<300&&jj_gen_partialMass>600&&jj_gen_partialMass<6000)'

cuts['acceptanceMJ']= "(jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ}&&jj_l2_softDrop_mass>{minMJ}&&jj_l2_softDrop_mass<{maxMJ})".format(minMJ=minMJ,maxMJ=maxMJ) 
cuts['looseacceptanceMJ']= "(jj_l1_softDrop_mass>35&&jj_l1_softDrop_mass<300&&jj_l2_softDrop_mass>35&&jj_l2_softDrop_mass<300)"
cuts['acceptanceMVV'] = "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV})".format(minMVV=minMVV,maxMVV=maxMVV)

def makeSignalShapesMVV(filename,template):
 cut='*'.join([cuts['common'],cuts['acceptanceMJ']])
 rootFile=filename+"_MVV.root"
 cmd='vvMakeSignalMVVShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "jj_LV_mass"   -m {minMVV} -M {maxMVV} --minMX {minMX} --maxMX {maxMX} samples'.format(template=template,cut=cut,rootFile=rootFile,minMVV=minMVV,maxMVV=maxMVV,minMX=minMX,maxMX=maxMX)
 os.system(cmd)
 jsonFile=filename+"_MVV.json"
 print 'Making JSON'
 cmd='vvMakeJSON.py  -o "{jsonFile}" -g "MEAN:pol1,SIGMA:pol2,ALPHA:pol3,N:pol0,SCALESIGMA:pol3,f:pol3" -m {minMVV} -M {maxMVV}  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile,minMVV=minMVV,maxMVV=maxMVV)
 os.system(cmd)

def makeSignalShapesMJ(filename,template,leg):
 for p in purities:
  cut='*'.join([cuts['common'],cuts[p]])
  rootFile=filename+"_MJ"+leg+"_"+p+".root"
  doExp=0
  if p=='HPHP':
      cmd='vvMakeSignalMJShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "jj_{leg}_softDrop_mass" -m {minMJ} -M {maxMJ} -e {doExp} -f "alpha:1.347" --minMX {minMX} --maxMX {maxMX} samples'.format(template=template,cut=cut,rootFile=rootFile,leg=leg,minMJ=minMJ,maxMJ=maxMJ,doExp=doExp,minMX=minMX,maxMX=maxMX)
  else:
      # doExp=1
      cmd='vvMakeSignalMJShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "jj_{leg}_softDrop_mass" -m {minMJ} -M {maxMJ} -e {doExp} -f "alpha:1.125" --minMX {minMX} --maxMX {maxMX} samples'.format(template=template,cut=cut,rootFile=rootFile,leg=leg,minMJ=minMJ,maxMJ=maxMJ,doExp=doExp,minMX=minMX,maxMX=maxMX)
  os.system(cmd)
  jsonFile=filename+"_MJ"+leg+"_"+p+".json"

  if p=='HPHP':
      cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol4,sigma:pol4,alpha:pol3,n:pol0,alpha2:pol3,n2:pol0,slope:pol0,f:pol0" -m 1000 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
  else:
      cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol4,sigma:pol4,alpha:pol3,n:pol0,alpha2:pol3,n2:pol0,slope:pol0,f:pol0" -m 1000 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)

  os.system(cmd)

def makeSignalYields(filename,template,branchingFraction,sfP = {'HPHP':1.0,'HPLP':1.0,'LPLP':1.0}):
 	 
 for p in purities:
  cut = "*".join([cuts[p],cuts['common'],cuts['acceptance'],str(sfP[p])])
  #Signal yields
  yieldFile=filename+"_"+p+"_yield"
  fnc = "pol2"
  # if p == "HPHP": fnc = "pol2"
  cmd='vvMakeSignalYields.py -s {template} -c "{cut}" -o {output} -V "jj_LV_mass" -m {minMVV} -M {maxMVV} -f {fnc} -b {BR} --minMX {minMX} --maxMX {maxMX} samples'.format(template=template, cut=cut, output=yieldFile,minMVV=minMVV,maxMVV=maxMVV,fnc=fnc,BR=branchingFraction,minMX=minMX,maxMX=maxMX)
  os.system(cmd)

def makeDetectorResponse(name,filename,template,addCut="1",jobName="DetPar"):
		pwd = os.getcwd()
		samples = pwd +"/samples"
		# cut='*'.join([cuts['common'],addCut,'(jj_l1_gen_softDrop_mass>30&&jj_l2_gen_softDrop_mass>30&&jj_gen_partialMass>500)'])
		cut='*'.join([cuts['common'],addCut,cuts['acceptanceGEN'],cuts['looseacceptanceMJ']])
		resFile=filename+"_"+name+"_detectorResponse.root"		 
		print "Saving detector resolution to file: " ,resFile
		bins = "200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000"
		if submitToBatch:
		        # template += ",QCD_Pt-,QCD_HT"
			from modules.submitJobs import Make2DDetectorParam,merge2DDetectorParam	
			jobList, files = Make2DDetectorParam(resFile,template,cut,samples,jobName,bins)
			jobList = []
			files = []
			merge2DDetectorParam(jobList,files,bins,jobName)
		else:
			cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_LV_mass,jj_l1_softDrop_mass"  -g "jj_gen_partialMass,jj_l1_gen_softDrop_mass,jj_l1_gen_pt"  -b {bins}   samples'.format(rootFile=resFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name,bins=bins)
			os.system(cmd)
		
		print "Done with ",resFile
  
def makeBackgroundShapesMJKernel(name,filename,template,leg,addCut="1"):
 
 #template += ",QCD_Pt-,QCD_HT"
 for p in purities:
  resFile=filename+"_"+name+"_detectorResponse.root"	
  print "=========== PURITY: ", p
  cut='*'.join([cuts['common'],cuts[p],addCut,cuts['acceptanceGENMJ'],cuts['acceptanceMVV']])
  rootFile=filename+"_"+name+"_MJ"+leg+"_"+p+".root"  	      
  cmd='vvMake1DTemplateWithKernels.py -H "y" -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_{leg}_gen_softDrop_mass" -b {binsMJ}  -x {minMJ} -X {maxMJ} -r {res} samples'.format(rootFile=rootFile,samples=template,cut=cut,leg=leg,res=resFile,binsMJ=binsMJ,minMJ=minMJ,maxMJ=maxMJ)
  os.system(cmd)

def makeBackgroundShapesMJSpline(name,filename,template,leg,addCut="1"):

 #template += ",QCD_Pt-,QCD_HT"
 for p in purities:
  print "=========== PURITY: ", p
  cut='*'.join([cuts['common'],cuts[p],addCut,cuts['acceptance']])
  rootFile=filename+"_"+name+"_MJ"+leg+"_"+p+"_spline.root"	      
  cmd='vvMake1DTemplateSpline.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_{leg}_softDrop_mass"  -b {binsMJ}  -x {minMJ} -X {maxMJ} -f 6 samples'.format(rootFile=rootFile,samples=template,cut=cut,leg=leg,binsMJ=binsMJ,minMJ=minMJ,maxMJ=maxMJ)
  os.system(cmd)

def makeBackgroundShapesMVVKernel(name,filename,template,addCut="1",jobName="1D",wait=True):
 pwd = os.getcwd()
 for p in purities:
  jobname = jobName+"_"+p
  print " Working on purity: ", p
  resFile  = pwd + "/"+ filename+"_"+name+"_detectorResponse.root"	
  rootFile = filename+"_"+name+"_MVV_"+p+".root"
  print "Reading " ,resFile
  print "Saving to ",rootFile
  cut='*'.join([cuts['common'],cuts[p],addCut,cuts['acceptanceGEN'],cuts['acceptanceMJ']])
  samples = pwd +"/samples"

  if submitToBatch:
    # template += ",QCD_Pt-,QCD_HT"
    from modules.submitJobs import Make1DMVVTemplateWithKernels,merge1DMVVTemplate
    jobList, files = Make1DMVVTemplateWithKernels(rootFile,template,cut,resFile,binsMVV,minMVV,maxMVV,samples,jobname,wait)
    if wait: merge1DMVVTemplate(jobList,files,jobname,p,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ)
  else:
    cmd='vvMake1DMVVTemplateWithKernels.py -H "x" -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_gen_partialMass" -b {binsMVV}  -x {minMVV} -X {maxMVV} -r {res} samples'.format(rootFile=rootFile,samples=template,cut=cut,res=resFile,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV)
    os.system(cmd)	  

def makeBackgroundShapesMVVConditional(name,filename,template,leg,addCut="",jobName="2DMVV",wait=True):
 pwd = os.getcwd()	
 for p in purities:
  jobname = jobName+"_"+p
  print " Working on purity: ", p
  resFile  = pwd + "/"+ filename+"_"+name+"_detectorResponse.root"
  rootFile=filename+"_"+name+"_COND2D_"+p+"_"+leg+".root"		
  print "Reading " ,resFile
  print "Saving to ",rootFile
  # cut='*'.join([cuts['common'],cuts[p],addCut,cuts['acceptanceGEN']])
  cut='*'.join([cuts['common'],cuts[p],addCut,cuts['acceptanceGEN'],cuts['looseacceptanceMJ']])
  samples = pwd +"/samples" 
  
  if submitToBatch:
    # template += ",QCD_Pt-,QCD_HT"
    from modules.submitJobs import Make2DTemplateWithKernels,merge2DTemplate
    jobList, files = Make2DTemplateWithKernels(rootFile,template,cut,leg,binsMVV,minMVV,maxMVV,resFile,binsMJ,minMJ,maxMJ,samples,jobname,wait)
    if wait: merge2DTemplate(jobList,files,jobname,p,leg,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ)
  else:
    cmd='vvMake2DTemplateWithKernels.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_{leg}_gen_softDrop_mass,jj_gen_partialMass"  -b {binsMJ} -B {binsMVV} -x {minMJ} -X {maxMJ} -y {minMVV} -Y {maxMVV}  -r {res} samples'.format(rootFile=rootFile,samples=template,cut=cut,leg=leg,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,res=resFile,binsMJ=binsMJ,minMJ=minMJ,maxMJ=maxMJ)
    os.system(cmd)

def mergeKernelJobs():
	for p in purities:
		jobList = []
		files   = []
		with open("tmp1D_%s_joblist.txt"%p,'r') as infile:
			for line in infile:
				if line.startswith("job"):
					for job in line.split("[")[1].split("]")[0].split(","):
						jobList.append(job.replace("'","").replace(" ",""))
			if line.startswith("file"):
				for job in line.split("[")[1].split("]")[0].split(","):
					files.append(job.replace("'","").replace(" ",""))	
		from modules.submitJobs import merge1DMVVTemplate
		merge1DMVVTemplate(jobList,files,"1D"+"_"+p,p,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ)		
		
		jobList = []
		files   = []
		with open("tmp2Dl1_%s_joblist.txt"%p,'r') as infile:
			for line in infile:
				if line.startswith("job"):
					for job in line.split("[")[1].split("]")[0].split(","):
						jobList.append(job.replace("'","").replace(" ",""))
			if line.startswith("file"):
				for job in line.split("[")[1].split("]")[0].split(","):
					files.append(job.replace("'","").replace(" ",""))	
		
		from modules.submitJobs import merge2DTemplate
		merge2DTemplate(jobList,files,"2Dl1"+"_"+p,p,"l1",binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ)
		merge2DTemplate(jobList,files,"2Dl2"+"_"+p,p,"l2",binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ)
			
def mergeBackgroundShapes(name,filename):

 for p in purities:
  inputx=filename+"_"+name+"_COND2D_"+p+"_l1.root"	
  inputy=filename+"_"+name+"_COND2D_"+p+"_l2.root"	
  inputz=filename+"_"+name+"_MVV_"+p+".root"      
  rootFile=filename+"_"+name+"_2D_"+p+".root"	 
  print "Reading " ,inputx
  print "Reading " ,inputy
  print "Reading " ,inputz
  print "Saving to ",rootFile    
  cmd='vvMergeHistosToPDF3D.py -i "{inputx}" -I "{inputy}" -z "{inputz}" -o "{rootFile}"'.format(rootFile=rootFile,inputx=inputx,inputy=inputy,inputz=inputz)
  os.system(cmd)

def makeNormalizations(name,filename,template,data=0,addCut='1',factor=1,jobName="nR"):
  pwd = os.getcwd()
  samples = pwd +"/samples"
  for p in purities:
   jobname = jobName+"_"+p
   rootFile=filename+"_"+name+"_"+p+".root"
   print "Saving to ",rootFile  
   cut='*'.join([cuts['common'],cuts[p],addCut,cuts['acceptance']])
   
   if submitToBatch:
           # template += ",QCD_Pt-,QCD_HT"
	   from modules.submitJobs import makeData,mergeData
	   jobList, files = makeData(template,cut,rootFile,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ,factor,name,data,jobname,samples,True)
	   mergeData(jobname,p,rootFile)
   else:
	   cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}"  -o "{rootFile}" -v "jj_l1_softDrop_mass,jj_l2_softDrop_mass,jj_LV_mass" -b "{bins},{bins},{BINS}" -m "{mini},{mini},{MINI}" -M "{maxi},{maxi},{MAXI}" -f {factor} -n "{name}"  samples'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV,bins=binsMJ,MINI=minMVV,MAXI=maxMVV,mini=minMJ,maxi=maxMJ,factor=factor,name=name,data=data)
	   os.system(cmd)
	

makeSignalShapesMVV("JJ_BulkGWW",BulkGravWWTemplate)
makeSignalShapesMJ("JJ_BulkGWW",BulkGravWWTemplate,'l1')
makeSignalShapesMJ("JJ_BulkGWW",BulkGravWWTemplate,'l2')
makeSignalYields("JJ_BulkGWW",BulkGravWWTemplate,BRWW,{'HPHP':0.99*0.99,'HPLP':0.99*1.03,'LPLP':1.03*1.03})
makeDetectorResponse("nonRes","JJ",nonResTemplate,cuts['nonres'])

# ------ do not use these ------
# makeBackgroundShapesMJKernel("nonRes","JJ",nonResTemplate,'l1',cuts['nonres'])
# makeBackgroundShapesMJKernel("nonRes","JJ",nonResTemplate,'l2',cuts['nonres'])
# makeBackgroundShapesMJSpline("nonRes","JJ",nonResTemplate,'l1',cuts['nonres'])
# makeBackgroundShapesMJSpline("nonRes","JJ",nonResTemplate,'l2',cuts['nonres'])
# ------------------------------

wait = True
if runParallel and submitToBatch:
	wait = False
	makeBackgroundShapesMVVKernel("nonRes","JJ",nonResTemplate,cuts['nonres'],"1D",wait)
	makeBackgroundShapesMVVConditional("nonRes","JJ",nonResTemplate,'l1',cuts['nonres'],"2Dl1",wait)
	makeBackgroundShapesMVVConditional("nonRes","JJ",nonResTemplate,'l2',cuts['nonres'],"2Dl2",wait)
	print "Exiting system! When all jobs are finished, please run mergeKernelJobs below"
	sys.exit()
	mergeKernelJobs()
elif submitToBatch and not runParallel:
	makeBackgroundShapesMVVKernel("nonRes","JJ",nonResTemplate,cuts['nonres'],"1D",wait)
	makeBackgroundShapesMVVConditional("nonRes","JJ",nonResTemplate,'l1',cuts['nonres'],"2Dl1",wait)
	makeBackgroundShapesMVVConditional("nonRes","JJ",nonResTemplate,'l2',cuts['nonres'],"2Dl2",wait)
elif not submitToBatch:
        #makeBackgroundShapesMJKernel("nonRes","JJ",nonResTemplate,'l1',cuts['nonres'])
        #makeBackgroundShapesMJKernel("nonRes","JJ",nonResTemplate,'l2',cuts['nonres'])
        makeBackgroundShapesMVVKernel("nonRes","JJ",nonResTemplate,cuts['nonres'],"1D",wait)
        makeBackgroundShapesMVVConditional("nonRes","JJ",nonResTemplate,'l1',cuts['nonres'],"2Dl1",wait)
        makeBackgroundShapesMVVConditional("nonRes","JJ",nonResTemplate,'l2',cuts['nonres'],"2Dl2",wait)

mergeBackgroundShapes("nonRes","JJ")
makeNormalizations("nonRes","JJ",nonResTemplate,0,cuts['nonres'],1.0,"nR")
# makeNormalizations("data","JJ",dataTemplate,1,'1',1.0,"normD") #run on data. Currently run on pseudodata only (below)
from modules.submitJobs import makePseudodata
for p in purities: makePseudodata("JJ_nonRes_%s.root"%p,p) #remove this when running on data!!
