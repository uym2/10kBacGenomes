#! /usr/bin/env python

from sys import argv
from dendropy import Tree


def readTaxonomy(taxFile):
# the taxonomy file must be restructed into the following form:
# each line has exactly 3 fields
# GenomeName GroupName GroupType
# for example
# G001027285 Bacteria Kingdom
# G001027285 Proteobacteria Phylum
# ...
    nameHash = {}
    #groupHash = {}
       
    with open(taxFile,'r') as fin:
        for line in fin:
            name,group,title = line.split()
            if name not in nameHash:
                nameHash[name] = [(group,title)]
            else:
                nameHash[name].append((group,title))
            #if group not in groupHash:
            #    groupHash[group] = title

    return nameHash#,groupHash

def preprocess(tree):
    for node in tree.postorder_node_iter():
        if node.is_leaf():
            node.nleaf = 1
        else:
            node.nleaf = 0
            for c in node.child_node_iter():
                node.nleaf += c.nleaf

#def computeTripletScore(tree,groupName,groupSize,nameHash):
    

def computeScore(tree,groupName,groupSize,nameHash,scoreType='Both'):
# by default, compute both triplet and quartet scores
# can output only triplet or quartet score if the scoreType is changed
# to either 'triplet' or 'quartet'
    trpls = 0
    quartets = 0
    newSeed = tree.seed_node
    for node in tree.postorder_node_iter():
        if node.is_leaf():
            node.count = 0 + ( groupName in nameHash[node.taxon.label])
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
            quartets += P*NP*(NP-1)/2
            
            if node.count >= groupSize: # break early when we found the LCA. This causes some complications later on, though
                newSeed = node
                break
    if scoreType == 'triplet':
        return trpls

    # UGLY SOLUTION! 
    # Dendropy seems to remove the node from the old tree when we make it the seed node of a new tree
    # therefore, I have to manually add the node back after finishing the job on the subtree
    parentNode = newSeed.parent_node
    subTree = Tree(seed_node=newSeed)

    for node in subTree.postorder_node_iter():
        if not node.is_leaf() and not node is subTree.seed_node:
            
            NP = node.nleaf - node.count # non-group leaves of the "inside"
            P = 0
            count_list = [ s.count for s in node.parent_node.child_node_iter() if s != node ]
            count_list.append(groupSize - node.parent_node.count)

            for i in range(len(count_list)-1):
                for j in range(i+1,len(count_list)):
                    P += count_list[i]*count_list[j]
            quartets += P*NP*(NP-1)/2
    if parentNode is not None:
        parentNode.add_child(newSeed)        # add the node back to the original tree. It is important if we want to continue using the tree after this function.

    return quartets if scoreType=='quartet' else (trpls,quartets)

def main():
    taxFile = argv[1]  # ~/10kBacGenome/repophlan_microbes_ranks.txt
    treefile = argv[2]
    outfile = argv[3]

    myTree = Tree.get_from_path(treefile,"newick")
    groupCount = {}
    
    '''with open(taxFile,'r') as f:
        for line in f:
            fields = line.split()
            name = fields[0]
            group = fields[2]
            nameHash[name] = [group] '''
                
    nameHash = readTaxonomy(taxFile)
        
# count the number of species in each group
    for node in myTree.leaf_node_iter():
        for group in nameHash[node.taxon.label]:
            groupCount[group] = 1 + (groupCount[group] if group in groupCount else 0)

    preprocess(myTree)

    #trpls = {}
    #quartets = {}
    scores = {}
# main tasks
    for group in groupCount:
        if groupCount[group] >= 2:
            scores[group] = computeScore(myTree,group,groupCount[group],nameHash)

    with open(outfile,'w') as fout:
        for group in scores:
             np = myTree.seed_node.nleaf - groupCount[group]
             p = groupCount[group]
             ntrpls = np*p*(p-1)/2
             nquartets = np*(np-1)*p*(p-1)/4
             trpls = scores[group][0]/(float(ntrpls))
             quartets = scores[group][1]/(float(nquartets))
             fout.write(group[0] + " " + group[1] + " " + str(groupCount[group]) + " " + str(trpls) + " " + str(quartets) + "\n")
  
if __name__== "__main__":
    main()
