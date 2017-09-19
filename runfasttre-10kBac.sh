#! /bin/bash

aln=$1
tre=$2
ncpu=$3

export OMP_NUM_THREADS=$ncpu

FastTreeMP $aln > $tre
