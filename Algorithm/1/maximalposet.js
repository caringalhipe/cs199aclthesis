class GetMaximalPoset {
    constructor(hspace, tgraph, arrPairs) {
        this.input = [];
        this.onePosetCovers = [];
        this.solutions = [];
        this.maximalPoset = null;
        this.n = hspace.getNumElement();
        this.relation = hspace.getRelation();
        this.anchorPairs = arrPairs;
        this.halfspace = hspace;
    }

    executeAlgo() {
        this.maximalPoset = new Poset(this.relation, this.n);
        this.maximalPoset.generateCoverRelation();
        const hsCoverRelation = this.maximalPoset.getCoverRelation();
        const g = new GenLE(this.n);
        for (let i = 1; i <= this.n; i++) {
            for (let j = 1; j <= this.n; j++) {
                if (hsCoverRelation[i][j] === 1) {
                    g.addEdge(i - 1, j - 1);
                }
            }
        }
        g.alltopologicalSorts();
        const curLEs = g.getAllLinearOrders();
        const distMat = [];
        for (let i = 0; i < this.anchorPairs.length; i++) {
            const curPair = this.anchorPairs[i];
            const dist = Utilities.getShortestDistByLinearOrdering(hsCoverRelation, curPair.x, curPair.y);
            if (dist > -1) {
                distMat[dist - 1].push(curPair);
            }
        }
        for (let i = 0; i < this.anchorPairs.length; i++) {
            const anchor = this.anchorPairs[i];
            const a = anchor.x;
            const b = anchor.y;
            const leqA = [a];
            const geqB = [b];
            for (let j = 1; j <= this.n + 1; j++) {
                if (this.relation[j][a] === 1) {
                    leqA.push(j);
                }
            }
            for (let j = 1; j <= this.n + 1; j++) {
                if (this.relation[b][j] === 1) {
                    geqB.push(j);
                }
            }
            for (let k = 0; k < leqA.length; k++) {
                const curA = leqA[k];
                for (let l = 0; l < geqB.length; l++) {
                    const curB = geqB[l];
                    const dist = Utilities.getShortestDistByLinearOrdering(hsCoverRelation, curA, curB);
                    if (dist > -1) {
                        distMat[dist - 1].push(new Pair(curA, curB));
                    }
                }
            }
        }

        /*
		 * for (int i=o; i<distMat.size(); i++) { ArrayList<Pair> curDistPairs =
		 * distMat.get(i); for (int j=0; j<curDistPairs.size();j++) { //getMirror //if
		 * one mirror does not exist continue //getConvex //if convex does not exist
		 * continue //extend
		 * 
		 * } }
		 */
		//for each pair, determine if it is extendible
		
		//stop until dist(nextPair)- dist(prevPair) > 1
        
        return this.maximalPoset;
    }

    getABMirror(los, ab) {
        const mirror = [];
        for (let i = 0; i < los.length; i++) {
            const lo = los[i];
            const covRel = lo.getCoverRelation();
        }
        return mirror;
    }

    doesMirrorExist() {
        return true;
    }

    doesConvexExist() {
        return true;
    }
}

