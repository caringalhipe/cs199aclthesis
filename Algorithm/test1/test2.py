import sys
import networkx as nx
import pylab as p
from collections import defaultdict, OrderedDict
from poset_utils import VERIFY, get_linear_extensions, binaryRelation, binaryToCover, superCover

class Poset:
    def __init__(self, upsilon):
        self.upsilon = upsilon
        self.poset_set = self._create_poset_set()

    def _create_poset_set(self):
        Pset = []
        nodes = self.upsilon[:]

        G = nx.Graph()
        l = len(self.upsilon)
        nodes = self.upsilon
        Edges = dict([])
        for u in self.upsilon:
            Edges[tuple(u)] = []  # Convert list to tuple
            G.add_node(tuple(u))  # Convert list to tuple

        for a in range(l):
            G.add_node(tuple(self.upsilon[a])) # Convert list to tuple
            for b in range(a+1, l):
                pairs = [self.upsilon[a][i:i+2] for i in range(len(self.upsilon[a])) if "".join(reversed(self.upsilon[a][i:i+2])) in self.upsilon[b] and 
                        self.upsilon[a][0:i]+self.upsilon[a][i+2:len(self.upsilon[a])] == self.upsilon[b][0:i]+self.upsilon[b][i+2:len(self.upsilon[b])]]
                if len(pairs) > 0:
                    G.add_edge(tuple(self.upsilon[a]), tuple(self.upsilon[b]), label=str(sorted([pairs[0][0],pairs[0][1]])))
                    Edges[tuple(self.upsilon[a])].append([tuple(sorted((int(pairs[0][0]), int(pairs[0][1])))), tuple(self.upsilon[b])]) # Convert lists to tuples
                    Edges[tuple(self.upsilon[b])].append([tuple(sorted((int(pairs[0][0]), int(pairs[0][1])))), tuple(self.upsilon[a])]) # Convert lists to tuples

        while len(nodes) > 0:
            Neighbors = dict([])
            for n in list(G.nodes):
                Neighbors[n] = list(G.neighbors(n))
            
            print("Neighbors:", Neighbors)  # Debug print
            
            numNeighbors = [[len(Neighbors[l]), l] for l in Neighbors]
            numNeighbors = sorted(numNeighbors, key=lambda l: l[0])
            print("numNeighbors:", numNeighbors)  # Debug print
            
            if numNeighbors:  # Check if numNeighbors is not empty
                startNode = numNeighbors[0][1]

                curLE = [startNode]
                curP = binaryRelation([startNode])
                remEdges = []

                cond = 1
                while(cond):
                    potentialPairs = []
                    potentialNodes = dict([])
                    for node in curLE:
                        potentialPairs += [Edges[node][n] for n in range(len(Edges[node])) 
                                        if Edges[node][n][1] in nodes]
                        for pair in potentialPairs:
                            id = tuple(sorted([int(p) for p in pair[0]]))
                            if potentialNodes.get(id) == None:
                                potentialNodes[id] = [pair[1]]
                            elif pair[1] not in potentialNodes[id]:
                                potentialNodes[id] += [pair[1]]
                    
                    potentialNodes = sorted(potentialNodes.items(), key=lambda x: len(x[1]), reverse=True)

                    i = 1
                    for potentials in potentialNodes:
                        pairsToRemove = [potentials[0], (potentials[0][1], potentials[0][0])]
                        nodesToAdd = potentials[1]
                        if len(potentials[1]) > 1:
                            mirrors = [set(binaryRelation([x])) for x in potentials[1]]
                            nodesToAdd += [s for s in superCover(mirrors, list(G.nodes)) if s not in nodesToAdd]
                            pairsToRemove += [Edges[l][x][0] for l in nodesToAdd for x in range(len(Edges[l])) if l not in potentials[1]]
                            pairsToRemove = list(set(pairsToRemove))
                        
                        tempNodes = [n for n in list(set(curP + binaryRelation(nodesToAdd))) if n not in remEdges + pairsToRemove and (n[1], n[0]) not in remEdges + pairsToRemove + curP]

                        P = get_linear_extensions(binaryToCover(tempNodes, len(self.upsilon[0])))
                        if VERIFY(P, curLE + [p for p in nodesToAdd if p not in curLE]):
                            curP = tempNodes
                            curLE += [p for p in nodesToAdd if p not in curLE]
                            nodes = [n for n in nodes if n not in curLE]
                            remEdges += pairsToRemove
                            break
                        elif i >= len(potentialNodes):
                            cond = 0
                        i += 1

                    if len(potentialNodes) == 0:
                        cond=0

                nodes = [n for n in nodes if n not in curLE]

                for le in curLE:
                    G.remove_node(le)

                Pset.append(curP)
            else:
                break  # Exit the loop if numNeighbors is empty

        return Pset

def main():
    sample_input = [
        12453, 12345, 13425, 13524, 12354, 12534, 12435, 14523, 14235, 13254, 13245, 14253
    ]
    
    count = 1
    for inputLinearOrders in sample_input:
        input_list = [int(x) for x in str(inputLinearOrders)]  # Convert integer to list
        print(f"Input: {input_list}")
        poset = Poset(input_list)
        posets = poset.poset_set
        if posets:
            for i, linear_order in enumerate(posets):
                print

