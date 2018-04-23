from dendropy import Tree,Node

def list_bipartitions(S):
    B = [ [],[S[0]],[S[1]],[S[2]],[S[3]],[S[0],S[1]],[S[0],S[2]],[S[0],S[3]] ]
    
    for s in S[4:]:
        B1 = []
        for b in B:
            b1 = [ x for x in b ] + [s]
            B1.append(b1)
        B += B1

    return B        

def resolve_node(node):
    S = node.child_nodes()
    B = list_bipartitions(S)

    R = []

    for b in B:
        if len(b) > 1:
            c = [ x for x in S if not x in b ]
            u = Node()
            v1 = Node()
            v2 = Node()
            for x in b:
                v1.add_child(x)
            for x in c:
                v2.add_child(x)    
            u.add_child(v1)
            u.add_child(v2)    
            
            R.append(Tree(seed_node=u).as_string("newick"))
            
            for x in S:
                node.add_child(x)

    return R

def resolve_tree(tree):
    H = []

    for node in tree.preorder_node_iter():
        nchilds = len(node.child_nodes())
        if  nchilds > 3 or (node is not tree.seed_node and nchilds > 2) :
            H.append(node)

    R = []

    for node in H:
        tree.reroot_at_node(node)
        R += resolve_node(node)
                
    return R

def main():
    from sys import argv
   
    treefile = argv[1]
    
    t = Tree.get_from_path(treefile,"newick")
    
    R = resolve_tree(t)
   
    
    for s in R:
        print(s) 
    
if __name__=="__main__":
    main()                
