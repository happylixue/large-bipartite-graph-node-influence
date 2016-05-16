import struct


def gen_left_node_index_file(left_in_file, left_out_file):
    with open(left_out_file, 'wb') as outf:
        temp_left_node_id = -1
        offset = -1
        length = 0
        with open(left_in_file, "rb") as f:
            byteblock = f.read(8)
            left_node_id, right_node_id = struct.unpack('i', byteblock[0:4])[0], \
                                          struct.unpack('i', byteblock[4:8])[0]
            offset = 0
            temp_left_node_id = left_node_id
            length = 8
            while len(byteblock) == 8:
                left_node_id, right_node_id = struct.unpack('i', byteblock[0:4])[0], \
                                              struct.unpack('i', byteblock[4:8])[0]
                if temp_left_node_id == left_node_id:
                    length = length + 8
                else:
                    outf.write(struct.pack('i', temp_left_node_id))
                    outf.write(struct.pack('i', offset))
                    outf.write(struct.pack('i', length))
                    offset = length + offset
                    length = 8
                    temp_left_node_id = left_node_id
                byteblock = f.read(8)
            outf.write(struct.pack('i', temp_left_node_id))
            outf.write(struct.pack('i', offset))
            outf.write(struct.pack('i', length))


def gen_right_node_index_file(right_in_file, right_out_file):
    with open(right_out_file, 'wb') as outf:
        temp_right_node_id = -1
        offset = -1
        length = 0
        with open(right_in_file, "rb") as f:
            byteblock = f.read(8)
            left_node_id, right_node_id = struct.unpack('i', byteblock[0:4])[0], \
                                          struct.unpack('i', byteblock[4:8])[0]
            offset = 0
            temp_right_node_id = right_node_id
            length = 8
            while len(byteblock) == 8:
                left_node_id, right_node_id = struct.unpack('i', byteblock[0:4])[0], \
                                              struct.unpack('i', byteblock[4:8])[0]
                if temp_right_node_id == right_node_id:
                    length = length + 8
                else:
                    outf.write(struct.pack('i', temp_right_node_id))
                    outf.write(struct.pack('i', offset))
                    outf.write(struct.pack('i', length))
                    offset = length + offset
                    length = 8
                    temp_right_node_id = right_node_id
                byteblock = f.read(8)
            outf.write(struct.pack('i', temp_right_node_id))
            outf.write(struct.pack('i', offset))
            outf.write(struct.pack('i', length))

if __name__ == "__main__":
    import time

    t_start = time.clock()
    gen_left_node_index_file("data\\graph_bipartite_left.bin", "data\\graph_bipartite_LI.bin")
    gen_right_node_index_file("data\\graph_bipartite_right.bin", "data\\graph_bipartite_RI.bin")
    t_stop = time.clock()
    print("")
    print("time elapsed: " + str(t_stop - t_start) + " seconds")