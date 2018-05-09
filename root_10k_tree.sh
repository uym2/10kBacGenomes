#! /bin/bash

tree=$1

outgroup=`grep Archaea repophlan_microbes_ranks.txt | awk '{print $1;}'`

nw_reroot -s $tree $outgroup 
