#! /usr/bin/env

from sys import argv
from dendropy import Tree
from bipartition_lib import resolve_tree


def collapse(node):
    p = node.parent_node
    if p is not None:
        p.remove_child(node)
        for v in node.child_node_iter():
            p.add_child(v)

infile = argv[1]
minSupport = float(argv[2])
outfile = argv[3] # output

if len(argv) > 4:
    collapsedTree = argv[4] # output, optional

tree = Tree.get_from_path(infile,"newick")

for node in tree.preorder_node_iter():
    if node.label is not None and float(node.label) < minSupport:
        collapse(node)

tree.write_to_path(collapsedTree,"newick")

print("Finish collapsing tree!")

R = resolve_tree(tree)

with open(outfile,'w') as fout:
    for r in R:
        fout.write(r)


#tree.write_to_path("collapsed.tre","newick")        

 
