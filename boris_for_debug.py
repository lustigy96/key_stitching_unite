#! /usr/bin/python
import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os
import datetime






if __name__ == "__main__":

    SIMULATION = True
    ALLOW_CYCLES = False
    CASE = 1 ## 1=error15%(5,5,5)  2=error30%(22,5,5) 3=error20%(10,5,5)
    try:
        os.mkdir("./results/")
    except:
        pass

    print "\n\n~~Start Gabi Algorithem...~~\n\n"

    stitch_shift_size = 1
    window_size = 20
    quantile = 0.6
    sample_len = 31
    key_length = 512
    megic_num = 1

    if CASE==1:
        flip_probability = 0.05
        delete_probability = 0.05
        insert_probability = 0.05

    if CASE==2:
        flip_probability = 0.22
        delete_probability = 0.05
        insert_probability = 0.05

    if CASE==3:
        flip_probability = 0.1
        delete_probability = 0.05
        insert_probability = 0.05


    i=0
    start_samp = 0
    result_dict = {}
    key = func.init_key(key_length, 41)

    try:
        os.mkdir("./results/debug")
    except:
        pass
    summryMy = open("./results/debug/summryMy_Debug_keyLength={0}_allowCycle={1}_shiftPointersMethod=GabiOptimized_windowSize={2}_simulation={3}_error={4}%.txt".format(key_length, ALLOW_CYCLES, window_size, SIMULATION, int(flip_probability*100)), "a+")
    samples_num = megic_num * (key_length - sample_len) * (sample_len - window_size)
    samples_num = 2000
    result_df, result_dict = func.build_samples_continues(key=key, sample_begin=start_samp, sample_end=samples_num, sample_len=sample_len, window_size=window_size, flip_probability=flip_probability, delete_probability=delete_probability, insert_probability=insert_probability, result_dict=result_dict)
    start_samp = samples_num
    common_samples_df = func.prune_samples_extended(result_df, min_count=-1, quantile=quantile)

    shift_pointers_Gabi = func.build_shift_pointers_gabi_pure(common_samples_df, stitch_shift_size)



    start = datetime.datetime.now()
    shift_pointers_Boris, all2PowerWindowArray, all2PowerWindowArray_idx, orderArrayMaxToMin = \
        func.build_shift_pointers_position_better(common_samples_df=common_samples_df,
                                                   stitch_shift_size=stitch_shift_size,
                                                   window_size=window_size)
    retrieved_key = func.stitch_boris(common_samples_df=common_samples_df,
                                      shift_pointers=shift_pointers_Boris,
                                      all2PowerWindowArray_idx=all2PowerWindowArray_idx,
                                      allowCycle=ALLOW_CYCLES,
                                      key_length=key_length)
    took_time1 = datetime.datetime.now() - start
    candidate_key = max(retrieved_key, key=len)

    start = datetime.datetime.now()
    all2PowerWindowArray_idx, shift_pointers_right_index, shift_pointers_right_index_left, shift_pointers_right_index_shift, shift_pointers_left_index, shift_pointers_left_index_right, shift_pointers_left_index_shift = \
        func.build_shift_pointers_noDict(common_samples_df=common_samples_df,
                                                   stitch_shift_size=stitch_shift_size,
                                                   window_size=window_size)
    retrieved_key2 = func.stitch_boris_noDict(common_samples_df=common_samples_df,
                                        all2PowerWindowArray_idx=all2PowerWindowArray_idx,
                                        shift_pointers_right_index=shift_pointers_right_index,
                                        shift_pointers_right_index_left=shift_pointers_right_index_left,
                                        shift_pointers_right_index_shift=shift_pointers_right_index_shift,
                                        shift_pointers_left_index=shift_pointers_left_index,
                                        shift_pointers_left_index_right=shift_pointers_left_index_right,
                                        shift_pointers_left_index_shift=shift_pointers_left_index_shift)
    took_time2 = datetime.datetime.now() - start
    candidate_key2 = max(retrieved_key2, key=len)

    func.compareGabiAndMe(shift_pointers_Boris,shift_pointers_Gabi)

    func.compareDictAndNoDict(shift_pointers=shift_pointers_Boris,
                              shift_pointers_right_index=shift_pointers_right_index,
                              shift_pointers_left_index=shift_pointers_left_index,
                              retrieved_key=retrieved_key,
                              retrieved_key2=retrieved_key2)

    print "time for stitch_boris:"
    print took_time1
    print "time for stitch_boris2"
    print took_time2


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






