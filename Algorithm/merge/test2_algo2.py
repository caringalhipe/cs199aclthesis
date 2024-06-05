import networkx as nx
from collections import defaultdict, OrderedDict
import itertools

def mirror_linear_order(order, anchor):
    """
    Generate the mirror of a linear order with respect to a chosen anchor pair.

    Parameters:
    order (str): The linear order to be mirrored.
    anchor (tuple): The anchor pair to be mirrored with.

    Returns:
    str: The mirrored linear order.
    """
    a, b = anchor
    mirror_order = order.replace(str(a), 'X').replace(str(b), str(a)).replace('X', str(b))
    return mirror_order

def find_convex(graph, start, end):
    """
    Find the convex of the mirror of a linear order in the transposition graph.

    Parameters:
    graph (nx.Graph): The transposition graph.
    start (str): The start node of the linear order.
    end (str): The end node of the linear order.

    Returns:
    list: The convex nodes in the graph.
    """
    return list(nx.shortest_path(graph, start, end))

def build_transposition_graph(upsilon):
    """
    Build the transposition graph based on the input sequences.

    Parameters:
    upsilon (list of str): A list of strings representing the input sequences.

    Returns:
    nx.Graph: The transposition graph.
    """
    G = nx.Graph()
    l = len(upsilon)

    for a in range(l):
        G.add_node(upsilon[a])
        for b in range(a + 1, l):
            pairs = [upsilon[a][i:i + 2] for i in range(len(upsilon[a]) - 1) if
                     "".join(reversed(upsilon[a][i:i + 2])) in upsilon[b] and
                     upsilon[a][0:i] + upsilon[a][i + 2:len(upsilon[a])] == upsilon[b][0:i] + upsilon[b][
                                                                                                 i + 2:len(
                                                                                                     upsilon[b])]]
            if len(pairs) > 0:
                G.add_edge(upsilon[a], upsilon[b], label=str(sorted([pairs[0][0], pairs[0][1]])))

    return G

def find_least_common_poset(orders, posets):
    """
    Find the linear order with the least amount of common poset based on P_A.

    Parameters:
    orders (list of str): List of linear orders.
    posets (list of set): List of posets.

    Returns:
    str: The linear order with the least amount of common poset.
    """
    least_common_order = None
    min_common_posets = float('inf')

    for order in orders:
        common_posets = sum(1 for poset in posets if order in poset)
        if common_posets < min_common_posets:
            min_common_posets = common_posets
            least_common_order = order

    return least_common_order
"""
def extend_poset(poset, order, anchor, convex):

    mirror_order = mirror_linear_order(order, anchor)
    extended_poset = poset.union({(x, y) for x, y in zip(order, order[1:])})
    extended_poset = extended_poset.union({(x, y) for x, y in zip(mirror_order, mirror_order[1:])})
    extended_poset = extended_poset.union({(x, y) for x, y in zip(convex, convex[1:])})

    return extended_poset
"""
def extend_poset(poset, order, anchor, convex, A):
    """
    Extend the poset based on the linear order chosen with the given conditions.

    Parameters:
    poset (set): The current poset.
    order (str): The chosen linear order.
    anchor (tuple): The current set of anchor pairs.
    convex (list): The convex nodes in the graph.
    A (tuple): The set of anchor pairs.

    Returns:
    set: The extended poset.
    """
    mirror_order = mirror_linear_order(order, anchor)
    extended_poset = poset.union({(x, y) for x, y in zip(order, order[1:])})
    extended_poset = extended_poset.union({(x, y) for x, y in zip(mirror_order, mirror_order[1:])})
    extended_poset = extended_poset.union({(x, y) for x, y in zip(convex, convex[1:])})

    # Filter newly added linear orders based on the conditions in A
    new_linear_orders = []
    for x, y in zip(order, order[1:]):
        if abs(order.index(x) - order.index(y)) == 1 and ((x, y) in A or (y, x) in A):
            new_linear_orders.append((x, y))
    print(new_linear_orders)

    # Add the newly filtered linear orders to the extended poset
    extended_poset = extended_poset.union(new_linear_orders)

    return extended_poset


def algorithm2(upsilon, P_A, A):
    """
    Perform algorithm 2 based on the provided inputs.

    Parameters:
    upsilon (list of str): A list of strings representing the input sequences.
    P_A (list of set): A list of posets.
    A (tuple): The current set of anchor pairs.

    Returns:
    set: The extended poset.
    """
    G = build_transposition_graph(upsilon)
    orders = list(G.nodes())

    least_common_order = find_least_common_poset(orders, P_A)
    mirror_order = mirror_linear_order(least_common_order, A)
    convex = find_convex(G, least_common_order, mirror_order)

    extended_poset = extend_poset(P_A[0], least_common_order, A, convex, A)
    return extended_poset

if __name__ == "__main__":
    # Example usage
    upsilon = [
        '12453', '12345', '13425', '13524', '12354', '12534', '12435', '14523', '14235', '13254', '13245', '14253'
    ]
    P_A = [{(1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (3, 2), (3, 4), (3, 5), (5, 2), (5, 4)}]
    A = ((5, 2), (5, 4))

    extended_poset = algorithm2(upsilon, P_A, A)
    print("Extended Poset:", extended_poset)
