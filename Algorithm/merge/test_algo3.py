import networkx as nx
from collections import defaultdict, OrderedDict
from algo2 import Poset
import itertools

def find_anchors(upsilon):
    """
    Function to find all anchor (a, b) pairs in the input sequences.
    
    Parameters:
    upsilon (list of str): A list of strings representing the input sequences.
    
    Returns:
    list: A list of tuples representing all anchor pairs (a, b).
    """
    anchors = []
    for sequence in upsilon:
        for i in range(len(sequence) - 1):
            anchor = (int(sequence[i]), int(sequence[i + 1]))
            if anchor not in anchors:
                anchors.append(anchor)
    return anchors

def group_anchors(anchors, k):
    """
    Function to generate all combinations of anchor pairs grouped by k-1.
    
    Parameters:
    anchors (list of tuples): A list of anchor pairs (a, b).
    k (int): The number of anchors per group.
    
    Returns:
    list: A list of combinations, each containing k-1 anchor pairs.
    """
    return list(itertools.combinations(anchors, k-1))

def k_poset_cover(upsilon, k):
    """
    Function to compute the k-poset cover for a given input.
    
    Parameters:
    upsilon (list of str): A list of strings representing the input sequences.
    k (int): The maximum number of posets to cover the input sequences.
    
    Returns:
    list: A list of posets that cover the input sequences.
    """
    anchors = find_anchors(upsilon)
    #print("Anchors:", anchors)
    
    grouped_anchors = group_anchors(anchors, k)
    #print("Grouped Anchors:", grouped_anchors)
    
    poset_cover = []
    for element in grouped_anchors:
        Upsilon_A = []
        print("Current Grouped Anchor:", element)
        
        for sequence in upsilon:
            satisfies = True
            for anchor in element:
                a, b = str(anchor[0]), str(anchor[1])
                if a in sequence and b in sequence:
                    if sequence.index(a) > sequence.index(b):
                        satisfies = False
                        break
                else:
                    satisfies = False
                    break
            if satisfies:
                Upsilon_A.append(sequence)
        
        print("Upsilon_A:", Upsilon_A)
        
        if Upsilon_A:
            P_A = Poset(Upsilon_A)
            print("P_A:", P_A)
            poset_cover.append(P_A)
    
    return poset_cover[:k]

def main():
    sample_input = [
        '12453', '12345', '13425', '13524', '12354', '12534', '12435', '14523', '14235', '13254', '13245', '14253'
    ]
    k = 3
    
    
    result = k_poset_cover(sample_input, k)
    
    """
    for poset in result:
        print(poset)
    
    
    with open("poset_cover_results.txt", "w") as file:
        for poset in result:
            file.write(str(poset) + "\n")
    """

if __name__ == "__main__":
    main()
