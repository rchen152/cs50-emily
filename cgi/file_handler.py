#!usr/bin/env python

import text_handler

def default_reply():
    return get_line(0)

'''def dump_topics():
    lines = get_all_lines()
    topics = []
    matches = []

    for i in range(len(lines)):
        words = text_handler.get_sorted_words(lines[i])
        for word in words:
            if len(word) >= 5:
                if not word in topics:
                    topics.append(word)
                    matches.append([i])
                else:
                    ind = topics.index(word)
                    mathces[ind].append(i)
    f = open('topics.txt', 'w')
    for i in range(len(topics)):
        f.write(topics[i]+'*')
        for j in range(len(mathces[i])):
            f.write(str(matches[i][j]))
            if j < len(matches[i])-1:
                f.write('*')
            else:
                f.write('\n')
    f.close()'''

def get_topic_match(line = '', prev_line = '', word_threshold = 0):
    words = text_handler.get_sorted_words(line)
    emily_lines = get_unsorted_emily_lines()
    for i in range(len(emily_lines)):
        emily_lines[i] = get_line(emily_lines[i])
    for word in words:
        if len(word) <= 4:
            return None
        for e_line in emily_lines:
            if text_handler.contains(e_line, word, word_threshold):
                if not text_handler.match(e_line, get_line(1), 0):
                    if not text_handler.match(e_line, prev_line, 0):
                        return e_line
    return None

def get_index(line = '', threshold = 0):
    lines = get_all_lines()
    length = len(lines)
    for i in xrange(length):
        if text_handler.match(line, lines[i], threshold):
            return [i, length]
    return [-1, length]
    
def get_line(index = 0):
    try:
        return get_all_lines()[index]
    except IndexError:
        return None

def get_lines_from_indices(indices = []):
    lines = []
    for index in indices:
        lines.append(get_line(index))
    return lines

def get_all_user_lines(emily_index = -1):
    if emily_index == -1:
        return __get_unsorted_user_lines()

    connected = []
    topic_matched = []
    unconnected = []
    connections = __get_all_connections()
    for conn in connections:
        indices = __split_indices(conn)
        if emily_index == -1 or indices[0] == emily_index:
            if not indices[1] in connected:
                connected.append(indices[1])
                if indices[1] in unconnected:
                    unconnected.pop(unconnected.index(indices[1]))
        else:
            if not indices[1] in connected and not indices[1] in unconnected:
                unconnected.append(indices[1])
    return connected + unconnected

def __get_unsorted_user_lines():
    lines = []
    connections = __get_all_connections()
    for conn in connections:
        indices = __split_indices(conn)
        if not indices[1] in lines:
            lines.append(indices[1])
    return lines

def get_emily_lines(k_0 = -1, k_1 = -1):
    if k_0 == -1 and k_1 == -1:
        return get_unsorted_emily_lines()
    med_connected = []
    weak_connected = []
    unconnected = []
    connections = __get_all_connections()
    for conn in connections:
        indices = __split_indices(conn)
        if indices[1] == k_1:
            if not indices[2] in med_connected:
                med_connected.append(indices[2])
                if indices[2] in weak_connected:
                    weak_connected.pop(weak_connected.index(indices[2]))
                if indices[2] in unconnected:
                    unconnected.pop(unconnected.index(indices[2]))
        elif indices[0] == k_0:
            if not indices[2] in med_connected and not indices[2] in weak_connected:
                weak_connected.append(indices[2])
                if indices[2] in unconnected:
                    unconnected.pop(unconnected.index(indices[2]))
        else:
            if not indices[2] in med_connected and not indices[2] in weak_connected and not indices[2] in unconnected:
                unconnected.append(indices[2])
        if not indices[0] in med_connected and not indices[0] in weak_connected and not indices[0] in unconnected:
            unconnected.append(indices[0])
    return med_connected + weak_connected + unconnected

def get_unsorted_emily_lines():
    lines = []
    connections = __get_all_connections()
    for conn in connections:
        indices = __split_indices(conn)
        if not indices[0] in lines:
            lines.append(indices[0])
        if not indices[2] in lines:
            lines.append(indices[2])
    return lines

def get_all_lines():
    f = open('lines.txt', 'r')
    lines = f.readlines()
    f.close()
    return lines

def insert_line(line = '', threshold = 0):
    ind = get_index(line, threshold)
    if ind[0] != -1:
        return ind[0]
    f = open('lines.txt', 'a')
    f.write(line+'\n')
    f.close()
    return ind[1]

def delete_line(ind = 0):
    lines = get_all_lines()
    f = open('lines.txt', 'w')
    for i in xrange(len(lines)):
        if not i == ind:
            f.write(lines[i])
    f.close()
    
    connections = __get_all_connections()
    f = open('connections.txt', 'w')
    for conn in connections:
        indices = __split_indices(conn)
        if not indices[0] == ind and not indices[1] == ind and not indices[2] == ind:
            for i in xrange(len(indices)):
                if indices[i] > ind:
                    indices[i] = indices[i] - 1
            f.write(__join_indices(indices[0], indices[1], indices[2]))
    f.close()
    return 0
    
def get_conn(k_0 = -1, k_1 = -1, k_2 = -1):
    connections = __get_all_connections()
    for conn in connections:
        indices = __split_indices(conn)
        if (k_0 == -2 or indices[0] == k_0) and (k_1 == -2 or indices[1] == k_1) and (k_2 == -2 or indices[2] == k_2):
            if not indices[2] == k_0:
                return [indices[2], True]
    return [0, False]

def get_approx_conn(k_0 = -1, k_1 = -1, teaching = False, first_reply = False):
    conn = get_conn(k_0, k_1, -2)
    if conn[1]:
        return conn[0]
    if not teaching:
        conn = get_conn(-2, k_1, -2)
        if conn[1]:
            return conn[0]
        if not first_reply:
            conn = get_conn(k_0, -2, -2)
            if conn[1]:
                return conn[0]
    return -1

def get_matching_conns(k = -1):
    matching_conns = []
    connections = __get_all_connections()
    for conn in connections:
        indices = __split_indices(conn)
        if indices[0] == k or indices[1] == k or indices[2] == k:
            matching_conns.append(indices)
    return matching_conns
        
def insert_conn(k_0 = 0, k_1 = 0, k_2 = 0):
    if get_conn(k_0, k_1, k_2)[1]:
        return False
    f = open('connections.txt', 'a')
    f.write(__join_indices(k_0, k_1, k_2))
    f.close()
    return True
    
def delete_conn(k_0 = 0, k_1 = 0, k_2 = 0):
    target_conn = __join_indices(k_0, k_1, k_2)
    connections = __get_all_connections()
    f = open('connections.txt', 'w')
    for i in xrange(len(connections)):
        if connections[i] == target_conn:
            i = i+1
            while i < len(connections):
                f.write(connections[i])
                i = i+1
            f.close()
            return True
        f.write(connections[i])
    f.close()
    return False
    
def match(line_0, line_1, threshold):
    return text_handler.match(line_0, line_1, threshold)

def __split_indices(connection = '0*0*0\n'):
    indices = connection.split('*')
    for i in xrange(len(indices)):
        try:
            indices[i] = int(indices[i].rstrip('\n'))
        except ValueError:
            indices[i] = indices[i].rstrip('\n')
    return indices
    
def __join_indices(k_0 = 0, k_1 = 0, k_2 = 0):
    return str(k_0) + "*" + str(k_1) + "*" + str(k_2) + '\n'

def __get_all_connections():
    f = open('connections.txt', 'r')
    connections = f.readlines()
    f.close()
    return connections
