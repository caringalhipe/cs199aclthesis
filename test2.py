# Function to print the pattern
def print_pattern():
    pattern = [
        "12",
        "3412",
        "3142",
        "3124",
        "2134",
        "2143",
        "1324",
        "1234",
        "1243",
        "1342",
        "1423",
        "1432",
        "4123"
    ]
    for line in pattern:
        print(line)

# Function to print anchor pairs and permutations
def print_anchor_pairs():
    anchor_pairs = [
        ((1, 3), (1, 4)),
        ((2, 1), (2, 3)),
        ((2, 3), (2, 4))
    ]
    permutations_list = [
        [(1, 2), (3, 2), (3, 4)],
        [(1, 3), (1, 4), (2, 4)],
        [(1, 2), (1, 3), (2, 3)]
    ]

    for i in range(len(anchor_pairs)):
        print("Anchor Pair:", anchor_pairs[i][0], anchor_pairs[i][1])
        for perm in permutations_list[i]:
            print(perm)

# Print the pattern
print_pattern()

# Print anchor pairs and corresponding permutations
print_anchor_pairs()
