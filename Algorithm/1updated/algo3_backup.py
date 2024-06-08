import os
import sys
from itertools import combinations
import networkx as nx
import random
from collections import defaultdict, OrderedDict
import itertools
from gui1 import check_swap
from algo1 import generatePoset
from algo3_2 import find_covering_poset
from algo2_1 import maximalPoset

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

def k_poset_cover(upsilon, k):
    G = nx.Graph()
    anchors = []
    N = len(upsilon)
    for i in range(N):
        G.add_node(upsilon[i])
        for j in range(i+1, N):
            adjacent = check_swap(upsilon[i], upsilon[j])
            if adjacent:
                G.add_edge(upsilon[i], upsilon[j], label=adjacent, color='k')
    anchors = find_anchors(G)
    #print("Anchors:", anchors)
    grouped_anchors = group_anchors(anchors, k)
    Pstar = []
    Pstar_total = []
    for A in grouped_anchors:
        Upsilon_A = []
        #print("Current Grouped Anchor:", A)
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
        #print("Upsilon_A:", Upsilon_A)
        if Upsilon_A:
            P_A = generatePoset(Upsilon_A)
            Pstar.append(P_A)
            
            if P_A:
                P_i = maximalPoset(upsilon, P_A, A)
                print(P_i)
                Pstar_total.append(P_i)
            
    
    Pfinal, LOfinal = find_covering_poset(Pstar_total, upsilon)
    return Pfinal, LOfinal


def main():
    sample_input = [
        '12453', '12345', '13425', '13524', '12354', '12534', '12435', '14523', '14235', '13254', '13245', '14253'
    ]
    k = 3
    result = k_poset_cover(sample_input, k)
    print("Final posets", result)

if __name__ == "__main__":
    main()

"""
args = sys.argv[1:]
args[0] = int(args[0])
args[1] = int(args[1])

count = 1
with open(f'optimalsolutions/optsol/inputs/{args[1]}posetsinput.txt', 'r') as input_file, open(f'outputs/output_{args[1]}.txt', 'w') as output_file:
    for line in input_file:
        print(count)
        count += 1
        inputLinearOrders = [int(x) for x in line.strip('[]\n').split(',')]
        inputLinearOrders.sort()
        inputLinearOrders = [str(item) for item in inputLinearOrders]
        posets, linear_orders = k_poset_cover(inputLinearOrders, args[1])

        if posets:
            output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
            for i, poset in enumerate(posets):
                output_file.write(f"P{str(i+1)}: {poset}\n")
            output_file.write("\n")
        else:
            output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
            output_file.write("None!!!!!\n\n")

if posets:
    print(f"Generated all output of input linear order sets with {args[1]} vertices")
    print("Check 'output' directory")
else:
    print("Generated nothing")
"""