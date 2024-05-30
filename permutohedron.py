import networkx as nx
import matplotlib.pyplot as plt
from random import shuffle
from matplotlib.widgets import Button

#Checks if two linear orders have an adjacent swap
def check_swap(str1, str2):
      for i in range(len(str1)-1):
            if str1[i] == str2[i+1] and str1[i+1] == str2[i]:
                  if str1[0:i] + str1[i+2:] != str2[0:i] + str2[i+2:]:
                        return None
                  return f"{str(min(int(str1[i]), int(str2[i])))}, {str(max(int(str1[i]), int(str2[i])))}"
      return None

def draw_atg(inp, N, poset = [], color = "None"):
      G = nx.Graph()

      #Add an edge between each node that has an adjacent swap
      for i in range(N):
            G.add_node(inp[i])
            for j in range(i+1, N):
                  adjacent = check_swap(inp[i], inp[j])
                  if adjacent:
                        G.add_edge(inp[i], inp[j], label=adjacent)

      #Determines the layout of the graph
      pos = nx.kamada_kawai_layout(G)

      #Color nodes
      color_map = []
      for node in G:
            color_map.append('pink')

      #Draw and show graph with labels on nodes and edges        
      nx.draw(G, pos, with_labels=True, node_size=1000, node_color=color_map)
      nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))
      
      #Button to redraw the graph in case the output looks wonky
      baxes = plt.axes([0.85, 0.05, 0.1, 0.05])
      redraw_button = Button(baxes, 'Redraw')
      redraw_button.on_clicked(redraw)
      
      plt.show()
      plt.draw()
      
def redraw(event):
      plt.clf()
      shuffle(inp)
      draw_atg(inp, N)

#First line of input N is the number of linear orders
#Following N lines are the linear orders to be displayed as a permutohedron
inp = []
N = int(input())
for i in range(N):
      inp.append(input().strip())
      
draw_atg(inp, N)