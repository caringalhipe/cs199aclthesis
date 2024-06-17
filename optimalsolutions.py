"""
----------- TO RUN -----------------
python optimalsolutions_randomized.py <vertex count*> <max posets>

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

#generate all possible permutations of tuples of size 2
all_combinations_relations = combinations(all_relations, n-1)

#generate all valid posets
Posets = []
for p in list(all_combinations_relations):
    G = nx.DiGraph(p)
    if nx.is_directed_acyclic_graph(G) and all(x in G.nodes for x in vertices):
        Posets.append(list(p))

#output lines
lines = []
#generate all posets
k = 1
covered_groups_LE = []
for P in Posets:
    L_P = get_linear_extensions(P)
    if L_P != [] and len(L_P) >= 3 and all(l[0] == '1' for l in L_P):  # Ensure there are at least 3 elements per set and same starting number
        covered_groups_LE.append(L_P)
        lines.append("Input: " + str([int(x) for x in L_P]))
        lines.append("Optimal solution cost: " + str(k))
        lines.append(str(P)+"\n")
    
count_posets = len(covered_groups_LE)

#generate all possible groups of posets

#get all possible combinations of size k from range 2 to len(posets)
#get linear extensions of the posets and combine into one group of linear extensions
#convert into set, then convert back to list
#check if group is already covered
#if no, print, append to covered groups

max_k = args[1]
if n < 5:
    for i in range(2, max_k + 1): #end should be count_posets + 1
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
else:
    for i in range(2, max_k): #end should be count_posets + 1
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
    
    # Randomize for additional cases (limited to 200-300 posets)
    if count_posets < 200:
        num_random = min(200 - count_posets, len(Posets)**max_k)
        k = max_k + 1
        print(f"Generating {num_random} random posets.")
        for i in range(num_random):
            group = random.choices(Posets, k=max_k)
            covered_group = []
            for poset in group:
                covered_group += get_linear_extensions(list(poset))
            covered_group = set(covered_group)
            covered_group = sorted(covered_group)
            if covered_group not in covered_groups_LE and covered_group != [] and len(covered_group) >= 3 and all(l[0] == '1' for l in covered_group):
                lines.append("Input: " + str([int(x) for x in covered_group]))
                lines.append("Optimal solution cost: " + str(k))
                for poset in group:
                    lines.append(str(list(poset)))
                lines.append("")
                covered_groups_LE.append(covered_group)
                count_posets += 1
            if count_posets >= 300:
                break

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
output.close()

print("FINISHED GENERATING INPUT LINEAR ORDERS")
