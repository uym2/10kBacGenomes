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
nleaves = 0
for node in myTree.leaf_node_iter():
    phylum = nameHash[node.taxon.label]
    global_phylCount[phylum] = 1 + (global_phylCount[phylum] if phylum in global_phylCount else 0)
    nleaves += ('Candi' not in nameHash[node.taxon.label] and 'candi' not in nameHash[node.taxon.label])

# label internal nodes
ID = 0
for node in myTree.levelorder_node_iter():
    if not node.is_leaf():
        node.label = "I_" + str(ID)
        ID += 1

trpls = {}
quartets = {}
# main tasks
for phylum in global_phylCount:
    if ( global_phylCount[phylum] <= 1 or ('Candi' in phylum or 'candi' in phylum) ):
        continue

    trpls[phylum] = 0
    quartets[phylum] = 0

    for node in myTree.postorder_node_iter():
        if node.is_leaf():
            if not ('Candi' in nameHash[node.taxon.label] or 'candi' in nameHash[node.taxon.label]):
                node.phylCount = 0 + (nameHash[node.taxon.label] == phylum)
                node.nleaf = 1
            else:
                node.phylCount = 0
                node.nleaf = 0
        else:
            node.phylCount = 0
            node.nleaf = 0

            for c in node.child_node_iter():
                node.nleaf += c.nleaf
                node.phylCount += c.phylCount
                #for phylum in c.phylCount:
                #    node.phylCount[phylum] = c.phylCount[phylum] + (node.phylCount[phylum] if phylum in node.phylCount else 0)
            
            count_list = [ c.phylCount for c in node.child_node_iter()  ]
            NP = (nleaves - node.nleaf) - (global_phylCount[phylum] - node.phylCount)
            P = 0
            for i in range(len(count_list)-1):
                for j in range(i+1,len(count_list)):
                    P += count_list[i]*count_list[j]
            trpls[phylum] += NP*P
            quartets[phylum] += P*NP*(NP-1)/2

    for node in myTree.postorder_node_iter():
        if not node.is_leaf() and not node is myTree.seed_node:
            NP = node.nleaf - node.phylCount # non-phylum leaves of the "inside"
            P = 0
            count_list = [ s.phylCount for s in node.parent_node.child_node_iter() if s != node  ]
            count_list.append(global_phylCount[phylum] - node.parent_node.phylCount)
            for i in range(len(count_list)-1):
                for j in range(i+1,len(count_list)):
                    P += count_list[i]*count_list[j]
            quartets[phylum] += P*NP*(NP-1)/2

for phylum in trpls:
     np = nleaves - global_phylCount[phylum]
     p = global_phylCount[phylum]
     ntrpls = np*p*(p-1)/2
     nquartets = np*(np-1)*p*(p-1)/4
     trpls[phylum] /= (float(ntrpls))
     quartets[phylum] /= (float(nquartets))
     print(phylum + " " + str(global_phylCount[phylum]) + " " + str(trpls[phylum]) + " " + str(quartets[phylum]) )
#    print(phylum,global_phylCount[phylum])

#print(global_phylCount['Firmicutes'])
#print(purity['Firmicutes'])

