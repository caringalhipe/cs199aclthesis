import networkx as nx
from collections import defaultdict

# Convert a linear order to its binary relation
def linear_order_to_binary_relation(order):
    """
    Takes a linear order as input and returns its binary relation as a list of tuples.
    """
    n = len(order)
    relation = []
    for i in range(n):
        for j in range(i + 1, n):
            relation.append((int(order[i]), int(order[j])))
    return sorted(relation, key=lambda x: (x[0], x[1]))

# Generate binary relations from input linear orders
def binaryRelation(input):
    P = []
    for linear_order in input:
        binaryRel = linear_order_to_binary_relation(linear_order)
        P += binaryRel
    return P

# Convert binary relation to cover relation
def binaryToCover(P, n):
    coverRelations = []
    for (u, v) in P:
        if (u, v) in coverRelations:
            continue
        if len(coverRelations) == n - 1:
            break
        transitive = False
        for w in range(1, n + 1):
            if w == u or w == v:
                continue
            else:
                if (u, w) in P and (w, v) in P:
                    transitive = True
                    break
        if not transitive:
            coverRelations.append((u, v))
    return sorted(coverRelations)

# Check for tail in posets
def checkerTail(P1, P2, a, b):
    V = getVertices(P1)
    for x in V:
        if (b, x) in P1 or (a, x) in P2:
            return False
    return True

# Get difference between two posets
def getDifference(P1, P2):
    return [x for x in P1 if x not in P2]

# Get vertices of a poset
def getVertices(P):
    return list(set([x for t in P for x in t]))

# Combine two posets
def combinePoset(P1, P2):
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
    elif len(P3) == 1:
        P3_ele = P3[0]
        a, b = P3_ele[0], P3_ele[1]
        if (b, a) in P4 and set(getDifference(P1, P3)) == set(getDifference(P2, P4)):
            P = getDifference(P1, P3)
            return P
    elif len(P4) == 1:
        P4_ele = P4[0]
        a, b = P4_ele[0], P4_ele[1]
        if (b, a) in P3 and set(getDifference(P1, P3)) == set(getDifference(P2, P4)):
            P = getDifference(P1, P3)
            return P
    return None

# Generate all linear extensions of a cover relation
def get_linear_extensions(cover_relation):
    G = nx.DiGraph()
    for a, b in cover_relation:
        G.add_edge(a, b)
    sortings = list(nx.all_topological_sorts(G))
    return sorted([''.join(map(str, sorting)) for sorting in sortings])

# Verify if two sets of linear orders are the same
def VERIFY(P, Y):
    # Check if Y is a subset of P
    if all(item in P for item in Y):
        return True
    return False

# Create a transposition graph for linear orders
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
        for b in range(a + 1, l):
            pairs = [upsilon[a][i:i + 2] for i in range(len(upsilon[a])) if "".join(reversed(upsilon[a][i:i + 2])) in upsilon[b] and 
                     upsilon[a][0:i] + upsilon[a][i + 2:len(upsilon[a])] == upsilon[b][0:i] + upsilon[b][i + 2:len(upsilon[b])]]
            if len(pairs) > 0:
                G.add_edge(upsilon[a], upsilon[b], label=str(sorted([pairs[0][0], pairs[0][1]])))
                Edges[upsilon[a]].append([tuple(sorted((pairs[0][0], pairs[0][1]))), upsilon[b]])
                Edges[upsilon[b]].append([tuple(sorted((pairs[0][0], pairs[0][1]))), upsilon[a]])
    for n in list(G.nodes):
        Neighbors[n] = list(G.neighbors(n))
    if len(Neighbors) > 0:
        numNeighbors = [[len(Neighbors[l]), l] for l in Neighbors]
        numNeighbors = sorted(numNeighbors, key=lambda l: l[0])
        startNode = numNeighbors[0][1]
        finalNodes = [startNode] + [Edges[startNode][n][1] for n in range(len(Edges[startNode]))]
        anchorPairs = [tuple(Edges[startNode][n][0]) for n in range(len(Edges[startNode]))]
        cond = 1
        while (cond):
            potentialPairs = []
            for node in finalNodes:
                potentialPairs += [(Edges[node][n][0][0], Edges[node][n][0][1]) for n in range(len(Edges[node]))]
            potentialPairs = [p for p in potentialPairs if p not in anchorPairs]
            d = defaultdict(lambda: 0)
            for i in range(len(potentialPairs)):
                d[potentialPairs[i]] += 1
            potentialPairs.sort(key=lambda x: (-d[x], x), reverse=False)
            if len(potentialPairs) > 0:
                anchor = potentialPairs[0]
                curFinalNodes = []
                for node in finalNodes:
                    curFinalNodes += [Edges[node][n][1] for n in range(len(Edges[node])) if Edges[node][n][0] == anchor and Edges[node][n][1] not in finalNodes]
                if len(curFinalNodes) > 0:
                    finalNodes += curFinalNodes
                    anchorPairs += anchor
                else:
                    cond = 0
            else:
                cond = 0
        nodes = finalNodes + [l for l in upsilon if l not in finalNodes]
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, with_labels=True, font_size=10, node_size=500, node_color='#9CE5FF')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'))
        p.show()
    return nodes

# Given linear orders, return their super cover
def superCover(mirrors, upsilon):
    P = set.intersection(*mirrors)
    if set(get_linear_extensions(binaryToCover(P, len(upsilon[0])))) <= set(upsilon):
        return get_linear_extensions(binaryToCover(P, len(upsilon[0])))
    else:
        return []

def isPoset(P):
    """
    Check if the given relation P defines a valid poset.
    
    Parameters:
    P (list of tuples): A list of pairs representing the partial order relations.
    
    Returns:
    bool: True if P is a valid poset, False otherwise.
    """
    V = getVertices(P)

    # Create dictionaries to store predecessors and successors
    prec = {v: set() for v in V}
    succ = {v: set() for v in V}
    
    for a, b in P:
        succ[a].add(b)
        prec[b].add(a)
    
    # Check reflexivity
    for v in V:
        if v not in succ[v]:
            succ[v].add(v)
        if v not in prec[v]:
            prec[v].add(v)
    
    # Check antisymmetry
    for a in V:
        for b in succ[a]:
            if a != b and a in succ[b]:
                return False
    
    # Check transitivity
    for a in V:
        for b in succ[a]:
            for c in succ[b]:
                if c not in succ[a]:
                    return False
    
    return True

def getVertices(P):
    """
    Get all unique vertices from the relations in P.
    
    Parameters:
    P (list of tuples): A list of pairs representing the partial order relations.
    
    Returns:
    list: A list of unique vertices.
    """
    return list(set([x for pair in P for x in pair]))


