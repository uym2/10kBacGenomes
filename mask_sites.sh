# !/bin/bash

infile=$1
outfile=$2
maxgap=$3 # sites with MORE than this proportion of GAPS will be masked (the LOWER the MORE agressive)

nrow=`grep ">" $infile | wc -l`

minresidue=$(echo 1-$maxgap | bc)
thres=`printf "%.0f" $(echo $nrow*$minresidue | bc)`

run_seqtools.py -infile $infile -outfile $outfile -masksites $thres

