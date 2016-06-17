#!usr/bin/env python

def contains(line = '', word = '', word_threshold = 0):
    words = __get_words(line)
    for line_word in words:
        if __edit_distance(word, line_word) <= word_threshold:
            return True
    return False

def get_sorted_words(line = ''):
    words = __get_words(line)
    sorted_words = []
    for i in xrange(len(words)):
        j = 0
        while j < len(sorted_words):
            if len(sorted_words[j]) > len(words[i]):
                j = j+1
            else:
                break
        sorted_words.insert(j, words[i])
    return sorted_words

def match(source = '', target = '', threshold = 0):
    return __edit_distance(source, target) <= threshold*len(target)

def __edit_distance(source = '', target = ''):
    source = __to_alnum(source)
    target = __to_alnum(target)
    
    if len(source) == 0:
        return len(target)
    if len(target) == 0:
        return len(source)
 
    INF = len(source) + len(target);
    score = {(0,0):INF}

    for i in xrange(len(source)+1):
        score[(i+1,1)] = i
        score[(i+1,0)] = INF
    for j in xrange(len(target)+1):
        score[(1,j+1)] = j
        score[(0,j+1)] = INF
 
    sd = {}
    for c in source+target:
        if not sd.has_key(c):
            sd[c] = 0
 
    for i in xrange(len(source)):
        DB = 0
        for j in xrange(len(target)):
            i1 = sd[target[j]]
            j1 = DB
 
            if source[i] == target[j]:
                score[i+2,j+2] = score[i+1, j+1]
                DB = j
            else:
                score[i+2,j+2] = min(score[i+1,j+1], min(score[i+2,j+1], score[i+1,j+2])) + 1
            score[i+2,j+2] = min(score[i+2,j+2], score[i1, j1] + (i-i1) + 1 + (j-j1))
        sd[source[i]] = i+1
    
    return score[(len(source)+1,len(target)+1)]
    
def __to_alnum(text = ''):
    text = text.strip()
    length = len(text)
    for i in xrange(len(text)):
        if not text[length-i-1] == ' ' and not text[length-i-1].isalnum():
            text = text[:length-i-1] + text[length-i:]
    return text.lower()

def __get_words(line = ''):
    line = __to_alnum(line)
    words = line.split(' ')
    length = len(words)
    for i in xrange(length):
        words[length-i-1] = words[length-i-1].strip()
        if len(words[length-i-1]) == 0:
            words.pop(length-i-1)
    return words
