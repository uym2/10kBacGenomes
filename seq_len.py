#! /usr/bin/env python

from sys import argv

infile=argv[1]

with open(infile,'r') as f:
	count=-1
	for line in f:
		if line[0] == '>':
			if count >= 0:
				print(count)
			count=0
		count += len(line)-1
