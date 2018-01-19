#! /bin/bash

# compute quartet score between two trees using ASTRAL

tre1=$1
tre2=$2
output=$3

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
temp=`mktemp`

java -Xmx200m -jar $DIR/Astral/astral.5.5.5.jar -i $tre1 -q $tre2 -t 1 > $temp 2>&1
grep "normalized" $temp> $output

