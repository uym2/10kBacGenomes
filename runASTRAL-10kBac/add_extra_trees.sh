#! /bin/bash

extract_support_type.py astral.tre astral.q1.tre q1
sed -i "s/NaN//g" astral.q1.tre

python /home/umai/my_gits/10kBacScripts/improve_ASTRAL/add_extra_bipartitions.py astral.q1.tre 0.37 extra.q37.trees collapsed.q37.tre > add_extra_trees.log 2>&1
arb_resolve_polytomies.py extra.q37.trees
