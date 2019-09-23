#! /usr/bin/python
import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os
import xlsxwriter



def Error(error):
    error_dict = {

        10: {"flip": 0.10,
            "del": 0.00,
            "insert": 0.00,
            "samples_num_vec": range(100000, 2000001, 100000)
             },

        3: {"flip": 0.03,
            "del": 0.03,
            "insert": 0.03,
            "samples_num_vec": [100000, 500000]
            #"samples_num_vec": [2000, 5000]
            },

        7: {"flip": 0.07,
            "del": 0.07,
            "insert": 0.07,
            #"samples_num_vec": [5000, 10000, 20000]
            "samples_num_vec": [500000, 1000000, 2000000]
            },
        9: {"flip": 0.09,
            "del": 0.09,
            "insert": 0.09,
            "samples_num_vec": [1000000, 2000000, 3000000, 4000000]
            },

    }

    return error_dict[error]



def Opposite(common_samples_df, stitch_shift_size, window_size):
    all2PowerWindowArray_idx, shift_pointers_right_index, shift_pointers_right_index_left, shift_pointers_right_index_shift, shift_pointers_left_index, shift_pointers_left_index_right, shift_pointers_left_index_shift = \
        func.build_shift_pointers_noDict_opposite(common_samples_df=common_samples_df,
                                                  stitch_shift_size=stitch_shift_size,
                                                  window_size=window_size)
    retrieved_key = func.stitch_boris_noDict_opposite(common_samples_df=common_samples_df,
                                                      all2PowerWindowArray_idx=all2PowerWindowArray_idx,
                                                      shift_pointers_right_index=shift_pointers_right_index,
                                                      shift_pointers_right_index_left=shift_pointers_right_index_left,
                                                      shift_pointers_right_index_shift=shift_pointers_right_index_shift,
                                                      shift_pointers_left_index=shift_pointers_left_index,
                                                      shift_pointers_left_index_right=shift_pointers_left_index_right,
                                                      shift_pointers_left_index_shift=shift_pointers_left_index_shift)
    return retrieved_key

def notOpposite(common_samples_df, stitch_shift_size, window_size):
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
    return retrieved_key

methodFunDict ={
    "Opposite" : Opposite,
    "notOpposite": notOpposite
}



def TryMkdir(path):
    try:
        os.mkdir(path)
    except:
        pass
    return path


def PrintToSummryFile(file, key, key_length, candidate_key, samples_num, result_df, quantile, common_samples_df,
                      stitch_shift_size, window_size, conclusion, s1_match_indices):
    ## print results22 conclusion to file
    string = "\noriginal key(len={0}):\n".format(key_length) + key
    file.write(string)
    string = "\ncandidate_key(len={0}):\n".format(len(candidate_key)) + candidate_key
    file.write(string)
    string = "\nkey.find(candidate_key) = " + str(key.find(candidate_key))
    file.write(string)
    #conclusion, s1_match_indices = func.levenshtein_edit_dist(key, candidate_key)
    string = "\nlevenshtein_edit_dist(key, candidate_key) = \n" + str(
        (conclusion, s1_match_indices))
    file.write(string)
    string = "\nsamples_num = " + str(samples_num) + \
             "\nresult_df = " + str(len(result_df)) + \
             "\ncommon_samples_df quantile = " + str(quantile) + \
             "\ncommon_samples_df = " + str(len(common_samples_df)) + \
             "\nstitch_shift_size = " + str(stitch_shift_size) + \
             "\nwindow_size = " + str(window_size) + \
             "\n"
    file.write(string)

    string = "\nDIST = " + str(conclusion['DIST']) + \
             "\nI = " + str(conclusion['I']) + \
             "\nD = " + str(conclusion['D']) + \
             "\nF = " + str(conclusion['F'])
    file.write(string)

    string = "\nDIST-INSERTION = " + str(conclusion['DIST'] - conclusion['I'])
    file.write(string)


    return conclusion






