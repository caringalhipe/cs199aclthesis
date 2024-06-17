import os
import sys
from itertools import combinations, chain
import networkx as nx
from permutohedron import check_swap
from algo1 import generatePoset
from algo3_2 import find_covering_poset
from algo2 import maximalPoset

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
    return [combi for combi in combinations(anchors, k-1) if no_dupe(combi)]

def covers_upsilon(linear_orders, Upsilon):
    return set(Upsilon).issubset(set(linear_orders))

def exact_k_poset_cover(upsilon, k, G):
    k = int(k)
    anchors = find_anchors(G)
    for i in range(1, k+1):
        grouped_anchors = group_anchors(anchors, k)
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
                if P_A:
                    P_i = maximalPoset(upsilon, P_A, A)
                    Pstar_total.append(P_i)
        
        result = find_covering_poset(Pstar_total, upsilon)
        if result:
            P, L = result
            for q in range(len(L) - i):
                if sorted(set(chain.from_iterable(L[q:q+i]))) == sorted(upsilon):
                    Pfinal = P[q:q+i]
                    LOfinal = L[q:q+i]
                    return Pfinal, LOfinal
    return None

def main():
    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: python optimalkposet.py <input_file> <k>")
        return

    input_file_id = args[0]
    k = int(args[1])

    input_file_path = f'optsol/inputs/{input_file_id}posetsinput.txt'
    output_file_path = f'outputs/output_{input_file_id}.txt'
    count = 1

    if not os.path.exists("outputs/"):
        os.makedirs("outputs/")

    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
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
            
            result = exact_k_poset_cover(inputLinearOrders, k, G)
            
            if result:
                Pfinal, LOfinal = result
                output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
                for i in range(len(Pfinal)):
                    output_file.write(f"P{str(i + 1)}: {Pfinal[i]}\n")
                output_file.write("\n")
            else:
                output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
                output_file.write("None!\n\n")

    print(f"Processed {count-1} input cases.")
    print("Check 'outputs' directory for results.")

if __name__ == "__main__":
    main()
