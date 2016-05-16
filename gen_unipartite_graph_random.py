# generate random edges for a large scale unipartite graph
# with possible edge duplications

import random
import struct
import time

n_nodes = 1000000
n_edges = 10000000

node_id_min = 1
node_id_max = node_id_min + n_nodes - 1

print("generate unipartite graph with random edges...")

t_start = time.clock()

with open("data\\graph_unipartite_no_order.bin", "wb") as f:
    cur_edge_id = 1
    while cur_edge_id <= n_edges:
        node_x_id = random.randint(node_id_min, node_id_max)
        node_y_id = random.randint(node_id_min, node_id_max)
        while node_x_id == node_y_id:
            node_y_id = random.randint(node_id_min, node_id_max)
        f.write(struct.pack('i', node_x_id))
        f.write(struct.pack('i', node_y_id))
        cur_edge_id += 1

t_stop = time.clock()

print("graph generation accomplished")
print("time elapsed: " + str(t_stop - t_start) + " seconds")
print("nodes: " + str(n_nodes))
print("edges (may have duplication): " + str(n_edges))
