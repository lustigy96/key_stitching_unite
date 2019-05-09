import numpy as np
import pandas as pd
import logging

import threading
import time
# import matplotlib.pyplot as plt
import os
import operator as op
from functools import reduce
from bitstring import BitArray
import sys


hex2bin_map = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "a": "1010",
    "b": "1011",
    "c": "1100",
    "d": "1101",
    "e": "1110",
    "f": "1111"
}

'''Gabi'''
def ncr(n, r):
    # calculates {n \choose r}
    r = min(r, n - r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer / denom
def flip_probability(k, r, p):
    '''
    returns the probability of having at most r flips in k bits, where each flips occurs with probability p
    '''
    return np.sum([ncr(k, j) * p ** j * (1 - p) ** (k - j) for j in xrange(r + 1)])
def find_window_for_flip_probability(delta, r, p, epsilon=0.001, k_max=1000):
    '''
    returns the largest window size k for which the probability of having at most r flips in the window is at least delta
    '''
    k_min = r
    k = k_max
    while flip_probability(k, r, p) < delta + epsilon:
        print 'k_min=%d, k_max=%d' % (k_min, k_max)
        if flip_probability((k_min + k_max) / 2, r, p) > delta:
            k_min = (k_min + k_max) / 2
        else:
            k_max = (k_min + k_max) / 2
        if k_max - k_min < 2:
            k = k_min
            break
    return k
def expected_number_flips(k, p):
    '''
    return the expected number of flips in a window of length k
    '''
    return np.sum([j * ncr(k, j) * p ** j * (1 - p) ** (k - j) for j in xrange(k + 1)])
def hamming_dist(s1, s2):
    '''
    Calculate the Hamming distance between two bit strings
    '''
    if len(s1) == len(s2):
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))
    else:
        return -1  # error return value
def iterative_levenshtein(s, t, costs=(1, 1, 1), print_match_length=0):
    """
        SLOW!!!!
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t

        costs: a tuple or a list with three integers (d, i, s)
               where d defines the costs for a deletion
                     i defines the costs for an insertion and
                     s defines the costs for a substitution
        print_match_length: block length for printing matche description.
                            if 0, then no print
        the conclusion is for s=source and t =res (important for the relation between s and t, deletion and insertions)
    """
    rows = len(s) + 1
    cols = len(t) + 1
    deletes, inserts, substitutes = costs
    conclusion = {"F": 0, "D": 0, "I": 0, "DIST": 0}  # F for flips, D for del, I for insertion
    pointer_dict = {}

    dist = np.array([[0 for x in xrange(cols)] for x in xrange(rows)])  # zeros matrix

    # source prefixes can be transformed into empty strings
    # by deletions:
    for row in xrange(1, rows): dist[row][0] = row * deletes

    # target prefixes can be created from an empty source string
    # by inserting the characters
    for col in xrange(1, cols): dist[0][col] = col * inserts

    for col in xrange(1, cols):
        for row in xrange(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min([dist[row - 1][col] + deletes,
                                  dist[row][col - 1] + inserts,
                                  dist[row - 1][col - 1] + cost])  # substitution
            if print_match_length > 0:  # the path throw the matrix, step by step
                if dist[row][col] == dist[row - 1][col - 1] + cost:
                    pointer_dict[(row, col)] = (row - 1, col - 1)
                elif dist[row][col] == dist[row][col - 1] + inserts:
                    pointer_dict[(row, col)] = (row, col - 1)
                else:
                    pointer_dict[(row, col)] = (row - 1, col)
    #    for r in range(rows):
    #        print(dist[r])
    print pointer_dict
    if print_match_length > 0:
        new_s = ''
        new_t = ''
        match = ''
        p_row = row
        p_col = col
        while (p_row != 0) and (p_col != 0):
            #            print (p_row,p_col)
            if (p_row == pointer_dict[(p_row, p_col)][0] + 1) and (p_col == pointer_dict[(p_row, p_col)][1] + 1):
                new_s += s[p_row - 1]
                new_t += t[p_col - 1]
                if new_s[-1] == new_t[-1]:
                    match += '*'
                else:
                    match += 'f'
                    conclusion['F'] += 1
            elif (p_row == pointer_dict[(p_row, p_col)][0] + 1):  # only the column moves back
                new_s += s[p_row - 1]
                new_t += '-'
                match += '-'
                conclusion['D'] += 1
            else:
                new_s += '-'
                new_t += t[p_col - 1]
                match += '-'
                conclusion['I'] += 1
            p_row, p_col = pointer_dict[(p_row, p_col)]
        if (p_row == 0) and (p_col > 0):
            new_s += '-' * p_col
            new_t += t[:p_col]
            match += '-' * (p_col)
            conclusion['I'] += 1 * p_col
        elif (p_row > 0) and (p_col == 0):
            new_s += s[:p_row]
            new_t += '-' * (p_row)
            match += '-' * (p_row)
            conclusion['D'] += 1 * (p_row)
        # reverse the strings
        new_s = new_s[::-1]
        new_t = new_t[::-1]
        match = match[::-1]
        block = 0
        while (block + 1) * print_match_length < len(new_s):
            print new_s[block * print_match_length:(block + 1) * print_match_length]
            print new_t[block * print_match_length:(block + 1) * print_match_length]
            print match[block * print_match_length:(block + 1) * print_match_length] + '\n'
            block += 1
        if len(new_s) > block * print_match_length:
            print new_s[block * print_match_length:]
            print new_t[block * print_match_length:]
            print match[block * print_match_length:] + '\n'
    conclusion['DIST'] = dist[row][col]
    return conclusion
def levenshtein_edit_dist(s1, s2, show_strings=False):
    '''
    FASTER THAN iterative_levenshtein()
    Calculate the Levenshtein edit distance between two bit strings
    also returns the s1 locations where an exact match was found
    '''
    #    if len(s1) > len(s2):
    #        s1, s2 = s2, s1
    #    s1 = '1001101'
    #    s2 = '001011'
    conclusion = {'F': 0, 'D': 0, 'I': 0, 'DIST': 0}
    pointers = {}
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
                pointers[(i2, i1)] = (i2 - 1, i1 - 1)
            else:
                candidates = (distances[i1], distances[i1 + 1], distances_[-1])
                candidates_pointers = ((i2 - 1, i1 - 1), (i2 - 1, i1), (i2, i1 - 1))
                min_ind = np.argmin(candidates)
                distances_.append(1 + candidates[min_ind])
                pointers[(i2, i1)] = candidates_pointers[min_ind]
        distances = distances_
    s1_match_indices = []
    curr_pointer = (len(s2) - 1, len(s1) - 1)
    while (curr_pointer[0] > -1) and (curr_pointer[1] != -1):
        if (curr_pointer[0] == pointers[curr_pointer][0] + 1) and (curr_pointer[1] == pointers[curr_pointer][1] + 1):
            if s2[curr_pointer[0]] == s1[curr_pointer[1]]:
                s1_match_indices.append(curr_pointer[1])
            else:
                conclusion['F'] += 1
        elif (curr_pointer[0] == pointers[curr_pointer][0]) and (curr_pointer[1] == pointers[curr_pointer][1] + 1):
            conclusion['D'] += 1
        else:
            conclusion['I'] += 1
        curr_pointer = pointers[curr_pointer]
    if (curr_pointer[0] == -1) and (curr_pointer[1] != -1):
        conclusion['D'] += 1 * (curr_pointer[1] + 1)
    if (curr_pointer[0] > -1) and (curr_pointer[1] == -1):
        conclusion['I'] += 1 * (curr_pointer[0] + 1)
    conclusion['DIST'] = distances[-1]
    return conclusion, s1_match_indices
def bitwise_majority_string(string_array):
    '''
    returns the majority string corresponding to an array of strings of the same length
    '''
    return ''.join(np.array(
        np.array([np.mean(x) for x in np.array([list(x) for x in string_array]).transpose().astype(int)]) > 0.5).astype(
        int).astype(str))
def stringify(array):
    '''
    turns a binary numpy vector into a string of 0/1
    '''
    return ''.join(array.astype(str))
def intify(bin_string):
    '''
    turns a string of 0/1 into a binary numpy vector
    '''
    return np.array(list(bin_string))
def init_key(n, rand_seed=-1):
    '''
    returns a random key of n bits
    '''
    print 'initiating key...'
    if rand_seed > 0:
        np.random.seed(rand_seed)
    print 'DONE!'
    return ''.join((np.random.rand(n) > 0.5).astype(int).astype(str))
def build_samples(key, num_samples, sample_len, window_size, flip_probability, delete_probability, insert_probability,n):
    '''
    build snippets dataset, where each sample is noisified, and then sliced using a sliding window into snippets
    '''
    print 'building samples...'
    result_dict = {}
    for sample_idx in xrange(num_samples):
        if sample_idx % 1000 == 0:
            print sample_idx
        sample_start = np.random.randint(n - sample_len + 1)
        sample = np.array(list(key[sample_start:sample_start + sample_len])).astype(int)
        # flip random bits
        rand_flip = (np.random.rand(len(sample)) < flip_probability).astype(int)
        sample[np.where(rand_flip > 0)] = 1 - sample[np.where(rand_flip > 0)]
        # delete random bits
        rand_delete = (np.random.rand(len(sample)) < delete_probability).astype(int)
        sample = sample[np.where(rand_delete == 0)]
        # insert random bits
        rand_insert = (np.random.rand(len(sample) + 1) < insert_probability).astype(int)
        rand_bits_to_insert = (np.random.rand(sum(rand_insert)) > 0.5).astype(int)
        sample = np.insert(sample, np.where(rand_insert == 1)[0], rand_bits_to_insert)
        # scan windows of sample
        for window_start in xrange(len(sample) - window_size + 1):
            window = sample[window_start:window_start + window_size]
            window_key = ''.join(window.astype(str))
            if window_key not in result_dict:
                result_dict[window_key] = {'sample': window_key,
                                           'count': 1,
                                           'weight': sum(window),
                                           'similar_count': 0,
                                           'sample_start': [sample_start + window_start],
                                           'similar_samples': [],
                                           'closest_majority_sample': ''}
            else:
                result_dict[window_key]['count'] += 1
                if sample_start + window_start not in result_dict[window_key]['similar_samples']:
                    result_dict[window_key]['similar_samples'] = result_dict[window_key]['similar_samples'] + [
                        sample_start + window_start]
    result_df = pd.DataFrame.from_dict(result_dict, orient='index').sort_values(by='weight')
    print 'DONE!'
    return result_df
def build_samples_from_file(p_list,window_size,sample_start, sample_end, result_dict):
    count_lines=-1
    stop=False
    print("build samples from file...")
    for p in p_list:
        if stop: break
        with open(p) as f:
            for line in f:
                count_lines += 1
                if count_lines>=sample_end:
                    stop=True
                    break
                if count_lines<sample_start: continue
                if count_lines%10000==0: print count_lines
                sample =  s=np.array(" ".join(line).split(" ")[:-1]).astype(int)
                for window_start in range(len(sample) - window_size + 1):
                    window = sample[window_start:window_start + window_size]
                    window_key = ''.join(window.astype(str))
                    if window_key not in result_dict: # change to sub-string
                        result_dict[window_key] = {'sample': window_key,
                                                    'count': 1,
                                                    'weight': sum(window),
                                                    'similar_count': 0,
                                                    #'sample_start': [sample_start + window_start],
                                                    #'similar_samples': [],
                                                    'closest_majority_sample': ''}
                    else:
                        result_dict[window_key]['count'] += 1
                        #if sample_start + window_start not in result_dict[window_key]['similar_samples']:
                        #    result_dict[window_key]['similar_samples'] = result_dict[window_key]['similar_samples'] + [
                        #        sample_start + window_start]
    result_df = pd.DataFrame.from_dict(result_dict, orient='index').sort_values(by='weight')
    print 'DONE!'
    return result_df, result_dict
def prune_samples(result_df, min_count=-1, quantile=0.5):
    '''
    returns a subset of the snippets dataset which consists only of snippets that show high statistical significance
    '''
    print 'prunning samples...'
    if min_count < 0:
        min_count = result_df['count'].quantile(quantile)
    common_samples_df = result_df[result_df['count'] > min_count]
    #    noisy_samples_df = result_df[result_df['count'] < 3].sort_values(by='weight')
    #    for idx, common_sample in enumerate(common_samples_df.index):
    #        print idx, common_sample
    #        candidate_noisy_samples_above_weight_df = noisy_samples_df[noisy_samples_df['weight'] > common_samples_df.loc[common_sample]['weight'] -2]
    #        candidate_noisy_samples_below_weight_df = candidate_noisy_samples_above_weight_df [candidate_noisy_samples_above_weight_df['weight'] < common_samples_df.loc[common_sample]['weight'] +2]
    #        candidate_noisy_samples_df = candidate_noisy_samples_below_weight_df[candidate_noisy_samples_below_weight_df['weight'] != common_samples_df.loc[common_sample]['weight']]
    #        for noisy_sample in candidate_noisy_samples_df.index:
    #            if hamming_dist(common_sample,noisy_sample) < 2:
    #                common_samples_df.set_value(common_sample, 'similar_count', common_samples_df.loc[common_sample]['similar_count'] + 1)
    print 'DONE!'
    return common_samples_df.sort_values(by='count', ascending=False)  # more reliable samples first
def prune_samples_extended(result_df, min_count=-1, quantile=0.5, ignore_similar=True, min_count_radius=1, levenshtein_radius=2):
    '''
    Consider common_samples_df: contain samples that are common, but not very common (have count > min_count).
    Consider noisy_samples_df: contain samples that are even more rare, but not complete outliers (have count > min_count - min_count_radius).
    For each common_sample, look for noisy samples that can be near this common_sample. Such samples must have weight close to that of common_sample.
    Add the noisy samples that are close to common_sample to the similar_count of common_sample.

    returns a subset of the snippets dataset which consists only of snippets that show high statistical significance,
    when considering their similar_count, i.e., their actual count as well as their near noisy samples
    '''

    #    min_count=16
    #    ignore_similar=False
    #    min_count_radius=2
    #    levenshtein_radius=2

    print 'prunning samples...'
    if min_count < 0:
        min_count = result_df['count'].quantile(quantile)
    if ignore_similar:
        common_samples_df = result_df[result_df['count'] > min_count]
        print 'DONE!'
        return common_samples_df.sort_values(by='count', ascending=False)  # more reliable samples first
    else:
        weight_radius = levenshtein_radius  # *2 # for slicing potential close samples
        common_samples_df = result_df[result_df['count'] > min_count].sort_values(by='count', ascending=False)
        noisy_samples_df = result_df[result_df['count'] > min_count - min_count_radius].sort_values(by='weight')
        for idx, common_sample in enumerate(common_samples_df.index):
            if idx % 10 == 0:
                print idx
            near_weight_sample_df = noisy_samples_df[noisy_samples_df['weight'].isin(
                np.arange(common_samples_df.iloc[idx]['weight'] - weight_radius,
                          common_samples_df.iloc[idx]['weight'] + weight_radius))]
            #    common_samples_df['similar_count'] = common_samples_df.apply(lambda row: validate_sample(row, near_weight_sample, levenshtein_radius))
            #    print idx, common_sample
            #    common_sample = common_samples_df.head(2).tail(1)
            #    candidate_noisy_samples_in_radius_df = noisy_samples_df[noisy_samples_df['weight'].isin(
            #                    np.arange(common_sample['weight'] - weight_radius , common_sample['weight'] + weight_radius)) ]
            similar_count = validate_sample(common_samples_df.iloc[idx], near_weight_sample_df, levenshtein_radius)
            common_samples_df.at[common_sample, 'similar_count'] = similar_count
        print 'DONE!'
        common_samples_df.sort_values(by='similar_count', ascending=False)['count'].hist(bins=100)
        return common_samples_df.sort_values(by='similar_count', ascending=False)  # more reliable samples first
def build_shift_pointers_gabi_pure(common_samples_df, stitch_shift_size):
    '''
    build DAG where snippets are connected if they can be stitched by a small shift
    only the highest-ranking snippet that can be stitched is used, where the snippets array is assumed to be sorted by popularity
    '''
    common_samples_array = np.array(common_samples_df['sample'])
    common_count_array = np.array(common_samples_df['count'])

    print 'building DAG...'
    shift_pointers2 = {'right_index': {}, 'left_index': {}}
    right_index = []
    '''this part is to test if gabi and my optimization give the same reasults'''
    for idx1, left_sample in enumerate(common_samples_array):
        if idx1 % 100 == 0:
            print idx1

        for stitch_shift in range(1, stitch_shift_size + 1):
            #            print 'stitch_shift %d' % stitch_shift
            for idx2, right_sample in enumerate(common_samples_array):
                #                print idx2, sample2

                if hamming_dist(left_sample[stitch_shift:], right_sample[:-stitch_shift]) == 0:
                    if right_sample not in shift_pointers2['right_index']:
                        shift_pointers2['right_index'][right_sample] = {'right_sample': right_sample,
                                                                        'left_sample': left_sample,
                                                                        'shift': stitch_shift}
                    if left_sample not in shift_pointers2['left_index']:
                        shift_pointers2['left_index'][left_sample] = {'right_sample': right_sample,
                                                                      'left_sample': left_sample, 'shift': stitch_shift}
                    break_stitch_shift_loop = True
                    break
            if break_stitch_shift_loop:
                break
    print 'DONE!'

    return shift_pointers2
def validate_sample(sample, near_sample_df, radius):
    '''
    sample is a Series representing a single sample in the original dataframe
    near_sample_df is a dataframe of samples that have a weight similar to that of sample
    radius is the threshold criteria for considering a near_sample as a noisy version of sample

    returns the number of near samples that satisfy the threshold for sufficiently many bits of sample
    '''
    sample_count = np.ones(len(sample['sample'])) * sample['count']
    for near_sample in near_sample_df.index:
        (dist_arr, match_array) = levenshtein_edit_dist(sample['sample'], near_sample)
        dist = dist_arr['DIST']
        if len(match_array) >= len(sample['sample']) - radius:
            sample_count[match_array] += 1
    #            print sample['sample']
    #            print near_sample, len(match_array), '\n'
    return min(sample_count)
def stitch(common_samples_df, shift_pointers):
    '''
    traverse the DAG, starting from the sinks, and generate as long sequences as possible
    the algorithm assumes each snippet (node) has at most one incoming link
    if it should support multiple incoming links, then the function should be adjusted
    '''

    common_samples_array = np.array(common_samples_df['sample'])

    start_samples = []
    for sample in common_samples_array:
        if sample not in shift_pointers['right_index']:
            start_samples += [sample]
    retrieved_key = []
    for start_sample in start_samples:
        print 'START SAMPLE: ' + start_sample
        curr_sample = start_sample
        curr_key = curr_sample
        total_shift = 0
        while curr_sample in shift_pointers['left_index']:
            curr_key += shift_pointers['left_index'][curr_sample]['right_sample'][
                        -shift_pointers['left_index'][curr_sample]['shift']:]
            total_shift += shift_pointers['left_index'][curr_sample]['shift']
            curr_sample = shift_pointers['left_index'][curr_sample]['right_sample']
        print curr_key
        retrieved_key += [curr_key]
    return retrieved_key


'''BORIS'''
def build_samples_continues(key, sample_begin, sample_end, sample_len, window_size, flip_probability, delete_probability, insert_probability, result_dict):
    '''
    build snippets dataset, where each sample is noisified, and then sliced using a sliding window into snippets
    '''
    print 'building samples...'
    n = len(key)
    for sample_idx in xrange(sample_begin, sample_end):
        if sample_idx % 1000 == 0:
            print sample_idx
        sample_start = np.random.randint(n - sample_len + 1)
        sample = np.array(list(key[sample_start:sample_start + sample_len])).astype(int)
        # flip random bits
        rand_flip = (np.random.rand(len(sample)) < flip_probability).astype(int)
        sample[np.where(rand_flip > 0)] = 1 - sample[np.where(rand_flip > 0)]
        # delete random bits
        rand_delete = (np.random.rand(len(sample)) < delete_probability).astype(int)
        sample = sample[np.where(rand_delete == 0)]
        # insert random bits
        rand_insert = (np.random.rand(len(sample) + 1) < insert_probability).astype(int)
        rand_bits_to_insert = (np.random.rand(sum(rand_insert)) > 0.5).astype(int)
        sample = np.insert(sample, np.where(rand_insert == 1)[0], rand_bits_to_insert)
        # scan windows of sample
        for window_start in xrange(len(sample) - window_size + 1):
            window = sample[window_start:window_start + window_size]
            window_key = ''.join(window.astype(str))
            if window_key not in result_dict:
                result_dict[window_key] = {'sample': window_key,
                                           'count': 1,
                                           'weight': sum(window),
                                           'similar_count': 0,
                                           'sample_start': [sample_start + window_start],
                                           'similar_samples': [],
                                           'closest_majority_sample': ''}
            else:
                result_dict[window_key]['count'] += 1
                if sample_start + window_start not in result_dict[window_key]['similar_samples']:
                    result_dict[window_key]['similar_samples'] = result_dict[window_key]['similar_samples'] + [
                        sample_start + window_start]
    result_df = pd.DataFrame.from_dict(result_dict, orient='index').sort_values(by='weight')
    print 'DONE!'
    return result_df, result_dict
def build_samples_continues_threads(key, sample_begin, sample_end, sample_len, window_size, flip_probability, delete_probability, insert_probability, result_dict, MAX_THREADS=100):
    '''
    build snippets dataset, where each sample is noisified, and then sliced using a sliding window into snippets
    '''
    print 'building samples...'
    n = len(key)
    mutex_result_dict = threading.Lock()
    threads = []
    for sample_idx in xrange(sample_begin, sample_end):
        threads.append(threading.Thread(target=build_samples_better_thread, args=(key, n, sample_idx, sample_len, window_size, flip_probability, delete_probability, insert_probability, result_dict, mutex_result_dict)))
    startThreads = threading.active_count()
    for t in threads:
        t.start()
        if threading.active_count() == MAX_THREADS + startThreads:
            # print "MAX Threads reached wait for finish"
            t.join()
    [t.join() for t in threads if t.isAlive()]
    result_df = pd.DataFrame.from_dict(result_dict, orient='index').sort_values(by='weight')
    print 'DONE!'
    return result_df, result_dict
def build_samples_better_thread(key, n, sample_idx, sample_len, window_size, flip_probability, delete_probability, insert_probability, result_dict, mutex_result_dict):
    if sample_idx % 1000 == 0:
        print sample_idx
    sample_start = np.random.randint(n - sample_len + 1)
    sample = np.array(list(key[sample_start:sample_start + sample_len])).astype(int)
    # flip random bits
    rand_flip = (np.random.rand(len(sample)) < flip_probability).astype(int)
    sample[np.where(rand_flip > 0)] = 1 - sample[np.where(rand_flip > 0)]
    # delete random bits
    rand_delete = (np.random.rand(len(sample)) < delete_probability).astype(int)
    sample = sample[np.where(rand_delete == 0)]
    # insert random bits
    rand_insert = (np.random.rand(len(sample) + 1) < insert_probability).astype(int)
    rand_bits_to_insert = (np.random.rand(sum(rand_insert)) > 0.5).astype(int)
    sample = np.insert(sample, np.where(rand_insert == 1)[0], rand_bits_to_insert)
    # scan windows of sample
    for window_start in xrange(len(sample) - window_size + 1):
        window = sample[window_start:window_start + window_size]
        window_key = ''.join(window.astype(str))
        mutex_result_dict.acquire()
        if window_key not in result_dict:
            result_dict[window_key] = {'sample': window_key,
                                       'count': 1,
                                       'weight': sum(window),
                                       'similar_count': 0,
                                       'sample_start': [sample_start + window_start],
                                       'similar_samples': [],
                                       'closest_majority_sample': ''}
        else:
            result_dict[window_key]['count'] += 1
            if sample_start + window_start not in result_dict[window_key]['similar_samples']:
                result_dict[window_key]['similar_samples'] = result_dict[window_key]['similar_samples'] + [
                    sample_start + window_start]
        mutex_result_dict.release()

def build_shift_pointers_position_better(common_samples_df, stitch_shift_size, window_size, allowCycle=False):
    '''
    build DAG where snippets are connected if they can be stitched by a small shift
    only the highest-ranking snippet that can be stitched is used, where the snippets array is assumed to be sorted by popularity
    '''
    common_samples_array = np.array(common_samples_df['sample'])
    common_count_array = np.array(common_samples_df['count'])

    print 'building DAG...'
    shift_pointers = {'right_index': {}, 'left_index': {}}

    '''************************************************************************************'''
    # build array 2^window, and put counted value in each index correspend for the samples
    # for example if sample = 00000000000000000001  in all2PowerWindowArray[1]=X where X is number times this sample was appeard
    all2PowerWindowArray = np.zeros(2 ** window_size, dtype=np.uint32)
    orderArrayMaxToMin = np.zeros(len(common_samples_array), dtype=np.uint32)
    all2PowerWindowArray_idx = np.zeros(2 ** window_size, dtype=np.uint32)

    for idx, sample in enumerate(common_samples_array):
        b = BitArray(bin=sample)
        all2PowerWindowArray[b.uint] = common_count_array[idx]
        all2PowerWindowArray_idx[b.uint] = idx
        orderArrayMaxToMin[idx] = b.uint

    idxMax = len(common_samples_array) + 1
    '''************************************************************************************'''

    for i in xrange(len(common_samples_array)):  # run over all the order of the samples
        left_sample_index = orderArrayMaxToMin[i]
        if i % 500 == 0:
            print "i = {0}".format(i)

        if (all2PowerWindowArray[left_sample_index] > 0):
            left_sample = common_samples_array[all2PowerWindowArray_idx[left_sample_index]]
            mask = 1
            for stitch_shift in range(1, stitch_shift_size + 1):
                temp = left_sample_index << stitch_shift  # shift the bit
                temp &= ~(mask << window_size)
                mask = (mask << 1) + 1

                right_sample_idx = idxMax
                for j in xrange(2 ** stitch_shift):
                    if (all2PowerWindowArray[temp + j] > 0):
                        if (all2PowerWindowArray_idx[temp + j] < right_sample_idx):
                            right_sample_idx = all2PowerWindowArray_idx[temp + j]
                            right_sample_index = temp + j

                if right_sample_idx != idxMax:
                    right_sample = common_samples_array[all2PowerWindowArray_idx[right_sample_index]]
                    if right_sample not in shift_pointers['right_index']:
                        shift_pointers['right_index'][right_sample] = {'right_sample': right_sample,
                                                                       'left_sample': left_sample,
                                                                       'shift': stitch_shift}

                    if left_sample not in shift_pointers['left_index']:
                        shift_pointers['left_index'][left_sample] = {'right_sample': right_sample,
                                                                     'left_sample': left_sample, 'shift': stitch_shift}
                    break

    print 'DONE!'
    return shift_pointers, all2PowerWindowArray, all2PowerWindowArray_idx, orderArrayMaxToMin

def stitch_boris(common_samples_df, shift_pointers, all2PowerWindowArray_idx, allowCycle=True, key_length=2048 ):
    '''
    traverse the DAG, starting from the sinks, and generate as long sequences as possible
    the algorithm assumes each snippet (node) has at most one incoming link
    if it should support multiple incoming links, then the function should be adjusted
    '''
    #    shift_pointers_right_index_df = pd.DataFrame(shift_pointers['right_index']).transpose()
    #    shift_pointers_left_index_df = pd.DataFrame(shift_pointers['left_index']).transpose()

    common_samples_array = np.array(common_samples_df['sample'])



    start_samples = []
    for sample in common_samples_array:
        if sample not in shift_pointers['right_index']:
            start_samples += [sample]
    retrieved_key = []

    for start_sample in start_samples:
        print 'START SAMPLE: ' + start_sample
        curr_sample = start_sample
        cycle_break = not allowCycle

        b = BitArray(bin=start_sample)
        path=[all2PowerWindowArray_idx[b.uint]]


        curr_key = curr_sample
        total_shift = 0
        curr_key_list = np.array([start_sample])

        while curr_sample in shift_pointers['left_index']:
            cycle_break = False
            curr_sample_right_neighbor_dict = shift_pointers['left_index'][curr_sample]
            curr_sample_right_neighbor = curr_sample_right_neighbor_dict['right_sample']
            curr_sample_right_neighbor_to_add = curr_sample_right_neighbor[-shift_pointers['left_index'][curr_sample]['shift']:]
            curr_key += curr_sample_right_neighbor_to_add
            total_shift += shift_pointers['left_index'][curr_sample]['shift']
            curr_sample = curr_sample_right_neighbor
            b = BitArray(bin=curr_sample)
            if all2PowerWindowArray_idx[b.uint] in path:
                break
            else:
                path.append(all2PowerWindowArray_idx[b.uint])


            # if len(curr_key) >= 3 * key_length:
            #     print "[Worning]: probably cycle!!"
            #     if not allowCycle:
            #         cycle_break = True
            #         break
        if not cycle_break:
            retrieved_key += [curr_key]
    return retrieved_key
def stitch_boris_threads(common_samples_df, shift_pointers, all2PowerWindowArray_idx, allowCycle=True, key_length=2048 , MAX_THREADS=100):
    '''
    traverse the DAG, starting from the sinks, and generate as long sequences as possible
    the algorithm assumes each snippet (node) has at most one incoming link
    if it should support multiple incoming links, then the function should be adjusted
    '''
    #    shift_pointers_right_index_df = pd.DataFrame(shift_pointers['right_index']).transpose()
    #    shift_pointers_left_index_df = pd.DataFrame(shift_pointers['left_index']).transpose()
    common_samples_array = np.array(common_samples_df['sample'])
    start_samples = []
    for sample in common_samples_array:
        if sample not in shift_pointers['right_index']:
            start_samples += [sample]
    retrieved_key = []

    mutex_retrieved_key = threading.Lock()
    threads = []
    for start_sample in start_samples:
        threads.append(threading.Thread(target=stitch_boris_thread, args=(start_sample, shift_pointers, all2PowerWindowArray_idx, allowCycle, retrieved_key, mutex_retrieved_key)))

    startThreads = threading.active_count()
    for t in threads:
        t.start()
        if threading.active_count() == MAX_THREADS + startThreads:
            # print "MAX Threads reached wait for finish"
            t.join()

    [t.join() for t in threads if t.isAlive()]
    return retrieved_key
def stitch_boris_thread(start_sample, shift_pointers, all2PowerWindowArray_idx, allowCycle, retrieved_key, mutex_retrieved_key):
    print '\nSTART SAMPLE: ' + start_sample
    curr_sample = start_sample
    cycle_break = not allowCycle
    b = BitArray(bin=start_sample)

    path = [all2PowerWindowArray_idx[b.uint]]

    curr_key = curr_sample
    while curr_sample in shift_pointers['left_index']:
        cycle_break = False
        curr_sample_right_neighbor_dict = shift_pointers['left_index'][curr_sample]
        curr_sample_right_neighbor = curr_sample_right_neighbor_dict['right_sample']
        curr_sample_right_neighbor_to_add = curr_sample_right_neighbor[
                                            -shift_pointers['left_index'][curr_sample]['shift']:]
        curr_key += curr_sample_right_neighbor_to_add
        curr_sample = curr_sample_right_neighbor
        b = BitArray(bin=curr_sample)
        if all2PowerWindowArray_idx[b.uint] in path:
            break
        else:
            path.append(all2PowerWindowArray_idx[b.uint])

    if not cycle_break:
        mutex_retrieved_key.acquire()
        retrieved_key += [curr_key]
        mutex_retrieved_key.release()


# debug
resultCompareGabiAndMe = True
def compareGabiAndMe(shift_pointers_Boris, shift_pointers_Gabi):
    '''this part is to test if gabi and my optimization give the same reasults'''
    # test this:
    print "[INFO][compareGabiAndMe]: START COMPRAED BORIS AND GABI! "
    if len(np.array(shift_pointers_Gabi['left_index'].keys())) != len(
            np.array(shift_pointers_Boris['left_index'].keys())):
        print "[ERROR][compareGabiAndMe][left_index]: len boris different len gabi"
        sys.exit(1)
        # resultCompareGabiAndMe = False
        # return resultCompareGabiAndMe

    if len(np.array(shift_pointers_Gabi['right_index'].keys())) != len(np.array(shift_pointers_Boris['right_index'].keys())):
        print "[ERROR][compareGabiAndMe][right_index]: len boris different len gabi"
        sys.exit(1)
        # resultCompareGabiAndMe = False
        # return resultCompareGabiAndMe

    threads = []
    for threadNum in xrange(4):
        t = threading.Thread(target=compareGabiAndMeThreads, args=(shift_pointers_Boris, shift_pointers_Gabi, threadNum))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    print "[INFO][compareGabiAndMe][RESULT={0}]: DONE! ".format(resultCompareGabiAndMe)
    return True
def compareGabiAndMeThreads(shift_pointers_Boris, shift_pointers_Gabi, case):
    '''this part is to test if gabi and my optimization give the same reasults'''
    # test this:
    if len(np.array(shift_pointers_Gabi['left_index'].keys())) != len(
            np.array(shift_pointers_Boris['left_index'].keys())):
        print "[ERROR][compareGabiAndMe][left_index]: len boris different len gabi"
        sys.exit(1)
        # resultCompareGabiAndMe = False
        # return resultCompareGabiAndMe


    if len(np.array(shift_pointers_Gabi['right_index'].keys())) != len(
            np.array(shift_pointers_Boris['right_index'].keys())):
        print "[ERROR][compareGabiAndMe][right_index]: len boris different len gabi"
        sys.exit(1)
        # resultCompareGabiAndMe = False
        # return resultCompareGabiAndMe

    if case == 1:
        # debug part to test if gabi dict are as my after optiomizations:
        for sample in shift_pointers_Boris['left_index'].keys():
            if sample not in shift_pointers_Gabi['left_index']:
                print "[ERROR][compareGabiAndMe][left_index]: boris have sample which gabi doesnt"
                sys.exit(1)
                # resultCompareGabiAndMe = False
                # return resultCompareGabiAndMe
            else:
                if shift_pointers_Boris['left_index'][sample]['right_sample'] != \
                        shift_pointers_Gabi['left_index'][sample]['right_sample']:
                    print "[ERROR][compareGabiAndMe][left_index]: boris peers and gabi are different"
                    sys.exit(1)
                    # resultCompareGabiAndMe = False
                    # return resultCompareGabiAndMe
    if case == 2:
        for sample in shift_pointers_Boris['right_index'].keys():
            if sample not in shift_pointers_Gabi['right_index']:
                print "[ERROR][compareGabiAndMe][right_index]: boris have sample which gabi doesnt"
                sys.exit(1)
                # resultCompareGabiAndMe = False
                # return resultCompareGabiAndMe
            else:
                if shift_pointers_Boris['right_index'][sample]['left_sample'] != \
                        shift_pointers_Gabi['right_index'][sample]['left_sample']:
                    print "[ERROR][compareGabiAndMe][right_index]: boris peers and gabi are different"
                    sys.exit(1)
                    # resultCompareGabiAndMe = False
                    # return resultCompareGabiAndMe

    if case == 3:
        # debug part to test if my dicts after optiomizations are as gabi dict :
        for sample in shift_pointers_Gabi['left_index'].keys():
            if sample not in shift_pointers_Boris['left_index']:
                print "[ERROR][compareGabiAndMe][left_index]: gabi have sample which boris doesnt"
                # sys.exit(1)
                resultCompareGabiAndMe = False
                return resultCompareGabiAndMe
            else:
                if shift_pointers_Gabi['left_index'][sample]['right_sample'] != \
                        shift_pointers_Boris['left_index'][sample]['right_sample']:
                    print "[ERROR][compareGabiAndMe][left_index]: boris peers and gabi are different"
                    # sys.exit(1)
                    resultCompareGabiAndMe = False
                    return resultCompareGabiAndMe

    if case == 4:
        for sample in shift_pointers_Gabi['right_index'].keys():
            if sample not in shift_pointers_Boris['right_index']:
                print "[ERROR][compareGabiAndMe][right_index]: gabi have sample which boris doesnt"
                sys.exit(1)
                # resultCompareGabiAndMe = False
                # return resultCompareGabiAndMe
            else:
                if shift_pointers_Boris['right_index'][sample]['left_sample'] != \
                        shift_pointers_Gabi['right_index'][sample]['left_sample']:
                    print "[ERROR][compareGabiAndMe][right_index]: gabi peers and boris are different"
                    sys.exit(1)
                    # resultCompareGabiAndMe = False
                    # return resultCompareGabiAndMe
def build_shift_pointers_position_better_more(common_samples_df, stitch_shift_size, window_size, allowCycle=False):
    '''
    build DAG where snippets are connected if they can be stitched by a small shift
    only the highest-ranking snippet that can be stitched is used, where the snippets array is assumed to be sorted by popularity
    '''
    common_samples_array = np.array(common_samples_df['sample'])
    common_count_array = np.array(common_samples_df['count'])

    print 'building DAG...'
    shift_pointers = {'right_index': {}, 'left_index': {}}

    '''************************************************************************************'''
    # build array 2^window, and put counted value in each index correspend for the samples
    # for example if sample = 00000000000000000001  in all2PowerWindowArray[1]=X where X is number times this sample was appeard
    all2PowerWindowArray = np.zeros(2 ** window_size, dtype=np.uint32)
    orderArrayMaxToMin = np.zeros(len(common_samples_array), dtype=np.uint32)
    all2PowerWindowArray_idx = np.zeros(2 ** window_size, dtype=np.uint32)

    for idx, sample in enumerate(common_samples_array):
        b = BitArray(bin=sample)
        all2PowerWindowArray[b.uint] = common_count_array[idx]
        all2PowerWindowArray_idx[b.uint] = idx
        orderArrayMaxToMin[idx] = b.uint

    idxMax = len(common_samples_array) + 1
    '''************************************************************************************'''

    for i in xrange(len(common_samples_array)):  # run over all the order of the samples
        left_sample_index = orderArrayMaxToMin[i]
        if i % 500 == 0:
            print "i = {0}".format(i)

        if (all2PowerWindowArray[left_sample_index] > 0):
            left_sample = common_samples_array[all2PowerWindowArray_idx[left_sample_index]]
            mask = 1
            for stitch_shift in range(1, stitch_shift_size + 1):
                temp = left_sample_index << stitch_shift  # shift the bit
                temp &= ~(mask << window_size)
                mask = (mask << 1) + 1

                right_sample_idx = idxMax
                jj=0
                for j in xrange(2 ** stitch_shift):
                    if (all2PowerWindowArray[temp + j] > 0):
                        if (all2PowerWindowArray_idx[temp + j] < right_sample_idx):
                            right_sample_idx = all2PowerWindowArray_idx[temp + j]
                            right_sample_index = temp + j
                            jj=j

                if right_sample_idx != idxMax:
                    right_sample = common_samples_array[all2PowerWindowArray_idx[right_sample_index]]
                    if right_sample not in shift_pointers['right_index']:
                        shift_pointers['right_index'][right_sample] = {'right_sample': right_sample,
                                                                       'my_sample_index': right_sample_index,
                                                                       'left_sample': left_sample,
                                                                       'left_sample_index': left_sample_index,
                                                                       'shift': stitch_shift,
                                                                       'bitsShift':right_sample[-stitch_shift:]
                                                                       }

                    if left_sample not in shift_pointers['left_index']:
                        shift_pointers['left_index'][left_sample] = {'right_sample': right_sample,
                                                                     'right_sample_index': right_sample_index,
                                                                     'left_sample': left_sample,
                                                                     'my_sample_index': left_sample_index,
                                                                     'shift': stitch_shift,
                                                                     'bitsShift':right_sample[-stitch_shift:]
                                                                     }
                    break

    print 'DONE!'
    return shift_pointers, all2PowerWindowArray, all2PowerWindowArray_idx, orderArrayMaxToMin


'''YAEL'''
def tow_dim_arr2file(pathes,f_path):
    for p in pathes:
        f_path.write(' '.join(map(str,p)))
        f_path.write("\n")

def build_shift_pointer_thread(all2PowerWindowArray,all2PowerWindowArray_idx,saveIndexArray,tree_pointers,stitch_shift_size,start_idx,end_idx,window_size,rm_right):

    for idx1 in xrange(start_idx,end_idx):
        left_sample_number = saveIndexArray[idx1]
        left_sample = np.binary_repr(num=left_sample_number, width=window_size)
        mask = 1
        for stitch_shift in range(1, stitch_shift_size + 1):
            temp = left_sample_number << stitch_shift  # shift the bit
            temp &= ~(mask << window_size)
            mask = (mask << 1) + 1

            for j in xrange(2 ** stitch_shift):
                if (all2PowerWindowArray[temp + j] > 0) and (left_sample_number != (temp + j)):
                    right_sample = np.binary_repr(num=temp + j, width=window_size)
                    idx2 = all2PowerWindowArray_idx[temp + j]
                    tree_pointers[idx1].append({'next': idx2,'shift': stitch_shift})
                    if idx2 not in rm_right: rm_right.append(idx2)
    print "done: "+str(start_idx)+"-"+str(end_idx)

def build_shift_pointers_tree(common_samples_df, stitch_shift_size, window_size):
    '''
    Build the tree pointers
    edge_left_pointers- the potential roots for a tree struct
    tree_pointers- array of the possible contionus options for each string

    build tree where snippets are connected if they can be stitched by a small shift
    !!! edge_left_pointers !!! is nnot necceraly fuul, cycles may be found
    '''
    common_samples_array = np.array(common_samples_df['sample'])
    common_count_array = np.array(common_samples_df['count'])
    remove = []
    tree_pointers = [[] for i in range(len(common_samples_array))]
    edge_left_pointers = range(len(common_samples_array))

    print 'building Tree no error fixing - Threading...'
    '''
     build array 2^window, and put counted value in each index correspend for the samples
     for example if sample = 00000000000000000001  in all2PowerWindowArray[1]=X where X is number times this sample was appeard 
    '''
    all2PowerWindowArray = np.zeros(2 ** window_size, dtype=np.uint32)
    all2PowerWindowArray_idx = np.zeros(2 ** window_size, dtype=np.uint32)
    saveIndexArray = np.zeros(len(common_samples_array),
                              dtype=np.uint32)  # this array in to save the order of the samples in common_samples_array

    for idx, sample in enumerate(common_samples_array):
        b = BitArray(bin=sample)
        all2PowerWindowArray[b.uint] = common_count_array[idx]
        all2PowerWindowArray_idx[b.uint] = idx
        saveIndexArray[idx] = b.uint

    rm_rights=[[]]*10
    threads = list()
    length_10=(len(saveIndexArray)/10)
    for thr in range(10): #creating threads
        if thr==9: end=len(saveIndexArray)-1
        else: end=(thr+1)*length_10
        t = threading.Thread(target=build_shift_pointer_thread, kwargs={'all2PowerWindowArray':all2PowerWindowArray,
                                                                'all2PowerWindowArray_idx':all2PowerWindowArray_idx,
                                                                'saveIndexArray':saveIndexArray,
                                                                'tree_pointers':tree_pointers,
                                                                'stitch_shift_size':stitch_shift_size,
                                                                'start_idx':thr*length_10,
                                                                'end_idx':end,
                                                                'window_size':window_size,
                                                                'rm_right':rm_rights[thr],})
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    for rm in rm_rights: remove = list(set(remove + rm))
    edge_left_pointers= list(set(edge_left_pointers) - set(remove))

    return tree_pointers, edge_left_pointers

def stitch_tree_iterative_no_thread(tree_pointers, edge_left_pointers,min_len_path=400): #at first, send the window_size as a shift
    '''
    stitch the tree itterativly (DFS)
    ---never run to the end, dont know if work ----

    notice: the min_len_path is compared to the path_len and not to the key_len
    '''
    pathes = []
    DFS_visit_arr=[False]*len(tree_pointers) # initiate DFS struct
    f_path=open("./key_candidates_pathes_iterative","w");
    for root in edge_left_pointers:
        stack, path = [root], []
        while stack:
            if len(pathes) > 10000:
                tow_dim_arr2file(pathes, f_path)
                pathes = []
            vertex = stack.pop()
            path.append(vertex)
            DFS_visit_arr[vertex] = True
            rm, booli = True, True

            if len(tree_pointers[vertex])==0: #end of path
                if len(path)>=min_len_path:
                    pathes.append(copy.deepcopy(path))
            else:
                for neighbor in tree_pointers[vertex]:
                    if DFS_visit_arr[neighbor["next"]]==True: #cycle
                        if len(path) >= min_len_path and booli:
                            pathes.append(copy.deepcopy(path))
                            booli=False
                    else:
                        rm = False
                        stack.append(neighbor["next"])

            while (rm): #back in the DFS
                popped_from_path = path.pop()
                # check if all the children were there the path should be continued
                if path:
                    for node in tree_pointers[path[-1]]:
                        if node["next"] in stack:
                            rm= False
                else: rm=False
                DFS_visit_arr[popped_from_path] = False

    tow_dim_arr2file(pathes, f_path)

#####works, but not very efficiencive#####
def build_shift_pointers_tree_noTreads(common_samples_df, stitch_shift_size,window_size):
    '''
    Build the tree pointers
    edge_left_pointers- the potential roots for a tree struct
    tree_pointers- array of the possible contionus options for each string

    build tree where snippets are connected if they can be stitched by a small shift
    !!! edge_left_pointers !!! is nnot necceraly fuul, cycles may be found
    '''
    common_samples_array = np.array(common_samples_df['sample'])
    common_count_array = np.array(common_samples_df['count'])

    tree_pointers = [[] for i in range(len(common_samples_array))]
    edge_left_pointers = range(len(common_samples_array))

    print 'building Tree no error fixing...'
    '''
     build array 2^window, and put counted value in each index correspend for the samples
     for example if sample = 00000000000000000001  in all2PowerWindowArray[1]=X where X is number times this sample was appeard 
    '''
    all2PowerWindowArray = np.zeros(2 ** window_size, dtype=np.uint32)
    all2PowerWindowArray_idx = np.zeros(2 ** window_size, dtype=np.uint32)
    saveIndexArray = np.zeros(len(common_samples_array),
                              dtype=np.uint32)  # this array in to save the order of the samples in common_samples_array

    for idx, sample in enumerate(common_samples_array):
        b = BitArray(bin=sample)
        all2PowerWindowArray[b.uint] = common_count_array[idx]
        all2PowerWindowArray_idx[b.uint] = idx
        saveIndexArray[idx] = b.uint

    ''' now is the tree'''
    for idx1 in xrange(len(saveIndexArray)):  # run over all the possible samples

        if idx1 % 10000 == 0: print idx1
        left_sample_number = saveIndexArray[idx1]
        #left_sample = np.binary_repr(num=left_sample_number, width=window_size)
        mask = 1
        for stitch_shift in range(1, stitch_shift_size + 1):
            temp = left_sample_number << stitch_shift  # shift the bit
            temp &= ~(mask << window_size)
            mask = (mask << 1) + 1

            for j in xrange(2 ** stitch_shift):
                if (all2PowerWindowArray[temp + j] > 0) and (left_sample_number != (temp + j)):
                    #right_sample = np.binary_repr(num=temp + j, width=window_size)
                    #idx2 = np.where(saveIndexArray == BitArray(bin=right_sample).uint)[0]
                    idx2 = all2PowerWindowArray_idx[temp + j]
                    tree_pointers[idx1].append({'next': idx2,
                                                'shift': stitch_shift})
                    if idx2 in edge_left_pointers:
                        edge_left_pointers.remove(idx2)
    print 'DONE!'
    return tree_pointers, edge_left_pointers

#--without files
def stitch_tree_recurcive(common_samples_df, tree_pointers, edge_left_pointers):
    '''
    call build_tree_path_recurcive function for each root
    Return all the possible keys. Technically, the pathes are unused, but may be easier to work with lately.
    ----Never run to the end because it is very long. the stack may be explode----
    '''
    print "building tree path + stich..."
    if len(edge_left_pointers) == 0:
        print 'no root'
        return [];
    pathes = []
    retrieved_key = []
    for root in edge_left_pointers:
        a=build_tree_path_recurcive([root], '', tree_pointers, common_samples_df['sample'], retrieved_key,30)#len(common_samples_df[root]['sample']) - 1)
        pathes.extend(a)
    return retrieved_key
def build_tree_path_recurcive(path, key, tree_pointers, common_samples_array, retrieved_key, shift):
    '''
    This function is called out of "stitch_tree_recurcive"
    Recurcive search of the tree
    Return an array of all the possible pathes in the tree (only the long enough)
    retrieved_key- includes the options for a key
    ----Never run to the end because it is very long. the stack may be explode----
    '''
    print path
    if len(tree_pointers[path[-1]]) == 0:  # there is an optional "next" node
        si = key[:-shift] + common_samples_array.iloc[path[-1]]#['sample']
        retrieved_key.append(si)
        return [path]
    else:
        a = []
        booli = True
        for node in tree_pointers[path[-1]]:
            if node['next'] not in path:
                si = key[:-node['shift']] + common_samples_array.iloc[path[-1]]#['sample']
                a.extend(
                    build_tree_path_recurcive(path + [node['next']], si, tree_pointers, common_samples_array, retrieved_key,
                                         node['shift']))
            elif booli:
                a.append(path)
                retrieved_key.append(key)
                booli = False
        return a
#--with files
def build_tree_path_recurcive_less_mem(path, key,common_samples_array,tree_pointers, shift,min_len_key,f_key,f_path): #at first, send the window_size as a shift
    '''
      This function is called out of "stitch_tree_recurcive_less_mem"
      Recurcive search of the tree
      Write to file all possible pathes and keys in the tree (only the long enough)
      ----Never run to the end because it is very long. the stack may be explode----
      '''
    # write to filepossible pathes
    if len(tree_pointers[path[-1]]) == 0:  # there is an optional "next" node
        si = key + common_samples_array.iloc[path[-1]][-shift:]
        if len(si) >= min_len_key:
            f_key.write(si+"\n")
            f_path.write(' '.join(map(str,path))); f_path.write("\n")
        return
    else:
        booli = True
        for node in tree_pointers[path[-1]]:
            if node['next'] not in path:
                si = key + common_samples_array.iloc[path[-1]][-node['shift']:]
                build_tree_path_recurcive_less_mem(path + [node['next']],si,common_samples_array,tree_pointers, node['shift'],min_len_key,f_key,f_path)
            elif booli and len(key) >= min_len_key:
                f_key.write(key + "\n")
                f_path.write(' '.join(map(str,path))); f_path.write("\n")
        return
def stitch_tree_recurcive_less_mem(common_samples_df, tree_pointers, edge_left_pointers,window_size,min_len_key):
    '''
    Recurcive stitch - with files - no threads.
    The stack would not explode because the pathes are written to file
    It works - but takes a lot of time
    traverse the tree pathes, starting from the root, and generate as long sequences as possible
    the algorithm assumes each snippet (node) has at most one incoming link
    if there is no root, the largest cycle will be found
    ----Never run to the end because it is very long. the stack may be explode----
    '''

    print "building tree path + stich..."
    f_key=open("./key_candidates.txt","w")
    f_path=open("./key_candidates_pathes.txt","w")

    if len(edge_left_pointers) == 0:
        print 'no root'
        return

    print len(edge_left_pointers)
    for idx, root in enumerate(edge_left_pointers):
        print idx
        #if idx==1: break;
        build_tree_path_recurcive_less_mem([root],'',common_samples_df['sample'],tree_pointers, window_size,min_len_key, f_key, f_path) #key=''
    f_key.close()
    f_path.close()

def stitch_tree__recurcive_less_mem_thread(common_samples_df, tree_pointers, edge_left_pointers,window_size,min_len_key,f_key,f_path):
    '''
    Called from stitch_tree_recurcive_less_mem_with_thread
    -----never run-----
    '''

    for idx, root in enumerate(edge_left_pointers):
        if idx % 100 == 0: print idx
        build_tree_path_recurcive_less_mem([root], '', common_samples_df['sample'],tree_pointers, window_size,
                                     min_len_key,f_key,f_path)
def stitch_tree_recurcive_less_mem_with_thread(common_samples_df, tree_pointers, edge_left_pointers,window_size,min_len_key):
    '''
    with files + threads
    traverse the tree pathes, starting from the root, and generate as long sequences as possible
    the algorithm assumes each snippet (node) has at most one incoming link
    if there is no root, the largest cycle will be found

    -----never run-----
    '''

    print "building tree path + stich using threads + using files..."

    if len(edge_left_pointers) == 0:
        print 'no root'
        return

    len_10= len(edge_left_pointers)/10
    threads=list()
    f_key_list=list()
    f_path_list=list()
    for i in range(10):
        if i == 9:   end = len(edge_left_pointers) - 1
        else: end = (i + 1) * len_10
        f_key=open("./key_candidates_"+str(i)+".txt","w")
        f_path=open("./key_pathes_"+str(i)+".txt","w")
        f_key_list.append(f_key)
        f_path_list.append(f_path)
        t = threading.Thread(target=stitch_tree__recurcive_less_mem_thread, kwargs={'common_samples_df': common_samples_df,
                                                                        'tree_pointers': tree_pointers,
                                                                        'edge_left_pointers': edge_left_pointers[i*len_10:end],
                                                                        'window_size': window_size,
                                                                        'min_len_key': min_len_key,
                                                                         'f_key': f_key_list[-1],
                                                                         'f_path':f_path_list[-1], })
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    for f1,f2 in zip(f_key_list,f_path_list):
        f1.close()
        f2.close()

#dont know if work

def stitch_tree_iterative_thread(tree_pointers, edge_left_pointers,min_len_path,f_path,window_size): #at first, send the window_size as a shift
    '''
    stitch the tree itterativly (DFS)
    ---never run to the end, dont know if work ----

    notice: the min_len_path is compared to the path_len and not to the key_len
    '''
    pathes = []
    DFS_visit_arr=[False]*len(tree_pointers) # initiate DFS struct
    for root in edge_left_pointers:
        stack, path = [root], []
        while stack:
            if len(pathes) > 100:
                tow_dim_arr2file(pathes, f_path)
                pathes = []
            vertex = stack.pop()
            path.append(vertex)
            DFS_visit_arr[vertex] = True
            rm, booli = True, True

            if len(tree_pointers[vertex])==0: #end of path
                if len(path)>=min_len_path:
                    pathes.append(copy.deepcopy(path))
            else:
                for neighbor in tree_pointers[vertex]:
                    if DFS_visit_arr[neighbor["next"]]==True: #cycle
                        if len(path) >= min_len_path and booli:
                            pathes.append(copy.deepcopy(path))
                            booli=False
                    else:
                        rm = False
                        stack.append(neighbor["next"])

            while (rm): #back in the DFS
                popped_from_path = path.pop()
                # check if all the children were there the path should be continued
                if path:
                    for node in tree_pointers[path[-1]]:
                        if node["next"] in stack:
                            rm= False
                else: rm=False
                DFS_visit_arr[popped_from_path] = False

    tow_dim_arr2file(pathes, f_path)

def stitch_tree_with_threads_iterative(tree_pointers, edge_left_pointers,window_size,min_len_path):
    '''
    stitch the tree itterativly (DFS) - with treads
    ---never run to the end, dont know if work ----

    notice: the min_len_path is compared to the path_len and not to the key_len
    '''
    print "building tree path + stich..."
    len_10=len(edge_left_pointers)/10
    threads = list()
    files=list()
    for i in range(10):
        s=i*len_10
        e=(i+1)*len_10
        f=open("./itertative_pathes_"+str(i)+".txt","w")
        files.append(f)
        if i==19:
            e= len_10-1
        t = threading.Thread(target=stitch_tree_iterative_thread, kwargs={'tree_pointers': tree_pointers,
                                                                  'edge_left_pointers': edge_left_pointers[s:e],
                                                                  'min_len_path': min_len_path,
                                                                  'f_path': f,
                                                                   'window_size':window_size, })
        threads.append(t)
        t.start()

    for idx,t in enumerate(threads):
        t.join()
        print "done: "+str(idx)
        files[idx].close()


#irrelavant'''
def prune_samples_yael_extended(result_df, min_count=-1, extended=True, max_dist=3):
	'''
	returns a subset of the snippets dataset which consists only of snippets that show high statistical significance
	'''
	print 'prunning samples...'
	if min_count < 0:
		min_count = result_df['count'].quantile(.5)  # the midian

	if not extended:
		common_samples_df = result_df[result_df['count'] > min_count]
	else:
		extended_result_df=result_df.sort_values(by='count', ascending=True) # more reliable samples last
		for idx1, samp_1 in enumerate(extended_result_df['sample'].index):
			for idx2, samp_2 in enumerate(extended_result_df['sample'].index):
				if idx1>idx2: break
				hd=hamming_dist(samp_1,samp_2)
				if hd>0 and hd <= max_dist:
					a= extended_result_df.iloc[idx1]['count']
					b= extended_result_df.iloc[idx2]['count']
					extended_result_df.iloc[idx2,extended_result_df.columns.get_loc('count')]=a+b
		common_samples_df = extended_result_df[extended_result_df['count'] > min_count]
	print "min count is "+str(min_count)
	print "the max repetition is: "+str(max(common_samples_df['count']))
	print 'DONE!'
	return common_samples_df.sort_values(by='count', ascending=False)  # more reliable samples first
def build_shift_pointers_yael_error_fixer(common_samples_array, stitch_shift_size, max_hd=1):
    '''
    this version includes simple error fixing
    build DAG where snippets are connected if they can be stitched by a small shift
    only the highest-ranking snippet that can be stitched is used, where the snippets array is assumed to be sorted by popularity
    '''
    print 'building DAG + simple error fixing...'
    shift_pointers = {'right_index': {}, 'left_index': {}}
    for idx1, left_sample in enumerate(common_samples_array['sample'].index):
        if idx1 % 1000 == 0:
            print idx1
        for stitch_shift in range(1, stitch_shift_size + 1):
            for idx2, right_sample in enumerate(common_samples_array['sample'].index):
                hd =hamming_dist(left_sample[stitch_shift:], right_sample[:-stitch_shift])
                if hd <=max_hd:
                    if hd==0:
                        new_right=right_sample
                        new_left=left_sample
                    elif levenshtein_edit_dist(right_sample,left_sample)[0]['DIST']<=max_hd:
                        if common_samples_array.iloc[idx2]['count'] > common_samples_array.iloc[idx1]['count']:
                            new_right=right_sample
                            new_left=left_sample[:stitch_shift] + right_sample[:-stitch_shift]
                        else:
                            new_right = left_sample[stitch_shift:] + right_sample[-stitch_shift:]
                            new_left = left_sample
                    if new_right not in shift_pointers['right_index']:
                        shift_pointers['right_index'][new_right] = {'right_sample': new_right,
                                                                       'left_sample': new_left,
                                                                       'shift': stitch_shift}
                    if new_left not in shift_pointers['left_index']:
                        shift_pointers['left_index'][new_left] = {'right_sample': new_right,
                                                                     'left_sample': new_left,
                                                                     'shift': stitch_shift}
                    break_stitch_shift_loop = True
                    break
            if break_stitch_shift_loop:
                break
    print 'DONE!'
    return shift_pointers




