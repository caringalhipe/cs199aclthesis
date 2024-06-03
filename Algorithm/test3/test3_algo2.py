import networkx as nx
from collections import defaultdict, deque
from test3_utils import linear_order_to_binary_relation, binaryRelation, binaryToCover, get_linear_extensions, VERIFY, superCover

def dist(x, y, PA):
    # BFS to find shortest path from x to y in PA
    if x == y:
        return 0
    visited = set()
    queue = deque([(x, 0)])
    while queue:
        current, d = queue.popleft()
        if current == y:
            return d
        visited.add(current)
        for neighbor in PA.get(current, []):
            if neighbor not in visited:
                queue.append((neighbor, d + 1))
    return -1  # No path found

def ancestors(x, PA):
    result = set()
    stack = [x]
    while stack:
        node = stack.pop()
        for parent in PA.get(node, []):
            if parent not in result:
                result.add(parent)
                stack.append(parent)
    return result

def descendants(y, PA):
    result = set()
    reverse_PA = defaultdict(list)
    for node, children in PA.items():
        for child in children:
            reverse_PA[child].append(node)
    
    stack = [y]
    while stack:
        node = stack.pop()
        for child in reverse_PA[node]:
            if child not in result:
                result.add(child)
                stack.append(child)
    return result

def algo2(Y, A, PA):
    # Step 1: Initialization
    P = PA.copy()  # Copy to avoid mutating the input PA directly
    Ycov = get_linear_extensions(P)
    Yuncov = [L for L in Y if L not in Ycov]

    J = set()
    for (ai, bi) in A:
        xi = ancestors(ai, PA) | {ai}
        yi = descendants(bi, PA) | {bi}
        for x in xi:
            for y in yi:
                J.add((x, y))

    J = sorted(J, key=lambda pair: dist(pair[0], pair[1], PA))
    I = J

    # Step 2: Main Loop
    currentPair = I[0] if I else None

    while currentPair:
        (x, y) = currentPair
        L = [L for L in Ycov if (x, y) in linear_order_to_binary_relation(L)]
        L_prime = [L for L in Yuncov if (x, y) in linear_order_to_binary_relation(L)]

        if len(L) == len(L_prime):
            if all(l in Y for l in get_linear_extensions(binaryToCover(binaryRelation(L_prime), len(P)))):
                P = P + [(x, y)]
                Ycov = Ycov + get_linear_extensions(binaryToCover(binaryRelation(L_prime), len(P)))
                Yuncov = [L for L in Y if L not in Ycov]

                I = [pair for pair in I if not (pair[0] in ancestors(x, PA) and pair[1] in descendants(y, PA))]
            else:
                I = [pair for pair in I if not (pair[0] in ancestors(x, PA) and pair[1] in descendants(y, PA))]
        else:
            I = [pair for pair in I if not (pair[0] in ancestors(x, PA) and pair[1] in descendants(y, PA))]

        prevPair = currentPair
        currentPair = I[0] if I else None
        if currentPair and dist(currentPair[0], currentPair[1], PA) - dist(prevPair[0], prevPair[1], PA) > 1:
            break

    return P

# Sample input
Y = [
    '12345', '12435', '12453', '12534', '13245', '13254', 
    '13425', '13452', '13524', '13542', '14235', '14253', '14325', 
    '14352', '14523', '14532', '15423'
]
A = [(1, 2), (3, 4)]  # Sample anchor pairs
PA = {1: [2], 2: [3], 3: [4], 4: [5], 5: []}  # Sample initial poset

# Run the algorithm
poset = algo2(Y, A, PA)
print(poset)
