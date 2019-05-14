#! /usr/bin/python

import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os







if __name__ == "__main__":

    SIMULATION = False
    ALLOW_CYCLES = False
    try:
        os.mkdir("./results/")
    except:
        None

    try:
        os.mkdir("./results/realChannel/")
    except:
        None

    print "\n\n~~Start Gabi Algorithem ...~~\n\n"



    hex_key_512="023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"
    key=''.join(func.hex2bin_map[i] for i in hex_key_512)
    path = "./samples/good_decoded_samples1.txt"
    # path = "./samples/key500_probe300_good_decoded_samples_486K.txt"
    # path2 = "./samples/key500_probe300_good_decoded_samples_486KV2.txt"
    # path3 = "./samples/key500_probe300_good_decoded_samples_170Ksamp.txt"
    p_list = [path]

    window_size_vec = [20, 25, 21, 26, 22, 27]  # each has its own graph
    quantile_vec=[0.6, 0.9, 0.8] #each has its own graph
    samples_num_vec=[100000, 300000 , 600000, 1000000, 2000000, 3500000] #bars section
    stitch_shift_size = 1
    key_length = n = len(key)
    window_size = None
    quantile = 0.6

    GRAPHS = "WINDOES" # QUANTILE
    X= "samplesNumVec"
    f_data_path = "./results/realChannel/dataForGraph_Key={0}_Graphs={1}_x={2}_windowSize={3}_quantile={4}.txt".format(key_length,GRAPHS,X, window_size,quantile)
    f_data = open(f_data_path,"a+")
    f_data.write(' '.join(map(str,window_size_vec))) #f_data.write(' '.join(map(str,quantile_vec)))
    f_data.write('\n')
    f_data.write(' '.join(map(str,samples_num_vec)))
    f_data.write('\n')
    f_data.close()
    i = 1
    for window_size in window_size_vec:
        start_samp = 0
        result_dict = {}
        for samples_num in samples_num_vec:
            f_data = open(f_data_path, "a+")
            summryMy = open("./results/realChannel/summryMy_keyLength={0}_windowSize={1}_quantile={2}.txt".format(key_length,  window_size,quantile), "a+")

            result_df, result_dict = func.build_samples_from_file(p_list=p_list, window_size=window_size, sample_start=start_samp, sample_end=samples_num, result_dict=result_dict)
            start_samp = samples_num
            common_samples_df = func.prune_samples_extended(result_df, min_count=-1, quantile=quantile)

            all2PowerWindowArray_idx, shift_pointers_right_index, shift_pointers_right_index_left, shift_pointers_right_index_shift, shift_pointers_left_index, shift_pointers_left_index_right, shift_pointers_left_index_shift = \
                func.build_shift_pointers_noDict(common_samples_df=common_samples_df,
                                                 stitch_shift_size=stitch_shift_size,
                                                 window_size=window_size)

            retrieved_key = func.stitch_boris_noDict(common_samples_df=common_samples_df,
                                                     all2PowerWindowArray_idx=all2PowerWindowArray_idx,
                                                     shift_pointers_right_index=shift_pointers_right_index,
                                                     shift_pointers_right_index_left=shift_pointers_right_index_left,
                                                     shift_pointers_right_index_shift=shift_pointers_right_index_shift,
                                                     shift_pointers_left_index=shift_pointers_left_index,
                                                     shift_pointers_left_index_right=shift_pointers_left_index_right,
                                                     shift_pointers_left_index_shift=shift_pointers_left_index_shift)

            candidate_key = max(retrieved_key, key=len)

            ## print results conclusion to file
            string = "\nRESULT_NUMBER = {0}".format(i)
            summryMy.write(string)
            string = "\noriginal key(len={0}):\n".format(key_length) + key
            summryMy.write(string)
            string = "\ncandidate_key(len={0}):\n".format(len(candidate_key)) + candidate_key
            summryMy.write(string)
            string = "\nkey.find(candidate_key) = " + str(key.find(candidate_key))
            summryMy.write(string)
            conclusion, s1_match_indices = func.levenshtein_edit_dist(key, candidate_key)
            string = "\nlevenshtein_edit_dist(key, candidate_key) = \n" + str((conclusion, s1_match_indices))
            summryMy.write(string)
            string = "\nSIMULATION = " + str(SIMULATION)
            summryMy.write(string)
            string = "\nsamples_num = " + str(samples_num) + \
                     "\nresult_df = " + str(len(result_df)) + \
                     "\ncommon_samples_df quantile = " + str(quantile) + \
                     "\ncommon_samples_df = " + str(len(common_samples_df)) + \
                     "\nstitch_shift_size = " + str(stitch_shift_size) + \
                     "\nwindow_size = " + str(window_size) + \
                     "\nallowCycle = " + str(ALLOW_CYCLES) + \
                     "\n"
            summryMy.write(string)
            summryMy.close()

            dist = conclusion #func.levenshtein_edit_dist(candidate_key,key, False)[0]
            f_data.write(str(dist['DIST'])+" "+str(dist['I'])+" "+str(dist['D'])+" "+str(dist['F'])+" "+str(len(candidate_key))+"\n")
            f_data.close()
            i+=1





