import networkx as nx

def is_all_connected(P, n):
    for p in P:
        check_vertices = [False for x in range(n)]
        for (a, b) in p:
            check_vertices[a - 1] = True
            check_vertices[b - 1] = True
        if False not in check_vertices and nx.is_directed_acyclic_graph(nx.DiGraph(p)):
            continue
        else:
            return False
    return True

def binary_to_cover(P, n):
    cover_relations = []
    for (u, v) in P:
        if (u, v) in cover_relations:
            continue
        if len(cover_relations) == n - 1:
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
            cover_relations.append((u, v))
    return sorted(cover_relations)

def covered(group_posets):
    covered_linear_orders = []
    for poset in group_posets:
        covered_linear_orders += get_linear_extensions(poset)
    covered_linear_orders = [int(x) for x in list(set(covered_linear_orders))]
    return sorted(covered_linear_orders)

def generate_rooted_relations(parent, vertices, relations):
    if len(vertices) == 0:
        return [sorted(relations)]
    else:
        rels = []
        for child in vertices:
            new_vertices = [v for v in vertices if v != child]
            rels.extend(generate_rooted_relations(parent, new_vertices, relations + [(parent, child)]))
            rels.extend(generate_rooted_relations(parent, new_vertices, relations + [(child, parent)]))
            rels.extend(generate_rooted_relations(child, new_vertices, relations + [(parent, child)]))
            rels.extend(generate_rooted_relations(child, new_vertices, relations + [(child, parent)]))

        true_rels = []
        for rel in rels:
            if rel not in true_rels:
                true_rels.append(rel)

        return true_rels

def is_all_connected(vertices, relations):
    for vertex in vertices:
        is_connected = False
        for relation in relations:
            if vertex in relation:
                is_connected = True
                break

        if not is_connected:
            return False

    return True

def get_linear_extensions(cover_relation):
    G = nx.DiGraph()
    for a, b in cover_relation:
        G.add_edge(a, b)
    
    sortings = list(nx.all_topological_sorts(G))
    
    return sorted([''.join(map(str, sorting)) for sorting in sortings])

def verify(P, Y):
    return sorted(P) == sorted(Y)

def rank_inverse(index, linear_order):
    return linear_order[index]

def group_linear_orders_by_its_root(upsilon):
    grouped_upsilon = {}
    for linear_order in upsilon:
        root = linear_order[0]
        if root in grouped_upsilon:
            grouped_upsilon[root].append(linear_order)
        else:
            grouped_upsilon[root] = [linear_order]

    return list(grouped_upsilon.values())
