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
    k = int(k)
    
    anchors = find_anchors(G)
    grouped_anchors = group_anchors(anchors, k)
    Pstar = []
    Pstar_total = []
    
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
                Pstar_total.append(P_i)
    
    P, L = find_covering_poset(Pstar_total, upsilon)
    if P and L:
        covered_orders = set()
        Pfinal = []
        LOfinal = []
        unique_posets = set()

        for i in range(len(L)):
            if len(Pfinal) >= k:
                break

            poset_tuple = tuple(map(tuple, P[i]))
            if poset_tuple not in unique_posets:
                unique_posets.add(poset_tuple)
                Pfinal.append(P[i])
                LOfinal.append(L[i])
                covered_orders.update(L[i])

                # Check if the current set of covered orders matches upsilon
                if sorted(covered_orders) == sorted(upsilon):
                    return Pfinal, LOfinal

        # In case the loop completes and we still need to check the coverage
        if sorted(covered_orders) == sorted(upsilon):
            return Pfinal, LOfinal
    else:
        return None, None

    
    return Pfinal, LOfinal

def main():
    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: python algorithm3_4.py <input_file> <k>")
        return

    input_file_id = args[0]
    k = int(args[1])

    input_file_path = f'optsol/inputs/{input_file_id}posetsinput.txt'
    output_file_path = f'outputs/output_{input_file_id}.txt'
    count = 1

    if not os.path.exists("outputs/"):
        os.makedirs("outputs/")

    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:  # work on each test case
            print(count)
            count += 1
            inputLinearOrders = [x.strip() for x in line.strip('[]\n').split(',')]

            inputLinearOrders.sort()
            inputLinearOrders = [str(item) for item in inputLinearOrders]

            G = nx.Graph()
            N = len(inputLinearOrders)
            for i in range(N):
                G.add_node(inputLinearOrders[i])
                for j in range(i + 1, N):
                    adjacent = check_swap(inputLinearOrders[i], inputLinearOrders[j])
                    if adjacent:
                        G.add_edge(inputLinearOrders[i], inputLinearOrders[j], label=adjacent, color='k')
            
            Pfinal, LOfinal = k_poset_cover(inputLinearOrders, k, G)
            
            if Pfinal:
                output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
                for i in range(len(Pfinal)):
                    output_file.write(f"P{str(i + 1)}: {Pfinal[i]}\n")
                output_file.write("\n")
            else:
                output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
                output_file.write("None!!!!!\n\n")

    if Pfinal:
        print(f"Generated all output of input linear order sets with {args[0]} vertices")
        print("Check 'outputs' directory")
    else:
        print("Generated nothing")

if __name__ == "__main__":
    main()