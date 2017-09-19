# !/bin/bash

infile=$1 # aligned sequences
outfile=$2

#sitemask=0.9
sitemask=0.95
seqmask=0.66
#seqmask=0.66

temp=`mktemp`

#echo Masking sites with more than 90% gaps ...
echo Masking sites with more than 95% gaps ...
mask_sites.sh $infile $temp $sitemask

echo Masking sequences with more than 66% gaps ...
#echo Masking sequences with more than 80% gaps ...
mask_sequences.sh $temp $outfile $seqmask
