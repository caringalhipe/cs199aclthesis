"""
----------- TO RUN -----------------
python optimalsolutions.py <vertex count*> <max posets>

where <vertex count*> = {3, 4, 5, 6}
<max posets*> = {1,2,3,4}

for <vertex count*> = 5, <max posets> should be limited to up to 4
for <vertex count*> = 6, <max posets> should be limited to up to 3
EXHAUSTIVE brute force algo
"""

import os
import sys
from itertools import combinations
import networkx as nx

# UTILS
def get_linear_extensions(cover_relation):
    # Create a directed graph from the cover relation
    G = nx.DiGraph()
    for a, b in cover_relation:
        G.add_edge(a, b)
    
    # Compute all possible topological sortings (i.e., linear extensions) of the graph
    sortings = list(nx.all_topological_sorts(G))
    
    # Convert each sorting to a string and return the list of all sortings
    return sorted([''.join(map(str, sorting)) for sorting in sortings])

def VERIFY(P, Y):
    if sorted(P) == sorted(Y):
        return True
    return False

def VERIFY_GROUP(Group_P, Y): 
    covered = []
    for P in Group_P:
        covered += get_linear_extensions(P)
    if sorted(covered) == sorted(Y):
        return True
    else:
        return False

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: python optimalsolutions.py <vertex count> <max posets>")
        return

    n = int(args[0])
    max_k = int(args[1])

    vertices = list(range(1, n + 1))

    # generate all possible tuples
    all_relations = [(a, b) for a in vertices for b in vertices if a != b]

    # generate all possible combinations of tuples of size n-1
    all_combinations_relations = combinations(all_relations, n - 1)

    # remove all invalid permutations; e.g [(1,2),(2,1)] - does not contain 3
    Posets = []
    for p in all_combinations_relations:
        G = nx.DiGraph(p)
        if nx.is_directed_acyclic_graph(G) and len(set([v for edge in p for v in edge])) == n:
            Posets.append(list(p))

    # output lines
    lines = []
    covered_groups_LE = []

    # generate all one-poset sets
    for P in Posets:
        L_P = get_linear_extensions(P)
        if L_P and len(L_P) > 1:  # Ensure there is more than one linear order
            start_num = L_P[0][0]  # Get the starting number of the first linear extension
            L_P = [le for le in L_P if le[0] == start_num]  # Filter linear extensions starting with the same number
            if L_P and len(L_P) > 1:  # Ensure the filtered list has more than one element
                covered_groups_LE.append(L_P)
                lines.append("Input: " + str(L_P))
                lines.append("Optimal solution cost: 1")
                lines.append(str(P) + "\n")

    count_one_posets = len(covered_groups_LE)

    # generate all possible groups of posets
    for i in range(2, max_k + 1):  # end should be count_one_posets + 1
        k = i

        unprocessed_combinations_of_posets = combinations(Posets, i)

        # Check if input covered groups are disjoint from one another/no duplicates
        for group in unprocessed_combinations_of_posets:
            covered_group = []
            for poset in group:
                covered_group += get_linear_extensions(list(poset))
            
            # Ensure all linear extensions in a group start with the same number
            start_num = covered_group[0][0]  # Get the starting number of the first linear extension
            covered_group = [le for le in covered_group if le[0] == start_num]  # Filter linear extensions
            
            covered_group = sorted(set(covered_group))
            if len(covered_group) > 1 and covered_group not in covered_groups_LE:  # Ensure there is more than one linear order
                lines.append("Input: " + str(covered_group))
                lines.append("Optimal solution cost: " + str(k))
                for poset in group:
                    lines.append(str(list(poset)))
                lines.append("")
                covered_groups_LE.append(covered_group)

    if not os.path.exists("optsol/"):
        os.makedirs("optsol/")

    if not os.path.exists(f"optsol/posets/"):
        os.makedirs(f"optsol/posets/")
        
    with open(f"optsol/posets/{n}posetsoptsol.txt", "w") as output:
        for l in lines:
            output.write(l + "\n")

    print("FINISHED GENERATING OPTIMAL SOLUTIONS")

    if not os.path.exists(f"optsol/inputs/"):
        os.makedirs(f"optsol/inputs/")

    with open(f"optsol/inputs/{n}posetsinput.txt", "w") as output:
        for LE in covered_groups_LE:
            output.write(str(LE) + "\n")

    print("FINISHED GENERATING INPUT LINEAR ORDERS")

if __name__ == "__main__":
    main()
