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
def binaryToCover(binary_relations, n):
    matrix = [[0]*n for _ in range(n)]
    for a, b in binary_relations:
        if 0 <= a < n and 0 <= b < n:
            matrix[a][b] = 1
    return matrix

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
# poset_utils.py

def get_linear_extensions(cover_relation):
    # Ensure cover_relation contains pairs (tuples of two elements)
    cover_relation = [tuple(pair) for pair in cover_relation if len(pair) == 2]

    def dfs(current, visited, stack, graph):
        visited[current] = True
        for neighbor in graph[current]:
            if not visited[neighbor]:
                dfs(neighbor, visited, stack, graph)
        stack.insert(0, current)

    # Create a graph from the cover relations
    elements = set()
    for a, b in cover_relation:
        elements.add(a)
        elements.add(b)

    graph = {element: [] for element in elements}
    for a, b in cover_relation:
        graph[a].append(b)

    visited = {element: False for element in elements}
    stack = []

    for element in elements:
        if not visited[element]:
            dfs(element, visited, stack, graph)

    return stack


# Verify if two sets of linear orders are the same
def VERIFY(P, Y):
    return sorted(P) == sorted(Y)

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


