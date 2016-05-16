import struct
import math
import sys
import os
from operator import itemgetter
import bucket_sort_bipartite
import bucket_sort_l1
import bucket_sort_r2



def gen_file_l1(in_file_name, out_left_node_l1):
    with open(out_left_node_l1, 'wb') as outf:
        right_node_list = []
        temp_left_node_id = -1
        temp_left_node_count = -1
        with open(in_file_name, "rb") as f:
            byteblock = f.read(8)
            left_node_id, right_node_id = struct.unpack('i', byteblock[0:4])[0], struct.unpack('i', byteblock[4:8])[0]
            temp_left_node_id = left_node_id
            right_node_list.append(right_node_id)
            temp_left_node_count = 1
            byteblock = f.read(8)
            while len(byteblock) == 8:
                left_node_id, right_node_id = struct.unpack('i', byteblock[0:4])[0], struct.unpack('i', byteblock[4:8])[
                    0]
                if temp_left_node_id == left_node_id:
                    temp_left_node_count = temp_left_node_count + 1
                    right_node_list.append(right_node_id)
                else:
                    for temp_right_node_id in right_node_list:
                        outf.write(struct.pack('i', temp_left_node_id))
                        outf.write(struct.pack('i', temp_right_node_id))
                        outf.write(struct.pack('i', temp_left_node_count))
                    right_node_list = [right_node_id]
                    temp_left_node_id = left_node_id
                    temp_left_node_count = 1
                byteblock = f.read(8)
            for temp_right_node_id in right_node_list:
                outf.write(struct.pack('i', left_node_id))
                outf.write(struct.pack('i', temp_right_node_id))
                outf.write(struct.pack('i', temp_left_node_count))


def gen_file_r2(in_file_name, out_left_node_r1):
    with open(out_left_node_r1, 'wb') as outf:
        left_node_list = []
        temp_right_node_id = -1
        temp_right_node_count = -1
        with open(in_file_name, "rb") as f:
            byteblock = f.read(12)
            left_node_id, right_node_id, left_node_count = struct.unpack('i', byteblock[0:4])[0], \
                                                           struct.unpack('i', byteblock[4:8])[0], \
                                                           struct.unpack('i', byteblock[8:12])[0]
            left_node_list.append((left_node_id, left_node_count))
            temp_right_node_id = right_node_id;
            temp_right_node_count = 1;
            while len(byteblock) == 12:
                left_node_id, right_node_id, left_node_count = struct.unpack('i', byteblock[0:4])[0], \
                                                               struct.unpack('i', byteblock[4:8])[0], \
                                                               struct.unpack('i', byteblock[8:12])[0]
                if temp_right_node_id == right_node_id:
                    temp_right_node_count = temp_right_node_count + 1
                    left_node_list.append((left_node_id, left_node_count))
                else:
                    for (temp_left_node_id, temp_left_node_count) in left_node_list:
                        outf.write(struct.pack('i', temp_left_node_id))
                        outf.write(struct.pack('i', temp_right_node_id))
                        outf.write(struct.pack('i', temp_left_node_count))
                        outf.write(struct.pack('i', temp_right_node_count))
                    left_node_list = [(left_node_id, left_node_count)]
                    temp_right_node_id = right_node_id
                    temp_right_node_count = 1
                byteblock = f.read(12)
            for (temp_left_node_id, temp_left_node_count) in left_node_list:
                outf.write(struct.pack('i', temp_left_node_id))
                outf.write(struct.pack('i', right_node_id))
                outf.write(struct.pack('i', temp_left_node_count))
                outf.write(struct.pack('i', temp_right_node_count))


if __name__ == "__main__":
    import time

    t_start = time.clock()
    import gen_bipartite_graph_random
    bucket_sort_bipartite.sort_bipartite("data\\graph_bipartite_no_order.bin", "data\\graph_bipartite_left.bin",
                                         "data\\graph_bipartite_right.bin")
    gen_file_l1("data\\graph_bipartite_left.bin", "data\\graph_bipartite_L1.bin")
    bucket_sort_l1.sort_bipartite("data\\graph_bipartite_L1.bin", "data\\graph_bipartite_L1temp.bin",
                                  "data\\graph_bipartite_R1.bin")
    gen_file_r2("data\\graph_bipartite_R1.bin", "data\\graph_bipartite_R2.bin")
    bucket_sort_r2.sort_bipartite("data\\graph_bipartite_R2.bin", "data\\graph_bipartite_L2.bin",
                                  "data\\graph_bipartite_R2temp.bin")
    t_stop = time.clock()
    print("")
    print("time elapsed: " + str(t_stop - t_start) + " seconds")
