#randomly generate a bipartite graph
#the storage is edge format without any order
#the outcome may have duplicated edges
#sorting process (in other programs) will be able to remove edge duplications

import random
import struct
import time

n_left_nodes = 1000000
n_right_nodes = 100000
n_edges = 10000000 #may contain duplicates
# n_left_nodes = 100
# n_right_nodes = 10
# n_edges = 1000

left_node_id_min = 1
left_node_id_max = left_node_id_min + n_left_nodes - 1
right_node_id_min = left_node_id_max + 1
right_node_id_max = right_node_id_min + n_right_nodes - 1

print("generate bipartite graph with random edges...")
t_start = time.clock()

f = open("data\\graph_bipartite_no_order.bin","wb")

edge_idx = 0
while edge_idx < n_edges:
	left_node_id = random.randint(left_node_id_min, left_node_id_max)
	right_node_id = random.randint(right_node_id_min, right_node_id_max)
	f.write(struct.pack('i',left_node_id))
	f.write(struct.pack('i',right_node_id))
	edge_idx += 1  		

f.close()

t_stop = time.clock()

print("graph generation accomplished")
print("time elapsed: " + str(t_stop-t_start) + " seconds")
print("left nodes: " + str(n_left_nodes))
print("right nodes: " + str(n_right_nodes))
print("number of edges (may have duplication): " + str(n_edges))