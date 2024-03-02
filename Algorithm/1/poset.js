class Poset {
    constructor(relation, n) {
        this.relation = relation;
        this.numElem = n;
        this.coverRelation = new Array(n + 1).fill(0).map(() => new Array(n + 1).fill(0));
        this.linearExtensions = [];
    }

    getRelation() {
        return this.relation;
    }

    getCoverRelation() {
        return this.coverRelation;
    }

    getNumElement() {
        return this.numElem;
    }

    getLinearExtensions() {
        return this.linearExtensions;
    }

    generateCoverRelation() {
        for (let i = 1; i <= this.numElem; i++) {
            for (let j = 1; j <= this.numElem; j++) {
                if (this.relation[i][j] === 1) {
                    let k = 1;
                    for (; k <= this.numElem; k++) {
                        if ((this.relation[i][k] === 1 && k !== j) && (this.relation[k][j] === 1 && k !== i)) {
                            break;
                        }
                    }
                    if (k === this.numElem + 1) {
                        this.coverRelation[i][j] = 1;
                    }
                }
            }
        }
    }

    printCoverRelation() {
        for (let i = 1; i <= this.numElem; i++) {
            for (let j = 1; j <= this.numElem; j++) {
                if (this.coverRelation[i][j] === 1) {
                    console.log(`(${i},${j})  `);
                }
            }
        }
        console.log("\n");
    }

    generateLE() {
        const n = this.numElem;
        const g = new GenLE(n);
        for (let i = 1; i <= n; i++) {
            for (let j = 1; j <= n; j++) {
                if (this.coverRelation[i][j] === 1) {
                    g.addEdge(i - 1, j - 1);
                }
            }
        }
        g.alltopologicalSorts();

        const les = g.getAllTopologicalSort();
        const iter = les[Symbol.iterator]();
        for (const le of iter) {
            const relation = new Array(n + 1).fill(0).map(() => new Array(n + 1).fill(0));
            for (let i = 0; i < le.length; i++) {
                console.log(le[i] + " ");
                let x1, y1;
                x1 = le[i];
                for (let j = i + 1; j < le.length; j++) {
                    y1 = le[j];
                    relation[x1][y1] = 1;
                }
            }
            const linearOrder = new LinearOrder(le, relation, n);
            this.linearExtensions.push(linearOrder);
            console.log("\n");
        }
    }
}

