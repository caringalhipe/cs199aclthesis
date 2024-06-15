import os
import sys
from itertools import combinations
import networkx as nx
import random
from collections import defaultdict, OrderedDict
import itertools
from permutohedron import check_swap
from algo1 import generatePoset
from algo3_2 import find_covering_poset
from algo2_1 import maximalPoset
from itertools import chain
from random import sample

def get_linear_extensions(cover_relation):
    G = nx.DiGraph()
    for a, b in cover_relation:
        G.add_edge(a, b)
    sortings = list(nx.all_topological_sorts(G))
    return sorted([''.join(map(str, sorting)) for sorting in sortings])

def VERIFY(P, Y):
    return sorted(P) == sorted(Y)

def VERIFY_GROUP(Group_P, Y):
    covered = []
    for P in Group_P:
        covered += get_linear_extensions(P)
    return sorted(covered) == sorted(Y)

def find_anchors(G):
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
    return [combi for combi in itertools.combinations(anchors, k-1) if no_dupe(combi)]

def covers_upsilon(linear_orders, Upsilon):
    return set(Upsilon).issubset(set(linear_orders))

def k_poset_cover(upsilon, k, G):
    # G = nx.Graph()
    # N = len(upsilon)
    # for i in range(N):
    #     G.add_node(upsilon[i])
    #     for j in range(i+1, N):
    #         adjacent = check_swap(upsilon[i], upsilon[j])
    #         if adjacent:
    #             G.add_edge(upsilon[i], upsilon[j], label=adjacent, color='k')
    k = int(k)
    
    anchors = find_anchors(G)
    grouped_anchors = group_anchors(anchors, k)
    Pstar = []
    Pstar_total = []
    # Initialize outside the loop
    for A in grouped_anchors:
        Upsilon_A = []
        
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
        if Upsilon_A:
            P_A = generatePoset(Upsilon_A)
            Pstar.append(P_A)
            if P_A:
                P_i = maximalPoset(upsilon, P_A, A)
                #print("P_i", P_i)
                Pstar_total.append(P_i)
    
    P, L = find_covering_poset(Pstar_total, upsilon)
    if P and L:
        for i in range(len(L) - k):
            if sorted(set(chain.from_iterable(L[i:i+k]))) == sorted(upsilon):
                Pfinal = P[i:i+k]
                LOfinal = L[i:i+k]
                return Pfinal, LOfinal
    else:
        return None
    

def main():
    
    sample_input = [
        '12453', '12345', '13425', '13524', '12354', '12534', '12435', '14523', '14235', '13254', '13245', '14253'
    ]
    """
    sample_input = ['3124', '3142', '3214', '3241', '3412', '3421', '4123', '4132', '4213', '4231', '4312', '4321']
    """
    k = 5
    G = nx.Graph()
    N = len(sample_input)
    for i in range(N):
        G.add_node(sample_input[i])
        for j in range(i+1, N):
            adjacent = check_swap(sample_input[i], sample_input[j])
            if adjacent:
                G.add_edge(sample_input[i], sample_input[j], label=adjacent, color='k')
    Pfinal, LOfinal = exact_k_poset_cover(sample_input, k, G)

    print(f"Input: {sorted(sample_input)}")
    
    if Pfinal and LOfinal:
        print("Final posets:")
        for i in Pfinal:
            print(i)
        print("Linear Orders Covered:")
        for i in LOfinal:
            print(i)
        print(f"Output: {sorted(set(chain.from_iterable(LOfinal)))}")
    else:
        print('it no work :<')
    
    # print("Final posets:", Pfinal)
    # print("Linear Orders Covered:", LOfinal)

if __name__ == "__main__":
    main()
