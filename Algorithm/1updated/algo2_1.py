import sys
import networkx as nx
import pylab as p
from collections import defaultdict, OrderedDict
from poset_utils import VERIFY, get_linear_extensions, binaryRelation, binaryToCover, superCover, isPoset
from algo1 import generatePoset
from permutohedron import check_swap


def maximalPoset(upsilon, P_A, A):
    G = nx.Graph()
    N = len(upsilon)

    # Add an edge between each node that has an adjacent swap
    for i in range(N):
        G.add_node(upsilon[i])
        for j in range(i+1, N):
            adjacent = check_swap(upsilon[i], upsilon[j])
            if adjacent:
                G.add_edge(upsilon[i], upsilon[j], label=adjacent, color='k')

    # Find linear extensions
    Y_cov = get_linear_extensions(P_A)
    print("Y_A", Y_cov)
    Y_uncov = [u for u in upsilon if u not in Y_cov]
    print("Y_uncov", Y_uncov)


    # Create a dictionary of neighbor nodes for each node
    #neighbors = {n: list(G.neighbors(n)) for n in G.nodes}
    Neighbors = dict([])
    for n in list(G.nodes):
        Neighbors[n]=list(G.neighbors(n))

    print("Neighbors", Neighbors)

    #Check least amount of neighbors in Y_cov
    least_neighbors_count = float('inf')
    start_node = None
    for linear_ext in Y_cov:
        neighbor_count = len(Neighbors.get(linear_ext, []))
        if neighbor_count < least_neighbors_count:
            least_neighbors_count = neighbor_count
            start_node = linear_ext

    print("Start Node:", start_node)

    
    

    return Y_cov

def main():
    sample_input = [
        '14523', '14253', '14235', '12453', '12435', '12345', '13245', '13425',
        '12354', '12534', '13254', '13524'
    ]
    """
    sample_input = [
        '135624', '315624', '153624', '153264', '135264', '315264'
    ]

    sample_input = [
        '12453', '12345', '13425', '13524', '12354', '12534', '12435', '14523', '14235', '13254', '13245', '14253'
    ]
    """
    #P_A = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (3, 2), (3, 4), (3, 5), (5, 2), (5, 4)] # ((5, 2), (2, 4))
    P_A = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (4, 2), (4, 3), (4, 5)] # ((4, 2), (4, 3))
    A = ((4, 2), (4, 3))
    
    output = maximalPoset(sample_input, P_A, A)
    for poset in output:
        print(poset)

if __name__ == "__main__":
    main()
