import networkx as nx
from collections import defaultdict, OrderedDict
from algo2 import Poset
from poset_utils import VERIFY, get_linear_extensions, binaryRelation, binaryToCover, superCover
from itertools import combinations
import matplotlib.pyplot as plt
from permutohedron import check_swap

# Copy the poset_utils.py functions here
# (VERIFY, get_linear_extensions, binaryRelation, binaryToCover, superCover)

def find_anchors(upsilon):

    anchors = []
    for sequence in upsilon:
        for i in range(len(sequence) - 1):
            anchor = (int(sequence[i]), int(sequence[i + 1]))
            if anchor not in anchors:
                anchors.append(anchor)
    return anchors

def group_anchors(anchors, k):

    return list(itertools.combinations(anchors, k-1))

def exact_k_poset_cover(Y, k):
    # G = nx.Graph()
    # print(enumerate(Y))
    # for i, L in enumerate(Y):
    #     G.add_node(i, linear_order=L)

    # for i in range(len(Y)):
    #     for j in range(i + 1, len(Y)):
    #         G.add_edge(i, j, label=f"{i}, {j}")
    
    G = nx.Graph()
    N = len(Y)
    #Add an edge between each node that has an adjacent swap
    for i in range(N):
        G.add_node(Y[i])
        for j in range(i+1, N):
                adjacent = check_swap(Y[i], Y[j])
                if adjacent:
                    G.add_edge(Y[i], Y[j], label=adjacent, color = 'k')
    
    pos = nx.kamada_kawai_layout(G)
    
    nx.draw(G, pos, with_labels=True, node_size=1000)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))
    
    #plt.show()

    anchors = find_anchors(upsilon)
    #print("Anchors:", anchors)
    
    grouped_anchors = group_anchors(anchors, k)
    #print("Grouped Anchors:", grouped_anchors)
    
    poset_cover = []
    for element in grouped_anchors:
        Upsilon_A = []
        print("Current Grouped Anchor:", element)
        
        for sequence in upsilon:
            satisfies = True
            for anchor in element:
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
            P_A = Poset(Upsilon_A)
            print("P_A:", P_A)
            poset_cover.append(P_A)
    
    return poset_cover[:k]

def main():
    sample_input = [
        '12453', '12345', '13425', '13524', '12354', '12534', '12435', '14523', '14235', '13254', '13245', '14253'
    ]
    k = 4
    
    
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
