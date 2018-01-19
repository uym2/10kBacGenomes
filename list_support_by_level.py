#! /usr/bin/env python

from sys import argv
from dendropy import Tree

treefile = argv[1]
outfile = argv[2]

mytree = Tree.get_from_path(treefile,"newick")
mytree.seed_node.level = 0

currLevel = 0
currIdx = 0
with open(outfile,"w") as fout:
    for node in mytree.levelorder_node_iter():
        if node is not mytree.seed_node:
            node.level = node.parent_node.level + 1
            if node.level > currLevel:
                currLevel = node.level
                currIdx = 0
            if not node.is_leaf():
                currIdx += 1
                fout.write(str(node.level) + " " + str(currIdx) + " " + str(node.label) + "\n")
