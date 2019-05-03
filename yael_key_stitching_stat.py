import numpy as np
import pandas as pd


cut_beginging=0
key_length= 2048
stitch_shift_size = 2
window_size=30

hex2bin_map = {
   "0":"0000",
   "1":"0001",
   "2":"0010",
   "3":"0011",
   "4":"0100",
   "5":"0101",
   "6":"0110",
   "7":"0111",
   "8":"1000",
   "9":"1001",
   "a":"1010",
   "b":"1011",
   "c":"1100",
   "d":"1101",
   "e":"1110",
   "f":"1111"
}
#hex_key_2048="023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e70f808182838485868788898a8b8c8d8e8909192939495969798999a9b9c9d9e91a0a1a2a3a4a5a6a7a8a9aaabacadaea1b0b1b2b3b4b5b6b7b8b9babbbcbdbeb1c0c1c2c3c4c5c6c7c8c9cacbcccdcec1"
hex_key_500="023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"
key=''.join(hex2bin_map[i] for i in hex_key_500)
#path="C:/YAEL/BGU/data_for_proj/key_stich/good_decoded_samples.txt"
path="/home/ubu/Yael/results/key500_probe300_good_decoded_samples_486K.txt"

def build_samples_from_file(p,window_size,sample_start, sample_end, result_dict):
    count_lines=-1
    print("build samples...")
    with open(p) as f:		 
        for line in f:
			count_lines += 1
			if count_lines>=sample_end: break
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
    conclusion={'F':0, 'D':0, 'I':0,'DIST':0}
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
            else: conclusion['F']+=1
        elif (curr_pointer[0] == pointers[curr_pointer][0]) and (curr_pointer[1] == pointers[curr_pointer][1] + 1):
            conclusion['D'] += 1
        else: conclusion['I'] += 1
        curr_pointer = pointers[curr_pointer]
    if(curr_pointer[0] == -1) and (curr_pointer[1] != -1):
        conclusion['D'] += 1*(curr_pointer[1]+1)
    if (curr_pointer[0] > -1) and (curr_pointer[1] == -1):
        conclusion['I'] += 1 * (curr_pointer[0] + 1)
    conclusion['DIST']=distances[-1]
    return conclusion, s1_match_indices

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
        dist=dist_arr['DIST']
        if len(match_array) >= len(sample['sample']) - radius:
            sample_count[match_array] += 1
    #            print sample['sample']
    #            print near_sample, len(match_array), '\n'
    return min(sample_count)

def hamming_dist(s1, s2):
    '''
    Calculate the Hamming distance between two bit strings
    '''
    if len(s1) == len(s2):
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))
    else:
        return -1  # error return value
	
def prune_samples(result_df, min_count=-1):
    '''
    returns a subset of the snippets dataset which consists only of snippets that show high statistical significance
    '''
    print 'prunning samples...'
    if min_count < 0:
        min_count = result_df['count'].quantile(.5) #the midian
	print "min count is "+str(min_count)
	print "the max repetition is: "+str(max(result_df['count']))
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

def prune_samples_extended(result_df, min_count=-1, ignore_similar=True, min_count_radius=1, levenshtein_radius=2):
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
        min_count = result_df['count'].quantile(.5)
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
                          common_samples_df.iloc[idx]['weight'] + weight_radius))] #take the samples in the weight-diffrance of #weight_radius
            #    common_samples_df['similar_count'] = common_samples_df.apply(lambda row: validate_sample(row, near_weight_sample, levenshtein_radius))
            #    print idx, common_sample
            #    common_sample = common_samples_df.head(2).tail(1)
            #    candidate_noisy_samples_in_radius_df = noisy_samples_df[noisy_samples_df['weight'].isin(
            #                    np.arange(common_sample['weight'] - weight_radius , common_sample['weight'] + weight_radius)) ]
            similar_count = validate_sample(common_samples_df.iloc[idx], near_weight_sample_df, levenshtein_radius) #caunt the relevant by the levinshtain distance
            common_samples_df.at[common_sample, 'similar_count'] = similar_count
        print 'DONE!'
        common_samples_df.sort_values(by='similar_count', ascending=False)['count'].hist(bins=100)
        return common_samples_df.sort_values(by='similar_count', ascending=False)  # more reliable samples first
	
def build_shift_pointers(common_samples_array, stitch_shift_size):
    '''
    build DAG where snippets are connected if they can be stitched by a small shift
    only the highest-ranking snippet that can be stitched is used, where the snippets array is assumed to be sorted by popularity
    '''
    print 'building DAG...'
    shift_pointers = {'right_index': {}, 'left_index': {}}
    for idx1, left_sample in enumerate(common_samples_array):
        if idx1 % 100 == 0:
            print idx1
        for stitch_shift in range(1, stitch_shift_size + 1):
            for idx2, right_sample in enumerate(common_samples_array):
                if hamming_dist(left_sample[stitch_shift:], right_sample[:-stitch_shift]) == 0:
                    if right_sample not in shift_pointers['right_index']:
                        shift_pointers['right_index'][right_sample] = {'right_sample': right_sample,
                                                                       'left_sample': left_sample,
                                                                       'shift': stitch_shift}
                    if left_sample not in shift_pointers['left_index']:
                        shift_pointers['left_index'][left_sample] = {'right_sample': right_sample,
                                                                     'left_sample': left_sample, 'shift': stitch_shift}
                    break_stitch_shift_loop = True
                    break
            if break_stitch_shift_loop:
                break
    print 'DONE!'
    return shift_pointers

def stitch(common_samples_array, shift_pointers):
    '''
    traverse the DAG, starting from the sinks, and generate as long sequences as possible
    the algorithm assumes each snippet (node) has at most one incoming link
    if it should support multiple incoming links, then the function should be adjusted
    '''
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

def build_shift_pointers_yael_tree(common_samples_array, stitch_shift_size):
    '''
    this version includes simple error fixing and tree
    build tree where snippets are connected if they can be stitched by a small shift
    only the highest-ranking snippet that can be stitched is used, where the snippets array is assumed to be sorted by popularity
    !!! edge_left_pointers !!! is nnot necceraly fuul, cycles may be found
    '''
    print 'building Tree no error fixing...'
    tree_pointers=  [None] *len(common_samples_array['sample'])
    edge_left_pointers= range(len(common_samples_array['sample']))
    for idx1, left_sample in enumerate(common_samples_array['sample'].index):
        if idx1 % 100 == 0:
            print idx1
        for stitch_shift in range(1, stitch_shift_size + 1):
            for idx2, right_sample in enumerate(common_samples_array['sample'].index):
                hd =hamming_dist(left_sample[stitch_shift:], right_sample[:-stitch_shift])
                if hd == 0 and idx1!= idx2:
                    tree_pointers[idx1].append({'next': idx2,
                                                'shift':stitch_shift})
                    if idx2 in edge_left_pointers:
                        edge_left_pointers.remove(idx2)
    print 'DONE!'
    return tree_pointers, edge_left_pointers

def build_tree_path_yael(path,s, tree_pointers, common_samples_array,retrieved_key,shift):
    #return an array of all the possible pathes
    if len(tree_pointers[ path[-1]]) == 0:
        si= s[:-shift]+common_samples_array.iloc[path[-1]]['sample']
        retrieved_key.append(si)
        return [path];
    else:
        a=[]
        booli=True
        for node in tree_pointers[ path[-1] ]:
            if node['next'] not in path:
                si = s[:-node['shift']] + common_samples_array.iloc[path[-1]]['sample']
                a.extend(build_tree_path_yael(path+[node['next']],si, tree_pointers,common_samples_array,retrieved_key,node['shift']))
            elif booli:
                a.append(path)
                retrieved_key.append(s)
                booli=False
        return a
	
def stitch_tree_yael(common_samples_array, tree_pointers, edge_left_pointers):
    '''
    traverse the tree pathes, starting from the root, and generate as long sequences as possible
    the algorithm assumes each snippet (node) has at most one incoming link
    if there is no root, the largest cycle will be found
    '''
    if len(edge_left_pointers)==0:
        print 'no root'
        return;
    pathes=[]
    retrieved_key = []
    for root in edge_left_pointers:
        pathes.extend(build_tree_path_yael([root],'',tree_pointers, common_samples_array,retrieved_key,len(common_samples_array[root]['sample'])-1))
    return retrieved_key




##############################MAIN############################



window_size_vec=[20,30] #each has its own graph
samples_num_vec=[100000, 200000, 300000] #bars section
start_samp=0 
result_dict={};

f_key_res=open("/home/ubu/Yael/results/key_res.txt","w")
f_data=open("/home/ubu/Yael/results/data.txt","w")

f_key_res.write("-------key------\n"+ key + '\n')
f_data.write(' '.join(window_size_vec))
f_data.write(' '.join(samples_num_vec))

for window_size in window_size_vec:
	for samples_num in samples_num_vec:
		result_df, result_dict=build_samples_from_file(path,window_size,start_samp,samples_num,result_dict)
		common_samples_df = prune_samples_yael_extended(result_df, min_count=-1)
		shift_pointers = build_shift_pointers(np.array(common_samples_df['sample']), stitch_shift_size)
		retrieved_key = stitch(np.array(common_samples_df['sample']), shift_pointers)
		candidate_key = max(retrieved_key, key=len)
		f_key_res.write('\n\nsamples: '+str(samples_num)+", window: "+str(window_size)+"\n" + candidate_key + '\n')
		f_key_res.write("len: "+str(len(candidate_key)))
		f_key_res.write("find: "+str(key.find(candidate_key)))
		dist=levenshtein_edit_dist(candidate_key,key, False)[0]
		f_data.write(str(dist['DIST'])+" "+str(dist['I'])+" "+str(dist['D'])+" "+str(dist['F'])+" "+str(len(key)-len(candidate_key))+"\n")
		f_candidates=open("/home/ubu/Yael/results/candidates_"+str(window_size)+"_"+str(samples_num)+".txt","w")
		for cand in retrieved_key:
			if len(cand)>300:
				f_candidates.write(cand)
				f_candidates.write("\n")
		f_candidates.close()
		
f_data.close()
f_key_res.close()