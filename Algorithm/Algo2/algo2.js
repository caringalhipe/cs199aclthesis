class GetMaximalPoset {
    constructor(halfspace, transposition_graph, anchor_pairs) {
        this.n = halfspace.getNumElement();
        this.relation = halfspace.getRelation();
        this.anchorPairs = anchor_pairs;
        this.halfspace = halfspace;
    }

    executeAlgo() {
        const maximalPoset = new Poset(this.relation, this.n);
        maximalPoset.generateCoverRelation();
        const hsCoverRelation = maximalPoset.getCoverRelation();

        const g = new GenLE(this.n);
        for (let i = 1; i <= this.n; i++) {
            for (let j = 1; j <= this.n; j++) {
                if (hsCoverRelation[i][j] === 1) {
                    g.addEdge(i - 1, j - 1);
                }
            }
        }
        g.allTopologicalSorts();

        const curLEs = g.getAllLinearOrders();
        const distMat = new Array(this.n).fill([]);  // Initialize distance matrix

        for (const anchor of this.anchorPairs) {
            const { x, y } = anchor;
            const dist = getShortestDistByLinearOrdering(hsCoverRelation, x, y);
            if (dist > -1) {
                distMat[dist - 1].push(anchor);
            }
        }

        for (const anchor of this.anchorPairs) {
            const { x, y } = anchor;
            const leqA = [x];
            const geqB = [y];
            for (let j = 1; j <= this.n + 1; j++) {
                if (this.relation[j][x] === 1) {
                    leqA.push(j);
                }
                if (this.relation[y][j] === 1) {
                    geqB.push(j);
                }
            }
            for (const curA of leqA) {
                for (const curB of geqB) {
                    const dist = getShortestDistByLinearOrdering(hsCoverRelation, curA, curB);
                    if (dist > -1) {
                        distMat[dist - 1].push(new Pair(curA, curB));
                    }
                }
            }
        }

        // Finish the implementation
        // For each pair, determine if it is extendable
        // Stop until dist(nextPair) - dist(prevPair) > 1

        return maximalPoset;
    }
}
