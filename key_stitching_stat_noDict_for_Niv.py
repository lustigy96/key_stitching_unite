#! /usr/bin/python
import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os



def Error(error):
    if error == 1:
        flip_probability = 0.01
        delete_probability = 0.01
        insert_probability = 0.01
    elif error == 3:
        flip_probability = 0.03
        delete_probability = 0.03
        insert_probability = 0.03
    elif error == 5:
        flip_probability = 0.05
        delete_probability = 0.05
        insert_probability = 0.05
    elif error == 7:
        flip_probability = 0.07
        delete_probability = 0.07
        insert_probability = 0.07
    elif error == 10:
        flip_probability = 0.10
        delete_probability = 0.10
        insert_probability = 0.10
    else:
        flip_probability = 0.0
        delete_probability = 0.0
        insert_probability = 0.0

    return flip_probability, delete_probability, insert_probability


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



    key_length_vec = [512,2048]
    sample_len_vec = [31,40,50,100]
    # megic_num_vec = [10, 30, 50]
    samples_num_vec = [100000, 500000, 1000000, 2000000, 3000000, 4000000]
    stitch_vec = [1]
    window_size_vec=[20,30] #each has its own graph
    quantile_vec=[0.5] #each has its own graph

    stitch_shift_size = 1
    # window_size = 30
    quantile = 0.6
    # sample_len = 50
    # key_length = 512
    # GRAPHS = "KEYLENGTH" #"WINDOES" # QUANTILE
    # X = "megicNumVec"

    error_vec = [5 , 7 , 9, 10 ]

    tableResult = {}


    i=0
    for key_length in key_length_vec:
        key = func.init_key(key_length, -1)
        DIR_RESULT_PATH = "./results/simulation/key_length{0}/".format(key_length)
        try:
            os.mkdir(DIR_RESULT_PATH)
        except:
            pass
        tableResult["key_length{0}".format(key_length)] = {}

        for sample_len in sample_len_vec:
            DIR_RESULT_PATH = DIR_RESULT_PATH + "/sample_len{0}/".format(sample_len)
            try:
                os.mkdir(DIR_RESULT_PATH)
            except:
                pass
            tableResult["key_length{0}".format(key_length)]["sample_len{0}".format(sample_len)] = {}

            for window_size in window_size_vec:
                DIR_RESULT_PATH = DIR_RESULT_PATH + "/window_size{0}/".format(window_size)
                try:
                    os.mkdir(DIR_RESULT_PATH)
                except:
                    pass
                tableResult["key_length{0}".format(key_length)]["sample_len{0}".format(sample_len)]["window_size{0}".format(window_size)] = {}



                for error in error_vec:
                    flip_probability, delete_probability, insert_probability = Error(error)
                    DIR_RESULT_PATH = DIR_RESULT_PATH + "/error{0}/".format(error)
                    try:
                        os.mkdir(DIR_RESULT_PATH)
                    except:
                        pass
                    tableResult["key_length{0}".format(key_length)]["sample_len{0}".format(sample_len)][
                        "window_size{0}".format(window_size)]["error{0}".format(error)] = {}


                    start_samp = 0
                    result_dict = {}
                    for samples_num in samples_num_vec:
                        DIR_RESULT_PATH = DIR_RESULT_PATH + "/samples_num{0}/".format(samples_num)
                        try:
                            os.mkdir(DIR_RESULT_PATH)
                        except:
                            pass
                        tableResult["key_length{0}".format(key_length)]["sample_len{0}".format(sample_len)][
                            "window_size{0}".format(window_size)]["error{0}".format(error)]["samples_num{0}".format(samples_num)] = {}



                        tableFile = open("./results/simulation/table.txt", "a+")
                        summryMy = open(DIR_RESULT_PATH + "summryMy.txt", "a+")

                        result_df, result_dict = func.build_samples_continues(key=key,
                                                                              sample_begin=start_samp,
                                                                              sample_end=samples_num,
                                                                              sample_len=sample_len,
                                                                              window_size=window_size,
                                                                              flip_probability=flip_probability,
                                                                              delete_probability=delete_probability,
                                                                              insert_probability=insert_probability,
                                                                              result_dict=result_dict)
                        start_samp = samples_num
                        common_samples_df = func.prune_samples_extended(result_df=result_df,
                                                                        min_count=-1,
                                                                        quantile=quantile)

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
                                 "\nsample_len = " + str(sample_len) + \
                                 "\nflip_probability = " + str(flip_probability) + \
                                 "\ninsert_probability = " + str(insert_probability) + \
                                 "\ndelete_probability = " + str(delete_probability) + \
                                 "\nresult_df = " + str(len(result_df)) + \
                                 "\ncommon_samples_df quantile = " + str(quantile) + \
                                 "\ncommon_samples_df = " + str(len(common_samples_df)) + \
                                 "\nstitch_shift_size = " + str(stitch_shift_size) + \
                                 "\nwindow_size = " + str(window_size) + \
                                 "\n"
                        summryMy.write(string)




                        dist = conclusion  # func.levenshtein_edit_dist(candidate_key,key, False)[0]
                        string = "\nDIST = " + str(dist['DIST']) + \
                                 "\nI = " + str(dist['I']) + \
                                 "\nD = " + str(dist['D']) + \
                                 "\nF = " + str(dist['F']) + \
                                 "\n"
                        summryMy.write(string)
                        summryMy.close()

                        tableResult["key_length{0}".format(key_length)]["sample_len{0}".format(sample_len)][
                            "window_size{0}".format(window_size)]["error{0}".format(error)]["samples_num{0}".format(samples_num)] = dist

                        tableFile.write(str(tableResult))
                        tableFile.close()















