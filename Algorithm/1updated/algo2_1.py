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
        for j in range(i + 1, N):
            adjacent = check_swap(upsilon[i], upsilon[j])
            if adjacent:
                G.add_edge(upsilon[i], upsilon[j], label=adjacent, color='k')

    # Find linear extensions
    Y_cov = get_linear_extensions(P_A)

    Y_uncov = [u for u in upsilon if u not in Y_cov]


    # Create a dictionary of neighbor nodes for each node
    Neighbors = {n: list(G.neighbors(n)) for n in G.nodes()}

    blacklist = []
    while(1):
        # Find neighbors of elements in Y_cov that are not yet in Y_cov
        # Finding mirror
        tempMirrors = []
        tempNodes = []
        for linear_ext in Y_cov:
            neighbors = Neighbors.get(linear_ext, [])
            for neighbor in neighbors:
                if neighbor not in Y_cov and neighbor not in blacklist:
                    swap = check_swap(linear_ext, neighbor)
                    if swap:
                        tempMirrors.append((tuple(map(int, swap.split(', '))), [neighbor]))
                        tempNodes.append(neighbor)
        
        if len(tempNodes) == 0:
            break


        # Finding convex of tempNodes
        P_tempnodes = generatePoset(tempNodes)
        LE_tempnodes = get_linear_extensions(P_tempnodes)
        print()
        
        temp_cov = []
        for i in LE_tempnodes:
            if i in upsilon:
                temp_cov.append(i)

        if sorted(get_linear_extensions(generatePoset(list(set(Y_cov).union(set(temp_cov)))))) == sorted(list(set(Y_cov).union(set(temp_cov)))):
            Y_cov = list(set(Y_cov).union(set(temp_cov)))

        else:
            for i in temp_cov:
                if sorted(get_linear_extensions(generatePoset(Y_cov + [i]))) == sorted(Y_cov + [i]):
                    Y_cov.append(i)

                else:
                    blacklist.append(i)
    
    P_i = generatePoset(Y_cov)

    return P_i

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

    P_A = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (3, 2), (3, 4), (3, 5), (5, 2), (5, 4)]
    A = ((5, 2), (2, 4))
    """

    P_A = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (2, 3), (2, 4), (5, 3), (5, 4), (3, 4)]
    
    A = ((5, 3), (5, 4))
    
    output = maximalPoset(sample_input, P_A, A)
    print(output)

if __name__ == "__main__":
    main()
