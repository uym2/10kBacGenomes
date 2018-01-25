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
from dendropy import Tree

taxonomyFile = argv[1]
treefile = argv[2]
outputFile = argv[3]

myTree = Tree.get_from_path(treefile,'newick')
nameHash = {}

for node in myTree.leaf_node_iter():
    nameHash[node.taxon.label] = []

with open(taxonomyFile,'r') as fin:
    titles = fin.readline().split()
    for line in fin:
        fields = line.split()
        if fields[0] in nameHash:
            for i in range(1,len(fields)):
                if fields[i] != '':
                    nameHash[fields[0]].append((fields[i],titles[i]))

with open(outputFile,'w') as fout:
    for name in nameHash:
        for (f,t) in nameHash[name]:
            fout.write(name + " " + f + " " + t + "\n")
                
