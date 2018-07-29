#! /bin/bash

tree1=$1
tree2=$2
matched_tree=$3

tree1_ordered=`mktemp`
tree2_ordered=`mktemp`

nw_order -c n $tree1 > $tree1_ordered
nw_order -c n $tree2 > $tree2_ordered

match_trees.py $tree1_ordered $tree2_ordered  $matched_tree

