#!bin/bash

#indirW=MapsDeltaEta/
#outdirW=testMapW_fineBinning_Pt_2016-2017-2018/
indirZH=MapsDeltaEta/DDTMap_ZHbbvsQCD_scaled_2018_withDeltaEta_finerbinning/
outdirZH=MapsDeltaEta/DDTMap_ZHbbvsQCD_scaled_2018_withDeltaEta_finerbinning/
cuts=("0p02" "0p03" "0p05" "0p10" "0p15" "0p20" "0p30" "0p50")


for cat in ${cuts[*]}; do
    echo $cat
#    python changeMapName.py -c $cat -i ${indirW} -o ${outdirW}
    python changeMapName.py -c $cat -i ${indirZH} -o ${outdirZH} -t "ZH"



done


