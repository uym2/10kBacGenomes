#! /usr/bin/env python

from sys import argv

infile = argv[1]

mapping={}

with open(infile,'r') as f:
    for line in f:
        fields = line.split()
        if ( fields[0] not in mapping ) or ( mapping[fields[0]][1] < float(fields[2]) ):
            mapping[fields[0]] = (fields[1],float(fields[2]))

for key in mapping:
    print(key + " " + mapping[key][0] + " " + str(mapping[key][1]))


