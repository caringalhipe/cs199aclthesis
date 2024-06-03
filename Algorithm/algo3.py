import networkx as nx
from collections import defaultdict, OrderedDict
from algo2 import Poset

# Copy the poset_utils.py functions here
# (VERIFY, get_linear_extensions, binaryRelation, binaryToCover, superCover)

def exact_k_poset_cover(Y, k):
    G = nx.Graph()
    for i, L in enumerate(Y):
        G.add_node(i, linear_order=L)

    for i in range(len(Y)):
        for j in range(i + 1, len(Y)):
            G.add_edge(i, j)

    A_star = []
    for a, b in G.edges():
        A_star.append({(a, b)})

    P_T_star = []
    for A in A_star:
        Y_A = [L for i, L in enumerate(Y) if all(a < b for (a, b) in A)]
        P_A = Poset(Y_A)
        if P_A is not None:
            P_i = Algorithm_2(Y, P_A, A)
            P_T_star.extend(P_i)

    for P_star in combinations(P_T_star, k):
        if set().union(*(get_linear_extensions(binaryToCover(P, len(Y[0]))) for P in P_star)) == set(Y):
            return P_star

    return None

def Algorithm_2(Y, P_A, A):
    P_i = Poset(Y)  # Call Poset function from algorithm2.py
    return P_i

def main():
    sample_input = [
        '12345', '12435', '12453', '12534', '13245', '13254', 
        '13425', '13452', '13524', '13542', '14235', '14253', '14325', 
        '14352', '14523', '14532', '15423'
    ]
    
    P_star_prime = exact_k_poset_cover(sample_input, 3)
    if P_star_prime is not None:
        print("Found Exact k-Poset Cover:")
        for i, P in enumerate(P_star_prime):
            print(f"P_{i+1}: {P}")
    else:
        print("No Exact k-Poset Cover found.")

if __name__ == "__main__":
    main()
