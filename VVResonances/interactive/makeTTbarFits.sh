#bin/bash!

## make pseudodata for ttbar only, change the category in the makeInputs before running it
#    python makeInputs.py -p 2016 --run "pseudoTT" 

#make the ws for ttbar only -> for the purpose of doing a ttbar only fit to get the true yields for the different ttbar contributions for the final fit 
# the workspaces need to be made with ttbar pseudodata from the ttbar-MC sample

#category=("VH_NPHP_control_region") # "VH_HPLP" "VH_LPHP" "VH_HPHP" "VV_HPLP" "VV_HPHP")
category=("VH_LPHP" "VH_HPLP" "VH_HPHP" "VV_HPLP" "VV_HPHP")

for c in ${category[@]}
do 

    outputdir=prefit_ttbar_2016/
    mkdir ${outputdir}

    echo "############## make prefit for ##############"
    label=prefit_ttbar_2016_${c}
    echo $label
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_BulkGWW_${c}_13TeV_2016_ttbar.root  -i  results_2016/JJ_2016_nonRes_${c}.root -M 2000  -o ${outputdir} --channel ${c} -l ${c} --doVjets --addTop | tee ${label}.log


    outputdir=postfit_ttbar_2016/
    mkdir ${outputdir}

    echo "############## make postfit for ##############"
    label=postfit_ttbar_2016_${c}
    echo $label
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n results_2016/workspace_JJ_BulkGWW_${c}_13TeV_2016_ttbar.root  -i  results_2016/JJ_2016_nonRes_${c}.root -M 2000  -o ${outputdir} --channel ${c} -l ${c} --doVjets --addTop --doFit | tee ${label}.log

done
  
## the fit produces output files named workspacename.json -> these are then included in the makeCard script to extract the yields if NOT pseudodata=ttbar
