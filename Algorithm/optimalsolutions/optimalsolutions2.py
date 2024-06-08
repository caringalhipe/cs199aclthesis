"""
----------- TO RUN -----------------
python optimalsolutions.py <vertex count*> <max posets>

where <vertex count*> = {3, 4, 5, 6}
<max posets*> = {1,2,3,4}

for <vertex count*> = 5, <max posets*> should be limited to up to 4
for <vertex count*> = 6, <max posets*> should be limited to up to 3
"""

import os, sys
from itertools import combinations
import networkx as nx
import random

#UTILS
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
    
args = sys.argv[1:]
args[0] = int(args[0])
args[1] = int(args[1])

#get number of vertices
n = args[0]
vertices = [int(x) for x in range(1,n+1)]

#generate all possible tuples
all_relations = []
for a in range(1,n+1):
    for b in range(1,n+1):
        if a!=b:
            all_relations.append((a,b))

#generate all possible combinations of tuples of size 2
all_combinations_relations = combinations(all_relations, n-1)

#remove all invalid permutations; e.g [(1,2),(2,1)] - does not contain 3
Posets = []
for p in list(all_combinations_relations):
    check_vertices = [False for x in range(n)] #array that checks if all vertices are included
    cycle = False
    for (a,b) in p:
        if (b,a) in p:
            cycle = True
        check_vertices[a-1] = True
        check_vertices[b-1] = True
    
    if False not in check_vertices and not cycle and nx.is_directed_acyclic_graph(nx.DiGraph(p)):
        Posets.append(list(p))

#output lines
lines = []
#generate all one posets
k = 1
covered_groups_LE = []
for P in Posets:
    L_P = get_linear_extensions(P)
    if L_P != []:
        covered_groups_LE.append(L_P)
        lines.append("Input: " + str([int(x) for x in L_P]))
        lines.append("Optimal solution cost: " + str(k))
        lines.append(str(P)+"\n")

count_posets = len(covered_groups_LE)

#generate all possible groups of posets
max_k = int(args[1])
for i in range(2, max_k + 1): #end shoud be count_one_posets + 1
    k = i

    unprocessed_combinations_of_posets = combinations(Posets, i)

    #Check if input covered groups are disjoint from one another/no duplicates
    combinations_of_posets = []
    for inputSet in list(unprocessed_combinations_of_posets):
        allPosets = []
        for p in inputSet:
            allPosets.extend(get_linear_extensions(list(p)))

        if len(allPosets)==len(list(set(allPosets))):
            combinations_of_posets.append(inputSet)

    for group in combinations_of_posets:
        covered_group = []
        for poset in group:
            covered_group += get_linear_extensions(list(poset))
        covered_group = set(covered_group)
        covered_group = sorted(covered_group)
        if covered_group not in covered_groups_LE and covered_group!=[]:
            lines.append("Input: " + str([int(x) for x in covered_group]))
            lines.append("Optimal solution cost: " + str(k))
            for poset in group:
                lines.append(str(list(poset)))
            lines.append("")
            covered_groups_LE.append(covered_group)

if not os.path.exists("optsol/"):
    os.makedirs("optsol/")

if not os.path.exists(f"optsol/posets/"):
    os.makedirs(f"optsol/posets/")
    
output = open(f"optsol/posets/{args[0]}posetsoptsol.txt", "w")

for l in lines:
    output.write(l+"\n")
output.close()

print("FINISHED GENERATING OPTIMAL SOLUTIONS")

if not os.path.exists(f"optsol/inputs/"):
    os.makedirs(f"optsol/inputs/")

output = open(f"optsol/inputs/{args[0]}posetsinput.txt", "w")

for LE in covered_groups_LE:
    output.write(str([int(x) for x in LE])+"\n")
output.close

print("FINISHED GENERATING INPUT LINEAR ORDERS")
