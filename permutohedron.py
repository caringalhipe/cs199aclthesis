import plotly.express as px
import numpy as np
import itertools
import pandas as pd

order = int(input())
inp = []
for i in range(int(input())):
      inp.append(list(int(i) for i in input()))
permuted_items = np.array(inp)

#Project the points onto 3D space--
A = np.array([[np.sqrt(2)/2, -np.sqrt(2)/2, 0, 0],\
     [np.sqrt(6)/6, np.sqrt(6)/6, -np.sqrt(2/3), 0],\
     [np.sqrt(12)/12, np.sqrt(12)/12, np.sqrt(12)/12, -np.sqrt(3)/2]])

permuted_items = np.einsum('ik,ak->ai',A,permuted_items)
#----------------------------------

xyzs = []
colors = []

for i, point in enumerate(permuted_items):

      d = np.linalg.norm(permuted_items-point[np.newaxis,:],axis=1)

      #Inspired by https://stackoverflow.com/questions/31352486/can-numpy-argsort-handle-ties 
      js = (abs(d - d[d.argsort()[1]])<1e-3).nonzero()[0]

      for j in js:
          xyzs.extend([point,permuted_items[j]])

          # Get unique string as color to group above line while plotting
          c = str(point) + str(permuted_items[j])
          colors.extend([c, c])


lines = np.array(xyzs)
x, y, z = lines.T

plotting_data = pd.DataFrame({
      "X": x,
      "Y": y,
      "Z": z,
      "color": colors,
})

fig = px.line_3d(plotting_data, x='X', y='Y', z='Z', color="color")
fig.show()