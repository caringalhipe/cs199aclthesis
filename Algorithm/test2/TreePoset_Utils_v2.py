import networkx as nx
# from classes import Poset
import pylab as p
from collections import defaultdict

# creates an object/class Poset for each linear order
def binaryRelation(input):
    P = []
    for linear_order in input:
        binaryRel = linear_order_to_binary_relation(linear_order)
        # poset = Poset(binaryRel, linear_order)
        P += binaryRel
    return P

# given a linear order, get its corresponding binary relation
def linear_order_to_binary_relation(order):
    """
    Takes a linear order as input and returns its binary relation as a list of tuples.
    """
    n = len(order)
    relation = []
    for i in range(n):
        for j in range(i+1, n):
            relation.append((int(order[i]), int(order[j])))
    relation = sorted(relation, key=lambda x: (x[0], x[1]))  # Sort the relation in ascending order

    return relation

# Example usage:
# order = '14235'
# relation = linear_order_to_binary_relation(order)
# print(relation)

def binaryToCover(P,n):
    coverRelations = []
    for (u,v) in P:
        if (u,v) in coverRelations:
            continue
        if len(coverRelations) == n - 1:
            break
        transitive = False
        for w in range(1, n+1):
            if w == u or w == v:
                continue
            else:
                if (u,w) in P and (w,v) in P:
                    transitive = True
                    break
        if not transitive:
            coverRelations.append((u,v))
    return sorted(coverRelations)

# returns True if (b, x) not in P1 and (a, x) not in P2
def checkerTail(P1, P2, a, b):
    V = getVertices(P1)
    for x in V:
        if (b, x) in P1 or (a, x) in P2:
            return False
    return True

# returns P1 - P2
def getDifference(P1, P2):
    return [x for x in P1 if x not in P2]

# given a poset -- a list of tuples -- returns V that contains all elements of poset
def getVertices(P):
    return list(set([x for t in P for x in t]))

# given a poset -- a list of tuples -- returns the root of the poset
def getRoot(P):
    index_1_elements = {t[1] for t in P}
    all_elements = {x for t in P for x in t}
    return list(all_elements - index_1_elements)[0]


# returns True if poset P is a Tree Poset
def isTreePoset(P):
    V = getVertices(P)
    root = getRoot(P)

    prec = [0 for i in range(len(V))]
    succ = [0 for i in range(len(V))]

    for i in range(len(P)):
        prec[P[i][1] - 1] += 1
        succ[P[i][0] - 1] += 1
    
    # for i in range(len(V)):
    #     if i == root-1 and prec[i] == 0:
    #         continue

    if sum(prec) == sum(succ) and succ[root-1] > 0:
        return True

    return False

    
def combinePoset(P1, P2):
    P3 = getDifference(P1, P2)
    P4 = getDifference(P2, P1)

    if len(P1) == len(P2):
        if len(P3)!=1 or len(P4)!=1:
            return None
        
        P3_ele = P3[0]
        P4_ele = P4[0]
        a, b = P3_ele[0], P3_ele[1]
        c, d = P4_ele[0], P4_ele[1]

        if a != d or b != c:
            return None
        
        P = getDifference(P1, P3)
        return P
    
    elif len(P3) > 1 and len(P4) > 1:
        return None
    elif len(P3) == 1:
        P3_ele = P3[0]
        a, b = P3_ele[0], P3_ele[1]

        # if (b,a) in P4 and checkerTail(P1, P2, a, b) and getDifference(P1, P3) == getDifference(P2, P4):
        #     P = getDifference(P1, P3)
        if (b, a) in P4 and set(getDifference(P1, P3)) == set(getDifference(P2, P4)):
            P = getDifference(P1, P3)
            return P
    elif len(P4) == 1:
        P4_ele = P4[0]
        a, b = P4_ele[0], P4_ele[1]
         
        if (b, a) in P3 and set(getDifference(P1, P3)) == set(getDifference(P2, P4)):
            P = getDifference(P1, P3)
            return P
    # if isTreePoset(P):
    return None

def combinePosetv2(P1, P2):
    # check first if same root
    if getRoot(P1) != getRoot(P2):
        return None
    P3 = getDifference(P1, P2)
    P4 = getDifference(P2, P1)

    if len(P1) == len(P2):
        if len(P3) != 1 or len(P4) != 1:
            return None
        
        P3_ele = P3[0]
        P4_ele = P4[0]
        a, b = P3_ele[0], P3_ele[1]
        c, d = P4_ele[0], P4_ele[1]

        if a != d or b != c:
            return None
        
        P = getDifference(P1, P3)
        return P

    elif len(P3) > 1 and len(P4) > 1:
        return None
    
    else:
        if len(P3) == 1:
            P3_ele = P3[0]
            a, b = P3_ele[0], P3_ele[1]

            P1_temp = P1.copy()
            P2_temp = P2.copy()
            P1_temp.remove((a, b))
            P2_temp.remove((b, a))

            if (b, a) not in P4:
                return None
            elif set(P1_temp).issubset(set(P2_temp)):
                P = getDifference(P1, P3)
                return P
        elif len(P4) == 1:
            P4_ele = P4[0]
            a, b = P4_ele[0], P4_ele[1]

            P1_temp = P1.copy()
            P2_temp = P2.copy()
            P1_temp.remove((b, a))
            P2_temp.remove((a, b))

            if (b, a) not in P3:
                return None
            elif set(P2_temp).issubset(set(P1_temp)):
                P = getDifference(P1, P3)
                return P 
            
            

    


# P1 = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
# P2 = [(1, 2), (1, 4), (1, 3), (2, 4), (2, 3), (4, 3)]

# P1 = [(1, 2), (1, 3), (1, 4), (2, 4), (3, 2), (3, 4)]
# P2 = [(1, 2), (1, 3), (1, 4), (3, 2), (3, 4), (4, 2)]
# P2 = [(1, 2), (1, 3), (1, 4), (2, 3), (4, 2), (4, 3)]
# P1 = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4)]

# P1 = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4)]
# P2 = [(1, 2), (1, 3), (1, 4), (3, 2), (3, 4)] 

# P1 = [(1, 2), (1, 3), (1, 4), (2, 4), (3, 2), (3, 4)]
# P2 = [(1, 2), (1, 3), (1, 4), (3, 2), (3, 4), (4, 2)]

# unbalanced P1 and P2
# P1 = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4)]
# P2 = [(1, 2), (1, 3), (1, 4), (2, 3), (4, 2), (4, 3)]

# P1 = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4)]
# P2 = [(1, 2), (1, 3), (1, 4), (2, 4), (3, 2), (3, 4)]

# P1 = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 5)]
# P2 = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (3, 2), (3, 4), (3, 5)]
# p = combinePosetv2(P1, P2)
# if p != None:
#     print(p)
# else:
#     print("No returned poset")

def gen_tree_poset(upsilon):    
    Ptree = []
    m = len(upsilon)     
    n = len(upsilon[0])

    minRank = [0 for i in range(n)]
    numCoverRelation = 0
    coverRelationP = []

    nextset = False
    canBeImproved = True
    while canBeImproved:
        canBeImproved = False
        nextset = False
        for h in range(m, 0, -1):
            if nextset:
                break
            for i in range(1,n):
                for j in range(h):
                    v2 = rankInverse(i, upsilon[j])
                    if minRank[int(v2)-1] == 0:
                        v1 = rankInverse(i-1, upsilon[j])
                        coverRelationP.append((int(v1),int(v2)))
                        minRank[int(v2)-1] = i
                        minRank[int(v1)-1] = i-1
                        numCoverRelation +=1
                if numCoverRelation == n-1:
                    P = get_linear_extensions(coverRelationP)
                    if VERIFY(P, upsilon[:h]):
                        Ptree.append(coverRelationP)
                        upsilon = upsilon[h:]
                        if len(upsilon) > 0:
                            m = len(upsilon)     
                            n = len(upsilon[0])
                        minRank = [0 for i in range(n)]
                        numCoverRelation = 0
                        coverRelationP = []
                        nextset = True
                        if len(upsilon) < 1:
                            canBeImproved = False
                        else:
                            canBeImproved = True
                        break
                    else:
                        minRank = [0 for i in range(n)]
                        numCoverRelation = 0
                        coverRelationP = []
                        break

    # if VERIFY(P, upsilon):
    return Ptree

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

def rankInverse(index, linearOrder): # where rank gives the position of an element, inverse gives the element in a position
    # sample input: index = 3; linearOrder = 1234; 
    return linearOrder[index]       # output: 4

def group_linearOrders_by_its_root(upsilon):
    grouped_upsilon = {}
    for linearOrder in upsilon:
        root = linearOrder[0]
        if root in grouped_upsilon:
            grouped_upsilon[root].append(linearOrder)
        else:
            grouped_upsilon[root] = [linearOrder]
    
    return list(grouped_upsilon.values())

def form_transposition_graph(upsilon):
    G = nx.Graph()
    l = len(upsilon)
    nodes = upsilon
    Neighbors = dict([])
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
                Edges[upsilon[a]].append([tuple(sorted((pairs[0][0],pairs[0][1]))), upsilon[b]])
                Edges[upsilon[b]].append([tuple(sorted((pairs[0][0],pairs[0][1]))), upsilon[a]])
                #print("Nodes", upsilon[a], upsilon[b])
                #print("Added edge/s", pairs)

    for n in list(G.nodes):
        #print(n,"-", list(G.neighbors(n)))
        Neighbors[n]=list(G.neighbors(n))
    #print("Nodes:", list(G.nodes))

    if len(Neighbors)>0:
        numNeighbors = [[len(Neighbors[l]),l] for l in Neighbors]
        numNeighbors = sorted(numNeighbors, key = lambda l: l[0])
        startNode = numNeighbors[0][1]
        finalNodes = [startNode]+[Edges[startNode][n][1] for n in range(len(Edges[startNode]))]
        anchorPairs = [tuple(Edges[startNode][n][0]) for n in range(len(Edges[startNode]))]
        #print("Final nodes:",finalNodes)
        #print("Remaining nodes:", [n for n in upsilon if n not in finalNodes])
        #print("Anchor Pairs:",anchorPairs)

        cond = 1
        while (cond):
            # Obtain potential anchor pairs to extend from
            potentialPairs = []
            for node in finalNodes:
                potentialPairs += [(Edges[node][n][0][0], Edges[node][n][0][1]) for n in range(len(Edges[node]))]
            
            potentialPairs = [p for p in potentialPairs if p not in anchorPairs]

            # Sort pairs by frequency
            d = defaultdict(lambda: 0)
            for i in range(len(potentialPairs)):
                d[potentialPairs[i]] += 1
            
            potentialPairs.sort(key=lambda x: (-d[x], x), reverse = False) 
            
            #print("Potential pairs:",potentialPairs)

            # Extend by most frequent pair (likely to be a mirror)
            if len(potentialPairs)>0:
                anchor = potentialPairs[0]
                #print("Edges:",Edges)
                #print(anchor)
                curFinalNodes = []
                for node in finalNodes:
                    curFinalNodes += [Edges[node][n][1] for n in range(len(Edges[node])) if Edges[node][n][0]==anchor and Edges[node][n][1] not in finalNodes]

                if len(curFinalNodes)>0:
                    finalNodes += curFinalNodes
                    anchorPairs += anchor
                else:
                    cond = 0
            else:
                cond = 0

        nodes = finalNodes + [l for l in upsilon if l not in finalNodes]

        '''
        edges = nx.bfs_edges(G, numNeighbors[0][1])
        nodes = [numNeighbors[0][1]] + [v for u, v in edges]
        nodes += [l for l in upsilon if l not in nodes]
        '''

        #print(numNeighbors)
        print(nodes)
        #print(Edges)
        
        
        # For drawing the transposition graphs
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, with_labels=True,font_size=10, node_size=500, node_color='#9CE5FF')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))

        p.show()
    return nodes
  
def superCover(mirrors, upsilon):
    P = set.intersection(*mirrors)

    if set(get_linear_extensions(binaryToCover(P,len(upsilon[0])))) <= set(upsilon):
        return get_linear_extensions(binaryToCover(P,len(upsilon[0])))
    else:
        return []

