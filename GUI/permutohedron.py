import networkx as nx
import matplotlib.pyplot as plt
from random import shuffle

#Checks if two linear orders have an adjacent swap
def check_swap(str1, str2):
      for i in range(len(str1) - 1):
            if str1[i] == str2[i+1] and str1[i+1] == str2[i]:
                  if str1[0:i] + str1[i+2:] != str2[0:i] + str2[i+2:]:
                        return None
                  return f"{str(min(int(str1[i]), int(str2[i])))}, {str(max(int(str1[i]), int(str2[i])))}"
      return None

#First line of input N is the number of linear orders
#Following N lines are the linear orders to be displayed as a permutohedron
inp = []
N = int(input())
for i in range(N):
      inp.append(input())

# UN COMMENT THESE LINES TO ENABLE INPUT SHUFFLING BEFORE DRAWING THE GRAPH
# shuffle(inp)
# print("INPUT ORDER:")
# for i in inp:
#       print(i)

G = nx.Graph()

#Add an edge between each node that has an adjacent swap
# for i in range(N):
#       G.add_node(inp[i])
#       for j in range(i+1, N):
#             adjacent = check_swap(inp[i], inp[j])
#             if adjacent:
#                   G.add_edge(inp[i], inp[j], label=adjacent)

for a in range(N):
      G.add_node(inp[a])
      for b in range(a+1, N):
            pairs = [inp[a][i:i+2] for i in range(len(inp[a])) if "".join(reversed(inp[a][i:i+2])) == "".join(inp[b][i:i+2]) and
            inp[a][0:i] + inp[a][i+2:] == inp[b][0:i] + inp[b][i+2:]]
            if len(pairs) > 0:
                  G.add_edge(inp[a], inp[b], label = str(sorted([pairs[0][0], pairs[0][1]])))

#Determines the layout of the graph
#Current choices:        nx.kamada_kawai_layout(G)
#                        nx.spectral_layour(G)
#                        nx.spiral_layout(G)
#More layouts can be found here: https://networkx.org/documentation/stable/reference/drawing.html#module-networkx.drawing.layout
pos = nx.kamada_kawai_layout(G)

#Color nodes
color_map = []
for node in G:
      color_map.append('pink')

#Draw and show graph with labels on nodes and edges        
nx.draw(G, pos, with_labels=True, node_size=1000, node_color=color_map, node_shape='s')
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))
plt.show()