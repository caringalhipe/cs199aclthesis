import sys
import networkx as nx
import pylab as p
from collections import defaultdict, OrderedDict
from poset_utils import VERIFY, get_linear_extensions, binaryRelation, binaryToCover, superCover

def Poset(upsilon):
    Pset = []
    
    # Generate Transposition Graph
    G = nx.Graph()
    l = len(upsilon)
    nodes = upsilon
    Edges = dict([])
    #print(upsilon)
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
    
    # Form Posets
    while len(nodes) > 0:
        # Create list of neighbor nodes
        Neighbors = dict([])
        for n in list(G.nodes):
            Neighbors[n] = list(G.neighbors(n))
        
        # Obtain starting node (node with least neighbors)
        numNeighbors = [[len(Neighbors[l]), l] for l in Neighbors]
        numNeighbors = sorted(numNeighbors, key=lambda l: l[0])
        startNode = numNeighbors[0][1]
        #print(startNode)
        # Initialize start values for traversal
        curLE = [startNode] # list of Linear Extensions currently in poset
        curP = binaryRelation([startNode]) # list of cover relations in current poset
        remEdges = [] # list of edges/anchor pairs to remove from cover relations

        cond = 1
        while(cond):
            # Obtain all edges/anchor pairs connected to members of curLE and their connected nodes
            potentialPairs = []
            potentialNodes = dict([])
            for node in curLE:
                potentialPairs += [Edges[node][n] for n in range(len(Edges[node])) 
                                   if Edges[node][n][1] in nodes]
                #print("potential pairs")
                #print(potentialPairs)
                for pair in potentialPairs:
                    id = tuple(sorted([int(p) for p in pair[0]]))
                    if potentialNodes.get(id) == None:
                        potentialNodes[id] = [pair[1]]
                    elif pair[1] not in potentialNodes[id]:
                        potentialNodes[id] += [pair[1]]
            #print(curLE)
            # Sort potential extensions by frequency from greatest to least 
            potentialNodes = sorted(potentialNodes.items(), key=lambda x: len(x[1]), reverse=True)
            #print("potential nodes")
            #print(potentialNodes)
            # Check potential anchor pairs to extend to
            i = 1
            for potentials in potentialNodes:
                pairsToRemove = [potentials[0], (potentials[0][1], potentials[0][0])]
                nodesToAdd = potentials[1]
                # If a potential mirror has more than 1 node, include convex of mirror
                if len(potentials[1]) > 1:
                    mirrors = [set(binaryRelation([x])) for x in potentials[1]] # list of sets of cover relations of each potential node to add from mirror
                    nodesToAdd += [s for s in superCover(mirrors, list(G.nodes)) if s not in nodesToAdd] # list of valid nodes to extend from if convex exists
                    pairsToRemove += [Edges[l][x][0] for l in nodesToAdd for x in range(len(Edges[l])) if l not in potentials[1]]
                    pairsToRemove = list(set(pairsToRemove))

                # List of cover relations to potentially add to poset
                tempNodes = [n for n in list(set(curP + binaryRelation(nodesToAdd))) if n not in remEdges + pairsToRemove and (n[1], n[0]) not in remEdges + pairsToRemove + curP]

                # Check if poset can be formed and if it will cover the input 
                P = get_linear_extensions(binaryToCover(tempNodes, len(upsilon[0])))
                # If the poset is valid, add node/s and continue traversal
                if VERIFY(P, curLE + [p for p in nodesToAdd if p not in curLE]):
                    curP = tempNodes
                    curLE += [p for p in nodesToAdd if p not in curLE]
                    nodes = [n for n in nodes if n not in curLE]
                    remEdges += pairsToRemove
                    break
                # If none of the potential node/s yield a valid poset, end traversal and continue with remaining graph
                elif i >= len(potentialNodes):
                    cond = 0
                i += 1

            # If there are no potential nodes to extend to, end traversal and continue with remaining graph
            if len(potentialNodes) == 0:
                cond=0

        nodes = [n for n in nodes if n not in curLE]
        
        # Remove nodes added to a poset from graph
        for le in curLE:
            G.remove_node(le)

        # Add poset to poset set, start over with remaining graph
        Pset.append(curP)
    
    # Return list of posets found
    return Pset

def main():
    """
    sample_input = [
        '12453', '12345', '13425', '13524', '12354', '12534', '12435', '14523', '14235', '13254', '13245', '14253'
    ]
    """
    sample_input = [
        '12345', '12435', '12453', '12534', '13245', '13254', 
        '13425', '13452', '13524', '13542', '14235', '14253', '14325', 
        '14352', '14523', '14532', '15423'
    ]
    
    output = Poset(sample_input)
    for poset in output:
        print(poset)
    # count = 1
    # for inputLinearOrders in sample_input:
    #     input_list = [int(x) for x in str(inputLinearOrders)]
    #     print(f"Input: {input_list}")
    #     posets = Poset(input_list)
    #     posets = poset.generateLinearExtensions()
    #     if posets:
    #         for i, linear_order in enumerate(posets):
    #             print(f"P{i+1}: {linear_order}")
    #     else:
    #         print(f"No posets found for input: {input_list}")
    #     print()

if __name__ == "__main__":
    main()


