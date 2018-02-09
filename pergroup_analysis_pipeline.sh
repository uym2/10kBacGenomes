#! /bin/bash

treefile=$1 # input
taxonomyfile=$2
datafile=$3 # output
tripfile=$4 # output
qurtfile=$5 # output

pergroup_stats.py $taxonomyfile $treefile $datafile

Rscript ~/my_gits/10kBacGenomes/TaxGroupScore.R $datafile $tripfile $qurtfile 
