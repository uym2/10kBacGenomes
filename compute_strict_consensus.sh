#! /bin/bash

trees=$1
name=$2
outdir=$3

raxmlHPC-PTHREADS -J STRICT -z $trees -n $name -m PROTCATLG -w $outdir
