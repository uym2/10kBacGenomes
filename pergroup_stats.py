#! /usr/bin/env python

from sys import argv
from dendropy import Tree

annoFile = argv[1]  # ~/10kBacGenome/repophlan_microbes_ranks.txt
treefile = argv[2]

myTree = Tree.get_from_path(treefile,"newick")
nameHash = {}
global_phylCount = {}

def preprocess(tree):
    for node in tree.postorder_node_iter():
        if node.is_leaf():
            node.nleaf = 1
        else:
            node.nleaf = 0
            for c in node.child_node_iter():
                node.nleaf += c.nleaf

def computeTripletScore(tree,groupName,groupSize,nameHash):
    trpls = 0
    for node in tree.postorder_node_iter():
        if node.is_leaf():
            node.count = 0 + (nameHash[node.taxon.label] == groupName)
        else:
            node.count = 0

            for c in node.child_node_iter():
                node.count += c.count
            
            count_list = [ c.count for c in node.child_node_iter()  ]
            NP = (tree.seed_node.nleaf - node.nleaf) - (groupSize - node.count)
            P = 0
            for i in range(len(count_list)-1):
                for j in range(i+1,len(count_list)):
                    P += count_list[i]*count_list[j]
            trpls += NP*P
            if node.count >= groupSize:
                break
    return trpls

def computeQuartetScore(tree,groupName,groupSize,nameHash):
    quartets = 0
    newSeed = tree.seed_node
    for node in tree.postorder_node_iter():
        if node.is_leaf():
            node.count = 0 + (nameHash[node.taxon.label] == groupName)
        else:
            node.count = 0

            for c in node.child_node_iter():
                node.count += c.count
            
            count_list = [ c.count for c in node.child_node_iter()  ]
            NP = (tree.seed_node.nleaf - node.nleaf) - (groupSize - node.count)
            P = 0
            for i in range(len(count_list)-1):
                for j in range(i+1,len(count_list)):
                    P += count_list[i]*count_list[j]
            quartets += P*NP*(NP-1)/2
            
            if node.count >= groupSize: # break early when we found the LCA. This causes some complications later on, though
                newSeed = node
                break

    # UGLY SOLUTION! 
    # Dendropy seems to remove the node from the old tree when we make it the seed node of a new tree
    # therefore, I have to manually add the node back after finishing the job on the subtree
    parentNode = newSeed.parent_node
    subTree = Tree(seed_node=newSeed)

    for node in subTree.postorder_node_iter():
        if not node.is_leaf() and not node is subTree.seed_node:
            
            NP = node.nleaf - node.count # non-phylum leaves of the "inside"
            P = 0
            count_list = [ s.count for s in node.parent_node.child_node_iter() if s != node ]
            count_list.append(groupSize - node.parent_node.count)

            for i in range(len(count_list)-1):
                for j in range(i+1,len(count_list)):
                    P += count_list[i]*count_list[j]
            quartets += P*NP*(NP-1)/2
    parentNode.add_child(newSeed)        # add the node back to the original tree. It is important if we want to continue using the tree after this function.
    return quartets

def main():
    with open(annoFile,'r') as f:
        for line in f:
            fields = line.split()
            name = fields[0]
            phylum = fields[2]
            nameHash[name] = phylum

# count the number of species in each phylum
    for node in myTree.leaf_node_iter():
        phylum = nameHash[node.taxon.label]
        global_phylCount[phylum] = 1 + (global_phylCount[phylum] if phylum in global_phylCount else 0)

    preprocess(myTree)

    trpls = {}
    quartets = {}

# main tasks
    for phylum in global_phylCount:
        if global_phylCount[phylum] >= 2:
            trpls[phylum] = computeTripletScore(myTree,phylum,global_phylCount[phylum],nameHash)
            quartets[phylum] = computeQuartetScore(myTree,phylum,global_phylCount[phylum],nameHash)



    for phylum in trpls:
         np = myTree.seed_node.nleaf - global_phylCount[phylum]
         p = global_phylCount[phylum]
         ntrpls = np*p*(p-1)/2
         nquartets = np*(np-1)*p*(p-1)/4
         trpls[phylum] /= (float(ntrpls))
         quartets[phylum] /= (float(nquartets))
         print(phylum + " " + str(global_phylCount[phylum]) + " " + str(trpls[phylum]) + " " + str(quartets[phylum]) )
  
if __name__== "__main__":
    main()
