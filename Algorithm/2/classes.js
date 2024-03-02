class Poset {
    constructor(size, relations, isNull = false) {
        this.vertices = isNull ? null : Array.from({ length: size }, (_, i) => i + 1);
        this.relations = isNull ? null : relations.slice().sort();
    }

    isEmpty(keyword = "both") {
        if ((keyword === 'both' || keyword === 'vertices') && this.vertices === null) return true;
        if ((keyword === 'both' || keyword === 'relations') && this.relations === null) return true;
        return false;
    }

    isEqual(poset) {
        if (!this.isEmpty() &&
            Math.max(...this.vertices) === Math.max(...poset.vertices) &&
            JSON.stringify(this.relations) === JSON.stringify(poset.relations)) {
            return true;
        }
        return false;
    }

    isIn(posets) {
        for (const p of posets) {
            if (this.isEqual(p)) return true;
        }
        return false;
    }

    subtract(poset) {
        const relations = [];
        for (const relation of this.relations) {
            if (!poset.relations.includes(relation)) {
                relations.push(relation);
            }
        }
        return relations;
    }

    generateLinearExtensions() {
        const graph = new Graph(this.relations, this.vertices.length, []);
        graph.getAllTopologicalOrders();
        return graph.listofLO;
    }
}

class LinearOrder extends Poset {
    constructor(sequence) {
        super(sequence.length, LinearOrder._getRelations(sequence));
        this.sequence = sequence;
    }

    static _getRelations(sequence) {
        const relations = [];
        for (let i = 0; i < sequence.length - 1; i++) {
            for (let j = i + 1; j < sequence.length; j++) {
                relations.push([sequence[i], sequence[j]]);
            }
        }
        return relations;
    }
}

class Graph {
    constructor(edges, N, inputs) {
        this.inputLO = inputs;
        this.listofLO = [];
        this.edges = edges;
        this.adjList = Array.from({ length: N }, () => []);

        this.indegree = Array(N).fill(0);

        for (const [src, dst] of edges) {
            this.adjList[src - 1].push(dst - 1);
            this.indegree[dst - 1]++;
        }
    }

    _findAllTopologicalOrders(path, marked, N) {
        for (let v = 0; v < N; v++) {
            if (this.indegree[v] === 0 && !marked[v]) {
                for (const u of this.adjList[v]) {
                    this.indegree[u]--;
                }
                path.push(v);
                marked[v] = true;
                this._findAllTopologicalOrders(path, marked, N);

                for (const u of this.adjList[v]) {
                    this.indegree[u]++;
                }

                path.pop();
                marked[v] = false;
            }
        }

        if (path.length === N) {
            path = path.map(i => i + 1);
            this.listofLO.push([...path]);
        }
    }

    getAllTopologicalOrders() {
        const lenNodes = this.adjList.length;
        const marked = Array(lenNodes).fill(false);
        const path = [];
        this._findAllTopologicalOrders(path, marked, lenNodes);
    }
}
