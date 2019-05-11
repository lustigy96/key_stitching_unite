#! /usr/bin/python
import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os







if __name__ == "__main__":

    SIMULATION = True
    ALLOW_CYCLES = False
    try:
        os.mkdir("./results/")
    except:
        pass

    try:
        os.mkdir("./results/simulation/")
    except:
        pass

    print "\n\n~~Start Gabi Algorithem...~~\n\n"





    key_length_vec = [512,1024,2048]
    sample_len_vec = [31,40,50]  # [50, 60, 70, 80, 100]
    megic_num_vec = [10, 30, 50]
    stitch_vec = [1]
    window_size_vec=[30] #each has its own graph
    quantile_vec=[0.5] #each has its own graph

    stitch_shift_size = 1
    window_size = 30
    quantile = 0.6
    sample_len = 50
    key_length = None
    GRAPHS = "KEYLENGTH" #"WINDOES" # QUANTILE
    X = "megicNumVec"


    CASE = 005 ## 1=error15%(5,5,5)  2=error30%(22,5,5) 3=error20%(10,5,5)


    if CASE==005:
        flip_probability = 0.05
        delete_probability = 0.05
        insert_probability = 0.05

    if CASE==022:
        flip_probability = 0.22
        delete_probability = 0.05
        insert_probability = 0.05

    if CASE==010:
        flip_probability = 0.10
        delete_probability = 0.05
        insert_probability = 0.05

    DIR_RESULT_PATH ="./results/simulation/CASE{0}/".format(CASE)
    try:
        os.mkdir(DIR_RESULT_PATH)
    except:
        pass
    RESULT_PATH = DIR_RESULT_PATH + "dataForGraph_Key={0}_Graphs={1}_x={2}_windowSize={3}_quantile={4}.txt".format(key_length,GRAPHS,X, window_size,quantile)


    f_data = open(RESULT_PATH,"a+")
    f_data.write(' '.join(map(str,key_length_vec)))
    f_data.write('\n')
    f_data.write(' '.join(map(str,megic_num_vec)))
    f_data.write('\n')
    f_data.close()

    i=0
    for key_length in key_length_vec:
        start_samp = 0
        result_dict = {}
        key = func.init_key(key_length, 41)
        for megic_num in megic_num_vec:
            f_data = open(RESULT_PATH, "a+")
            summryMy = open(DIR_RESULT_PATH+"summryMy_keyLength={0}_windowSize={1}_quantile={2}.txt".format(key_length, window_size,quantile), "a+")
            samples_num = megic_num * (key_length - sample_len) * (sample_len - window_size)
            result_df, result_dict = func.build_samples_continues(key=key, sample_begin=start_samp, sample_end=samples_num, sample_len=sample_len, window_size=window_size, flip_probability=flip_probability, delete_probability=delete_probability, insert_probability=insert_probability, result_dict=result_dict)
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
            string = "\nmegic_num = " + str(megic_num) + \
                     "\nsample_len = " + str(sample_len) + \
                     "\nsamples_num = megic_num * (key_length - sample_len) * (sample_len - window_size) = " + str(samples_num) + \
                     "\nflip_probability = " + str(flip_probability) + \
                     "\ninsert_probability = " + str(insert_probability) + \
                     "\ndelete_probability = " + str(delete_probability) + \
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





