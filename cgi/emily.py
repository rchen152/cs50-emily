#!usr/bin/env python

import file_handler

STRICT_THRESHOLD = 0.05
LOOSE_THRESHOLD = 0.2

WORD_THRESHOLD = 1

def start_conversation():
    return file_handler.get_line(1)

def say(line_0, line_1, teaching = False):
    k_0 = file_handler.get_index(line_0, 0)[0]
    if not teaching and k_0 == -1:
        k_0 = file_handler.get_index(line_0, STRICT_THRESHOLD)[0]
        if k_0 == -1:
            k_0 = file_handler.get_index(line_0, LOOSE_THRESHOLD)[0]
    k_1 = file_handler.get_index(line_1, 0)[0]
    if not teaching and k_1 == -1:
        k_1 = file_handler.get_index(line_1, STRICT_THRESHOLD)[0]
        if k_1 == -1:
            k_1 = file_handler.get_index(line_1, LOOSE_THRESHOLD)[0]
    if teaching and (k_0 == -1 or k_1 == -1):
        return None
    ind = file_handler.get_approx_conn(k_0, k_1, teaching, file_handler.match(line_0, start_conversation(), 0))
    if ind == -1:
        if teaching:
            return None
        line = file_handler.get_topic_match(line = line_1, prev_line = line_0, word_threshold = WORD_THRESHOLD)
        if line == None and not file_handler.match(line_0, start_conversation(), 0):
            line = file_handler.get_topic_match(line = line_0, prev_line = line_0, word_threshold = WORD_THRESHOLD)
        if line == None:
            return file_handler.default_reply()
        return line
    else:
        return file_handler.get_line(ind)
    
def teach(line_0, line_1, line_2):
    k_0 = file_handler.insert_line(line_0.rstrip('\n'))
    k_1 = file_handler.insert_line(line_1.rstrip('\n'))
    k_2 = file_handler.insert_line(line_2.rstrip('\n'))
    return file_handler.insert_conn(k_0, k_1, k_2)

def get_user_responses(line):
    indices = file_handler.get_all_user_lines(file_handler.get_index(line, 0)[0])
    return file_handler.get_lines_from_indices(indices)
    
def get_emily_responses(line_0, line_1):
    indices = file_handler.get_emily_lines(file_handler.get_index(line_0, 0)[0], file_handler.get_index(line_1, 0)[0])
    return file_handler.get_lines_from_indices(indices)

def get_all_responses():
    responses = file_handler.get_all_lines()
    responses.reverse()
    return responses

def delete_response(line = None, threshold = 0, index = -1):
    if line == None:
        ind = [index, -1]
    else:
        ind = file_handler.get_index(line, threshold)
    if ind[0] == -1:
        return False
    file_handler.delete_line(ind[0])
    return True

def get_conns(line = None, threshold = 0, index = -1):
    if line == None:
        ind = [index, -1]
    else:
        ind = file_handler.get_index(line, threshold)
    if ind[0] == -1:
        return None
    return file_handler.get_matching_conns(ind[0])
