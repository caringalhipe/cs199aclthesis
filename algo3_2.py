from poset_utils import get_linear_extensions
"""
Last part of kposet
"""
def find_covering_poset(Pstar, Upsilon):
    def covers_upsilon(linear_orders, Upsilon):
        for order in linear_orders:
            if any(ups in order for ups in Upsilon):
                return True
        return False
    
    Pfinal = []
    LOfinal = []
    
    for P in Pstar:
        #print("P", P)
        linear_order = get_linear_extensions(P)
        #print("Linear orders for P:", linear_order)
        
        covered_orders = []
        for order in Upsilon:
            if any(part in order for part in linear_order):
                covered_orders.append(order)
        
        LOfinal.append(covered_orders)
        #print("Covered orders:", covered_orders)
        
        if covers_upsilon(linear_order, Upsilon):
            #print("Covering poset found:", P)
            Pfinal.append(P)

    if not Pfinal:
        #print("No covering poset found.")
        return None
        
    
    return Pfinal, LOfinal

# Example usage
if __name__ == "__main__":
    """
    Pstar = [
        [(1, 2), (2, 3)],  # Example poset 1
        [(1, 3), (2, 3)],  # Example poset 2
        [(3, 1), (3, 2)],
    ]
    Upsilon = ['123', '213', '312']  # Example input Upsilon
    """
    Upsilon = ['14523', '14253', '14235', '12453', '12435', '12345', '13245', '13425',
                '12354', '12534', '13254', '13524']
    Pstar = [
                [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (4, 2), (4, 3), (4, 5), (5, 2), (5, 3)], 
                [(1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (3, 2), (3, 4), (3, 5), (4, 2), (4, 5)], 
                [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (5, 3), (5, 4)], 
                [(1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (3, 2), (3, 4), (3, 5), (5, 2), (5, 4)], 
                [(1, 2), (1, 5), (4, 3), (1, 4), (4, 2), (2, 3), (4, 5), (2, 5), (1, 3)], 
                [(2, 4), (1, 2), (1, 5), (1, 4), (4, 5), (2, 5), (1, 3)], 
                [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (5, 4)], 
                [(1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (2, 5), (3, 2), (3, 4), (3, 5), (5, 4)]
            ]
    Pfinal, LOfinal = find_covering_poset(Pstar, Upsilon)
    print("Final covering posets:", Pfinal)
    print("Covered linear orders:", LOfinal)
