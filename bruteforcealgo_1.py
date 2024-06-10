"RANDOM BRUTE FORCE ALGO"
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
    return sorted(P) == sorted(Y)

def VERIFY_GROUP(Group_P, Y): 
    covered = []
    for P in Group_P:
        covered += get_linear_extensions(P)
    return sorted(covered) == sorted(Y)

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: algorithm3.py <number_of_vertices> <k>")
        return

    n = int(args[0])
    max_k = int(args[1])

    vertices = list(range(1, n + 1))

    # Generate all possible tuples
    all_relations = [(a, b) for a in vertices for b in vertices if a != b]

    # Generate all possible combinations of tuples of size n-1
    all_combinations_relations = combinations(all_relations, n - 1)

    # Remove all invalid permutations; e.g [(1,2),(2,1)] - does not contain 3
    Posets = []
    for p in all_combinations_relations:
        check_vertices = [False] * n  # Array that checks if all vertices are included
        cycle = False
        for a, b in p:
            if (b, a) in p:
                cycle = True
                break
            check_vertices[a - 1] = True
            check_vertices[b - 1] = True
        
        if not cycle and all(check_vertices) and nx.is_directed_acyclic_graph(nx.DiGraph(p)):
            Posets.append(list(p))

    # Output lines
    lines = []
    covered_groups_LE = []

    # Generate all one posets
    for P in Posets:
        L_P = get_linear_extensions(P)
        if L_P and len(L_P) > 1:  # Ensure there is more than one linear order
            start_num = L_P[0][0]  # Get the starting number of the first linear extension
            L_P = [le for le in L_P if le[0] == start_num]  # Filter linear extensions starting with the same number
            if L_P and len(L_P) > 1:  # Ensure the filtered list has more than one element
                covered_groups_LE.append(L_P)
                lines.append("Input: " + str([int(x) for x in L_P]))
                lines.append("Optimal solution cost: 1")
                lines.append(str(P) + "\n")

    # Generate all possible groups of posets
    for i in range(2, max_k + 1):  # End should be count_one_posets + 1
        unprocessed_combinations_of_posets = combinations(Posets, i)

        # Check if input covered groups are disjoint from one another/no duplicates
        for group in unprocessed_combinations_of_posets:
            covered_group = []
            for poset in group:
                covered_group += get_linear_extensions(poset)
            
            # Ensure all linear extensions in a group start with the same number
            start_num = covered_group[0][0]  # Get the starting number of the first linear extension
            covered_group = [le for le in covered_group if le[0] == start_num]  # Filter linear extensions
            
            covered_group = sorted(set(covered_group))
            if len(covered_group) > 1 and covered_group not in covered_groups_LE:  # Ensure there is more than one linear order
                lines.append("Input: " + str([int(x) for x in covered_group]))
                lines.append("Optimal solution cost: " + str(i))
                for poset in group:
                    lines.append(str(poset))
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
            output.write(str([int(x) for x in LE]) + "\n")

    print("FINISHED GENERATING INPUT LINEAR ORDERS")

if __name__ == "__main__":
    main()
