import networkx as nx
import matplotlib.pyplot as plt

def check_swap(str1, str2):
    for i in range(len(str1) - 1):
        if str1[i] == str2[i+1] and str1[i+1] == str2[i]:
            if str1[i+2:] != str2[i+2:]:
                return None
            return f"{str(min(int(str1[i]), int(str2[i])))}-{str(max(int(str1[i]), int(str2[i])))}"
    return None

# Input the number of nodes and the nodes themselves
inp = []
for i in range(int(input(""))):
    inp.append(input(""))

# Input the specific edges to highlight
highlight_edges_input = input("Enter the edges to highlight (comma-separated, e.g., '1,2 3,4 2,4'): ")
highlight_edges = [tuple(edge.split(',')) for edge in highlight_edges_input.split()]

G = nx.Graph()
G.add_nodes_from(inp)

for i in range(len(inp) - 1):
    for j in range(i + 1, len(inp)):
        adjacent = check_swap(inp[i], inp[j])
        if adjacent:
            G.add_edge(inp[i], inp[j], label=adjacent)

pos = nx.kamada_kawai_layout(G)
color_map = ['pink' for node in G]

# Default edge color and style
edge_colors = []
edge_labels = nx.get_edge_attributes(G, 'label')
for edge in G.edges():
    u, v = edge
    label = edge_labels[(u, v)]
    label_tuple = tuple(label.split('-'))
    if label_tuple in highlight_edges or label_tuple[::-1] in highlight_edges:
        edge_colors.append('red')
    else:
        edge_colors.append('black')

# Draw nodes
nx.draw(G, pos, with_labels=True, node_size=1000, node_color=color_map, node_shape='s')

# Draw edges with specified colors
nx.draw_networkx_edges(G, pos, edge_color=edge_colors)

# Draw edge labels
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()
