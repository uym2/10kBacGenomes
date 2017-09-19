# !/bin/bash

infile=$1 # ALIGNED sequences
outfile=$2
maxgap=$3 # sequences with MORE than this proportion of GAPS will be masked (the LOWER the MORE aggressive)

ncol=`cat $infile | wc -L`

minresidue=$(echo 1-$maxgap | bc)
thres=`printf "%.0f" $(echo $ncol*$minresidue | bc)`

run_seqtools.py -infile $infile -outfile $outfile -filterfragments $thres

