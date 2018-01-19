#! /bin/bash

#infile=/oasis/projects/nsf/uot138/umai/10k_bac_genome_updated/GeneTrees_raxml/raxml.bestlikelihood.dat

wdir=$1
infile=$2
outfile=$3

while read line; do
    p=`echo $line | awk '{print $1;}'`; 
    q=`echo $line | awk '{print $2;}'`; 
    if [ "$q" == "ft" ]; then
        #cp $p/RAxML_result.$p.reduced.pt24FfDD $p/raxml.$p.bestllh.tre; 
        echo "nw_support $p/RAxML_result.$p.reduced.pt24FfDD $p/RAxML_rellBootstrap.$p.reduced.pt24FfDD > $p/raxml.$p.bestllh.tre"
    else 
        #cp $p/RAxML_result.$p.reduced.pt24FfDD.$q $p/raxml.$p.bestllh.tre; 
        echo "nw_support $p/RAxML_result.$p.reduced.pt24FfDD.$q $p/RAxML_rellBootstrap.$p.reduced.pt24FfDD.$q > $p/raxml.$p.bestllh.tre"
    fi
done < $infile
