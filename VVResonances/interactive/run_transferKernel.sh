#!/bin/bash

catIn=$1
catOut=$2
samples=(pythia herwig madgraph)
labels=("" _altshapeUp _altshape2)

#create the directory to store the results
mkdir postfit_qcd

#fit MC in catOut category with templates of catIn category
for i in ${!samples[*]}
do
	python transferKernel.py -i results_2016/JJ_2016_nonRes_${catOut}${labels[$i]}.root --sample ${samples[$i]} --year 2016 -p xyz --pdfIn results_2016/JJ_2016_nonRes_3D_${catIn}.root --channel ${catOut}
done

#merge post-fit 1Dx2Dx2D templates for catOut category
python transferKernel.py -i results_2016/JJ_2016_nonRes_${catOut}.root --year 2016 --pdfIn results_2016/JJ_2016_nonRes_3D_${catIn}.root --merge

#make post-fit validation plots for category catOut
for i in ${!samples[*]}
do
        python Projections3DHisto.py --mc results_2016/JJ_2016_nonRes_${catOut}${labels[$i]}.root,nonRes -k save_new_shapes_2016_${samples[$i]}_${catOut}_3D.root,histo -o control-plots-${catOut}-${samples[$i]}
        python Projections3DHisto_HPHP.py --mc results_2016/JJ_2016_nonRes_${catOut}${labels[$i]}.root,nonRes -k save_new_shapes_2016_${samples[$i]}_${catOut}_3D.root,histo -o control-plots-coarse-${catOut}-${samples[$i]}
done	
