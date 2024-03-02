class PosetCover {
    constructor(linearOrders) {
        this.inputLinearOrders = linearOrders;
        this.poset = null;
    }

    getPoset() {
        return this.poset;
    }

    getOnePoset() {
        const tempPoset = this.inputLinearOrders[0];
        const n = tempPoset.getNumElement();
        const tempRelation = tempPoset.getRelation();
        const relation = new Array(n + 1).fill(0).map(() => new Array(n + 1).fill(0));
        for (let i = 1; i <= n; i++) {
            for (let j = 1; j <= n; j++) {
                relation[i][j] = tempRelation[i][j];
            }
        }
        let curRelation;
        for (let k = 1; k < this.inputLinearOrders.length; k++) {
            curRelation = this.inputLinearOrders[k].getRelation();
            for (let a = 1; a <= n; a++) {
                for (let b = 1; b <= n; b++) {
                    if (relation[a][b] === 1 && curRelation[b][a] === 1) {
                        relation[a][b] = 0;
                    }
                }
            }
        }
        this.poset = new Poset(relation, n);
        return this.poset;
    }

    isOnePosetCover() {
        const poset1 = this.getOnePoset();
        const n = poset1.getNumElement();
        poset1.generateCoverRelation();
        const coverRelation = poset1.getCoverRelation();
        const g = new GenLE(n);
        for (let i = 1; i <= n; i++) {
            for (let j = 1; j <= n; j++) {
                if (coverRelation[i][j] === 1) {
                    g.addEdge(i - 1, j - 1);
                }
            }
        }
        g.alltopologicalSorts();

        const les = g.getAllTopologicalSort();
        if (les.length !== this.inputLinearOrders.length) {
            return false;
        }
        for (const le of les) {
            const relation = new Array(le.length + 1).fill(0).map(() => new Array(le.length + 1).fill(0));
            let x, y;
            for (let i = 0; i < le.length; i++) {
                x = le[i];
                for (let j = i + 1; j < le.length; j++) {
                    y = le[j];
                    relation[x][y] = 1;
                }
            }
            const poset2 = new Poset(relation, n);
            let k = 0;
            for (; k < this.inputLinearOrders.length; k++) {
                if (Utilities.isEqualPoset(this.inputLinearOrders[k], poset2)) {
                    break;
                }
            }
            if (k === this.inputLinearOrders.length) {
                return false;
            }
        }
        return true;
    }

    printInputLinearOrders() {
        let p;
        for (let i = 0; i < this.inputLinearOrders.length; i++) {
            p = this.inputLinearOrders[i];
            p.generateCoverRelation();
            p.printCoverRelation();
        }
    }
}

