"""
----------- TO RUN -----------------
python Poset.py <vertex count*> 

where <vertex count*> = {3, 4, 5, 6}
"""

import sys
import os
from collections import defaultdict
import networkx as nx
from poset_utils import (
    VERIFY, get_linear_extensions, binaryToCover, 
    binaryRelation, superCover, form_transposition_graph
)
from classes import Poset, LinearOrder

# Create output directory if not exists
if not os.path.exists("outputs/"):
    os.makedirs("outputs/")

args = sys.argv

def generate_poset(upsilon):
    Pset = []
    G = nx.Graph()
    l = len(upsilon)
    nodes = upsilon
    Edges = {u: [] for u in upsilon}
    
    for a in range(l):
        G.add_node(upsilon[a])
        for b in range(a + 1, l):
            pairs = [
                upsilon[a][i:i + 2] for i in range(len(upsilon[a])) 
                if "".join(reversed(upsilon[a][i:i + 2])) in upsilon[b] and 
                upsilon[a][:i] + upsilon[a][i + 2:] == upsilon[b][:i] + upsilon[b][i + 2:]
            ]
            if pairs:
                G.add_edge(upsilon[a], upsilon[b], label=str(sorted([pairs[0][0], pairs[0][1]])))
                Edges[upsilon[a]].append([tuple(sorted((int(pairs[0][0]), int(pairs[0][1])))), upsilon[b]])
                Edges[upsilon[b]].append([tuple(sorted((int(pairs[0][0]), int(pairs[0][1])))), upsilon[a]])
    
    while nodes:
        Neighbors = {n: list(G.neighbors(n)) for n in G.nodes}
        numNeighbors = sorted([[len(Neighbors[l]), l] for l in Neighbors], key=lambda l: l[0])
        startNode = numNeighbors[0][1]

        curLE = [startNode]
        curP = binaryRelation([startNode])
        remEdges = []

        while True:
            potentialPairs = []
            potentialNodes = defaultdict(list)
            
            for node in curLE:
                potentialPairs += [Edges[node][n] for n in range(len(Edges[node])) if Edges[node][n][1] in nodes]
                for pair in potentialPairs:
                    id = tuple(sorted([int(p) for p in pair[0]]))
                    potentialNodes[id].append(pair[1])
            
            potentialNodes = sorted(potentialNodes.items(), key=lambda x: len(x[1]), reverse=True)
            if not potentialNodes:
                break

            i = 1
            for potentials in potentialNodes:
                pairsToRemove = [potentials[0], (potentials[0][1], potentials[0][0])]
                nodesToAdd = potentials[1]
                
                if len(potentials[1]) > 1:
                    mirrors = [set(binaryRelation([x])) for x in potentials[1]]
                    nodesToAdd += [
                        s for s in superCover(mirrors, list(G.nodes)) if s not in nodesToAdd
                    ]
                    pairsToRemove += [
                        Edges[l][x][0] for l in nodesToAdd for x in range(len(Edges[l])) if l not in potentials[1]
                    ]
                    pairsToRemove = list(set(pairsToRemove))

                tempNodes = [
                    n for n in set(curP + binaryRelation(nodesToAdd)) 
                    if n not in remEdges + pairsToRemove and (n[1], n[0]) not in remEdges + pairsToRemove + curP
                ]
                
                P = get_linear_extensions(binaryToCover(tempNodes, len(upsilon[0])))
                
                if VERIFY(P, curLE + [p for p in nodesToAdd if p not in curLE]):
                    curP = tempNodes
                    curLE += [p for p in nodesToAdd if p not in curLE]
                    nodes = [n for n in nodes if n not in curLE]
                    remEdges += pairsToRemove
                    break
                elif i >= len(potentialNodes):
                    break
                i += 1
            else:
                break
        
        nodes = [n for n in nodes if n not in curLE]
        for le in curLE:
            G.remove_node(le)
        Pset.append(curP)
    
    return Pset

def main():
    count = 1
    input_path = f'optsol/inputs/input{args[1]}.txt'
    output_path = f'outputs/output_{args[1]}.txt'
    
    with open(input_path, 'r') as input_file, open(output_path, 'w') as output_file:
        for line in input_file:
            print(count)
            count += 1
            inputLinearOrders = [int(x) for x in line.strip('[]\n').split(',')]
            inputLinearOrders.sort()
            inputLinearOrders = [str(item) for item in inputLinearOrders]

            posets = []
            
            # Directly form groups based on initial character of each order
            groupings = defaultdict(list)
            for order in inputLinearOrders:
                groupings[order[0]].append(order)

            for group in groupings.values():
                poset_group = generate_poset(group)
                posets.extend(poset_group)
            
            output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
            if posets:
                for i, poset in enumerate(posets):
                    output_file.write(f"P{str(i+1)}: {poset}\n")
                output_file.write("\n")
            else:
                output_file.write("None!!!!!\n\n")

    if posets:
        print(f"Generated all output of input linear order sets with {args[1]} vertices")
        print("Check 'outputs' directory")
    else:
        print("Generated nothing")

if __name__ == "__main__":
    main()
