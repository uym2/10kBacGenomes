#! /usr/bin/env python

# quick, dirty, and temporary solution
# the current version of ASTRAL seems to mess up the branch length after scoring the species tree
# this script match the nodes of two trees and report the node's branch length using one tree and the support (also is the node label) using the other tree
# as said, this is a dirty solution: assuming the trees a ordered in an exact same way
# a better solution should be LCA mapping, but it takes more effort to implement!

from sys import argv
from dendropy import Tree

treefile1 = argv[1]
treefile2 = argv[2]
outfile = argv[3]

tree1 = Tree.get_from_path(treefile1,"newick")
tree2 = Tree.get_from_path(treefile2,"newick")


my_branches = []

for node in tree1.levelorder_node_iter():
    my_branches.append(node.edge_length)

currIdx = 0
for node in tree2.levelorder_node_iter():            
    node.edge_length = my_branches[currIdx]
    currIdx += 1
    
tree2.write_to_path(outfile,'newick')     
