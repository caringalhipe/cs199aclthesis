import networkx as nx
import matplotlib.pyplot as plt

def check_swap(str1, str2):
      for i in range(len(str1) - 1):
            if str1[i] == str2[i+1] and str1[i+1] == str2[i]:
                  if str1[i+2:] != str2[i+2:]:
                        return None
                  return f"{str(min(int(str1[i]), int(str2[i])))}, {str(max(int(str1[i]), int(str2[i])))}"
      return None

inp = []
for i in range(int(input())):
      inp.append(input())

G = nx.Graph()
G.add_nodes_from(inp)

for i in range(len(inp)-1):
      for j in range(i+1,len(inp)):
            adjacent = check_swap(inp[i], inp[j])
            if adjacent:
                  G.add_edge(inp[i], inp[j], label=adjacent)

pos = nx.kamada_kawai_layout(G)
color_map = []
for node in G:
      color_map.append('pink')
            
nx.draw(G, pos, with_labels=True, node_size=1000, node_color=color_map, node_shape='s')
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))
plt.show()