
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
#ox.config(log_console=True)

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



#visualize_graph(G)

#Starting point is LGRC and ending point is ILC.

start_point = (start_lat,start_long)
end_point = (end_lat, end_long)

def getting_node_and_bbox(G):
	origin = ox.get_nearest_node(G, (float(start_lat), float(start_long))) #(37.77, -122.426))
	destination = ox.get_nearest_node(G, (float(end_lat), float(end_long))) #(37.773, -122.441))
	point = ((float(start_lat), float(start_long)))
	bbox = ox.utils_geo.bbox_from_point(point, dist = 100)
	return bbox

#bbox = getting_node_and_bbox(G)


# Checking out the data members of G_proj:


print(G_proj.nodes[origin]['elevation'] - G_proj.nodes[destination]['elevation'])
print(G_proj.nodes[origin])
print(G_proj.nodes[destination])


print(G_proj.edges(origin))

def find_lowest_elevation_path(G):
def algorithms():
	startnode = store start node
	getAllNeighbourNodes = node.neighbours
	function Dijkstra(Graph, source):
	for each vertex v in Graph:	# Initialization
		dist[v] := infinity	# initial distance from source to vertex v is set to infinite
		previous[v] := undefined	# Previous node in optimal path from source
		dist[source] := 0	# Distance from source to source
		Q := the set of all nodes in Graph	# all nodes in the graph are unoptimized - thus are in Q
	while Q is not empty:	# main loop
		u := node in Q with smallest dist[ ]
		remove u from Q
		for each neighbor v of u:	#// where v has not yet been removed from Q.
			alt := dist[u] + dist_between(u, v)
			if alt < dist[v]	// Relax (u,v)
				dist[v] := alt
				previous[v] := u
	return previous[ ]




start_lat = 42.3916
start_long= -72.5194
end_lat= 42.3843
end_long = -72.5302



G_proj = pkl.load(open("graph_projected.pkl","rb")) 
G = pkl.load(open("graph.pkl","rb"))
origin = ox.get_nearest_node(G, (float(start_lat), float(start_long))) 
destination = ox.get_nearest_node(G, (float(end_lat), float(end_long)))

#adj_mat = [[0]*len(G.nodes())]*len(G.nodes())
print(origin, destination)

def calc_weight (a,b):
	elev = abs(G.nodes[a]['elevation']- G.nodes[b]['elevation'])
	dist = G.edges[a,b,0]['length']

	return math.sqrt((elev**2+dist**2))


def create_adj(G):
	adj_mat = {}
	for node in G.nodes():
		if node not in adj_mat:
			adj_mat[node] = {}
		for _,neighbor in G.edges(node):
			adj_mat[node][neighbor] = calc_weight(node,neighbor)
	return adj_mat

def initialize_variables(G, origin):
	cost = {} #Initialized with infinity
	parent = {} #Initialized with None
	unvisited = set() # A set of all unvisited nodes

	for node in G.nodes():
		cost[node] = float("inf")
		parent[node] = None
		unvisited.add(node)
	cost[origin]=0
	return cost,parent,unvisited


def get_min_cost_node(cost_dict, unvisited):
	min_cost = float("inf")
	ret_node = None

	for node in cost_dict:
		if cost_dict[node]<=min_cost and node in unvisited:
			min_cost = cost_dict[node]
			ret_node = node
	return ret_node


def get_path(parent, cur, path):
	if parent[cur] == None:
		path.append(cur)
		return
	get_path(parent, parent[cur], path)
	path.append(cur)
	return path

def shortest_distance(G, origin, destination):
	adj_mat = create_adj(G)
	path=[]
	cost, parent, unvisited = initialize_variables(G, origin)
	while unvisited:
		cur = get_min_cost_node(cost, unvisited)
		unvisited.remove(cur)
		for neighbour in adj_mat[cur]:
			if neighbour in unvisited:
				if cost[cur] + adj_mat[cur][neighbour]<cost[neighbour]:
					cost[neighbour]= cost[cur] + adj_mat[cur][neighbour]
					parent[neighbour]= cur

	best_path = get_path(parent, destination, path)
	best_path_lat_long = []

	for node in best_path:
		best_path_lat_long.append((G.nodes[node]['x'], G.nodes[node]['y']))
	
	return best_path_lat_long

shortest_distance(G, origin, destination)



'''
adj_mat: { Node: {neigh1:weight1, neigh2:weight2, .... }}

'''























