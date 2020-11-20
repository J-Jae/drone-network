# https://junpyopark.github.io/road-network-construction-1/
# https://junpyopark.github.io/road-network-construction-2/

# https://medium.com/@thlee33/%EC%9C%88%EB%8F%84%EC%9A%B0-%EA%B8%B0%EB%B0%98-geopandas-%EC%84%A4%EC%B9%98-%EB%B0%8F-%EC%A2%8C%ED%91%9C-%EB%B3%80%ED%99%98-e9b9ef16d9f9

# https://github.com/JunPyoPark/Networkx-Projects/blob/master/%EC%9A%B8%EC%82%B0%20%EB%8F%84%EB%A1%9C%EA%B5%90%ED%86%B5%EC%A0%95%EB%B3%B4/shp_to_csv.ipynb

# http://nodelink.its.go.kr/intro/intro06_05.aspx

# https://m.blog.naver.com/PostView.nhn?blogId=woosoung1993&logNo=221622062441&proxyReferer=https:%2F%2Fwww.google.com%2F


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from pyproj import Proj, transform

folder_path = './.data'

shp_path_node = f'{folder_path}/MOCT_NODE.shp'
shp_path_link = f'{folder_path}/MOCT_LINK.shp'

shp_node = gpd.read_file(shp_path_node, encoding='euc-kr')
shp_link = gpd.read_file(shp_path_link, encoding='euc-kr')

shp_node = shp_node[shp_node['NODE_ID'].str[0:3] == '161']
shp_link = shp_link[shp_link['LINK_ID'].str[0:3] == '161']

# Change column name to draw network in Gephi
shp_node.rename(columns={'NODE_ID': 'Id'}, inplace=True)
shp_link.rename(columns={'F_NODE': 'Source', 'T_NODE': 'Target'}, inplace=True)


print(shp_node.head(3))
print(shp_link.head(3))

shp_node.to_csv('Incheon_nodes.csv')
shp_link.to_csv('Incheon_links.csv')


nodes = pd.read_csv('Incheon_nodes.csv')

# print(nodes.head())
# print(nodes.geometry)
# print(nodes.geometry[0])

inProj = Proj(init='epsg:5186')
outProj = Proj(init='epsg:4326')
latitude = []
longitude = []
for idx, row in nodes.iterrows():
    geometry = row.geometry.split(' ')
    x = geometry[1][1:]
    y = geometry[2][:-1]
    nx, ny = transform(inProj, outProj, x, y)     # 새로운 좌표계
    latitude.append(ny)
    longitude.append(nx)
nodes['latitude'] = latitude
nodes['longitude'] = longitude
del nodes['geometry']  # delete coords

nodes.to_csv('Incheon_nodes_coord.csv')
