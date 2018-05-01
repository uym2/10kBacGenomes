from dendropy import Tree,Node

def list_bipartitions(S):
    B = [ [] ]
    #B = [ [],[S[0]],[S[1]],[S[2]] ] #,[S[0],S[1]],[S[0],S[2]],[S[0],S[3]] ]
    
    for s in S:
        B1 = []
        for b in B:
            b1 = [ x for x in b ] + [s]
            B1.append(b1)
        B += B1

    return B        

def resolve_node(u,S,b):
    p = u.parent_node
    c = [ x for x in S if not x in b]

    children = u.child_nodes()

    for x in b:
        if x in children:
            u.remove_child(x)
        if x not in p.child_nodes():    
            p.add_child(x)
        
    for x in c:
        if x in p.child_nodes():
            p.remove_child(x)
        if not x in children:
            u.add_child(x)        
    
def resolve_tree(tree):
    H = []
    C = {}

    # make a new root if the root node has more than 2 children
    if len(tree.seed_node.child_nodes()) > 2:
        new_root = Node()
        u = tree.seed_node
        v = u.child_nodes()[0]
        u.remove_child(v)
        new_root.add_child(u)
        new_root.add_child(v)
        tree.seed_node = new_root

    # find all polytomies and bipartitions around them
    for node in tree.preorder_node_iter():
        S = node.child_nodes()
        if  len(S) > 2:
            C[node] = S
            B = [ x for x in list_bipartitions(S) if len(x) > 0 and len(S)-len(x) > 1]
            for j,b in enumerate(B):
                if j < len(H): 
                    H[j].append((node,b))
                else:
                    H.append([(node,b)])    


    R = []

    for T in H:
        for u,b in T:
            resolve_node(u,C[u],b)
        R.append(tree.as_string('newick'))

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
