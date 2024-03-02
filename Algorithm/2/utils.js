//const nx = require('networkx'); find equivalent networkx library

function isAllConnected(P, n) {
    for (const p of P) {
        const checkVertices = Array(n).fill(false);
        for (const [a, b] of p) {
            checkVertices[a - 1] = true;
            checkVertices[b - 1] = true;
        }
        if (!checkVertices.includes(false) && nx.isDirectedAcyclicGraph(new nx.DiGraph(p))) {
            continue;
        } else {
            return false;
        }
    }
    return true;
}

function binaryToCover(P, n) {
    const coverRelations = [];
    for (const [u, v] of P) {
        if (coverRelations.some(([cu, cv]) => cu === u && cv === v)) {
            continue;
        }
        if (coverRelations.length === n - 1) {
            break;
        }
        let transitive = false;
        for (let w = 1; w <= n; w++) {
            if (w === u || w === v) {
                continue;
            } else {
                if (P.some(([pu, pw]) => pu === u && pw === w) && P.some(([pw, pv]) => pw === w && pv === v)) {
                    transitive = true;
                    break;
                }
            }
        }
        if (!transitive) {
            coverRelations.push([u, v]);
        }
    }
    return coverRelations.sort();
}

function covered(groupPosets) {
    let coveredLinearOrders = [];
    for (const poset of groupPosets) {
        coveredLinearOrders = coveredLinearOrders.concat(getLinearExtensions(poset));
    }
    coveredLinearOrders = [...new Set(coveredLinearOrders.map(x => parseInt(x)))].sort();
    return coveredLinearOrders;
}

function generateRootedRelations(parent, vertices, relations) {
    if (vertices.length === 0) {
        return [relations.sort()];
    } else {
        let rels = [];
        for (const child of vertices) {
            const newVertices = vertices.filter(v => v !== child);
            rels = rels.concat(generateRootedRelations(parent, newVertices, relations.concat([[parent, child]])));
            rels = rels.concat(generateRootedRelations(parent, newVertices, relations.concat([[child, parent]])));
            rels = rels.concat(generateRootedRelations(child, newVertices, relations.concat([[parent, child]])));
            rels = rels.concat(generateRootedRelations(child, newVertices, relations.concat([[child, parent]])));
        }

        const trueRels = [...new Set(rels.map(JSON.stringify))].map(JSON.parse);
        return trueRels;
    }
}

function isAllConnected(vertices, relations) {
    for (const vertex of vertices) {
        let isConnected = false;
        for (const relation of relations) {
            if (relation.includes(vertex)) {
                isConnected = true;
                break;
            }
        }
        if (!isConnected) {
            return false;
        }
    }
    return true;
}

function getLinearExtensions(coverRelation) {
    const G = new nx.DiGraph();
    for (const [a, b] of coverRelation) {
        G.addEdge(a, b);
    }
    const sortings = Array.from(nx.allTopologicalSorts(G));
    return sortings.map(sorting => sorting.join('')).sort();
}

function VERIFY(P, Y) {
    return JSON.stringify(P.sort()) === JSON.stringify(Y.sort());
}

function rankInverse(index, linearOrder) {
    return linearOrder[index];
}

function groupLinearOrdersByItsRoot(upsilon) {
    const groupedUpsilon = {};
    for (const linearOrder of upsilon) {
        const root = linearOrder[0];
        if (groupedUpsilon[root]) {
            groupedUpsilon[root].push(linearOrder);
        } else {
            groupedUpsilon[root] = [linearOrder];
        }
    }
    return Object.values(groupedUpsilon);
}

// Example usage:
// const P = [[1, 2], [2, 3], [3, 4]];
// const result = isAllConnected(P, 4);
// console.log(result);
