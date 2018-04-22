#! /usr/bin/env python

from sys import argv
from dendropy import Tree
from pergroup_stats import readTaxonomy, preprocess


def find_LCA_of_groups(myTree,nameHash):
    groupings = {}

# main tasks
    for node in myTree.postorder_node_iter():
        if node.is_leaf():
            node.groupCount = {}
            for group in nameHash[node.taxon.label]:
                node.groupCount[group] = 1
        else:
            node.groupCount = {}
            for c in node.child_node_iter():
                for group in c.groupCount:
                    node.groupCount[group] = c.groupCount[group] + (node.groupCount[group] if group in node.groupCount else 0)

        for group in node.groupCount:
            for c in node.child_node_iter():
                for group in c.groupCount:
                    if c.groupCount[group] == c.nleaf and node.groupCount[group] != node.nleaf:
                        #if group not in convergence or c.groupCount[group] > convergence[group][0]:
                        if group not in groupings:
                            groupings[group] = set([c])
                        else:
                            groupings[group].add(c)
    return groupings
           
           
def main():
    taxFile = argv[1]
    treefile = argv[2]  
    outfile = argv[3]
    
                
    myTree = Tree.get_from_path(treefile,"newick")
    nameHash = readTaxonomy(taxFile)
    preprocess(myTree)
    
    groupings = find_LCA_of_groups(myTree,nameHash) 

    with open(outfile,'w') as fout:
        fout.write("group rank br2root d2root support\n")
        for group in groupings:
            if len(list(groupings[group])) == 1:
                ID = None
            else:
                ID = 1
            for node in groupings[group]:
                if not node.label:
                    continue
                suffix = ("_" + str(ID)) if ID else ''
                fout.write(group[0] + suffix + " " + group[1] + " " + str(node.br2root) + " " + str(node.d2root-node.edge_length) + " " + str(node.label) + "\n")
                if ID:
                    ID += 1  
    
                
if __name__ == "__main__":
    main()        
