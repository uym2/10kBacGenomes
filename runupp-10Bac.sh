#! /bin/bash

seqfile=$1
ncpu=$2

output=UPP.`basename $seqfile .faa`
t=0.66

{ time run_upp.py -s $seqfile -B 100000 -M -1 -T $t -o $output -m amino -x $ncpu > log.$output\.upp 2<&1; } 2> log.$output\.time
