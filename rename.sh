#! /bin/bash

mapfile=/oasis/projects/nsf/uot138/umai/10k_bac_genome/orgs2prots.txt
infile=$1
outfile=$2

while read line; do 
	x=`echo $line | head -c1`
	if [ "$x" == ">" ]; then 
		sname=`echo $line | tail -c+2 | awk '{print $1;}'`
		echo ">"`grep $sname $mapfile | awk '{print $1;}'`
	else
		echo $line
	fi
done < $infile > $outfile
