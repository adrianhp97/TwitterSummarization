import math

def word_frequencies_list(tweets):
    word_frequencies = []
    word_dict = []
    for tweet in tweets:
        words_in_sentence = tweet.split(' ')
        for word in words_in_sentence:
            if word in word_dict:
                word_frequencies[word_dict.index(word)] += 1
            else:
                word_frequencies.append(1)
                word_dict.append(word)
    return word_dict, word_frequencies

def reduce_word_list(word_dict, word_frequencies, treshold=2):
    new_word_frequencies = word_frequencies.copy()
    new_word_dict = word_dict.copy()
    idx = 0
    while idx < len(new_word_frequencies):
        if new_word_frequencies[idx] < treshold:
            new_word_dict.pop(idx)
            new_word_frequencies.pop(idx)
        else:
            idx += 1
    return new_word_dict, new_word_frequencies

def graph_frequencies_list_all(tweets):
    graph = []
    graph_idx = 0
    for tweet in tweets:
        words_in_sentence = tweet.split(' ')
        prev_idx = -1
        idx_now = 0
        for word in words_in_sentence:
            if word != '':
                is_not_in_graph = True
                for idx_graph in range(len(graph)):
                    if graph[idx_graph]['word'] == word:
                        graph[idx_graph]['counter'] += 1
                        is_not_in_graph = False
                        idx_graph_representation = idx_graph
                        break
                if is_not_in_graph:
                    node = {
                        'idx': graph_idx,
                        'word': word,
                        'counter': 1,
                        'next_neighbours': [],
                        'prev_neighbours': []
                    }
                    if prev_idx != -1:
                        node['prev_neighbours'].append(prev_idx)
                        if graph_idx not in graph[prev_idx]['next_neighbours'] and graph_idx != prev_idx:
                            graph[prev_idx]['next_neighbours'].append(graph_idx)
                    prev_idx = graph_idx
                    graph_idx += 1
                    graph.append(node)
                else:
                    if prev_idx != -1:
                        if prev_idx not in graph[idx_graph_representation]['prev_neighbours'] and idx_graph_representation != prev_idx:
                            graph[idx_graph_representation]['prev_neighbours'].append(prev_idx)
                        if idx_graph_representation not in graph[prev_idx]['next_neighbours'] and idx_graph_representation != prev_idx:
                            graph[prev_idx]['next_neighbours'].append(idx_graph_representation)
                    prev_idx = idx_graph_representation
    return graph

def graph_frequencies_list_reduce(tweets, treshold=2):
    words, freqs = word_frequencies_list(tweets)
    new_words, new_freqs = reduce_word_list(words, freqs, treshold)
    graph = []
    graph_idx = 0
    for tweet in tweets:
        words_in_sentence = tweet.split(' ')
        prev_idx = -1
        idx_now = 0
        for word in words_in_sentence:
            if word != '' and word in new_words:
                is_not_in_graph = True
                for idx_graph in range(len(graph)):
                    if graph[idx_graph]['word'] == word:
                        graph[idx_graph]['counter'] += 1
                        is_not_in_graph = False
                        idx_graph_representation = idx_graph
                        break
                if is_not_in_graph:
                    node = {
                        'idx': graph_idx,
                        'word': word,
                        'counter': 1,
                        'next_neighbours': [],
                        'prev_neighbours': []
                    }
                    if prev_idx != -1:
                        node['prev_neighbours'].append(prev_idx)
                        if graph_idx not in graph[prev_idx]['next_neighbours'] and graph_idx != prev_idx:
                            graph[prev_idx]['next_neighbours'].append(graph_idx)
                    prev_idx = graph_idx
                    graph_idx += 1
                    graph.append(node)
                else:
                    if prev_idx != -1:
                        if prev_idx not in graph[idx_graph_representation]['prev_neighbours'] and idx_graph_representation != prev_idx:
                            graph[idx_graph_representation]['prev_neighbours'].append(prev_idx)
                        if idx_graph_representation not in graph[prev_idx]['next_neighbours'] and idx_graph_representation != prev_idx:
                            graph[prev_idx]['next_neighbours'].append(idx_graph_representation)
                    prev_idx = idx_graph_representation
    return graph

def calculate_weight(counter, distance, base):
    return counter - (distance * (math.log(counter)/math.log(base)))

def get_next_path(idx, graph, distance, base, data={'path': [], 'weight': 0}, iterator=5):
    if len(graph[idx]['next_neighbours']) == 0 or iterator == distance:
        new_data = {
            'path': data['path'].copy(),
            'weight': data['weight']
        }
        if idx not in data['path']:
            new_data['path'].append(idx)
            new_data['weight'] += calculate_weight(graph[idx]['counter'], distance, base)
        return new_data
    else:
        new_data = {
            'path': data['path'].copy(),
            'weight': data['weight']
        }
        if idx not in data['path']:
            new_data['path'].append(idx)
            new_data['weight'] += calculate_weight(graph[idx]['counter'], distance, base)
            neighbours = []
            for next_idx in graph[idx]['next_neighbours']:
                data_send = {
                    'path': new_data['path'].copy(),
                    'weight': data['weight']
                }
                if next_idx not in data_send['path']:
                    neighbours.append(get_next_path(next_idx, graph, distance + 1, base, data_send, iterator))
            data_max = {'path': [], 'weight': 0}
            for neighbour in neighbours:
                if neighbour['weight'] > data_max['weight']:
                    data_max = neighbour.copy()
            return data_max.copy()
        else:
            return new_data.copy()

def get_prev_path(idx, graph, distance, base, data={'path': [], 'weight': 0}, iterator=5):
    if len(graph[idx]['next_neighbours']) == 0 or iterator == distance:
        new_data = {
            'path': data['path'].copy(),
            'weight': data['weight']
        }
        if idx not in data['path']:
            new_data['path'].insert(0, idx)
            new_data['weight'] += calculate_weight(graph[idx]['counter'], distance, base)
        return new_data
    else:
        new_data = {
            'path': data['path'].copy(),
            'weight': data['weight']
        }
        if idx not in data['path']:
            new_data['path'].insert(0, idx)
            new_data['weight'] += calculate_weight(graph[idx]['counter'], distance, base)
            neighbours = []
            for next_idx in graph[idx]['prev_neighbours']:
                data_send = {
                    'path': new_data['path'].copy(),
                    'weight': data['weight']
                }
                if next_idx not in data_send['path']:
                    neighbours.append(get_prev_path(next_idx, graph, distance + 1, base, data_send, iterator))
            data_max = {'path': [], 'weight': 0}
            for neighbour in neighbours:
                if neighbour['weight'] > data_max['weight']:
                    data_max = neighbour.copy()
            return data_max.copy()
        else:
            return new_data.copy()

def get_topic_index(graph, topic):
    for node in graph:
        if node['word'] == topic:
            return node['idx']
    return -1

def combine_path(path_next, path_prev):
    all_path = {
        'path': path_prev['path'][:-1] + path_next['path'],
        'weight': path_prev['weight'] + path_next['weight']
    }
    return all_path

def get_sentence(graph, path):
    sentence = ''
    for item in path['path']:
        for node in graph:
            if node['idx'] == item:
                sentence += node['word'] + ' '
    return sentence

def summarize(tweets, topic, base=2, iterator=5, treshold=10):
    graph = graph_frequencies_list_reduce(tweets, treshold)
    topic_index = get_topic_index(graph, topic)
    if topic_index == -1:
        return 'this string cannot be a topic'
    path_next = get_next_path(topic_index, graph, 0, base, iterator=iterator)
    path_prev = get_prev_path(topic_index, graph, 0, base, iterator=iterator)
    all_path = combine_path(path_next, path_prev)
    return get_sentence(graph, all_path)