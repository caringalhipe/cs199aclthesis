import networkx as nx
import pylab as p
from collections import defaultdict
from poset_utils import VERIFY, get_linear_extensions, binaryRelation, binaryToCover, superCover, isPoset

def check_swap(u, v):
    for i in range(len(u) - 1):
        if u[i:i + 2] == v[i:i + 2][::-1]:
            return u[i:i + 2]
    return None

def Poset(upsilon, P_initial, A):
    Pset = []

    # Generate Transposition Graph
    G = nx.Graph()
    anchors = []
    N = len(upsilon)

    for i in range(N):
        G.add_node(upsilon[i])
        for j in range(i + 1, N):
            adjacent = check_swap(upsilon[i], upsilon[j])
            if adjacent:
                G.add_edge(upsilon[i], upsilon[j], label=adjacent, color='k')

    nodes = upsilon
    Edges = defaultdict(list)

    for u in upsilon:
        for a in range(N):
            for b in range(a + 1, N):
                pairs = [u[i:i + 2] for i in range(len(u)) if "".join(reversed(u[i:i + 2])) in upsilon[b] and 
                         u[0:i] + u[i + 2:] == upsilon[b][0:i] + upsilon[b][i + 2:]]
                if pairs:
                    pair = pairs[0]
                    G.add_edge(u, upsilon[b], label=str(sorted([pair[0], pair[1]])))
                    Edges[u].append([tuple(sorted((int(pair[0]), int(pair[1])))), upsilon[b]])
                    Edges[upsilon[b]].append([tuple(sorted((int(pair[0]), int(pair[1])))), u])

    # Initialization with P_initial
    Υ_cov = [u for u in upsilon if all(str(pair[0]) in u and str(pair[1]) in u and u.index(str(pair[0])) < u.index(str(pair[1])) for pair in P_initial)]
    Υ_uncov = [u for u in upsilon if u not in Υ_cov]
    P = P_initial
    J = sorted([(u[i], u[i + 1]) for u in upsilon for i in range(len(u) - 1) if u[i] != u[i + 1]], key=lambda pair: pair[0])
    I = J
    nextPair = I[0] if I else None

    while I:
        (x, y) = nextPair
        L = [u for u in Υ_cov if x in u and y in u and u.index(x) < u.index(y)]
        L_prime = [u for u in Υ_uncov if x in u and y in u and u.index(x) < u.index(y)]

        if len(L) == len(L_prime):
            if all(u in upsilon for u in L_prime):
                P = binaryRelation(L_prime)
                Υ_cov = [u for u in Υ_cov if u in L_prime]
                Υ_uncov = [u for u in Υ_uncov if u not in L_prime]
            else:
                I = [(u[i], u[i + 1]) for u in Υ_cov for i in range(len(u) - 1) if u[i] == x or u[i + 1] == y and u[i] != u[i + 1]]
        else:
            I = [(u[i], u[i + 1]) for u in Υ_uncov for i in range(len(u) - 1) if u[i] == x or u[i + 1] == y and u[i] != u[i + 1]]

        prevPair = nextPair
        if I:
            nextPair = I[0]
        else:
            break

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True, font_size=10, node_size=500, node_color='#9CE5FF')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'))
    p.show()

    return Pset

def main():
    sample_input = [
        '14523', '14253', '14235', '12453', '12435', '12345', '13245', '13425',
        '12354', '12534', '13254', '13524'
    ]
    P_initial = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (3, 2), (3, 4), (3, 5), (5, 2), (5, 4)]  # Initial P

    # Get user input for A
    #A_input = input("Enter the pairs for A in the format (x, y), (a, b), ... : ")
    A = ((5, 2), (2, 4))

    output = Poset(sample_input, P_initial, A)
    for poset in output:
        print(poset)

if __name__ == "__main__":
    main()
