import struct


def gen_left_node_power(input_file_name):
    left_power_list = []
    temp_left_node_id = -1
    temp_left_node_id_power = 0
    with open(input_file_name, "rb") as f:
        byteblock = f.read(16)
        left_node_id, right_node_id, left_node_count, right_node_count = struct.unpack('i', byteblock[0:4])[0], \
                                                                         struct.unpack('i', byteblock[4:8])[0], \
                                                                         struct.unpack('i', byteblock[8:12])[0], \
                                                                         struct.unpack('i', byteblock[12:16])[0]
        temp_left_node_id = left_node_id
        temp_left_node_id_power = left_node_count * left_node_count
        while len(byteblock) == 16:
            left_node_id, right_node_id, left_node_count, right_node_count = struct.unpack('i', byteblock[0:4])[0], \
                                                                             struct.unpack('i', byteblock[4:8])[0], \
                                                                             struct.unpack('i', byteblock[8:12])[0], \
                                                                             struct.unpack('i', byteblock[12:16])[0]
            if temp_left_node_id == left_node_id:
                temp_left_node_id_power = temp_left_node_id_power + (left_node_count * left_node_count)
            else:
                left_power_list.append((temp_left_node_id, temp_left_node_id_power))
                temp_left_node_id = left_node_id
                temp_left_node_id_power = 0

            byteblock = f.read(16)
        left_power_list.append((temp_left_node_id, temp_left_node_id_power))

    left_power_list.sort(key=lambda x: x[1])
    N = 10

    print("")
    print("top " + str(N) + " most powerful left nodes")
    idx = 0
    for idx in range(0, N):
        print(str(idx) + " : " + str(left_power_list[-1+-idx]) )


def gen_right_node_power(input_file_name):
    right_power_list = []
    temp_right_node_id = -1
    temp_right_node_id_power = 0
    with open(input_file_name, "rb") as f:
        byteblock = f.read(16)
        left_node_id, right_node_id, left_node_count, right_node_count = struct.unpack('i', byteblock[0:4])[0], \
                                                                         struct.unpack('i', byteblock[4:8])[0], \
                                                                         struct.unpack('i', byteblock[8:12])[0], \
                                                                         struct.unpack('i', byteblock[12:16])[0]
        temp_right_node_id = right_node_id
        temp_right_node_id_power = right_node_count * right_node_count
        while len(byteblock) == 16:
            left_node_id, right_node_id, left_node_count, right_node_count = struct.unpack('i', byteblock[0:4])[0], \
                                                                             struct.unpack('i', byteblock[4:8])[0], \
                                                                             struct.unpack('i', byteblock[8:12])[0], \
                                                                             struct.unpack('i', byteblock[12:16])[0]
            if temp_right_node_id == right_node_id:
                temp_right_node_id_power = temp_right_node_id_power + (right_node_count * right_node_count)
            else:
                right_power_list.append((temp_right_node_id, temp_right_node_id_power))
                temp_right_node_id = right_node_id
                temp_right_node_id_power = 0

            byteblock = f.read(16)
        right_power_list.append((temp_right_node_id, temp_right_node_id_power))

    right_power_list.sort(key=lambda x: x[1])
    N = 10

    print("")
    print("top " + str(N) + " most powerful right nodes")
    idx = 0
    for idx in range(0, N):
        print(str(idx) + " : " + str(right_power_list[-1+-idx]) )


if __name__ == "__main__":
    import time

    t_start = time.clock()
    gen_left_node_power("data\\graph_bipartite_L2.bin")
    gen_right_node_power("data\\graph_bipartite_R2.bin")
    t_stop = time.clock()
    print("")
    print("time elapsed: " + str(t_stop - t_start) + " seconds")

