// Define sample data for testing
const relations = [[1, 2], [2, 3], [3, 4], [4, 5]];
const sequence = [1, 2, 3, 4, 5];

// Instantiate a Poset object
const poset = new Poset(5, relations);

// Test isEmpty method
console.log("Is poset empty?", poset.isEmpty());

// Test isEqual method
const poset2 = new Poset(5, relations);
console.log("Are poset and poset2 equal?", poset.isEqual(poset2));

// Instantiate a LinearOrder object
const linearOrder = new LinearOrder(sequence);

// Test generateLinearExtensions method
console.log("Linear extensions:", linearOrder.generateLinearExtensions());

// Instantiate a Graph object
const graph = new Graph(relations, 5, []);

// Test getAllTopologicalOrders method
graph.getAllTopologicalOrders();
console.log("List of Linear Orders:", graph.listofLO);
