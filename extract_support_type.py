#! /usr/bin/env python

from sys import argv
from dendropy import Tree,Node

infile = argv[1]
outfile = argv[2]
supportType = argv[3] # q1, q2, q3, pp1, pp2, pp3,  etc.

tree = Tree.get_from_path(infile,'newick')

for node in tree.preorder_node_iter():
    if not node.is_leaf() and node.label is not None:
        supports = node.label[1:-1].split(';')
        for s in supports:
            stype, sval = s.split('=')
            if stype == supportType:
                node.label = sval


tree.write_to_path(outfile,'newick')                
