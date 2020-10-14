#bin/bash!

category=("VH_HPLP" "VH_LPHP" "VH_HPHP" "VV_HPLP" "VV_HPHP")
for c in ${category[@]}
do 
    outputdir=postfit_data_blindSR_newC3_2016/
    mkdir ${outputdir}
#for c in ${category[@]}
#do
    echo "############## make postfit for ##############"
    label=postfit_data_blindSR_newC3_2016_${c}
    echo $label
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n results_2016/workspace_JJ_BulkGWW_VVVH_13TeV_2016_data_newC3.root  -i  results_2016/JJ_2016_nonRes_${c}.root -M 2000  -o ${outputdir} --channel ${c} -l ${c} --doVjets --addTop --doFit --blind -x 55,65,140,215 -y 55,65,140,215 | tee ${label}.log
  
done
  
## the fit produces output files named workspacename.json -> these are then included in the makeCard script to extract the yields if NOT pseudodata=ttbar
