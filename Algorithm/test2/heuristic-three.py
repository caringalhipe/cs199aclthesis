"""
----------- TO RUN -----------------
python TreePoset.py <vertex count*> 

where <vertex count*> = {3, 4, 5, 6}

"""
import sys, os
import networkx as nx
import pylab as p
from collections import defaultdict, OrderedDict
sys.path.append('Utils')
from TreePoset_Utils_v2 import VERIFY, get_linear_extensions, group_linearOrders_by_its_root, binaryToCover, isTreePoset, binaryRelation, superCover

args = sys.argv

if not os.path.exists("outputs/"):
    os.makedirs("outputs/")

def TreePoset(upsilon):
    Ptree = []
    
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
            if len(pairs)>0:
                G.add_edge(upsilon[a], upsilon[b], label=str(sorted([pairs[0][0],pairs[0][1]])))
                Edges[upsilon[a]].append([tuple(sorted((int(pairs[0][0]),int(pairs[0][1])))), upsilon[b]])
                Edges[upsilon[b]].append([tuple(sorted((int(pairs[0][0]),int(pairs[0][1])))), upsilon[a]])

    # Form Tree Posets
    while len(nodes)>0:
        # Create list of neighbor nodes
        Neighbors = dict([])
        for n in list(G.nodes):
            Neighbors[n]=list(G.neighbors(n))
        
        # Obtain starting node (node with least neighbors)
        numNeighbors = [[len(Neighbors[l]),l] for l in Neighbors]
        numNeighbors = sorted(numNeighbors, key = lambda l: l[0])
        startNode = numNeighbors[0][1]

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
                for pair in potentialPairs:
                    id = tuple(sorted([int(p) for p in pair[0]]))
                    if potentialNodes.get(id)==None:
                        potentialNodes[id] = [pair[1]]
                    elif pair[1] not in potentialNodes[id]:
                        potentialNodes[id] += [pair[1]]

            # Sort potential extensions by frequency from greatest to least 
            potentialNodes = sorted(potentialNodes.items(), key=lambda x: len(x[1]), reverse=True)

            # Check potential anchor pairs to extend to
            i = 1
            for potentials in potentialNodes:
                pairsToRemove = [potentials[0],(potentials[0][1], potentials[0][0])]
                nodesToAdd = potentials[1]
                # If a potential mirror has more than 1 node, include convex of mirror
                if len(potentials[1])>1:
                    mirrors = [set(binaryRelation([x])) for x in potentials[1]] # list of sets of cover relations of each potential node to add from mirror
                    nodesToAdd += [s for s in superCover(mirrors, list(G.nodes)) if s not in nodesToAdd] # list of valid nodes to extend from if convex exists
                    pairsToRemove += [Edges[l][x][0] for l in nodesToAdd for x in range(len(Edges[l])) if l not in potentials[1]]
                    pairsToRemove = list(set(pairsToRemove))

                # List of cover relations to potentially add to poset
                tempNodes = [n for n in list(set(curP + binaryRelation(nodesToAdd))) if n not in remEdges+pairsToRemove and (n[1],n[0]) not in remEdges+pairsToRemove+curP]

                # Check if tree poset can be formed and if it will cover the input 
                P = get_linear_extensions(binaryToCover(tempNodes,len(upsilon[0])))
                # If the poset is valid, add node/s and continue traversal
                if isTreePoset(tempNodes) and VERIFY(P, curLE+[p for p in nodesToAdd if p not in curLE]):
                    curP = tempNodes
                    curLE += [p for p in nodesToAdd if p not in curLE]
                    nodes = [n for n in nodes if n not in curLE]
                    remEdges += pairsToRemove
                    break
                # If none of the potential node/s yield a valid tree poset, end traversal and continue with remaining graph
                elif i>=len(potentialNodes):
                    cond = 0
                i += 1

            # If there are no potential nodes to extend to, end traversal and continue with remaining graph
            if len(potentialNodes)==0:
                cond=0

        '''
        # For drawing the transposition graphs
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, with_labels=True,font_size=10, node_size=500, node_color='#9CE5FF')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))

        p.show()
        '''

        nodes = [n for n in nodes if n not in curLE]
        
        # Remove nodes added to a tree poset from graph
        for le in curLE:
            G.remove_node(le)

        # Add poset to poset tree, start over with remaining graph
        Ptree.append(curP)
    
    # Return list of tree posets found
    return Ptree

count = 1
with open(f'optsol/inputs/{args[1]}treesinput.txt', 'r') as input_file, open(f'outputs/output_{args[1]}.txt', 'w') as output_file:
    for line in input_file: # work on each test case
        print(count)
        count+=1
        inputLinearOrders = [int(x) for x in line.strip('[]\n').split(',')]

        inputLinearOrders.sort()
        inputLinearOrders = [str(item) for item in inputLinearOrders]

        posets = []
        # group linear orders according to their root
        groupings = group_linearOrders_by_its_root(inputLinearOrders)

        #print("Groupings: ", groupings)

        # for each group, there is a set of posets
        # append each poset to the list posets
        
        for group in groupings:
            poset_group = TreePoset(group)
            for poset in poset_group:
                posets.append(poset)
        
        if posets != None:
            output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
            for i in range(len(posets)):
                output_file.write(f"P{str(i+1)}: {posets[i]}\n")
            output_file.write("\n")

        else:
            output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
            output_file.write("None!!!!!\n\n")

if posets != None:
    print(f"Generated all output of input linear order sets with {args[1]} vertices")
    print("Check 'output' directory")
else:
    print("Generated nothing")




