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
    
    #print("Edges", Edges)
    while len(G.nodes) > 0:
        # Create a dictionary of neighbor nodes for each node
        #neighbors = {n: list(G.neighbors(n)) for n in G.nodes}
        Neighbors = dict([])
        for n in list(G.nodes):
            Neighbors[n]=list(G.neighbors(n))

        print("Neighbors", Neighbors)
        # Obtain the starting node (node with the least neighbors)
        numNeighbors = [[len(Neighbors[l]), l] for l in Neighbors]
        #print("numNeighbors", numNeighbors)
        numNeighbors = sorted(numNeighbors, key=lambda l: l[0])
        #print("numNeighbors", numNeighbors)
        startNode = numNeighbors[0][1]
        print("startNode:", startNode)
        # Initialize values for traversal
        curLE = [startNode]  # List of linear extensions currently in poset
        print("curLE", curLE)
        curP = binaryRelation([startNode])  # List of cover relations in current poset
        print("curP", curP)
        remEdges = []  # List of edges/anchor pairs to remove from cover relations

        cond = 1
        while(cond):
            # Obtain all edges/anchor pairs connected to members of curLE and their connected nodes
            potentialPairs = []
            potentialNodes = dict([])
            for node in curLE:
                potentialPairs += [Edges[node][n] for n in range(len(Edges[node])) 
                                if Edges[node][n][1] in nodes]
                #print("potentialPairs", potentialPairs)
                for pair in potentialPairs:
                    id = tuple(sorted([int(p) for p in pair[0]]))
                    if potentialNodes.get(id)==None:
                        potentialNodes[id] = [pair[1]]
                        #print("potentialNodes[id], None", potentialNodes[id])
                    elif pair[1] not in potentialNodes[id]:
                        potentialNodes[id] += [pair[1]]
                       #print("potentialNodes[id], pair[1] not in potentialNodes[id]", potentialNodes[id])
                #print("potentialNodes", potentialNodes)

            # Sort potential extensions by frequency from greatest to least 
            potentialNodes = sorted(potentialNodes.items(), key=lambda x: len(x[1]), reverse=True)
            print("potentialNodes", potentialNodes)
            # Check potential anchor pairs to extend to

            i = 1
            for potentials in potentialNodes:
                pairsToRemove = [potentials[0], (potentials[0][1], potentials[0][0])]
                print("pairsToRemove", pairsToRemove)
                nodesToAdd = potentials[1]
                print("nodesToAdd", nodesToAdd)
                
                # Debug: Print potential nodes and their connections
                #print(f"Evaluating potentials: {potentials}")
                #print(f"Number of nodes connected to the potential anchor pair: {len(potentials[1])}")
                
                # If a potential mirror has more than 1 node, include convex of mirror
                
                if len(potentials[1]) > 1: # initially 1
                    mirrors = [set(binaryRelation([x])) for x in potentials[1]]  # list of sets of cover relations of each potential node to add from mirror
                    nodesToAdd += [s for s in superCover(mirrors, list(G.nodes)) if s not in nodesToAdd]  # list of valid nodes to extend from if convex exists
                    pairsToRemove += [Edges[l][x][0] for l in nodesToAdd for x in range(len(Edges[l])) if l not in potentials[1]]
                    pairsToRemove = list(set(pairsToRemove))
                    print("mirrors", mirrors)
                """

                mirrors = [set(binaryRelation([x])) for x in potentials[1]]  # list of sets of cover relations of each potential node to add from mirror
                nodesToAdd += [s for s in superCover(mirrors, list(G.nodes)) if s not in nodesToAdd]  # list of valid nodes to extend from if convex exists
                pairsToRemove += [Edges[l][x][0] for l in nodesToAdd for x in range(len(Edges[l])) if l not in potentials[1]]
                pairsToRemove = list(set(pairsToRemove))
                print("mirrors", mirrors)
                """

                # List of cover relations to potentially add to poset
                tempNodes = [n for n in list(set(curP + binaryRelation(nodesToAdd))) if n not in remEdges + pairsToRemove and (n[1], n[0]) not in remEdges + pairsToRemove + curP]
                print("tempNodes", tempNodes)
                # Check if tree poset can be formed and if it will cover the input
                #P = get_linear_extensions(binaryToCover(tempNodes, len(upsilon[0])))
                #print("upsilon[0]", upsilon[0])
                #print("len of upsilon", len(upsilon[0]))
                #print("binary to cover", binaryToCover(tempNodes, len(upsilon[0])))
                #P = get_linear_extensions(binaryToCover(tempNodes, len(upsilon[0])))
                P = get_linear_extensions(tempNodes)
                print("P", P)
                # If the poset is valid, add node/s and continue traversal
                print("isPoset(tempNodes)", isPoset(tempNodes))
                print("Verify", VERIFY(P, curLE + [p for p in nodesToAdd if p not in curLE]))
                print("curLE + nodesToAdd", curLE + [p for p in nodesToAdd if p not in curLE])
                #if isPoset(tempNodes) and VERIFY(P, curLE + [p for p in nodesToAdd if p not in curLE]):
                if isPoset(tempNodes) and VERIFY(P, curLE + [p for p in nodesToAdd if p not in curLE]):
                    curP = tempNodes
                    curLE += [p for p in nodesToAdd if p not in curLE]
                    nodes = [n for n in nodes if n not in curLE]
                    remEdges += pairsToRemove
                    print("curP", curP)
                    print("curLE", curLE)
                    print("nodes", nodes)
                    print("remEdges", remEdges)
                    break
                # If none of the potential node/s yield a valid tree poset, end traversal and continue with remaining graph
                elif i >= len(potentialNodes):
                    cond = 0
                    #print("potentialNodes", potentialNodes)
                i += 1

            # If there are no potential nodes to extend to, end traversal and continue with remaining graph
            if len(potentialNodes) == 0:
                cond = 0


        """
        # For drawing the transposition graphs
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, with_labels=True,font_size=10, node_size=500, node_color='#9CE5FF')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))

        p.show()
        """

        nodes = [n for n in nodes if n not in curLE]
        
        # Remove nodes added to a tree poset from graph
        for le in curLE:
            G.remove_node(le)

        # Add poset to poset tree, start over with remaining graph
        Pset.append(curP)
    
    # Return list of posets found
    return Pset


def main():
    
    sample_input = [
        '14523', '14253', '14235', '12453', '12435', '12345', '13245', '13425',
                '12354', '12534', '13254', '13524'
    ]
    """
    sample_input = [
        '135624', '315624', '153624', '153264', '135264', '315264'
    ]

    sample_input = [
        '12453', '12345', '13425', '13524', '12354', '12534', '12435', '14523', '14235', '13254', '13245', '14253'
    ]
    """
    P_A = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (3, 2), (3, 4), (3, 5), (5, 2), (5, 4)]
    A = ((5, 2), (2, 4))
    
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


