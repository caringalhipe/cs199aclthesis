import sys
import networkx as nx
import pylab as p
from collections import defaultdict, OrderedDict
from poset_utils import VERIFY, get_linear_extensions, binaryRelation, binaryToCover, superCover, isPoset

def Poset(upsilon):
    Pset = []
    
    # Generate Transposition Graph
    G = nx.Graph()
    l = len(upsilon)
    nodes = upsilon
    Edges = dict([])
    
    for u in upsilon:
        Edges[u] = []
    
    for a in range(l):
        G.add_node(upsilon[a])
        for b in range(a+1, l):
            pairs = [upsilon[a][i:i+2] for i in range(len(upsilon[a])) if "".join(reversed(upsilon[a][i:i+2])) in upsilon[b] and 
                     upsilon[a][0:i]+upsilon[a][i+2:len(upsilon[a])] == upsilon[b][0:i]+upsilon[b][i+2:len(upsilon[b])]]
            if len(pairs) > 0:
                G.add_edge(upsilon[a], upsilon[b], label=str(sorted([pairs[0][0],pairs[0][1]])))
                Edges[upsilon[a]].append([tuple(sorted((int(pairs[0][0]), int(pairs[0][1])))), upsilon[b]])
                Edges[upsilon[b]].append([tuple(sorted((int(pairs[0][0]), int(pairs[0][1])))), upsilon[a]])
    
    while len(G.nodes) > 0:
        # Create a dictionary of neighbor nodes for each node
        Neighbors = dict([])
        for n in list(G.nodes):
            Neighbors[n]=list(G.neighbors(n))

        # Obtain the starting node (node with the least neighbors)
        numNeighbors = [[len(Neighbors[l]), l] for l in Neighbors]
        numNeighbors = sorted(numNeighbors, key=lambda l: l[0])
        startNode = numNeighbors[0][1]

        # Initialize values for traversal
        curLE = [startNode]  # List of linear extensions currently in poset
        curP = binaryRelation([startNode])  # List of cover relations in current poset
        remEdges = []  # List of edges/anchor pairs to remove from cover relations

        cond = 1
        while(cond):
            # Obtain all edges/anchor pairs connected to members of curLE and their connected nodes
            potentialPairs = []
            potentialNodes = dict([])
            for node in curLE:
                potentialPairs += [Edges[node][n] for n in range(len(Edges[node])) 
                                if Edges[node][n][1] in nodes]
                for pair in potentialPairs:
                    id = tuple(sorted([int(p) for p in pair[0]]))
                    if potentialNodes.get(id)==None:
                        potentialNodes[id] = [pair[1]]
                    elif pair[1] not in potentialNodes[id]:
                        potentialNodes[id] += [pair[1]]

            # Sort potential extensions by frequency from greatest to least 
            potentialNodes = sorted(potentialNodes.items(), key=lambda x: len(x[1]), reverse=True)

            valid_nodes = []
            for potentials in potentialNodes:
                pairsToRemove = [potentials[0], (potentials[0][1], potentials[0][0])]
                nodesToAdd = potentials[1]

                if len(potentials[1]) > 1:
                    mirrors = [set(binaryRelation([x])) for x in potentials[1]]
                    nodesToAdd += [s for s in superCover(mirrors, list(G.nodes)) if s not in nodesToAdd]
                    pairsToRemove += [Edges[l][x][0] for l in nodesToAdd for x in range(len(Edges[l])) if l not in potentials[1]]
                    pairsToRemove = list(set(pairsToRemove))

                valid_nodes += [p for p in nodesToAdd if p not in curLE and any(all((int(x), int(y)) in G.edges for x, y in zip(p, cur_node)) or all((int(x), int(y)) in G.edges for x, y in zip(cur_node, p)) for cur_node in curLE)]

            # Update curLE only with valid nodesToAdd
            curLE += valid_nodes

            # If there are no valid nodes to extend to, end traversal and continue with remaining graph
            if len(valid_nodes) == 0:
                cond = 0

            tempNodes = [n for n in list(set(curP + binaryRelation(valid_nodes))) if n not in remEdges + pairsToRemove and (n[1], n[0]) not in remEdges + pairsToRemove + curP]
            # Check if tree poset can be formed and if it will cover the input
            P = get_linear_extensions(tempNodes)
            # If the poset is valid, add node/s and continue traversal
            if isPoset(tempNodes) and VERIFY(P, curLE + valid_nodes):
                curP = tempNodes
                curLE += valid_nodes
                nodes = [n for n in nodes if n not in curLE]
                remEdges += pairsToRemove
                break
            # If none of the potential node/s yield a valid tree poset, end traversal and continue with remaining graph
            elif i >= len(potentialNodes):
                cond = 0
            i += 1

        # If there are no potential nodes to extend to, end traversal and continue with remaining graph
        if len(potentialNodes) == 0:
            cond = 0

        nodes = [n for n in nodes if n not in curLE]
        
        # Remove nodes added to a tree poset from graph
        for le in curLE:
            G.remove_node(le)

        # Add poset to poset tree, start over with remaining graph
        Pset.append(curP)
    
    return Pset

def main():
    
    sample_input = [
        '14523', '14253', '14235', '12453', '12435', '12345', '13245', '13425',
                '12354', '12534', '13254', '13524'
    ]
    
    output = Poset(sample_input)
    for poset in output:
        print(poset)

if __name__ == "__main__":
    main()
