# Function to print the pattern
def print_pattern():
    pattern = [
        "12",
        "14523",
        "14253",
        "12453",
        "14235",
        "12435",
        "12345",
        "13245",
        "13425",
        "13254",
        "12354",
        "12534",
        "13524"
    ]
    for line in pattern:
        print(line)

# Function to print anchor pairs and permutations
def print_anchor_pairs():
    anchor_pairs = [
        ((5, 2), (2, 4)),
        ((5, 3), (5, 4)),
        ((4, 2), (4, 3))
    ]
    permutations_list = [
        [(1, 3), (1, 5), (1, 2), (1, 4), (3, 5), (2, 4)],
        [(1, 2), (1, 5), (1, 3), (1, 4), (2, 5), (3, 4)],
        [(1, 2), (1, 5), (1, 3), (1, 4), (2, 3), (4, 5)]
    ]

    for i in range(len(anchor_pairs)):
        print("Anchor Pair:", anchor_pairs[i][0], anchor_pairs[i][1])
        for perm in permutations_list[i]:
            print(perm)

# Print the pattern
print_pattern()

# Print anchor pairs and corresponding permutations
print_anchor_pairs()
