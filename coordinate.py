import os
import folium
import pandas as pd
import numpy as np
from pyproj import Proj, transform

nodes = pd.read_csv('Incheon_nodes.csv')
links = pd.read_csv('Incheon_links.csv')

print(nodes.head())
print(nodes.geometry)
print(nodes.geometry[0])

inProj = Proj(init='epsg:5186')
outProj = Proj(init='epsg:4326')
latitude = []
longitude = []
for idx, row in nodes.iterrows():
    geometry = row.geometry.split(' ')
    x = geometry[1][1:]
    y = geometry[2][:-1]
    # x, y = row.coords[0][0], row.coords[0][1]
    # latitude.append(x)
    # longitude.append(y)
    nx, ny = transform(inProj, outProj, x, y)     # 새로운 좌표계
    latitude.append(ny)
    longitude.append(nx)
nodes['latitude'] = latitude
nodes['longitude'] = longitude
del nodes['geometry']  # delete coords

nodes.to_csv('Incheon_nodes_coord.csv')
