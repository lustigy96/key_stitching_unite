#! /usr/bin/python

#


import xlsxwriter
import numpy as np

import pandas as pd
import key_stitching_functinos as func
import os
import datetime


def Error(error):
    error_dict = {

        5: {"flip": 0.05,
            "del": 0.05,
            "insert": 0.05,
            "samples_num_vec": [200000, 500000]
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


def opposite(common_samples_df, stitch_shift_size, window_size):
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


if __name__ == "__main__":

    SIMULATION = True

    DIR_RESULT_PATH = "./results"
    DIR_PATH_SIMULATION = "/simulation"

    try:
        os.mkdir(DIR_RESULT_PATH)
    except:
        pass
    try:
        os.mkdir(DIR_RESULT_PATH + DIR_PATH_SIMULATION)
    except:
        pass

    key_length_vec = [2048]
    sample_len_vec = [40]
    # megic_num_vec = [10, 30, 50]
    # samples_num_vec = [600000]
    stitch_vec = [1]
    window_size_vec = [15, 18, 23, 26, 30]  # each has its own graph
    stitch_shift_size = 1
    quantile_vec = [0.6, 0.9]  # each has
    method_vec = ["notOpposite", "Opposite"]  # ["notOpposite","Opposite"]
    error_vec = [5, 7,9]

    tableResult = {}

    i = 0
    for key_length in key_length_vec:
        key = func.init_key(key_length, -1)
        KEY_LENGTH_PATH = "/key_length{0}".format(key_length)

        try:
            os.mkdir(DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH)
        except:
            pass
        tableResult["key_length{0}".format(key_length)] = {}

        for quantile in quantile_vec:
            QUANTILE_NUM_PATH = "/quantile{0}".format(quantile)
            try:
                os.mkdir(DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH)
            except:
                pass
            tableResult["key_length{0}".format(key_length)]["quantile{0}".format(quantile)] = {}
            for sample_len in sample_len_vec:
                SAMPLE_LEN_PATH = "/sample_len{0}".format(sample_len)

                try:
                    os.mkdir(
                        DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH)
                except:
                    pass
                tableResult["key_length{0}".format(key_length)]["quantile{0}".format(quantile)][
                    "sample_len{0}".format(sample_len)] = {}




                for error in error_vec:
                    error_dict = Error(error)
                    ERROR_PATH = "/error{0}".format(error)

                    try:
                        os.mkdir(
                            DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH)
                    except:
                        pass
                    tableResult["key_length{0}".format(key_length)]["quantile{0}".format(quantile)][
                        "sample_len{0}".format(sample_len)]["error{0}".format(error)] = {}


                    workbook = xlsxwriter.Workbook(DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH + '/simulation_table{0}.xlsx'.format(key_length_vec[0]))

                    worksheet = workbook.add_worksheet()

                    row = -2
                    for window_size in window_size_vec:
                        row += 2
                        WINDOWS_SIZE_PATH = "/window_size{0}".format(window_size)
                        try:
                            os.mkdir(
                                DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH + WINDOWS_SIZE_PATH)
                        except:
                            pass
                        tableResult["key_length{0}".format(key_length)]["quantile{0}".format(quantile)]["sample_len{0}".format(sample_len)][
                            "error{0}".format(error)]["window_size{0}".format(window_size)] = {}

                        start_samp = 0
                        result_dict = {}
                        samples_num_vec = error_dict["samples_num_vec"]

                        col=0
                        for samples_num in samples_num_vec:
                            SAMPLE_NUM_PATH = "/samples_num{0}".format(samples_num)
                            try:
                                os.mkdir(
                                    DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH + WINDOWS_SIZE_PATH + SAMPLE_NUM_PATH)
                            except:
                                pass
                            tableResult["key_length{0}".format(key_length)]["quantile{0}".format(quantile)][
                                "sample_len{0}".format(sample_len)]["error{0}".format(error)][
                                "window_size{0}".format(window_size)]["samples_num{0}".format(samples_num)] = {}

                            result_df, result_dict = func.build_samples_continues(key=key,
                                                                                  sample_begin=start_samp,
                                                                                  sample_end=samples_num,
                                                                                  sample_len=sample_len,
                                                                                  window_size=window_size,
                                                                                  flip_probability=error_dict["flip"],
                                                                                  delete_probability=error_dict["del"],
                                                                                  insert_probability=error_dict[
                                                                                      "insert"],
                                                                                  result_dict=result_dict)
                            start_samp = samples_num

                            common_samples_df = func.prune_samples_extended(result_df=result_df, min_count=-1,
                                                                            quantile=quantile)

                            for method in method_vec:
                                METHOD_PATH = "/{0}".format(method)
                                try:
                                    os.mkdir(
                                        DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH + WINDOWS_SIZE_PATH + SAMPLE_NUM_PATH + METHOD_PATH)
                                except:
                                    pass

                                if method == "notOpposite":

                                    retrieved_key = notOpposite(common_samples_df, stitch_shift_size,
                                                                window_size)
                                elif method == "Opposite":
                                    retrieved_key = opposite(common_samples_df, stitch_shift_size, window_size)

                                candidate_key = max(retrieved_key, key=len)

                                summryMy = open(
                                    DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH + WINDOWS_SIZE_PATH + SAMPLE_NUM_PATH + METHOD_PATH + "/summryMy.txt",
                                    "w")

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

                                string = "\nlevenshtein_edit_dist(key, candidate_key) = \n" + str(
                                    (conclusion, s1_match_indices))
                                summryMy.write(string)
                                string = "\nSIMULATION = " + str(SIMULATION)
                                summryMy.write(string)
                                string = "\nsamples_num = " + str(samples_num) + \
                                         "\nsample_len = " + str(sample_len) + \
                                         "\nflip_probability = " + str(error_dict["flip"]) + \
                                         "\ninsert_probability = " + str(error_dict["insert"]) + \
                                         "\ndelete_probability = " + str(error_dict["del"]) + \
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

                                worksheet.write(row, col, int(dist['DIST']))

                                worksheet.write(row+1, col, str(dist))


                                tableResult["key_length{0}".format(key_length)]["quantile{0}".format(quantile)][
                                    "sample_len{0}".format(sample_len)]["error{0}".format(error)][
                                    "window_size{0}".format(window_size)]["samples_num{0}".format(samples_num)][
                                    "{0}".format(method)] = dist

                                tableFile = open(
                                    DIR_RESULT_PATH + DIR_PATH_SIMULATION + "/simulation_table{0}.txt".format(key_length),
                                    "w")
                                tableFile.write(str(tableResult))
                                tableFile.close()
                                col+=1
                    workbook.close()

















