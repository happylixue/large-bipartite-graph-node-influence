# customized bucket sort

import struct
import math
import sys
import os
from operator import itemgetter


def sort_bipartite(in_file_name, left_pivot_out_file_name, right_pivot_out_file_name,bucket_size_expect=100):
    left_node_id_min = sys.maxsize
    right_node_id_min = sys.maxsize
    left_node_id_max = -1
    right_node_id_max = -1
    n_left_nodes = 0
    n_right_nodes = 0
    n_edges = 0

    # first scan
    # we may skip this scan in case we already have id range statistics and total number of edges
    print("edge format file scan starting...")

    with open(in_file_name, "rb") as f:
        byteblock = f.read(16)
        while len(byteblock) == 16:
            left_node_id, right_node_id, left_node_count, right_node_count = struct.unpack('i', byteblock[0:4])[0], \
                                                                             struct.unpack('i', byteblock[4:8])[0], \
                                                                             struct.unpack('i', byteblock[8:12])[0], \
                                                                             struct.unpack('i', byteblock[12:16])[0]
            if left_node_id < left_node_id_min:
                left_node_id_min = left_node_id
            elif left_node_id > left_node_id_max:
                left_node_id_max = left_node_id
            if right_node_id < right_node_id_min:
                right_node_id_min = right_node_id
            elif right_node_id > right_node_id_max:
                right_node_id_max = right_node_id
            n_edges += 1
            byteblock = f.read(16)

    print("scan finished.")
    print("edges: " + str(n_edges))
    print("left node id: " + str(left_node_id_min) + " - " + str(left_node_id_max))
    print("right node id: " + str(right_node_id_min) + " - " + str(right_node_id_max))

    # bucketing
    bucket_size_max = 10000000  # max value for sort-able bucket, according to memory and cpu limit
    # bucket_size_expect = 1000000 #expect each bucket to have this size in order to be efficiently sorted in the host machine / cluster
    # bucket_size_expect = 100
    n_buckets = int(n_edges / bucket_size_expect)  # number of buckets

    print("")
    print("expected buckets: " + str(n_buckets))
    print("bucketing...")

    left_node_id_range = left_node_id_max - left_node_id_min + 1
    right_node_id_range = right_node_id_max - right_node_id_min + 1

    left_node_id_step = math.floor(left_node_id_range / n_buckets) + 1
    right_node_id_step = math.floor(right_node_id_range / n_buckets) + 1

    bucket_sizes_left_pivot = [0] * n_buckets
    bucket_sizes_right_pivot = [0] * n_buckets

    bucket_fh_left_pivot = [None] * n_buckets
    bucket_fh_right_pivot = [None] * n_buckets

    bucket_fn_prefix_left_pivot = "data\\bucket_left_pivot.bin."
    bucket_fn_prefix_right_pivot = "data\\bucket_right_pivot.bin."

    for idx in range(0, n_buckets):
        bucket_fh_left_pivot[idx] = open(bucket_fn_prefix_left_pivot + str(idx), 'wb')
        bucket_fh_right_pivot[idx] = open(bucket_fn_prefix_right_pivot + str(idx), 'wb')

    with open(in_file_name, "rb") as f:
        byteblock = f.read(16)
        while len(byteblock) == 16:
            left_node_id, right_node_id, left_node_count, right_node_count = struct.unpack('i', byteblock[0:4])[0], \
                                                                             struct.unpack('i', byteblock[4:8])[0], \
                                                                             struct.unpack('i', byteblock[8:12])[0], \
                                                                             struct.unpack('i', byteblock[12:16])[0]
            bucket_idx_left = math.floor((left_node_id - left_node_id_min + 1) / left_node_id_step)
            bucket_idx_left = int(bucket_idx_left)
            if bucket_idx_left == n_buckets: bucket_idx_left -= 1
            bucket_idx_right = math.floor((right_node_id - right_node_id_min + 1) / right_node_id_step)
            bucket_idx_right = int(bucket_idx_right)
            if bucket_idx_right == n_buckets: bucket_idx_right -= 1
            bucket_fh_left_pivot[bucket_idx_left].write(byteblock)
            bucket_fh_right_pivot[bucket_idx_right].write(byteblock)
            byteblock = f.read(16)

    for idx in range(0, n_buckets):
        bucket_fh_left_pivot[idx].close()
        bucket_fh_right_pivot[idx].close()

    print("bucketing finished.")
    print("left node pivoting bucket files created: " + str(len(bucket_fh_left_pivot)))
    print("right node pivoting bucket files created: " + str(len(bucket_fh_right_pivot)))

    # local sort
    for idx in range(0, n_buckets):
        bucket_fh_left_pivot[idx] = open(bucket_fn_prefix_left_pivot + str(idx), 'rb')
        bucket_fh_right_pivot[idx] = open(bucket_fn_prefix_right_pivot + str(idx), 'rb')

    # left pivot sort
    with open(left_pivot_out_file_name, 'wb') as f:
        for idx in range(0, n_buckets):
            list_to_sort = []
            byteblock = bucket_fh_left_pivot[idx].read(16)
            while len(byteblock) == 16:
                left_node_id, right_node_id, left_node_count, right_node_count = struct.unpack('i', byteblock[0:4])[0], \
                                                                                 struct.unpack('i', byteblock[4:8])[0], \
                                                                                 struct.unpack('i', byteblock[8:12])[0], \
                                                                                 struct.unpack('i', byteblock[12:16])[0]
                list_to_sort.append((left_node_id, right_node_id, left_node_count, right_node_count))
                byteblock = bucket_fh_left_pivot[idx].read(16)
            list_to_sort = list(set(list_to_sort))  # de-duplicate
            list_to_sort.sort(key=itemgetter(0, 1, 0, 0))
            for edge in list_to_sort:
                f.write(struct.pack('i', edge[0]))
                f.write(struct.pack('i', edge[1]))
                f.write(struct.pack('i', edge[2]))
                f.write(struct.pack('i', edge[3]))
    print("")
    print("left pivot sorted data file created.")

    n_edges_dedup = 0
    # right pivot sort
    with open(right_pivot_out_file_name, 'wb') as f:
        for idx in range(0, n_buckets):
            list_to_sort = []
            byteblock = bucket_fh_right_pivot[idx].read(16)
            while len(byteblock) == 16:
                left_node_id, right_node_id, left_node_count, right_node_count = struct.unpack('i', byteblock[0:4])[0], \
                                                                                 struct.unpack('i', byteblock[4:8])[0], \
                                                                                 struct.unpack('i', byteblock[8:12])[0], \
                                                                                 struct.unpack('i', byteblock[12:16])[0]
                list_to_sort.append((left_node_id, right_node_id, left_node_count, right_node_count))
                byteblock = bucket_fh_right_pivot[idx].read(16)
            list_to_sort = list(set(list_to_sort))  # de-duplicate
            n_edges_dedup += len(list_to_sort)
            list_to_sort.sort(key=itemgetter(1, 0, 0, 0))
            for edge in list_to_sort:
                f.write(struct.pack('i', edge[0]))
                f.write(struct.pack('i', edge[1]))
                f.write(struct.pack('i', edge[2]))
                f.write(struct.pack('i', edge[3]))
    print("right pivot sorted data file created.")

    for idx in range(0, n_buckets):
        bucket_fh_left_pivot[idx].close()
        bucket_fh_right_pivot[idx].close()

    for idx in range(0, n_buckets):
        os.remove(bucket_fn_prefix_left_pivot + str(idx))
        os.remove(bucket_fn_prefix_right_pivot + str(idx))

    print("")
    print("left node pivoting bucket files removed: " + str(len(bucket_fh_left_pivot)))
    print("right node pivoting bucket files removed: " + str(len(bucket_fh_right_pivot)))

    return left_node_id_min, right_node_id_min, left_node_id_max, right_node_id_max, n_edges_dedup


if __name__ == "__main__":
    import time

    t_start = time.clock()
    sort_bipartite("data\graph_bipartite_R2.bin", "data\graph_bipartite_L2.bin", "data\graph_bipartite_R_temp.bin")
    t_stop = time.clock()
    print("")
    print("time elapsed: " + str(t_stop - t_start) + " seconds")
