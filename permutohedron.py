import networkx as nx
import matplotlib.pyplot as plt

def check_swap(str1, str2):
      for i in range(len(str1) - 1):
            if str1[i] == str2[i+1] and str1[i+1] == str2[i]:
                  return True
      return False

inp = []
for i in range(int(input())):
      inp.append(input())
      
print(inp)

G = nx.Graph()
G.add_nodes_from(inp)

for i in range(len(inp)-1):
      for j in range(i+1,len(inp)):
            if check_swap(inp[i], inp[j]):
                  G.add_edge(inp[i], inp[j])

nx.draw_kamada_kawai(G, with_labels=True)
plt.show()