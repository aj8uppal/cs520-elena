
import osmnx as ox
import pickle as pkl
from pathlib import Path
import os
import sys
sys.path.append('.')

import math
import time
import requests
import pandas as pd
import networkx as nx
api_key = "AIzaSyCVIV5wNiui7WQ4_k56ugLOKRlzvlzBkmk"
from osmnx.utils import log
ox.config(log_console=True)


'''

Sample start and end coordinates.
LGRC
start_lat = 42.3941
start_long= -72.5267

ILC
end_lat= 42.3909
end_long = -72.5257

'''


class EleNa :
	#Setting up the basic things required for the map and algo
	def __init__(self, origin, destination, weight = "elevation", alg="min_elev_dist"):

		self.origin = origin
		self.destination = destination
		self.weight = weight
		self.G, self.G_proj = self.load_map()
		self.origin_node = ox.get_nearest_node(self.G, (float(self.origin[0]), float(self.origin[1])))
		self.destination_node = ox.get_nearest_node(self.G, (float(self.destination[0]), float(self.destination[1])))
		self.alg = alg

	'''
	This is the code to retireve the code from the API. We have the
	result in the pkl files and we will be loading those for the future.

	Gproj , G = get_map("Amherst", "MA")
	pkl.dump(Gproj, open("graph_projected.pkl","wb"))
	pkl.dump(G, open("graph.pkl","wb"))
	'''

	def load_map(self):
		# place_query = {'city': "Amherst", 'state': "Massachusetts", 'country': 'USA'}
	    # G = ox.graph_from_place(place_query, network_type='drive')
	    # G = ox.add_node_elevations_google(G, api_key=api_key)
	    # G = ox.add_edge_grades(G)
	    # G_proj = ox.project_graph(G)
	    G = pkl.load(open("graph.pkl","rb"))
	    G_proj = pkl.load(open("graph_projected.pkl","rb"))
	    return G,G_proj

	def shortest_path(self):
		paths = list(ox.k_shortest_paths(self.G, self.origin, self.destination, 10))

		min_elev_path= None
		min_elev = float("inf")

		for path in paths:
			avg_elev = 0
			num_nodes = len(path)

			for i in range(num_nodes-1):
				avg_elev+= abs(self.G.nodes[path[i]]['elevation'] - self.G.nodes[path[i+1]]['elevation'])

			elevation= avg_elev/num_nodes
			if elevation<min_elev:
				min_elev_path = path
				min_elev = elevation
		return min_elev_path

	def calc_max_elev(self, a,b):
		elev = abs(self.G.nodes[a]['elevation']- self.G.nodes[b]['elevation'])
		return -1*elev

	def calc_min_elev(self, a,b):
		elev = abs(self.G.nodes[a]['elevation']- self.G.nodes[b]['elevation'])
		return elev

	def calc_max_elev_dist(self, a,b):
		elev = abs(self.G.nodes[a]['elevation']- self.G.nodes[b]['elevation'])
		dist = self.G.edges[a,b,0]['length']
		return math.sqrt((dist**2-elev**2))

	def calc_min_elev_dist(self, a,b):
		elev = abs(self.G.nodes[a]['elevation']- self.G.nodes[b]['elevation'])
		dist = self.G.edges[a,b,0]['length']

		return math.sqrt((elev**2+dist**2))

	def create_adj(self):
		adj_mat = {}
		for node in self.G.nodes():
			if node not in adj_mat:
				adj_mat[node] = {}
			for _,neighbor in self.G.edges(node):
				if self.alg=="max_elev":
					adj_mat[node][neighbor] = self.calc_max_elev(node,neighbor)
				elif self.alg == "min_elev":
					adj_mat[node][neighbor] = self.calc_min_elev(node,neighbor)
				elif self.alg=="max_elev_dist":
					adj_mat[node][neighbor] = self.calc_max_elev_dist(node,neighbor)
				else:
					adj_mat[node][neighbor] = self.calc_min_elev_dist(node,neighbor)



		return adj_mat

	def initialize_variables(self):
		cost = {} #Initialized with infinity
		parent = {} #Initialized with None
		unvisited = set() # A set of all unvisited nodes

		for node in self.G.nodes():
			cost[node] = float("inf")
			parent[node] = None
			unvisited.add(node)
		cost[self.origin_node]=0
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
		EleNa.get_path(parent, parent[cur], path)
		path.append(cur)
		return path

	def shortest_path_custom(self):
		adj_mat = self.create_adj()
		path=[]
		cost, parent, unvisited = self.initialize_variables()
		while unvisited:
			cur = EleNa.get_min_cost_node(cost, unvisited)
			unvisited.remove(cur)
			for neighbour in adj_mat[cur]:
				if neighbour in unvisited:
					if cost[cur] + adj_mat[cur][neighbour]<cost[neighbour]:
						cost[neighbour]= cost[cur] + adj_mat[cur][neighbour]
						parent[neighbour]= cur

		best_path = EleNa.get_path(parent, self.destination_node, path)
		best_path_lat_long = []

		for node in best_path:
			best_path_lat_long.append((self.G.nodes[node]['x'], self.G.nodes[node]['y']))

		return best_path_lat_long




# start_lat = 42.3916
# start_long= -72.5194
# end_lat= 42.3843
# end_long = -72.5302

# E1 = EleNa((start_lat, start_long), (end_lat, end_long))
# path1= E1.shortest_path_custom()

# E2 = EleNa((start_lat, start_long), (end_lat, end_long), alg = "max_elev")
# path2 = E2.shortest_path_custom()

# E3 = EleNa((start_lat, start_long), (end_lat, end_long), alg = "min_elev")
# path3 = E3.shortest_path_custom()

# E4 = EleNa((start_lat, start_long), (end_lat, end_long), alg = "max_elev_dist")
# path4 = E4.shortest_path_custom()

# routes = [path1, path2, path3, path4]
# rc = ['r', 'y', 'c', 'b']
# plt, ax = ox.plot_graph_routes(E1.G, routes, route_colors=rc, route_linewidth=6, node_size=0)
# plt.show()
