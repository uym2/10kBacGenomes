#! /usr/bin/env python

# restrict the taxonomy file to the subset of genomes in our tree
# each line in the ouput file has 3 fields
# Genome_ID GroupName GroupType
# For example, the following line in the original NCBI taxonomy file
# G001027285	Bacteria	Proteobacteria	Deltaproteobacteria	Myxococcales	Archangiaceae	Archangium	Archangium_gephyra
# will be transformed into 7 lines in the restructered file
# G001027285 Bacteria Kingdom
# G001027285 Proteobacteria Phylum
# G001027285 Deltaproteobacteria Class
# G001027285 Myxococcales Order
# G001027285 Archangiaceae Family
# G001027285 Archangium Genus
# G001027285 Archangium_gephyra Species


from sys import argv
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i","--input",required=True,help="Input file")
parser.add_argument("-o","--output",required=True,help="Output file")
parser.add_argument("-m","--mapping",required=False,help="Mapping file")
parser.add_argument("-d","--delim",required=False,help="Delimiter between the fields")

args = vars(parser.parse_args())

#from dendropy import Tree

taxonomyFile = args["input"]
#treefile = argv[2]
outputFile = args["output"]

# optional: to map the genome ID in one database to another, or to restrict the Genome set to a specific subset
mappingFile = args["mapping"] if args["mapping"] else None
delim = args["delim"] if args["delim"]  else "\t"

 
#myTree = Tree.get_from_path(treefile,'newick')
nameHash = {}

#for node in myTree.leaf_node_iter():
#    nameHash[node.taxon.label] = []

if mappingFile is not None:
    with open(mappingFile) as f:
        for line in f:
            fields = line.split()
            if len(fields) == 1:
                nameHash[fields[0]] = (fields[0],[])
            elif len(fields) > 1:
                nameHash[fields[0]] = (fields[1],[])

with open(taxonomyFile,'r') as fin:
    titles = fin.readline().rstrip().split(delim)
    print(titles)
    for line in fin:
        fields = line.rstrip().split(delim)
        if mappingFile is None:
            nameHash[fields[0]] = (fields[0],[])
        if fields[0] in nameHash:
            #print(nameHash[fields[0]])
            for i in range(1,len(fields)):
                if fields[i] != '':
                    nameHash[fields[0]][1].append((fields[i],titles[i]))

with open(outputFile,'w') as fout:
    for name in nameHash:
        for (f,t) in nameHash[name][1]:
            fout.write(nameHash[name][0] + " " + f + " " + t + "\n")
                
