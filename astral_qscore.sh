#! /bin/bash

# compute quartet score between two trees using ASTRAL

tre1=$1
tre2=$2
output=$3

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#temp=`mktemp`
temp=$output

java -Xmx200m -jar $astral -i $tre1 -q $tre2 -t 1 > $temp 2>&1
#java -Xmx200m -jar ~/Packages_N_Libraries/astralGPU/astral.5.1.2.jar -C -i $tre1 -q $tre2 -t 1 > $temp 2>&1
#grep "normalized" $temp> $output

