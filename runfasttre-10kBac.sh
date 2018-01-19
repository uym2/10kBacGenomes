#! /bin/bash

aln=$1
tre=$2
ncpu=$3

export OMP_NUM_THREADS=$ncpu


# the lg model did not work for p0105 and p0278 on the first round
# and it did not work for p0019, p0254, and p0300 on the second round
#FastTreeMP -lg $aln > $tre
FastTreeMP $aln > $tre
