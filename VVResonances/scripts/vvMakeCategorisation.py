#!/usr/bin/env python 
# make tree containing genweight, other event weights, as well as is jet H/ V jet, what category is the event classified in, what V/Htag has each jet -> for each signal sample!
#use this as input for the migrationUncertainties.py script
import ROOT
import os, sys, re, optparse,pickle,shutil,json,time
from collections import defaultdict
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
from array import array
ROOT.gROOT.ProcessLine("struct rootint { Int_t ri;};")
from ROOT import rootint
ROOT.gROOT.ProcessLine("struct rootfloat { Float_t rf;};")
from ROOT import rootfloat
ROOT.gROOT.ProcessLine("struct rootlong { Long_t li;};")
from ROOT import rootlong
ROOT.v5.TFormula.SetMaxima(10000)

from rootpy.tree import CharArrayCol
sys.path.insert(0, "../interactive/")
import cuts
# python categorisation.py -y "2016" -s WJetsToQQ -d deepAK8V2/
# python categorisation.py -y "2016,2017,2018" -s WJetsToQQ -d deepAK8V2/
# python categorisation.py -y "2016" -s BulkGravToWW -d deepAK8V2/

parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",default='2016',help="year of data taking")
parser.add_option("-s","--signal",dest="signal",help="signal to categorise",default='ZprimeToZh')
parser.add_option("-d","--directory",dest="directory",help="directory with signal samples",default='deepAK8V2/')

(options,args) = parser.parse_args()

def getSamplelist(directories,signal,minMX=1200.,maxMX=8000.):
    samples = {}
    dirs=directories.split(",")
    for directory in dirs:
        for filename in os.listdir(directory):
            if filename.find(signal)!=-1 and filename.find('root')!=-1:
                if filename.find("VBF")!=-1 and signal.find("VBF")==-1: continue  
                fnameParts=filename.split('.')
                fname=fnameParts[0]

                mass = float(fname.split('_')[-1])
                if mass < minMX or mass > maxMX: continue
                print fname 
                if fname not in samples:         
                    samples.update({fname : []}   )
                    samples[fname].append(directory+fname)
                else:
                    samples[fname].append(directory+fname)
                print 'found ',directory+fname,' mass',str(mass)


    complete_mass = {} #defaultdict(dict)
    for mass in samples.keys():
        print mass
        x = samples[mass]
        if len(x) < len(dirs):    
            print "!!!!    directories missing for mass", mass ," !!!!!!!! only ",x, "available "
        else:
            complete_mass.update({ mass: x})


    print " complete ",complete_mass

    return complete_mass



def getBkgSamplelist(directories,signal):
    samples = {}
    dirs=directories.split(",")
    for directory in dirs:
        for filename in os.listdir(directory):
            if filename.find(signal)!=-1 and filename.find('root')!=-1:
                if filename.find("VBF")!=-1 and signal.find("VBF")==-1: continue
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                fpart=fnameParts[0].split("_")[0]
                if fpart not in samples:
                    samples.update({fpart : []}   )
                    samples[fpart].append(directory+fname)
                else:
                    samples[fpart].append(directory+fname)
                print 'found ',directory+fname

    print "samples ",samples
    return samples




def selectSignalTree(cs,sample):
    print sample 
    chain = ROOT.TChain('AnalysisTree')
    tmpname = "/tmp/tmp_"+time.strftime("%Y%m%d-%H%M%S")
    outfile = ROOT.TFile(tmpname+'.root','RECREATE')
    for signal in sample:
        rfile = signal+".root"
        chain.Add(rfile)
        print " entries ",chain.GetEntries()
    bigtree = chain.CopyTree("1")

    finaltree = chain.CopyTree(cs['common']+'*'+cs['acceptance'])
    print "VBF "
    finaltreeVBF = chain.CopyTree(cs['common_VBF']+'*'+cs['acceptance'])
    signaltree_VBF_VH_HPHP = finaltreeVBF.CopyTree(cs['VH_HPHP'])
    signaltree_VBF_VV_HPHP = finaltreeVBF.CopyTree(cs['VV_HPHP'])#all other categories before are explicitly removed so that each event can only live in one category!!
    signaltree_VBF_VH_LPHP = finaltreeVBF.CopyTree(cs['VH_LPHP'])
    signaltree_VBF_VH_HPLP = finaltreeVBF.CopyTree(cs['VH_HPLP'])
    signaltree_VBF_VV_HPLP = finaltreeVBF.CopyTree(cs['VV_HPLP'])
    print " common_VV * acceptance ",cs['common_VV']+'*'+cs['acceptance']
    finaltreeVV = chain.CopyTree(cs['common_VV']+'*'+cs['acceptance'])
    print 'overall entries in tree '+str(chain.GetEntries())
    print 'entries after analysis selections '+str(finaltree.GetEntries())
    print "VH HPHP ",cs['VH_HPHP']
    signaltree_VH_HPHP = finaltreeVV.CopyTree(cs['VH_HPHP'])
    print "VV HPHP ",cs['VV_HPHP']
    signaltree_VV_HPHP = finaltreeVV.CopyTree(cs['VV_HPHP'])#all other categories before are explicitly removed so that each event can only live in one category!!
    signaltree_VH_LPHP = finaltreeVV.CopyTree(cs['VH_LPHP'])
    signaltree_VH_HPLP = finaltreeVV.CopyTree(cs['VH_HPLP'])
    signaltree_VV_HPLP = finaltreeVV.CopyTree(cs['VV_HPLP'])
    signaltree_VV_NPHP = finaltreeVV.CopyTree(cs['VV_NPHP_control_region'])
    #rest = finaltree.CopyTree('!('+cs['VV_HPLP']+')*!('+cs['VH_LPHP']+')*!('+cs['VH_HPLP']+')*!('+cs['VH_HPHP']+')*!('+cs['VV_HPHP']+')*!('+cs['VV_NPHP_control_region']+')')
    print ' #event VH_HPHP '+str(signaltree_VH_HPHP.GetEntries())+' #event VV_HPHP '+str(signaltree_VV_HPHP.GetEntries())+' #event VH_LPHP '+str(signaltree_VH_LPHP.GetEntries())+' #event VH_HPLP '+str(signaltree_VH_HPLP.GetEntries())+' #event VV_HPLP '+str(signaltree_VV_HPLP.GetEntries())
    print ' #event in control region',signaltree_VV_NPHP.GetEntries()
    #print '#event no category '+str(rest.GetEntries())
    sumcat = signaltree_VH_HPHP.GetEntries()+signaltree_VV_HPHP.GetEntries()+signaltree_VH_LPHP.GetEntries()+signaltree_VH_HPLP.GetEntries()+signaltree_VV_HPLP.GetEntries()
    print 'sum '+str(sumcat)
    print 'overall signal efficiency after selection cut '+str(finaltree.GetEntries()/float(chain.GetEntries()))
    print 'signal efficiency after category cuts '+str(sumcat/float(chain.GetEntries()))
    if finaltree.GetEntries() !=0 :
        print 'efficiency of all category cuts '+str(sumcat/float(finaltree.GetEntries()))
    else: 
        print ' no events left after preselection, presumably it is a low pt bin sample '
    signaltree_VBF_VH_HPHP.SetName('VBF_VH_HPHP')
    signaltree_VBF_VV_HPHP.SetName('VBF_VV_HPHP')
    signaltree_VBF_VH_LPHP.SetName('VBF_VH_LPHP')
    signaltree_VBF_VH_HPLP.SetName('VBF_VH_HPLP')
    signaltree_VBF_VV_HPLP.SetName('VBF_VV_HPLP')

    signaltree_VH_HPHP.SetName('VH_HPHP')
    signaltree_VV_HPHP.SetName('VV_HPHP')
    signaltree_VH_LPHP.SetName('VH_LPHP')
    signaltree_VH_HPLP.SetName('VH_HPLP')
    signaltree_VV_HPLP.SetName('VV_HPLP')
    signaltree_VV_NPHP.SetName('VV_NPHP')
    bigtree.SetName('all')
    finaltree.SetName('commonacceptance')
    signaltree_VBF_VH_HPHP.Write()
    signaltree_VBF_VV_HPHP.Write()
    signaltree_VBF_VH_LPHP.Write()
    signaltree_VBF_VH_HPLP.Write()
    signaltree_VBF_VV_HPLP.Write()

    signaltree_VH_HPHP.Write()
    signaltree_VV_HPHP.Write()
    signaltree_VH_LPHP.Write()
    signaltree_VH_HPLP.Write()
    signaltree_VV_HPLP.Write()
    signaltree_VV_NPHP.Write()
    finaltree.Write()
    bigtree.Write()
    outfile.Close()
    return tmpname


def calculateSFUnc(self,event,ctx,year,jet,SF,eff_vtag=[1,1],eff_htag=[1,1],mistag_top=[1,1],TTruth1=0,TTruth2=0,HTruth1=0,HTruth2=0,tag1="",tag2=""):

    VTruth = event.jj_l1_mergedVTruth
    HTruth = HTruth1
    ZbbTruth = event.jj_l1_mergedZbbTruth
    TTruth = TTruth1
    jetTag = tag1

    if jet == 2:
        VTruth = event.jj_l2_mergedVTruth
        HTruth = HTruth2
        ZbbTruth = event.jj_l2_mergedZbbTruth
        TTruth = TTruth2
        jetTag = tag2

    jetTruth = ""

    if TTruth == 1: jetTruth = "top"
    elif VTruth ==1 and TTruth == 0: jetTruth = "V"
    elif  HTruth ==1 or ZbbTruth ==1 : jetTruth = "H"    
    
    if (jetTruth=='H' or jetTruth=='V' ):

        if jetTag == 'HPHtag':            
            
            eff_htag[0] *= SF*(ctx.HPSF_htag[year]+ctx.H_tag_unc_HP[year])
            eff_htag[1] *= SF*(ctx.HPSF_htag[year]-ctx.H_tag_unc_HP[year])

        elif jetTag == 'LPHtag':            
            
            eff_htag[0] *= SF*(ctx.LPSF_htag[year]+ctx.H_tag_unc_LP[year])
            eff_htag[1] *= SF*(ctx.LPSF_htag[year]-ctx.H_tag_unc_LP[year])

        elif jetTag == 'HPVtag':            
            
            eff_vtag[0] *= SF*(ctx.HPSF_vtag[year]+ctx.W_tag_unc_HP[year])
            eff_vtag[1] *= SF*(ctx.HPSF_vtag[year]-ctx.W_tag_unc_HP[year])

        elif jetTag == 'LPVtag':            
            
            eff_vtag[0] *= SF*(ctx.LPSF_vtag[year]+ctx.W_tag_unc_LP[year])
            eff_vtag[1] *= SF*(ctx.LPSF_vtag[year]-ctx.W_tag_unc_LP[year])

        elif jetTag == 'NPVtag':	
	    
            eff_vtag[0] *= SF*(ctx.LPSF_vtag[year]+ctx.W_tag_unc_LP[year])
            eff_vtag[1] *= SF*(ctx.LPSF_vtag[year]-ctx.W_tag_unc_LP[year])

        else:
	
            eff_vtag[0] *=1.
            eff_vtag[1] *=1.
	    
    elif jetTruth=='top' :

        if jetTag == 'HPHtag':

            mistag_top[0] *= SF*(ctx.HPSF_toptag[year]+ctx.TOP_tag_unc_HP[year])
            mistag_top[1] *= SF*(ctx.HPSF_toptag[year]-ctx.TOP_tag_unc_HP[year])

        elif jetTag == 'LPHtag':

            mistag_top[0] *= SF*(ctx.LPSF_toptag[year]+ctx.TOP_tag_unc_LP[year])
            mistag_top[1] *= SF*(ctx.LPSF_toptag[year]-ctx.TOP_tag_unc_LP[year])	    
     
    return eff_vtag,eff_htag,mistag_top

def calculateSF(self,event,ctx,year,jet,TTruth1=0,TTruth2=0,HTruth1=0,HTruth2=0,tag1="",tag2=""):

    SF = 1.0
    SFW = 1.0
    SFH =1.0
    VTruth = event.jj_l1_mergedVTruth
    HTruth = HTruth1
    ZbbTruth = event.jj_l1_mergedZbbTruth
    TTruth = TTruth1
    jetTag = tag1
    pt = event.jj_l1_pt
    if jet == 2:
        VTruth = event.jj_l2_mergedVTruth
        HTruth = HTruth2
        ZbbTruth = event.jj_l2_mergedZbbTruth
        TTruth = TTruth2
        jetTag = tag2
        pt = event.jj_l2_pt
    jetTruth = ""

    if TTruth == 1: jetTruth = "top"
    elif VTruth ==1 and TTruth == 0: jetTruth = "V"
    elif  HTruth ==1 or ZbbTruth ==1 : jetTruth = "H"    
    
    if (jetTruth=='H' or jetTruth=='V' ):

        if jetTag == 'HPHtag': SF *= ctx.HPSF_htag[year]
        elif jetTag == 'LPHtag': SF *= ctx.LPSF_htag[year]
        elif jetTag == 'HPVtag': SF *= ctx.HPSF_vtag[year]
        elif jetTag == 'LPVtag': SF *= ctx.LPSF_vtag[year]
        elif jetTag == 'NPVtag': SF *= ctx.LPSF_vtag[year]
        else: SF*=1.

    elif jetTruth=='top' :
    
        if jetTag == 'HPHtag': SF *= ctx.HPSF_toptag[year]
        elif jetTag == 'LPHtag': SF *= ctx.LPSF_toptag[year]

    #pt dependent part
    # I calculate 2 additional SF to take into account the impact the tagger pt dependence separately for each tagger
    # if the jet is W tagged, the SF to take into account the pt dependence for the W gets modified while the one taking into account the H tagger gets the nominal value
    if (jetTruth=='H' or jetTruth=='V' ):
        if jetTag == 'HPHtag' or jetTag == 'LPHtag':
            SFH *= (ctx.Htag_intercept+ pt*ctx.Htag_slope)
            SFW *=SF
        elif jetTag == 'HPVtag' or jetTag == 'LPVtag':
            SFH *=SF
            SFW *= (ctx.Wtag_intercept+ pt*ctx.Wtag_slope)
        else:
            SFH *=SF
            SFW *=SF
    else:
        SFH *=SF
        SFW *=SF

    return SF,SFW,SFH

    
class myTree:
    
    run = rootint()
    lumi = rootint()
    puWeight  = rootfloat()
    genWeight = rootfloat()
    xsec      = rootfloat()
    evt       = rootlong()

    sf  = rootfloat()
    CMS_eff_vtag_sf_up = rootfloat()
    CMS_eff_vtag_sf_down = rootfloat()
    CMS_eff_htag_sf_up = rootfloat()
    CMS_eff_htag_sf_down = rootfloat()
    CMS_mistag_top_sf_up = rootfloat()
    CMS_mistag_top_sf_down = rootfloat()
    
    jj_l1_mergedVTruth           = rootint()
    jj_l2_mergedVTruth           = rootint()
    
    jj_l1_mergedHbbTruth           = rootint()
    jj_l2_mergedHbbTruth           = rootint()
    
    jj_l1_mergedHccTruth           = rootint()
    jj_l2_mergedHccTruth           = rootint()

    jj_l1_mergedHggTruth           = rootint()
    jj_l2_mergedHggTruth           = rootint()

    jj_l1_mergedHVV4qTruth           = rootint()
    jj_l2_mergedHVV4qTruth           = rootint()

    jj_l1_mergedHVVlepTruth           = rootint()
    jj_l2_mergedHVVlepTruth           = rootint()

    jj_l1_mergedTopTruth           = rootint()
    jj_l2_mergedTopTruth           = rootint()

    jj_l1_mergedZbbTruth           = rootint()
    jj_l2_mergedZbbTruth           = rootint()
    
    jj_l1_jetTag           = bytearray(6)
    jj_l2_jetTag           = bytearray(6)
    
    category               =  bytearray(7)
    newTree = None
    File = None

    #parameters for pt dependence
    Wsfpt = rootfloat()
    Hsfpt = rootfloat()
    jj_l1_pt = rootfloat()
    jj_l2_pt = rootfloat()
    
    def __init__(self, treename,outfile):
        self.File = outfile
        self.File.cd()
    #ROOT.gROOT.ProcessLine("struct string { TString s;};")
    #from ROOT import string
        self.newTree = ROOT.TTree(treename,treename)

        self.newTree.Branch("SF",self.sf,"SF/F")
        self.newTree.Branch("CMS_eff_vtag_sf_up",self.CMS_eff_vtag_sf_up,"CMS_eff_vtag_sf_up/F")
        self.newTree.Branch("CMS_eff_vtag_sf_down",self.CMS_eff_vtag_sf_down,"CMS_eff_vtag_sf_down/F")
        self.newTree.Branch("CMS_eff_htag_sf_up",self.CMS_eff_htag_sf_up,"CMS_eff_htag_sf_up/F")
        self.newTree.Branch("CMS_eff_htag_sf_down",self.CMS_eff_htag_sf_down,"CMS_eff_htag_sf_down/F")
        self.newTree.Branch("CMS_mistag_top_sf_up",self.CMS_mistag_top_sf_up,"CMS_mistag_top_sf_up/F")
        self.newTree.Branch("CMS_mistag_top_sf_down",self.CMS_mistag_top_sf_down,"CMS_mistag_top_sf_down/F")

        self.newTree.Branch("run",self.run,"run/i")
        self.newTree.Branch("lumi",self.lumi,"lumi/i")
        self.newTree.Branch("evt",self.evt,"evt/l")
        self.newTree.Branch("xsec",(self.xsec),"xsec/F")        
        self.newTree.Branch("puWeight",(self.puWeight),"puWeight/F")                 
        self.newTree.Branch("genWeight",(self.genWeight),"genWeight/F")
   
        self.newTree.Branch("jj_l1_mergedVTruth",self.jj_l1_mergedVTruth,"jj_l1_mergedVTruth/i")
        self.newTree.Branch("jj_l2_mergedVTruth",self.jj_l2_mergedVTruth,"jj_l2_mergedVTruth/i")
        self.newTree.Branch("jj_l1_mergedHbbTruth",self.jj_l1_mergedHbbTruth,"jj_l1_mergedHbbTruth/i")
        self.newTree.Branch("jj_l2_mergedHbbTruth",self.jj_l2_mergedHbbTruth,"jj_l2_mergedHbbTruth/i")
        self.newTree.Branch("jj_l1_mergedHccTruth",self.jj_l1_mergedHccTruth,"jj_l1_mergedHccTruth/i")
        self.newTree.Branch("jj_l2_mergedHccTruth",self.jj_l2_mergedHccTruth,"jj_l2_mergedHccTruth/i")
        self.newTree.Branch("jj_l1_mergedHggTruth",self.jj_l1_mergedHggTruth,"jj_l1_mergedHggTruth/i")
        self.newTree.Branch("jj_l2_mergedHggTruth",self.jj_l2_mergedHggTruth,"jj_l2_mergedHggTruth/i")
        self.newTree.Branch("jj_l1_mergedHVV4qTruth",self.jj_l1_mergedHVV4qTruth,"jj_l1_mergedHVV4qTruth/i")
        self.newTree.Branch("jj_l2_mergedHVV4qTruth",self.jj_l2_mergedHVV4qTruth,"jj_l2_mergedHVV4qTruth/i")
        self.newTree.Branch("jj_l1_mergedHVVlepTruth",self.jj_l1_mergedHVVlepTruth,"jj_l1_mergedHVVlepTruth/i")
        self.newTree.Branch("jj_l2_mergedHVVlepTruth",self.jj_l2_mergedHVVlepTruth,"jj_l2_mergedHVVlepTruth/i")
        self.newTree.Branch("jj_l1_mergedTopTruth",self.jj_l1_mergedTopTruth,"jj_l1_mergedTopTruth/i")
        self.newTree.Branch("jj_l2_mergedTopTruth",self.jj_l2_mergedTopTruth,"jj_l2_mergedTopTruth/i")
        self.newTree.Branch("jj_l1_mergedZbbTruth",self.jj_l1_mergedZbbTruth,"jj_l1_mergedZbbTruth/i")
        self.newTree.Branch("jj_l2_mergedZbbTruth",self.jj_l2_mergedZbbTruth,"jj_l2_mergedZbbTruth/i")
   
        self.newTree.Branch("jj_l1_jetTag",self.jj_l1_jetTag,"jj_l1_jetTag[6]/C")
        self.newTree.Branch("jj_l2_jetTag",self.jj_l2_jetTag,"jj_l2_jetTag[6]/C")
     
        self.newTree.Branch("category",self.category,"category[12]/C")

        #parameters for pt dependence
        self.newTree.Branch("Hsfpt",self.Hsfpt,"Hsfpt/F")
        self.newTree.Branch("Wsfpt",self.Wsfpt,"Wsfpt/F")
        self.newTree.Branch("jj_l1_pt",self.jj_l1_pt,"jj_l1_pt/F")
        self.newTree.Branch("jj_l2_pt",self.jj_l2_pt,"jj_l2_pt/F")


    def setOutputTreeBranchValues(self,cat,ctx,tmpname,year,LO):
        print " setOutputTreeBranchValues ",cat
        rf = ROOT.TFile(tmpname+'.root','READ')
        cattree = rf.Get(cat)
        print " cat "+cat+" "+str(cattree.GetEntries())


        ZHbb_branch_l1 = cattree.GetBranch(ctx.varl1Htag)
        ZHbb_leaf_l1 = ZHbb_branch_l1.GetLeaf(ctx.varl1Htag)	
        W_branch_l1 = cattree.GetBranch(ctx.varl1Wtag)
        W_leaf_l1 = W_branch_l1.GetLeaf(ctx.varl1Wtag)
        ZHbb_branch_l2 = cattree.GetBranch(ctx.varl2Htag)
        ZHbb_leaf_l2 = ZHbb_branch_l2.GetLeaf(ctx.varl2Htag)
        W_branch_l2 = cattree.GetBranch(ctx.varl2Wtag)
        W_leaf_l2 = W_branch_l2.GetLeaf(ctx.varl2Wtag)
        	
        WPHP_ZHbb_branch_l1 = cattree.GetBranch(ctx.WPHPl1Htag)
        WPHP_ZHbb_leaf_l1 = WPHP_ZHbb_branch_l1.GetLeaf(ctx.WPHPl1Htag)
        WPHP_W_branch_l1 = cattree.GetBranch(ctx.WPHPl1Wtag)
        WPHP_W_leaf_l1 = WPHP_W_branch_l1.GetLeaf(ctx.WPHPl1Wtag)
        
        WPHP_ZHbb_branch_l2 = cattree.GetBranch(ctx.WPHPl2Htag)
        WPHP_ZHbb_leaf_l2 = WPHP_ZHbb_branch_l2.GetLeaf(ctx.WPHPl2Htag)
        WPHP_W_branch_l2 = cattree.GetBranch(ctx.WPHPl2Wtag)
        WPHP_W_leaf_l2 = WPHP_W_branch_l2.GetLeaf(ctx.WPHPl2Wtag)
        
        
        WPLP_ZHbb_branch_l1 = cattree.GetBranch(ctx.WPLPl1Htag)
        WPLP_ZHbb_leaf_l1 = WPLP_ZHbb_branch_l1.GetLeaf(ctx.WPLPl1Htag)
        WPLP_W_branch_l1 = cattree.GetBranch(ctx.WPLPl1Wtag)
        WPLP_W_leaf_l1 = WPLP_W_branch_l1.GetLeaf(ctx.WPLPl1Wtag)
        
        WPLP_ZHbb_branch_l2 = cattree.GetBranch(ctx.WPLPl2Htag)
        WPLP_ZHbb_leaf_l2 = WPLP_ZHbb_branch_l2.GetLeaf(ctx.WPLPl2Htag)
        WPLP_W_branch_l2 = cattree.GetBranch(ctx.WPLPl2Wtag)
        WPLP_W_leaf_l2 = WPLP_W_branch_l2.GetLeaf(ctx.WPLPl2Wtag)


        WPNP_W_branch_l1 = cattree.GetBranch(ctx.WPNPl1Wtag)
        WPNP_W_leaf_l1 = WPNP_W_branch_l1.GetLeaf(ctx.WPNPl1Wtag)
        WPNP_W_branch_l2 = cattree.GetBranch(ctx.WPNPl2Wtag)
        WPNP_W_leaf_l2 = WPNP_W_branch_l2.GetLeaf(ctx.WPNPl2Wtag)


        noW=0
        oneW=0
        twoW=0
        notop=0
        onetop=0
        twotop=0
        Wintop=0
        Wnotintop=0
        twoWnotintop=0
	count = 0
	nEvents = cattree.GetEntries()
        for count,event in enumerate(cattree):
	    
	    if count%10000==0: print "Event",count,"/",nEvents
	    
            self.puWeight.rf       = event.puWeight 
            self.genWeight.rf      = event.genWeight
            if LO == True: self.genWeight.rf      = event.genWeight_LO
            self.xsec.rf           = event.xsec     
            self.evt.rl            = event.evt                  
            self.lumi.ri           = event.lumi
            self.run.ri = event.run 
            
            self.jj_l1_mergedVTruth.ri = event.jj_l1_mergedVTruth
            self.jj_l2_mergedVTruth.ri = event.jj_l2_mergedVTruth
            try:
                self.jj_l1_mergedHbbTruth.ri = event.jj_l1_mergedHTruth
                self.jj_l2_mergedHbbTruth.ri = event.jj_l2_mergedHTruth
                Hbb1=event.jj_l1_mergedHTruth
                Hbb2=event.jj_l2_mergedHTruth
            except:
                self.jj_l1_mergedHbbTruth.ri = 0
                self.jj_l2_mergedHbbTruth.ri = 0
                Hbb1=0
                Hbb2=0
            try:
                self.jj_l1_mergedHbbTruth.ri = event.jj_l1_mergedHbbTruth
                self.jj_l2_mergedHbbTruth.ri = event.jj_l2_mergedHbbTruth
                Hbb1=event.jj_l1_mergedHbbTruth
                Hbb2=event.jj_l2_mergedHbbTruth
            except:
                self.jj_l1_mergedHbbTruth.ri = 0
                self.jj_l2_mergedHbbTruth.ri = 0
                Hbb1=0
                Hbb2=0
            try:
                self.jj_l1_mergedHccTruth.ri = event.jj_l1_mergedHccTruth
                self.jj_l2_mergedHccTruth.ri = event.jj_l2_mergedHccTruth
                Hcc1=event.jj_l1_mergedHccTruth
                Hcc2=event.jj_l2_mergedHccTruth
            except:
                self.jj_l1_mergedHccTruth.ri = 0
                self.jj_l2_mergedHccTruth.ri = 0
                Hcc1=0
                Hcc2=0
            try:
                self.jj_l1_mergedHggTruth.ri = event.jj_l1_mergedHggTruth
                self.jj_l2_mergedHggTruth.ri = event.jj_l2_mergedHggTruth
                Hgg1=event.jj_l1_mergedHggTruth
                Hgg2=event.jj_l2_mergedHggTruth
            except:
                self.jj_l1_mergedHggTruth.ri = 0
                self.jj_l2_mergedHggTruth.ri = 0
                Hgg1=0
                Hgg2=0
            try:
                self.jj_l1_mergedHVV4qTruth.ri = event.jj_l1_mergedHVVTruth_4q
                self.jj_l2_mergedHVV4qTruth.ri = event.jj_l2_mergedHVVTruth_4q
                HVV4q1=event.jj_l1_mergedHVVTruth_4q
                HVV4q2=event.jj_l2_mergedHVVTruth_4q
            except:
                self.jj_l1_mergedHVV4qTruth.ri = 0
                self.jj_l2_mergedHVV4qTruth.ri = 0
                HVV4q1=0
                HVV4q2=0
            try:
                self.jj_l1_mergedHVVlepTruth.ri = event.jj_l1_mergedHVVTruth_lept
                self.jj_l2_mergedHVVlepTruth.ri = event.jj_l2_mergedHVVTruth_lept
                HVVlep1=event.jj_l1_mergedHVVTruth_lept
                HVVlep2=event.jj_l2_mergedHVVTruth_lept
            except:
                self.jj_l1_mergedHVVlepTruth.ri = 0
                self.jj_l2_mergedHVVlepTruth.ri = 0
                HVVlep1=0
                HVVlep2=0

            try:
                self.jj_l1_mergedTopTruth.ri = event.jj_l1_mergedTopTruth
                self.jj_l2_mergedTopTruth.ri = event.jj_l2_mergedTopTruth
                top1=event.jj_l1_mergedTopTruth
                top2=event.jj_l2_mergedTopTruth
            except:
                self.jj_l1_mergedTopTruth.ri = 0
                self.jj_l2_mergedTopTruth.ri = 0
                top1=0
                top2=0
            #print " event top ",event.jj_l1_mergedTopTruth,event.jj_l2_mergedTopTruth
            #print " self top ",self.jj_l1_mergedTopTruth.ri,self.jj_l2_mergedTopTruth.ri
            HTruth1 = 0
            HTruth2 = 0
            if self.jj_l1_mergedHbbTruth.ri == 1 or self.jj_l1_mergedHccTruth.ri == 1  or self.jj_l1_mergedHggTruth.ri == 1 or self.jj_l1_mergedHVV4qTruth.ri == 1 or self.jj_l1_mergedHVVlepTruth.ri ==1:
                HTruth1 = 1
            if self.jj_l2_mergedHbbTruth.ri == 1 or self.jj_l2_mergedHccTruth.ri == 1  or self.jj_l2_mergedHggTruth.ri == 1 or self.jj_l2_mergedHVV4qTruth.ri == 1 or self.jj_l2_mergedHVVlepTruth.ri ==1:
                HTruth2 = 1


            self.jj_l1_mergedZbbTruth.ri = event.jj_l1_mergedZbbTruth
            self.jj_l2_mergedZbbTruth.ri = event.jj_l2_mergedZbbTruth
            if cat !='all':
                self.category[:12] = cat
            else: self.category[:12] = "0"

            # this depends now on the actual cuts in the analysis!!
            if ZHbb_leaf_l1.GetValue() > WPHP_ZHbb_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'HPHtag'
            elif W_leaf_l1.GetValue() > WPHP_W_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'HPVtag'
            elif ZHbb_leaf_l1.GetValue() > WPLP_ZHbb_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'LPHtag'
            elif W_leaf_l1.GetValue() > WPLP_W_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'LPVtag'
            elif W_leaf_l1.GetValue() < WPNP_W_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'NPVtag'
            else:
                self.jj_l1_jetTag[:6] = 'Notag'
                
            if ZHbb_leaf_l2.GetValue() > WPHP_ZHbb_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'HPHtag'
            elif W_leaf_l2.GetValue() > WPHP_W_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'HPVtag'
            elif ZHbb_leaf_l2.GetValue() > WPLP_ZHbb_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'LPHtag'
            elif W_leaf_l2.GetValue() > WPLP_W_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'LPVtag'
            elif W_leaf_l2.GetValue() < WPNP_W_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'NPVtag'
            else:
                self.jj_l2_jetTag[:6] = 'Notag'

            tag1=self.jj_l1_jetTag[:6]
            tag2=self.jj_l2_jetTag[:6]
            CMS_eff_vtag_sf = [1.0,1.0] #for up and down variations
            CMS_eff_htag_sf = [1.0,1.0]
            CMS_mistag_top_sf = [1.0,1.0]
            jet = 1
            SF1,SFW1,SFH1 = calculateSF(self,event,ctx,year,jet,top1,top2,HTruth1,HTruth2,tag1,tag2)
            jet = 2
            SF2,SFW2,SFH2 = calculateSF(self,event,ctx,year,jet,top1,top2,HTruth1,HTruth2,tag1,tag2)
            SF = SF1*SF2
            #pt dependent part
            # I calculate 2 additional SF to take into account the impact the tagger pt dependence separately for each tagger
            # if the jet is W tagged, the SF to take into account the pt dependence for the W gets modified while the one taking into account the H tagger gets the nominal value
            Hsfpt= SFH1*SFH2
            Wsfpt= SFW1*SFW2
	    if (tag1.find('Htag') != tag2.find('Htag')) or (tag1.find('Vtag') != tag2.find('Vtag')):
	     jet = 1
             CMS_eff_vtag_sf,CMS_eff_htag_sf,CMS_mistag_top_sf = calculateSFUnc(self,event,ctx,year,jet,SF2,CMS_eff_vtag_sf,CMS_eff_htag_sf,CMS_mistag_top_sf,top1,top2,HTruth1,HTruth2,tag1,tag2)
	     jet = 2
             CMS_eff_vtag_sf,CMS_eff_htag_sf,CMS_mistag_top_sf = calculateSFUnc(self,event,ctx,year,jet,SF1,CMS_eff_vtag_sf,CMS_eff_htag_sf,CMS_mistag_top_sf,top1,top2,HTruth1,HTruth2,tag1,tag2)
	    else:
	     jet = 1
             CMS_eff_vtag_sf,CMS_eff_htag_sf,CMS_mistag_top_sf = calculateSFUnc(self,event,ctx,year,jet,1.0,CMS_eff_vtag_sf,CMS_eff_htag_sf,CMS_mistag_top_sf,top1,top2,HTruth1,HTruth2,tag1,tag2)
	     jet = 2
             CMS_eff_vtag_sf,CMS_eff_htag_sf,CMS_mistag_top_sf = calculateSFUnc(self,event,ctx,year,jet,1.0,CMS_eff_vtag_sf,CMS_eff_htag_sf,CMS_mistag_top_sf,top1,top2,HTruth1,HTruth2,tag1,tag2)
            if CMS_eff_htag_sf[0] == 1 and CMS_eff_htag_sf[1] == 1: CMS_eff_htag_sf = [SF,SF]
	    if CMS_eff_vtag_sf[0] == 1 and CMS_eff_vtag_sf[1] == 1: CMS_eff_vtag_sf = [SF,SF]
	    if CMS_mistag_top_sf[0] == 1 and CMS_mistag_top_sf[1] == 1: CMS_mistag_top_sf = [SF,SF]
            self.sf.rf = SF
            self.Wsfpt.rf = Wsfpt
            self.Hsfpt.rf = Hsfpt
            self.jj_l1_pt.rf = event.jj_l1_pt
            self.jj_l2_pt.rf = event.jj_l2_pt
            self.CMS_eff_vtag_sf_up.rf = CMS_eff_vtag_sf[0]
            self.CMS_eff_vtag_sf_down.rf = CMS_eff_vtag_sf[1]
            self.CMS_eff_htag_sf_up.rf = CMS_eff_htag_sf[0]
            self.CMS_eff_htag_sf_down.rf = CMS_eff_htag_sf[1]
            self.CMS_mistag_top_sf_up.rf = CMS_mistag_top_sf[0]
            self.CMS_mistag_top_sf_down.rf = CMS_mistag_top_sf[1]
            if event.jj_l1_mergedVTruth == 0 and event.jj_l2_mergedVTruth ==0 : noW=noW+1 
            if event.jj_l1_mergedVTruth == 1 and event.jj_l2_mergedVTruth ==1 : twoW=twoW+1
            if ( (event.jj_l1_mergedVTruth == 0 and event.jj_l2_mergedVTruth ==1) or  (event.jj_l1_mergedVTruth == 1 and event.jj_l2_mergedVTruth ==0)): oneW=oneW+1
            if ((event.jj_l1_mergedTopTruth ==0 and event.jj_l2_mergedTopTruth ==1) or (event.jj_l1_mergedTopTruth ==1 and event.jj_l2_mergedTopTruth ==0)): onetop=onetop+1
            if event.jj_l1_mergedTopTruth ==0 and event.jj_l2_mergedTopTruth ==0 : notop=notop+1
            if ((event.jj_l1_mergedVTruth == 1 and event.jj_l1_mergedTopTruth ==0) or  (event.jj_l2_mergedVTruth == 1 and event.jj_l2_mergedTopTruth ==0)): Wnotintop=Wnotintop+1
            if ((event.jj_l1_mergedVTruth == 1 and event.jj_l1_mergedTopTruth ==0) and  (event.jj_l2_mergedVTruth == 1 and event.jj_l2_mergedTopTruth ==0)): twoWnotintop=twoWnotintop+1
            if event.jj_l1_mergedTopTruth ==1 and event.jj_l2_mergedTopTruth ==1 : twotop=twotop+1
            if((event.jj_l1_mergedVTruth==0 and event.jj_l2_mergedVTruth ==1  and event.jj_l2_mergedTopTruth ==1 ) or  (event.jj_l1_mergedVTruth == 1  and event.jj_l1_mergedTopTruth ==1 and event.jj_l2_mergedVTruth ==0)): Wintop=Wintop+1
            self.newTree.Fill()
        #print 'number of events in this category '+str(self.newTree.GetEntries())
        print 'number of events without Ws in this category '+str(noW)
        print 'number of events without tops in this category '+str(notop)
        print 'number of events with 1 W in this category '+str(oneW)
        print 'number of Ws in top in this category '+str(Wintop)
        print 'number of event with 1 W not top in this category '+str(Wnotintop)
        print 'number of event with 2 Ws not top in this category '+str(twoWnotintop)
        print 'number of events with 1 top in this category '+str(onetop)
        print 'number of events with 2 Ws in this category '+str(twoW)
        print 'number of events with 2 tops in this category '+str(twotop)

    def test(self):
        for event in self.newTree:
            print event.jj_l1_mergedVTruth
            print event.jj_l1_mergedTopTruth
            print event.jj_l2_mergedTopTruth
    def write(self,name=""):
        self.File.cd()
        self.newTree.Write(name)

if __name__=='__main__':
    if options.directory.find(options.year)== -1: print 'ATTENTION: are you sure you are using the right directory for '+options.year+' data?'    
    period = options.year
    ctx  = cuts.cuts("init_VV_VH.json",period,"random_dijetbins",True)
    samples=""
    basedir=options.directory
    filePeriod=options.year

    if options.year.find(",")!=-1:
        period = options.year.split(',')
        filePeriod="Run2"

        for year in period:
            print year
            if year==period[-1]: samples+=basedir+"/"
            else: samples+=basedir+"/,"
    else: 
        samples=basedir+"/"
    outfile = ROOT.TFile('migrationunc/'+options.signal+'_'+filePeriod+'.root','RECREATE')

    samplelist= getBkgSamplelist(samples,options.signal)
    print " samplelist ", samplelist

    for sample in samplelist.keys():
        print sample
        print 'init new tree'
        outtree = myTree(sample,outfile)
        outtreeAll = myTree(sample,outfile)
        tmpfilename = selectSignalTree(ctx.cuts,samplelist[sample])
        print " tmpfilename ",tmpfilename
        LO = False
        if (filePeriod == "2017" or filePeriod == "2018") and (sample.find("QCD")==-1 or sample.find("Jets")==-1):  LO = True
        outtree.setOutputTreeBranchValues('VBF_VH_HPHP',ctx,tmpfilename,filePeriod,LO)
        outtree.setOutputTreeBranchValues('VBF_VV_HPHP',ctx,tmpfilename,filePeriod,LO)
        outtree.setOutputTreeBranchValues('VBF_VH_LPHP',ctx,tmpfilename,filePeriod,LO)
        outtree.setOutputTreeBranchValues('VBF_VH_HPLP',ctx,tmpfilename,filePeriod,LO)
        outtree.setOutputTreeBranchValues('VBF_VV_HPLP',ctx,tmpfilename,filePeriod,LO)

        outtree.setOutputTreeBranchValues('VH_HPHP',ctx,tmpfilename,filePeriod,LO)
        outtree.setOutputTreeBranchValues('VV_HPHP',ctx,tmpfilename,filePeriod,LO)
        outtree.setOutputTreeBranchValues('VH_LPHP',ctx,tmpfilename,filePeriod,LO)
        outtree.setOutputTreeBranchValues('VH_HPLP',ctx,tmpfilename,filePeriod,LO)
        outtree.setOutputTreeBranchValues('VV_HPLP',ctx,tmpfilename,filePeriod,LO)
        outtree.setOutputTreeBranchValues('VV_NPHP',ctx,tmpfilename,filePeriod,LO)
        outtree.write('signalregion')
        outtreeAll.setOutputTreeBranchValues('all',ctx,tmpfilename,filePeriod,LO)
        outfile.cd()
        outtreeAll.write('all')
        
        os.system("rm "+tmpfilename+".root")
        
