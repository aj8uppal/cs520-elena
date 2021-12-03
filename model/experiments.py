
import osmnx as ox
import pickle as pkl
from pathlib import Path
import os

import math
import time
import requests
import pandas as pd
import networkx as nx
api_key = "AIzaSyCVIV5wNiui7WQ4_k56ugLOKRlzvlzBkmk"
from osmnx.utils import log
ox.config(log_console=True)

'''
This is the function that helps us get the data of Amherst from 
the osmnx api and get the elevations for those points from the 
Google API. We have stored that value in the pkl file so we dont keep 
using the API.
'''

def get_map(city, state):
    place_query = {'city': city, 'state': state, 'country': 'USA'}
    G = ox.graph_from_place(place_query, network_type='drive')
    G = ox.add_node_elevations_google(G, api_key=api_key)
    G = ox.add_edge_grades(G)
    G_proj = ox.project_graph(G)
    return G_proj, G

'''
This is the code to retireve the code from the API. We have the 
result in the pkl files and we will be loading those for the future.

Gproj , G = get_map("Amherst", "MA")
pkl.dump(Gproj, open("graph_projected.pkl","wb"))
pkl.dump(G, open("graph.pkl","wb"))
'''


#Attempt to visualize the graph but failed.
def visualize_graph(G):
	gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
	G = ox.graph_from_gdfs(gdf_nodes, gdf_edges, graph_attrs=G.graph)
	# G = ox.add_edge_speeds(G)
	# G = ox.add_edge_travel_times(G)
	# convert MultiDiGraph to DiGraph to use nx.betweenness_centrality function
	# choose between parallel edges by minimizing travel_time attribute value
	D = ox.utils_graph.get_digraph(G, weight="elevation")

	# calculate node betweenness centrality, weighted by travel time
	bc = nx.betweenness_centrality(D, weight="elevation", normalized=True)
	nx.set_node_attributes(G, values=bc, name="bc")

	# plot the graph, coloring nodes by betweenness centrality
	nc = ox.plot.get_node_colors_by_attr(G, "bc", cmap="plasma")
	fig, ax = ox.plot_graph(G, bgcolor="k", node_color=nc, node_size=50, edge_linewidth=2, edge_color="#333333")


G = pkl.load(open("graph.pkl","rb"))

#visualize_graph(G)

#Starting point is LGRC and ending point is ILC.
start_lat = 42.3941
start_long= -72.5267
end_lat= 42.3909
end_long = -72.5257

start_point = (start_lat,start_long)
end_point = (end_lat, end_long)

def getting_node_and_bbox(G):
	origin = ox.get_nearest_node(G, (float(start_lat), float(start_long))) #(37.77, -122.426))
	destination = ox.get_nearest_node(G, (float(end_lat), float(end_long))) #(37.773, -122.441))
	point = ((float(start_lat), float(start_long)))
	bbox = ox.utils_geo.bbox_from_point(point, dist = 100)
	return bbox

#bbox = getting_node_and_bbox(G)

origin = ox.get_nearest_node(G, (float(start_lat), float(start_long))) 
destination = ox.get_nearest_node(G, (float(end_lat), float(end_long)))

# Checking out the data members of G_proj:

G_proj = pkl.load(open("graph_projected.pkl","rb")) 

print(G_proj.nodes[origin]['elevation'] - G_proj.nodes[destination]['elevation'])
print(G_proj.nodes[origin])
print(G_proj.nodes[destination])


print(G_proj.edges(origin))

#def find_lowest_elevation_path(G):






