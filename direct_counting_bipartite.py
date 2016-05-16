#direct in memory degree counting and spectrum forming

import struct
import time

in_filename = "data\\graph_bipartite_no_order.bin"

t_start_overall = time.clock()

print("start building degree statistics for a bipartite graph...")

t_start = time.clock()

with open(in_filename, 'rb') as f:
    n_edges = 0
    left_node_degree_dict = {}
    right_node_degree_dict = {}
    byteblock = f.read(8)  
    while len(byteblock) == 8:
        n_edges += 1 
        left_node_id, right_node_id = struct.unpack('i', byteblock[0:4])[0], struct.unpack('i', byteblock[4:8])[0]
        if left_node_id in left_node_degree_dict:
            left_node_degree_dict[left_node_id] += 1
        else:
            left_node_degree_dict[left_node_id] = 1
        if right_node_id in right_node_degree_dict:
            right_node_degree_dict[right_node_id] += 1
        else:
            right_node_degree_dict[right_node_id] = 1
        byteblock = f.read(8)

t_stop = time.clock()
            
print("done.")    
print("edges: " + str(n_edges))
print("time elapsed: " + str(t_stop-t_start) + " seconds")


print("")
print("spectrum calculating...")

t_start = time.clock()

with open(in_filename, 'rb') as f:
    left_node_spectrum_dict = {}
    right_node_spectrum_dict = {}
    byteblock = f.read(8)
    while len(byteblock) == 8:
        left_node_id, right_node_id = struct.unpack('i', byteblock[0:4])[0], struct.unpack('i', byteblock[4:8])[0]
        if left_node_id not in left_node_spectrum_dict:
            left_node_spectrum_dict[left_node_id] = {right_node_degree_dict[right_node_id]:1}
        elif right_node_degree_dict[right_node_id] not in left_node_spectrum_dict[left_node_id]:
            left_node_spectrum_dict[left_node_id][right_node_degree_dict[right_node_id]] = 1
        else:
            left_node_spectrum_dict[left_node_id][right_node_degree_dict[right_node_id]] += 1
        if right_node_id not in right_node_spectrum_dict:
            right_node_spectrum_dict[right_node_id] = {left_node_degree_dict[left_node_id]:1}
        elif left_node_degree_dict[left_node_id] not in right_node_spectrum_dict[right_node_id]:
            right_node_spectrum_dict[right_node_id][left_node_degree_dict[left_node_id]] = 1
        else:
            right_node_spectrum_dict[right_node_id][left_node_degree_dict[left_node_id]] += 1
        byteblock = f.read(8)

t_stop = time.clock()

print("done.")    
print("left nodes: " + str(len(left_node_spectrum_dict)))
print("right nodes: " + str(len(right_node_spectrum_dict)))
print("time elapsed: " + str(t_stop-t_start) + " seconds")

t_stop_overall = time.clock()

print("")
print("time elapsed: " + str(t_stop_overall-t_start_overall) + " seconds")

#output power top N and bottom N for both sides
def spectrum_power(spectrum):
    power = 0
    for key in spectrum:
        power += key * key * spectrum[key]
    return power
    
left_node_power_list = []
right_node_power_list = []

for node_id in left_node_spectrum_dict:
    left_node_power_list.append((node_id, spectrum_power(left_node_spectrum_dict[node_id])))
    
for node_id in right_node_spectrum_dict:
    right_node_power_list.append((node_id, spectrum_power(right_node_spectrum_dict[node_id])))
    
left_node_power_list.sort(key=lambda x: x[1])
right_node_power_list.sort(key=lambda x: x[1])

N = 10

print("")
print("top " + str(N) + " most powerful left nodes")
idx = 0
for idx in range(0,N):
    print(str(idx) + " : " + str(left_node_power_list[-1 + -1*idx]) + " - " + str(left_node_spectrum_dict[left_node_power_list[-1 + -1*idx][0]]))

print("top " + str(N) + " least powerful left nodes")
idx = 0
for idx in range(0,N):
    print(str(idx) + " : " + str(left_node_power_list[idx]) + " - " + str(left_node_spectrum_dict[left_node_power_list[idx][0]]))

print("top " + str(N) + " most powerful right nodes")
idx = 0
for idx in range(0,N):
    print(str(idx) + " : " + str(right_node_power_list[-1 + -1*idx]) + " - " + str(right_node_spectrum_dict[right_node_power_list[-1 + -1*idx][0]]))

print("top " + str(N) + " least powerful right nodes")
idx = 0
for idx in range(0,N):
    print(str(idx) + " : " + str(right_node_power_list[idx]) + " - " + str(right_node_spectrum_dict[right_node_power_list[idx][0]]))
    