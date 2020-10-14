
# class to initialize all analysis cuts
# init_ VV_VH.json contains all analysis cuts! -> need category import this file
import json
import ast

class cuts():
    lumi = 1.
    lumi_unc = 1.
    yeartag = "16"
    HPSF_vtag = 1.                                
    LPSF_vtag = 1.                                
    HPSF_htag = 1.                                
    LPSF_htag = 1.                                
                                                  
    W_LPmassscale = 1.                                
    W_HPmassscale = 1.
                  
    H_LPmassscale = 1.
    H_HPmassscale = 1.
                                                  
    minMJ = 0.                                    
    maxMJ = 0.                                    
    binsMJ = 0.                                   
  
    minMVV = 0.0
    maxMVV = 0.0
    binsMVV = 0.
    
    minMX = 0.
    maxMX = 0.
    
    minGenMJ = 1.
    maxGenMJ = 1.
    minGenMVV = 1.
    maxGenMVV = 1.

    HCALbinsMVV  = ""#" --binsMVV "
    HCALbinsMVVSignal= ""# 
    
    fixParsSig = {}
    fixParsSigMVV ={}
    catVtag = {}
    catHtag = {}
    
    varl1Wtag = ""
    varl1Htag = ""
    
    WPHPl1Wtag = ""
    WPLPl1Wtag = ""
    WPNPl1Wtag = ""
    WPNPLPl1Wtag = ""

    WPHPl1Htag = ""
    WPLPl1Htag = ""
    WPNPl1Htag = ""
    WPNPl1Htag = ""
    WPNPLPl1Htag = ""
    
    varl2Wtag = ""
    varl2Htag = ""
    
    WPHPl2Wtag = ""
    WPLPl2Wtag = ""
    WPNPl2Wtag = ""
    WPNPLPl2Wtag = ""
    
    WPHPl2Htag = ""
    WPLPl2Htag = ""
    WPNPl2Htag = ""
    WPNPLPl2Htag = ""

    W_tag_unc_HP= 1.
    W_tag_unc_LP= 1.
    H_tag_unc_HP= 1.
    H_tag_unc_LP= 1.
    
    vtag_pt_dependence ={}
    
    cuts={}
    
    
    def __init__(self,jsonfile,year,options,widerMVV=False):
        
        with open(jsonfile) as json_file:
                     
            
            data = json.load(json_file)
            ##### load binning and cut offs
            self.minMJ = data["ranges_and_binning"]["minMJ"]
            self.maxMJ = data["ranges_and_binning"]["maxMJ"]
            self.binsMJ = data["ranges_and_binning"]["binsMJ"]
            
            self.minMVV = data["ranges_and_binning"]["minMVV"]
            self.maxMVV = data["ranges_and_binning"]["maxMVV"]
            self.binsMVV = data["ranges_and_binning"]["binsMVV"]
            
            self.minGenMJ = data["ranges_and_binning"]["minGenMJ"]
            self.maxGenMJ = data["ranges_and_binning"]["maxGenMJ"]
            self.minGenMVV = data["ranges_and_binning"]["minGenMVV"]
            self.maxGenMVV = data["ranges_and_binning"]["maxGenMVV"]
            
            self.minMX = data["ranges_and_binning"]["minMX"]
            self.maxMX = data["ranges_and_binning"]["maxMX"]
            if widerMVV==True:
                self.maxMVV = data["ranges_and_binning"]["widerMVV_maxMVV"]
                self.maxGenMVV = data["ranges_and_binning"]["widerMVV_maxGenMVV"]
            
            ## load SF for the different years 
            if year==2016:
                self.yeartag = "16"
            elif year==2017:
                self.yeartag = "17"
            elif year==2018:
                self.yeartag = "18"
                print " attention  lumi to be checked #to be checked! https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2018Analysis"
            else: print "no such data taking year -> running with default values on 2016 data"
           
         
         
            self.W_tag_unc_HP= data["W_tag_unc_HP"][str(year)]
            self.W_tag_unc_LP= data["W_tag_unc_LP"][str(year)]
            self.H_tag_unc_HP= data["H_tag_unc_HP"][str(year)]
            self.H_tag_unc_LP= data["H_tag_unc_LP"][str(year)]
            
            self.varl1Wtag = data["tagging_variables_and_wp"]["varl1Wtag"]
            self.varl1Htag = data["tagging_variables_and_wp"]["varl1Htag"]
            self.WPHPl1Wtag = data["tagging_variables_and_wp"]["l1Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_HP_Wtag"+self.yeartag])
            self.WPLPl1Wtag = data["tagging_variables_and_wp"]["l1Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_LP_Wtag"+self.yeartag])
            self.WPNPl1Wtag = data["tagging_variables_and_wp"]["l1Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_NP_Wtag"+self.yeartag])
            self.WPNPLPl1Wtag = data["tagging_variables_and_wp"]["l1Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_NPLP_Wtag"+self.yeartag])
            self.WPHPl1Htag = data["tagging_variables_and_wp"]["l1Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_HP_Htag"+self.yeartag])
            self.WPLPl1Htag = data["tagging_variables_and_wp"]["l1Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_LP_Htag"+self.yeartag])
            self.WPNPl1Htag = data["tagging_variables_and_wp"]["l1Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_NP_Htag"+self.yeartag])
            self.WPNPLPl1Htag = data["tagging_variables_and_wp"]["l1Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_NPLP_Htag"+self.yeartag])
   
            self.varl2Wtag = data["tagging_variables_and_wp"]["varl2Wtag"]
            self.varl2Htag = data["tagging_variables_and_wp"]["varl2Htag"]
            self.WPHPl2Wtag = data["tagging_variables_and_wp"]["l2Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_HP_Wtag"+self.yeartag])
            self.WPLPl2Wtag = data["tagging_variables_and_wp"]["l2Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_LP_Wtag"+self.yeartag])
            self.WPNPl2Wtag = data["tagging_variables_and_wp"]["l2Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_NP_Wtag"+self.yeartag])
            self.WPNPLPl2Wtag = data["tagging_variables_and_wp"]["l2Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_NPLP_Wtag"+self.yeartag])
            self.WPHPl2Htag = data["tagging_variables_and_wp"]["l2Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_HP_Htag"+self.yeartag])
            self.WPLPl2Htag = data["tagging_variables_and_wp"]["l2Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_LP_Htag"+self.yeartag])
            self.WPNPl2Htag = data["tagging_variables_and_wp"]["l2Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_NP_Htag"+self.yeartag])
            self.WPNPLPl2Htag = data["tagging_variables_and_wp"]["l2Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_NPLP_Htag"+self.yeartag])
            
            self.lumi = data["lumi"+self.yeartag]
            self.lumi_unc = data["unc_lumi"+self.yeartag]
            
        
            self.W_LPmassscale = data["W_HPmassscale"+self.yeartag]
            self.W_HPmassscale = data["W_LPmassscale"+self.yeartag]
                          
            self.H_LPmassscale = data["H_HPmassscale"+self.yeartag]
            self.H_HPmassscale = data["H_LPmassscale"+self.yeartag]

            self.fixParsSigMVV = data["fixParsSigMVV"]
            self.fixParsSig = data["fixParsSig"]
            self.HPSF_vtag = data['HPSF'+self.yeartag]
            self.LPSF_vtag = data['LPSF'+self.yeartag]
            self.HPSF_htag = data['htagHPSF'+self.yeartag]
            self.LPSF_htag = data['htagLPSF'+self.yeartag]
            self.vtag_pt_dependence = data["vtag_pt_dependence"+self.yeartag]
            
            self.catVtag['HP1'] =  '('+ self.varl1Wtag +'>'+ self.WPHPl1Wtag +')'
            self.catVtag['HP2'] =  '('+ self.varl2Wtag +'>'+ self.WPHPl2Wtag +')'
            self.catVtag['LP1'] = '(('+ self.varl1Wtag +'<'+ self.WPHPl1Wtag +')&&('+ self.varl1Wtag +'>'+ self.WPLPl1Wtag +'))' 
            self.catVtag['LP2'] = '(('+ self.varl2Wtag +'<'+ self.WPHPl2Wtag +')&&('+ self.varl2Wtag +'>'+ self.WPLPl2Wtag +'))'
            self.catVtag['NP1'] = '(('+ self.varl1Wtag +'<'+ self.WPNPl1Wtag +')&&('+ self.varl1Wtag +'>'+ self.WPNPLPl1Wtag +'))'
            self.catVtag['NP2'] = '(('+ self.varl2Wtag +'<'+ self.WPNPl2Wtag +')&&('+ self.varl2Wtag +'>'+ self.WPNPLPl2Wtag +'))'


            self.catHtag['HP1'] =  '('+ self.varl1Htag +'>'+ self.WPHPl1Htag +')' 
            self.catHtag['HP2'] =  '('+ self.varl2Htag +'>'+ self.WPHPl2Htag +')' 
            self.catHtag['LP1'] = '(('+ self.varl1Htag +'<'+ self.WPHPl1Htag +')&&('+ self.varl1Htag +'>'+ self.WPLPl1Htag +'))' 
            self.catHtag['LP2'] = '(('+ self.varl2Htag +'<'+ self.WPHPl2Htag +')&&('+ self.varl2Htag +'>'+ self.WPLPl2Htag +'))'
            self.catHtag['NP1'] = '(('+ self.varl1Htag +'<'+ self.WPNPl1Htag +')&&('+ self.varl1Htag +'>'+ self.WPNPLPl1Htag +'))'
            self.catHtag['NP2'] = '(('+ self.varl2Htag +'<'+ self.WPNPl2Htag +')&&('+ self.varl2Htag +'>'+ self.WPNPLPl2Htag +'))'
            
            selections = ["common","common_VV","common_VBF","NP","res","nonres","resTT","resTT_W","nonresTT","resTnonresT","resWnonresT","resTresW","acceptance","acceptanceMJ","acceptanceMVV","acceptanceGEN","looseacceptanceMJ"]
            for sel in selections:
                self.cuts[sel] = data["selection_cuts"][sel]
                self.cuts[sel] = self.cuts[sel].replace("minMJ",str(self.minMJ))
                self.cuts[sel] = self.cuts[sel].replace("maxMJ",str(self.maxMJ))
                self.cuts[sel] = self.cuts[sel].replace("minMVV",str(self.minMVV))
                self.cuts[sel] = self.cuts[sel].replace("maxMVV",str(self.maxMVV))
                
                self.cuts[sel] = self.cuts[sel].replace("minGenMJ",str(self.minGenMJ))
                self.cuts[sel] = self.cuts[sel].replace("maxGenMJ",str(self.maxGenMJ))
                self.cuts[sel] = self.cuts[sel].replace("minGenMVV",str(self.minGenMVV))
                self.cuts[sel] = self.cuts[sel].replace("maxGenMVV",str(self.maxGenMVV))
            if options.find('dijetbins')!=-1:
                print "use dijet binning! "
                alldijetbins =  data["ranges_and_binning"]["dijetbins"]
                dijetbins = []
                for b in alldijetbins:
                    if b > self.maxMVV: continue
                    if b < self.minMVV: continue
                    dijetbins.append(b)
                
                self.HCALbinsMVV = " --binsMVV " 
                self.HCALbinsMVV += ','.join(str(e) for e in dijetbins)

                self.minMVV = float(dijetbins[0])
                self.maxMVV = float(dijetbins[-1])
                self.binsMVV= len(dijetbins)-1
                
                dijetbins = []
                for b in alldijetbins:
                    if b > self.maxMX: continue
                    if b < self.minMX: continue
                    dijetbins.append(b)
                
                self.HCALbinsMVVSignal = " --binsMVV "
                self.HCALbinsMVVSignal += ','.join(str(e) for e in dijetbins)
            else:
                self.HCALbinsMVV=""
                self.HCALbinsMVVSignal=""
            if options.find('random')!=-1:
                print "Use random sorting!"
                print "ortoghonal VV + VH"
                catsAll = {}
                #scheme 2: improves VV HPHP (VH_HPHP -> VV_HPHP -> VH_LPHP,VH_HPLP -> VV_HPLP) 
                #at least one H tag HP (+ one V/H tag HP)                                                                                                                                                                                                                                     
                catsAll['VH_HPHP'] = '('+'&&'.join([self.catVtag['HP1'],self.catHtag['HP2']])+')'
                catsAll['HV_HPHP'] = '('+'&&'.join([self.catHtag['HP1'],self.catVtag['HP2']])+')'
                catsAll['HH_HPHP'] = '('+'&&'.join([self.catHtag['HP1'],self.catHtag['HP2']])+')'
                self.cuts['VH_HPHP'] = '('+'||'.join([catsAll['VH_HPHP'],catsAll['HV_HPHP'],catsAll['HH_HPHP']])+')'

                # two V tag HP                                                                                                                                                                                                                                                                
                self.cuts['VV_HPHP'] = '('+'!'+self.cuts['VH_HPHP']+'&&'+'(' +  '&&'.join([self.catVtag['HP1'],self.catVtag['HP2']]) + ')' + ')'

                #at least one H-tag HP (+one V OR H-tag LP)                                                                                                                                                                                                                                   
                catsAll['VH_LPHP'] = '('+'&&'.join([self.catVtag['LP1'],self.catHtag['HP2']])+')'
                catsAll['HV_HPLP'] = '('+'&&'.join([self.catHtag['HP1'],self.catVtag['LP2']])+')'
                catsAll['HH_HPLP'] = '('+'&&'.join([self.catHtag['HP1'],self.catHtag['LP2']])+')'
                catsAll['HH_LPHP'] = '('+'&&'.join([self.catHtag['LP1'],self.catHtag['HP2']])+')'
                self.cuts['VH_LPHP'] = '('+'('+'!'+self.cuts['VH_HPHP']+'&&!'+self.cuts['VV_HPHP']+')&&('+'||'.join([catsAll['VH_LPHP'],catsAll['HV_HPLP'],catsAll['HH_HPLP'],catsAll['HH_LPHP']])+')'+')'

                #at least one V-tag HP (+ one H-tag LP)                                  
                catsAll['VH_HPLP'] = '('+'&&'.join([self.catVtag['HP1'],self.catHtag['LP2']])+')'
                catsAll['HV_LPHP'] = '('+'&&'.join([self.catHtag['LP1'],self.catVtag['HP2']])+')'
                self.cuts['VH_HPLP'] = '('+'('+'!'+self.cuts['VH_LPHP']+'&&!'+self.cuts['VH_HPHP']+'&&!'+self.cuts['VV_HPHP']+')&&('+'||'.join([catsAll['VH_HPLP'],catsAll['HV_LPHP']])+')'+')'

                self.cuts['VH_all'] =  '('+  '||'.join([self.cuts['VH_HPHP'],self.cuts['VH_LPHP'],self.cuts['VH_HPLP']]) + ')'                

                self.cuts['VV_HPLP'] = '(' +'('+'!'+self.cuts['VH_all']+') &&' + '(' + '('+  '&&'.join([self.catVtag['HP1'],self.catVtag['LP2']]) + ')' + '||' + '(' + '&&'.join([self.catVtag['HP2'],self.catVtag['LP1']]) + ')' + ')' + ')'

                self.cuts['VV_all'] = '('+  '||'.join([self.cuts['VV_HPHP'],self.cuts['VV_HPLP']]) + ')'
                self.cuts['VV_VH']= '('+  '||'.join([self.cuts['VH_all'],self.cuts['VV_all']]) + ')'

                '''
                #control region (invert w-tag)
                catsAll['VH_NPHP'] = '('+'&&'.join([self.catVtag['NP1'],self.catHtag['HP2']])+')'
                catsAll['HV_HPNP'] = '('+'&&'.join([self.catHtag['HP1'],self.catVtag['NP2']])+')'
                # I am excluding only the VH categories because it is already othogonal to VV and TTree.Draw doesn't like "overlapping" conditions
                self.cuts['VH_NPHP_control_region'] = '('+'('+'||'.join([catsAll['VH_NPHP'],catsAll['HV_HPNP']])+')'+'&&'+'('+'!'+self.cuts['VH_all']+')'+')'

                #control region (invert h-tag)
                catsAll['VH_HPNP'] = '('+'&&'.join([self.catVtag['HP1'],self.catHtag['NP2']])+')'
                catsAll['HV_NPHP'] = '('+'&&'.join([self.catHtag['NP1'],self.catVtag['HP2']])+')'
                self.cuts['VH_HPNP_control_region'] = '('+'('+'||'.join([catsAll['VH_HPNP'],catsAll['HV_NPHP']])+')'+'&&'+'('+'!'+'('+ '||'.join([self.cuts['VV_all'],self.cuts['VH_NPHP_control_region']]) +')'+')'+')'
                '''
                #only one CR inverting H-tag
                catsAll['VH_HPNP'] = '('+'&&'.join([self.catVtag['HP1'],self.catHtag['NP2']])+')'
                catsAll['HV_NPHP'] = '('+'&&'.join([self.catHtag['NP1'],self.catVtag['HP2']])+')'
                self.cuts['VH_HPNP_control_region'] = '('+'('+'||'.join([catsAll['VH_HPNP'],catsAll['HV_NPHP']])+')'+'&&'+'('+'!'+self.cuts['VV_all']+')'+')'
            else:
                print "Use b-tagging sorting"
                self.cuts['VH_HPHP'] = '('+  '&&'.join([self.catHtag['HP1'],self.catVtag['HP2']]) + ')'
                self.cuts['VH_HPLP'] = '('+  '&&'.join([self.catHtag['HP1'],self.catVtag['LP2']]) + ')'
                self.cuts['VH_LPHP'] = '('+  '&&'.join([self.catHtag['LP1'],self.catVtag['HP2']]) + ')'
                self.cuts['VH_LPLP'] = '('+  '&&'.join([self.catHtag['LP1'],self.catVtag['LP2']]) + ')'
                self.cuts['VH_all'] =  '('+  '||'.join([self.cuts['VH_HPHP'],self.cuts['VH_HPLP'],self.cuts['VH_LPHP'],self.cuts['VH_LPLP']]) + ')'
                self.cuts['VV_HPHP'] = '(' + '!' + self.cuts['VH_all'] + '&&' + '(' + '&&'.join([self.catVtag['HP1'],self.catVtag['HP2']]) + ')' + ')'
                self.cuts['VV_HPLP'] = '(' + '!' + self.cuts['VH_all'] + '&&' + '(' + '('+  '&&'.join([self.catVtag['HP1'],self.catVtag['LP2']]) + ')' + '||' + '(' + '&&'.join([self.catVtag['HP2'],self.catVtag['LP1']]) + ')' + ')' + ')'



if __name__ == "__main__":
    c = cuts("init_VV_VH.json",2016,"dijetbins_random")
    #print c.HPSF_vtag
    #print c.LPSF_vtag
    #print c.minMJ
    #print c.catVtag['LP1']
    
    #print c.catHtag['LP1']
    #print c.maxMX
    #print c.HCALbinsMVV 
    #print c.HCALbinsMVVSignal 
    
    #print c.cuts["VV_HPHP"]
    
    #selections = ["common","common_VV","common_VBF","NP","res","nonres","resTT","acceptance","acceptanceMJ","acceptanceMVV","acceptanceGEN","looseacceptanceMJ"]
    
    #for sel in selections:
        #print c. cuts[sel]
    
    
    #print c.fixParsSig["ZprimeWW"]['NP']

    #print c.minMX
    print c.binsMVV
    print c.HCALbinsMVV
    
    for k in c.catVtag.keys():
        print k,  c.catVtag[k]
        print k, c.catHtag[k]
