
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
	def __init__(self, origin, destination, weight = "elevation", alg="default"):
		
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










