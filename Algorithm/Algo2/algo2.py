class GetMaximalPoset:
    def __init__(self, halfspace, transposition_graph, anchor_pairs):
        self.n = halfspace.get_num_elements()
        self.relation = halfspace.get_relation()
        self.anchor_pairs = anchor_pairs
        self.halfspace = halfspace

    def execute_algo(self):
        maximal_poset = Poset(self.relation, self.n)
        maximal_poset.generate_cover_relation()
        hs_cover_relation = maximal_poset.get_cover_relation()

        g = GenLE(self.n)
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                if hs_cover_relation[i][j] == 1:
                    g.add_edge(i - 1, j - 1)
        g.all_topological_sorts()

        cur_les = g.get_all_linear_orders()

        # Arrange pairs
        dist_mat = [[] for _ in range(self.n)]  # Initialize distance matrix
        for anchor in self.anchor_pairs:
            x, y = anchor.x, anchor.y
            dist = get_shortest_dist_by_linear_ordering(hs_cover_relation, x, y)
            if dist > -1:
                dist_mat[dist - 1].append(anchor)

        # Add ancestors
        for anchor in self.anchor_pairs:
            a, b = anchor.x, anchor.y
            leq_a = [a]
            geq_b = [b]
            for j in range(1, self.n + 2):
                if self.relation[j][a] == 1:
                    leq_a.append(j)
                if self.relation[b][j] == 1:
                    geq_b.append(j)
            for cur_a in leq_a:
                for cur_b in geq_b:
                    dist = get_shortest_dist_by_linear_ordering(hs_cover_relation, cur_a, cur_b)
                    if dist > -1:
                        dist_mat[dist - 1].append(Pair(cur_a, cur_b))

        # Finish the implementation
        # For each pair, determine if it is extendable
        # Stop until dist(nextPair) - dist(prevPair) > 1

        return maximal_poset
