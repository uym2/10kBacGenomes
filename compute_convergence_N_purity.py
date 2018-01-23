#! /usr/bin/env python

from sys import argv
from dendropy import Tree

annoFile = argv[1]  # ~/10kBacGenome/repophlan_microbes_ranks.txt
treefile = argv[2]

myTree = Tree.get_from_path(treefile,"newick")
nameHash = {}
global_phylCount = {}

with open(annoFile,'r') as f:
    for line in f:
        fields = line.split()
        name = fields[0]
        phylum = fields[2]
        nameHash[name] = phylum
        #global_phylCount[phylum] = 1 + (global_phylCount[phylum] if phylum in global_phylCount else 0)

# count the number of species in each phylum
for node in myTree.leaf_node_iter():
    phylum = nameHash[node.taxon.label]
    global_phylCount[phylum] = 1 + (global_phylCount[phylum] if phylum in global_phylCount else 0)
    


# label internal nodes
ID = 0
for node in myTree.preorder_node_iter():
    if not node.is_leaf():
        node.label = "I_" + str(ID)
        ID += 1

purity = {} # map each phylum to a tuple of (p,I), where p is the purity 
            # of the phylum and I is the ID of the LCA of that phylum
convergence = {} # map each phylum to a tuple of (c,I) where c in the convergence
            # of the phylum and I is the ID of the internal node with the highest convergence of that phylum

# main tasks
for node in myTree.postorder_node_iter():
    if node.is_leaf():
        if not ('Candi' in nameHash[node.taxon.label] or 'candi' in nameHash[node.taxon.label]):
            node.phylCount={ nameHash[node.taxon.label]:1 }
            node.nleaf = 1
        else:
            node.phylCount = {}
            node.nleaf = 0
    else:
        node.phylCount = {}
        node.nleaf = 0
        for c in node.child_node_iter():
            node.nleaf += c.nleaf
            for phylum in c.phylCount:
                node.phylCount[phylum] = c.phylCount[phylum] + (node.phylCount[phylum] if phylum in node.phylCount else 0)

    for phylum in node.phylCount:
        if phylum not in purity and node.phylCount[phylum] == global_phylCount[phylum]:
            purity[phylum] = (node.phylCount[phylum]/float(node.nleaf),node.label)
        for c in node.child_node_iter():
            for phylum in c.phylCount:
                if c.phylCount[phylum] == c.nleaf and node.phylCount[phylum] != node.nleaf:
                    if phylum not in convergence or c.phylCount[phylum] > convergence[phylum][0]:
                        convergence[phylum] = (c.phylCount[phylum]/float(global_phylCount[phylum]),c.label)


for phylum in global_phylCount:
     if global_phylCount[phylum] > 1 and not ('Candi' in phylum or 'candi' in phylum):
         print(phylum + " " + str(global_phylCount[phylum]) + " " + str(purity[phylum][0]) + " " + str(convergence[phylum][0]))
#    print(phylum,global_phylCount[phylum])

#print(global_phylCount['Firmicutes'])
#print(purity['Firmicutes'])

