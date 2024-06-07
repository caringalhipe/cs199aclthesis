from typing import List, Tuple
from classes import LinearOrder

def generatePoset(linear_orders: List[str]) -> List[Tuple[int, int]]:
    def parse_order(order_str: str) -> List[int]:
        return [int(char) for char in order_str]

    # Initialize all_relations with the relations of the first linear order
    first_order = parse_order(linear_orders[0])
    initial_linear_order = LinearOrder(first_order)
    all_relations = set(initial_linear_order.relations)

    # Intersect relations from all subsequent linear orders
    for order_str in linear_orders[1:]:
        sequence = parse_order(order_str)
        linear_order = LinearOrder(sequence)
        all_relations.intersection_update(linear_order.relations)

    # Convert the set of relations to a sorted list
    sorted_relations = sorted(all_relations)
    return sorted_relations

# Example usage
if __name__ == "__main__":
    linear_orders = ['3412', '1342']
    poset_relations = generatePoset(linear_orders)
    print(poset_relations)  # Should print the relations of the poset in sorted order
