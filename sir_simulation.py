import struct
import random
import bucket_sort_bipartite
import bucket_sort_l1
import bucket_sort_r2
import gen_node_spectrum_file
import gen_node_index_file


def sir_simulation(left_in_file, right_in_file, left_index_file, right_index_file, first_node_id, infection_rate,
                   immunization_rate, time, limit):
    node_count = 0
    with open(left_index_file, "rb") as f:
        byteblock = f.read(12)
        node_count = 1
        while len(byteblock) == 12:
            node_count = node_count + 1
            byteblock = f.read(12)

    with open(right_index_file, "rb") as f:
        byteblock = f.read(12)
        node_count = node_count + 1
        while len(byteblock) == 12:
            node_count = node_count + 1
            byteblock = f.read(12)

    infection_left_node_set = set([])
    infection_right_node_set = set([])

    if first_node_id < limit:
        infection_left_node_set.add(first_node_id)
    else:
        infection_right_node_set.add(first_node_id)
    immunization_node_set = set([])
    for current_time in range(1, time):
        infection_left_node_set, infection_right_node_set, immunization_node_set = infect_process(left_in_file,
                                                                                                  right_in_file,
                                                                                                  left_index_file,
                                                                                                  right_index_file,
                                                                                                  infection_left_node_set,
                                                                                                  infection_right_node_set,
                                                                                                  immunization_node_set,
                                                                                                  infection_rate,
                                                                                                  immunization_rate)

        rate = float((len(infection_left_node_set) + len(infection_right_node_set)) / float(node_count))
        # print "infect left node=======",len(infection_left_node_set)
        # print "infect right node======",len(infection_right_node_set)
        # print "immunization node======",len(immunization_node_set)
        print "s(time=" + str(current_time) + ") = " + str(rate)


def infect_process(left_in_file, right_in_file, left_index_file, right_index_file, infection_left_node_set,
                   infection_right_node_set, immunization_node_set, infection_rate,
                   immunization_rate):
    infection_right_node_set_copy = infection_right_node_set.copy()
    immunization_left_node_set = set([])
    for infection_left_node in infection_left_node_set:
        if random.uniform(0, 1) < immunization_rate:
            immunization_node_set.add(infection_left_node)
            immunization_left_node_set.add(infection_left_node)
        else:
            with open(left_index_file, "rb") as f:
                byteblock = f.read(12)
                while len(byteblock) == 12:
                    left_node_index_id, left_node_offset, left_node_length = struct.unpack('i', byteblock[0:4])[0], \
                                                                             struct.unpack('i', byteblock[4:8])[0], \
                                                                             struct.unpack('i', byteblock[8:12])[0]
                    if infection_left_node == left_node_index_id:
                        with open(left_in_file, "rb") as in_f:
                            in_f.read(left_node_offset)
                            remain_length = left_node_length
                            while remain_length >= 8:
                                node_value = in_f.read(8)
                                remain_length = remain_length - 8
                                if len(node_value) == 0:
                                    continue
                                new_left_node_id, new_right_node_id = struct.unpack('i', node_value[0:4])[0], \
                                                                      struct.unpack('i', node_value[4:8])[0]
                                if new_right_node_id not in list(immunization_node_set):
                                    if random.uniform(0, 1) < infection_rate:
                                        infection_right_node_set.add(new_right_node_id)
                        break
                    byteblock = f.read(12)
    for i_node in immunization_left_node_set:
        infection_left_node_set.remove(i_node)
    # infection_left_node_set = set(infection_left_node_list)


    # infection_right_node_list = list(infection_right_node_set)
    immunization_right_node_set = set([])
    for infection_right_node in list(infection_right_node_set_copy):
        if random.uniform(0, 1) < immunization_rate:
            immunization_node_set.add(infection_right_node)
            immunization_right_node_set.add(infection_right_node)
        with open(right_index_file, "rb") as f:
            byteblock = f.read(12)
            while len(byteblock) == 12:
                right_node_index_id, right_node_offset, right_node_length = struct.unpack('i', byteblock[0:4])[0], \
                                                                            struct.unpack('i', byteblock[4:8])[0], \
                                                                            struct.unpack('i', byteblock[8:12])[0]
                if infection_right_node == right_node_index_id:
                    with open(right_in_file, "rb") as in_f:
                        in_f.read(right_node_offset)
                        remain_length = right_node_length
                        while remain_length >= 8:
                            node_value = in_f.read(8)
                            remain_length = remain_length - 8
                            if len(node_value) == 0:
                                continue
                            new_left_node_id, new_right_node_id = struct.unpack('i', node_value[0:4])[0], \
                                                                  struct.unpack('i', node_value[4:8])[0]
                            if new_left_node_id not in list(immunization_node_set):
                                if random.uniform(0, 1) < infection_rate:
                                    infection_left_node_set.add(new_left_node_id)
                    break
                byteblock = f.read(12)

    for i_node in immunization_right_node_set:
        infection_right_node_set.remove(i_node)

    return infection_left_node_set, infection_right_node_set, immunization_node_set


if __name__ == "__main__":
    import time

    t_start = time.clock()

    import gen_bipartite_graph_random

    bucket_sort_bipartite.sort_bipartite("data\\graph_bipartite_no_order.bin", "data\\graph_bipartite_left.bin",
                                         "data\\graph_bipartite_right.bin", 1000000)
    gen_node_spectrum_file.gen_file_l1("data\\graph_bipartite_left.bin", "data\\graph_bipartite_L1.bin")
    bucket_sort_l1.sort_bipartite("data\\graph_bipartite_L1.bin", "data\\graph_bipartite_L1temp.bin",
                                  "data\\graph_bipartite_R1.bin", 1000000)
    gen_node_spectrum_file.gen_file_r2("data\\graph_bipartite_R1.bin", "data\\graph_bipartite_R2.bin")
    bucket_sort_r2.sort_bipartite("data\\graph_bipartite_R2.bin", "data\\graph_bipartite_L2.bin",
                                  "data\\graph_bipartite_R2temp.bin", 1000000)

    gen_node_index_file.gen_left_node_index_file("data\\graph_bipartite_left.bin", "data\\graph_bipartite_LI.bin")
    gen_node_index_file.gen_right_node_index_file("data\\graph_bipartite_right.bin", "data\\graph_bipartite_RI.bin")

    sir_simulation("data\\graph_bipartite_left.bin", "data\\graph_bipartite_right.bin", "data\\graph_bipartite_LI.bin",
                   "data\\graph_bipartite_RI.bin", 21, 0.7, 0.1, 50, 100)

    t_stop = time.clock()
    print("")
    print("time elapsed: " + str(t_stop - t_start) + " seconds")
