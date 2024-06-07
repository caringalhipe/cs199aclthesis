import networkx as nx
from collections import defaultdict, OrderedDict
from algo2 import Poset
import itertools
from permutohedron import check_swap
from algo1 import generatePoset
from algo3_2 import find_covering_poset

def find_anchors(G):
    """
    Function to find all anchor (a, b) pairs in the input sequences.
    
    Parameters:
    upsilon (list of str): A list of strings representing the input sequences.
    
    Returns:
    list: A list of tuples representing all anchor pairs (a, b).
    """
    anchors = list(set(anchor[2]['label'] for anchor in G.edges.data()))
    
    anchors += [''.join(reversed(anchor)) for anchor in anchors]
    
    for i in range(len(anchors)):
        anchors[i] = (int(anchors[i][0]), int(anchors[i][3]))
    
    return anchors

def no_dupe(anchors):
    N = len(anchors)
    for i in range(N-1):
        for j in range(i+1, N):
            if ''.join(str(num) for num in anchors[i]) == ''.join(reversed(''.join(str(num) for num in anchors[j]))):
                return False
    return True

def group_anchors(anchors, k):
    """
    Function to generate all combinations of anchor pairs grouped by k-1.
    
    Parameters:
    anchors (list of tuples): A list of anchor pairs (a, b).
    k (int): The number of anchors per group.
    
    Returns:
    list: A list of combinations, each containing k-1 anchor pairs.
    """
    return [combi for combi in itertools.combinations(anchors, k-1) if no_dupe(combi)]

def covers_upsilon(linear_orders, Upsilon):
        return set(Upsilon).issubset(set(linear_orders))

def k_poset_cover(upsilon, k):
    """
    Function to compute the k-poset cover for a given input.
    
    Parameters:
    upsilon (list of str): A list of strings representing the input sequences.
    k (int): The maximum number of posets to cover the input sequences.
    
    Returns:
    list: A list of posets that cover the input sequences.
    """
    G = nx.Graph()
    anchors = []
    N = len(upsilon)
    #Add an edge between each node that has an adjacent swap
    for i in range(N):
        G.add_node(upsilon[i])
        for j in range(i+1, N):
                adjacent = check_swap(upsilon[i], upsilon[j])
                if adjacent:
                    G.add_edge(upsilon[i], upsilon[j], label=adjacent, color = 'k')
    
    #pos = nx.kamada_kawai_layout(G)
    
    #nx.draw(G, pos, with_labels=True, node_size=1000)
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))
    
    anchors = find_anchors(G)
    print("Anchors:", anchors)
    
    grouped_anchors = group_anchors(anchors, k)
    #print("Grouped Anchors:", grouped_anchors)
    
    Pstar = []
    for A in grouped_anchors:
        Upsilon_A = []
        print("Current Grouped Anchor:", A)
        
        for sequence in upsilon:
            satisfies = True
            for anchor in A:
                a, b = str(anchor[0]), str(anchor[1])
                if a in sequence and b in sequence:
                    if sequence.index(a) > sequence.index(b):
                        satisfies = False
                        break
                else:
                    satisfies = False
                    break
            if satisfies:
                Upsilon_A.append(sequence)
        
        print("Upsilon_A:", Upsilon_A)
        
        if Upsilon_A:
            P_A = generatePoset(Upsilon_A)
            print("P_A:", P_A)
            #poset_cover.append(P_A)
            #P_i = maximalPoset(Upsilon_A, P_A, A)
            Pstar.append(P_A)
    
    """
    for P in Pstar:
        linear_order = get_linear_extensions(P)
        if covers_upsilon(linear_order, upsilon):
            return P[:k] #original return

        poset_star, lo_star = find_covering_poset(P, Upsilon)
        Pfinal.append(P)
        LOfinal.append(LO)
    """
    
    return Pstar[:k]

def main():
    sample_input = [
        '12453', '12345', '13425', '13524', '12354', '12534', '12435', '14523', '14235', '13254', '13245', '14253'
    ]
    k = 3
    
    
    result = k_poset_cover(sample_input, k)
    
    """
    for poset in result:
        print(poset)
    
    
    with open("poset_cover_results.txt", "w") as file:
        for poset in result:
            file.write(str(poset) + "\n")
    """

if __name__ == "__main__":
    main()
