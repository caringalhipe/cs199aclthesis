import networkx as nx
from collections import defaultdict
from test2_utils import VERIFY, get_linear_extensions, binaryRelation, binaryToCover, superCover

def get_ancestors(node, poset):
    ancestors = set()
    stack = [node]
    while stack:
        n = stack.pop()
        for i in range(len(poset)):
            if i < len(poset[n]) and poset[n][i] == 1 and i not in ancestors:
                ancestors.add(i)
                stack.append(i)
    return ancestors

def get_descendants(node, poset):
    descendants = set()
    stack = [node]
    while stack:
        n = stack.pop()
        for i in range(len(poset)):
            if i < len(poset[n]) and poset[n][i] == 1 and i not in descendants:
                descendants.add(i)
                stack.append(i)
    return descendants

def dist(x, y, poset):
    try:
        graph = nx.DiGraph(poset)
        return nx.shortest_path_length(graph, source=x, target=y)
    except nx.NetworkXNoPath:
        return float('inf')

def psi(L, L_prime):
    return [(x, y) for x in L for y in L_prime if x != y]

def is_convex(L_prime, Y):
    for l in L_prime:
        if l not in Y:
            return False
    return True

def remove_pair_from_poset(poset, pair):
    poset[pair[0]][pair[1]] = 0
    return poset

def remove_related_pairs(I, pair, poset):
    ancestors = get_ancestors(pair[0], poset)
    descendants = get_descendants(pair[1], poset)
    return [(x, y) for (x, y) in I if x not in ancestors and y not in descendants]

def next_pair(I, previous_pair):
    for i, pair in enumerate(I):
        if pair == previous_pair:
            return I[i+1] if i+1 < len(I) else None
    return None


def Poset(upsilon):
    G = nx.DiGraph()

    for a in range(len(upsilon)):
        G.add_node(upsilon[a])

    for a in range(len(upsilon)):
        for b in range(a + 1, len(upsilon)):
            if len(upsilon[a]) == len(upsilon[b]) - 1 and set(upsilon[a]).issubset(set(upsilon[b])):
                G.add_edge(upsilon[a], upsilon[b])

    linear_extensions = get_linear_extensions(list(G.nodes))
    P_A = nx.adjacency_matrix(G).todense()

    return P_A, linear_extensions


def algorithm2(Y, P_A, A):
    P = [row[:] for row in P_A]  # Deep copy of P_A
    Y_cov = set(get_linear_extensions(P_A))  # Placeholder for covered set
    Y_uncov = set(Y) - Y_cov  # Uncovered set

    J = set()
    for (a, b) in A:
        ancestors_a = get_ancestors(a, P_A)
        descendants_b = get_descendants(b, P_A)
        for x in ancestors_a.union({a}):
            for y in descendants_b.union({b}):
                J.add((x, y))
    J = sorted(J, key=lambda pair: dist(pair[0], pair[1], P_A))
    I = J.copy()

    current_pair = I[0] if I else None
    while current_pair:
        x, y = current_pair
        L = {L for L in Y_cov if x < y in L}
        L_prime = {L_prime for L_prime in Y_uncov if any((x, y) in psi(L, L_prime) for L in L)}
        if len(L) == len(L_prime):
            if is_convex(L_prime, Y):
                P = remove_pair_from_poset(P, (x, y))
                Y_cov.update(L_prime)
                Y_uncov.difference_update(L_prime)
            else:
                I = remove_related_pairs(I, (x, y), P_A)
        else:
            I = remove_related_pairs(I, (x, y), P_A)
        
        previous_pair = current_pair
        current_pair = next_pair(I, previous_pair)
        if not current_pair or dist(current_pair[0], current_pair[1], P_A) - dist(previous_pair[0], previous_pair[1], P_A) > 1:
            break

    # Convert J to edge list format
    edge_list = [(pair[0], pair[1]) for pair in J]

    # Create a directed graph from the edge list
    graph = nx.DiGraph()
    graph.add_edges_from(edge_list)

    return P

def main():
    sample_input = [
        '12345', '12435', '12453', '12534', '13245', '13254', 
        '13425', '13452', '13524', '13542', '14235', '14253', '14325', 
        '14352', '14523', '14532', '15423'
    ]
    
    P_A, linear_extensions = Poset(sample_input)
    A = [(2, 4), (5, 2)]  # Example anchor pairs, should be replaced with actual pairs

    output = algorithm2(sample_input, P_A, A)
    print(output)

if __name__ == "__main__":
    main()
