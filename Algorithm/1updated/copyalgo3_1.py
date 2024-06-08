import networkx as nx
from collections import defaultdict, OrderedDict
import itertools
from gui1 import check_swap
from algo1 import generatePoset
from algo3_2 import find_covering_poset
from algo2 import maximalPoset

def find_anchors(G):
    """
    Function to find all anchor (a, b) pairs in the input sequences.
    
    Parameters:
    upsilon (list of str): A list of strings representing the input sequences.
    
    Returns:
    list: A list of tuples representing all anchor pairs (a, b).
    """
    anchors = list(set(anchor[2]['label'] for anchor in G.edges.data()))
    
    anchors += [''.join(reversed(anchor)) for anchor in anchors]
    
    for i in range(len(anchors)):
        anchors[i] = (int(anchors[i][0]), int(anchors[i][3]))
    
    return anchors

def no_dupe(anchors):
    N = len(anchors)
    for i in range(N-1):
        for j in range(i+1, N):
            if ''.join(str(num) for num in anchors[i]) == ''.join(reversed(''.join(str(num) for num in anchors[j]))):
                return False
    return True

def group_anchors(anchors, k):
    """
    Function to generate all combinations of anchor pairs grouped by k-1.
    
    Parameters:
    anchors (list of tuples): A list of anchor pairs (a, b).
    k (int): The number of anchors per group.
    
    Returns:
    list: A list of combinations, each containing k-1 anchor pairs.
    """
    return [combi for combi in itertools.combinations(anchors, k-1) if no_dupe(combi)]

def covers_upsilon(linear_orders, Upsilon):
        return set(Upsilon).issubset(set(linear_orders))

def k_poset_cover(upsilon, k):
    """
    Function to compute the k-poset cover for a given input.
    
    Parameters:
    upsilon (list of str): A list of strings representing the input sequences.
    k (int): The maximum number of posets to cover the input sequences.
    
    Returns:
    list: A list of posets that cover the input sequences.
    """
    G = nx.Graph()
    anchors = []
    N = len(upsilon)
    
    #Add an edge between each node that has an adjacent swap
    for i in range(N):
        G.add_node(upsilon[i])
        for j in range(i+1, N):
                adjacent = check_swap(upsilon[i], upsilon[j])
                if adjacent:
                    G.add_edge(upsilon[i], upsilon[j], label=adjacent, color = 'k')
    
    #pos = nx.kamada_kawai_layout(G)
    
    #nx.draw(G, pos, with_labels=True, node_size=1000)
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))
    
    anchors = find_anchors(G)
    print("Anchors:", anchors)
    
    grouped_anchors = group_anchors(anchors, k)
    #print("Grouped Anchors:", grouped_anchors)
    
    Pstar = []
    for A in grouped_anchors:
        Upsilon_A = []
        print("Current Grouped Anchor:", A)
        
        for sequence in upsilon:
            satisfies = True
            for anchor in A:
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
            P_A = generatePoset(Upsilon_A)
            print("P_A:", P_A)
            #poset_cover.append(P_A)
            #P_i = maximalPoset(Upsilon, P_A, A)
            Pstar.append(P_A)
            """
            if P_A:
                P_i = maximalPoset(Upsilon, P_A, A)
                Pstar_total.append(P_i)
            """
    
    """

    Pfinal, LOfinal = find_covering_poset(Pstar_total, Upsilon)

    return Pfinal, LOfinal
    """
    
    return Pstar[:k]


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

"""
count = 1
with open(f'optimalsolutions/optsol/inputs/{args[1]}posetsinput.txt', 'r') as input_file, open(f'outputs/output_{args[1]}.txt', 'w') as output_file:
    for line in input_file: # work on each test case
        print(count)
        count+=1
        inputLinearOrders = [int(x) for x in line.strip('[]\n').split(',')]

        inputLinearOrders.sort()
        inputLinearOrders = [str(item) for item in inputLinearOrders]

        posets = []
        # group linear orders according to their root
        groupings = group_linearOrders_by_its_root(inputLinearOrders)

        #print("Groupings: ", groupings)

        # for each group, there is a set of posets
        # append each poset to the list posets
        
        for group in groupings:
            poset_group = TreePoset(group)
            for poset in poset_group:
                posets.append(poset)
        
        if posets != None:
            output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
            for i in range(len(posets)):
                output_file.write(f"P{str(i+1)}: {posets[i]}\n")
            output_file.write("\n")

        else:
            output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
            output_file.write("None!!!!!\n\n")

if posets != None:
    print(f"Generated all output of input linear order sets with {args[1]} vertices")
    print("Check 'output' directory")
else:
    print("Generated nothing")
"""