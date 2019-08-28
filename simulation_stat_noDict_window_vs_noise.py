#! /usr/bin/python

#


import xlsxwriter
import numpy as np

import pandas as pd
import key_stitching_functinos as func
import os
import datetime





#key without repetition (length 11) = no 11 bits repeat themselve:
key11rep0 = '00000000000100000000011000000001010000000011100000001001000000010110000000110100000001111000000100010000001001100000010101000000101110000001100100000011011000000111010000001111100000100001000001000110000010010100000100111000001010010000010101100000101101000001011110000011000100000110011000001101010000011011100000111001000001110110000011110100000111111000010000110000100010100001000111000010010010000100101100001001101000010011110000101000100001010011000010101010000101011100001011001000010110110000101110100001011111000011000110000110010100001100111000011010010000110101100001101101000011011110000111000100001110011000011101010000111011100001111001000011110110000111110100001111111000100010010001000101100010001101000100011110001001001100010010101000100101110001001100100010011011000100111010001001111100010100011000101001010001010011100010101001000101010110001010110100010101111000101100110001011010100010110111000101110010001011101100010111101000101111110001100011100011001001000110010110001100110100011001111000110100110001101010100011010111000110110010001101101100011011101000110111110001110010100011100111000111010010001110101100011101101000111011110001111001100011110101000111101110001111100100011111011000111111010001111111100100100101001001001110010010101100100101101001001011110010011001100100110101001001101110010011101100100111101001001111110010100101100101001101001010011110010101001100101010101001010101110010101101100101011101001010111110010110011100101101011001011011010010110111100101110011001011101010010111011100101111011001011111010010111111100110011011001100111010011001111100110100111001101010110011010110100110101111001101101010011011011100110111011001101111010011011111100111001111001110101010011101011100111011011001110111010011101111100111101011001111011010011110111100111110101001111101110011111101100111111101001111111110101010101101010101111010101101110101011101101010111111010110101110101101101101011011111010111011110101111011101011111011010111111110110110111101101110111011011111110111011111101111011111011111111111'
#key with 4 repetition size 25:
key25rep4 = '10000011111010000110101010010011000100011111001100111011100010001101100110100011101011010111110110011110101011110101100100011110011100011111101101110101101010011010110101001101011101001111111101001111101010010001111110101110000000100001100001100100011101001100010110111111101101011101110110011100010011101111000111000111001110010110011110110101001011111110100010100110110000100110111001111000000010000011011101110011010010011001110110010110001000101001010011010011110100010011101011010100110101110100010001000110100111111101001110001110001001111110101010010110110001111111010000000010110000101000000001111111010000111100100010010001000111110011001111101001011011111100010101000011110011011011100101011010101111100111010110111101010111111111011011000010100111011110011101101010001010010011110101101010011010111010000100111000100101110111000111000111111010100111011001000110001111010001111111111101111111011110010001101011000010111110111010101010001100010001001000111010111110110100110100010110011100011011110100000000101000111111001001011101001111101111001100001011010100110000111001111111111000011010100110000111010010001001110011011110111010001011010110000011110101001100001101010000101100000000111101111100010100001101100001110100101000101010101010011010101100000011000100011100101110001000010010101111001010010000010101100011001000000011001000111010111101010101001100110101111101010110000101010100001011101100011110110111101001000110101001100010111110010111101110100111100001001100111110100000111001010011110101000111100000111001110100010001100000001000100010011000010110010101010110100100001000111100101001110101011100011010100011100101001000100100100011010010111111010001010001101011100110100100000111000111111001001000010011001100000111000000100101110011001001110100101101011110100100001101110000101111011100010101100111000001011100100000001011101011111010110000010100111101011010100110101110100111111000101101001010000010110010110011111100011110011010010110111101110001010111101011010010001101010110110011000111000111101000110100101011110111'

#key with 2 repetition size 25:
key25rep2 = '01010000010001010100100011010010010111111111000011010101101101000111001011101101011001100101010101011110100001110101100011101101001111101101110111000110100011011110101110010100010101100011101100111000001000111111101111101100111011011110100001011000100001101000111010101000010001100111011100110110100101100010111000100111111001010000010011001011111110110001111011011111100100000011100111011100110110010111111100110110010000011111101111011111000101111111001100011001001111011010111011010010110010000111110111100001010000001100011110100101001001101100000111001011010110010001010011110010000111001111100010011011101110100000011100001101000001010010101101000110101000101000001111100000111001010100011111010111001011110110110000110110000100110101011101011000111011010010110101010111000110001011000101000000001010111110101110110111110110101110001000001000101010111111100000010100011000101011001110001000001101111110000010011001001111011011001010011000101111100100100110010111001111010011001110101010100000000011001100000100011111110110100101111111111001110100110010100100001111000011011100000000110001000100110100100111000111101011111011110010110011100011111100100111001101000110101101000100110010011101110011100011000000001001011001010010000000101110111011011100111011001111010011001110101010100000011101111111000100111111000010010101100011001100010010000100001110010000001011111100000101111110011010000111101000010001011101000101110000100001010000101111011111001101010001101110001011111110001111000101100001111000101110110010001000111000101101011111111001100111111100110010000100010110101111001011101111111100010100000010010011000111111010001100110111000001110000001100000110101011111100110100001110011110011111010011001110101010100000000101011010000011100001000010011101001110111000110011101100000010010000011001100001000100101000010110010011111101000000011110100001010101111100111101000110101011110001000111011001100010001100001101011110110101010100100101010000010111001001001001010000010100110111110000100000110011110110100100111001101101101101111101'

#key with 4 repetition size 15:
key15rep4 = '01101110110010111111110100100100101011011001101011011101100001011010010101010100111010000010010001100000111001000010000101000110100010100101100100001111000001111110100110100101010011010011101000001000010101011011011000111011001110100100110000000001110110000010110001000000110111011111001100000011101101000111101011011011000100101011000010110100110111010100111100011100000000101100111101111001011100100100111001001101111010000011001110101100001101101111100010011010101011010010011110101110010010111010001110010010000110100011100010110100110000010001110110000101010000010100110000001001000001110010001001010001110101010111100110011011001010001000101001011110111000110010010011011000110101000011010100110101001000111011101111110110010110011110111100100101110111010001100101011000000010010000110001111101101110001100010101010100100000101000010110110110101000010111111000111010101000110100001011011111000011010101111010001111010010000001011101000001100010110111001011110001110110110011011011100000011111010001110111111111100100101101101101110010111111001101100010011100111000011000011011110110101011011111101001001110011010100000010110000011011001110110011111010010100000111001000010001101111011000001101101110011110100001101010010110100111011110100010011111110110000010100110011100100100001000001111100110111101000010001111101100010100101101000011000101011110010010100100010100001111101001001101000111110100010110110111010100101011010010010111011011101000010111110110000001011100000111001000100000010011000101101000101011111111011011011101110111010110101001110011110100010001100001010100010000010100010110110111000100011001110011000011101000110000110011010001101001011100000110100000101000000000100010011000110010100101010010111001011111100011010100100100011010101011000101101101011010010111010111001111100011111011100100000000001000000000110001000000000011101001100100010101010011101100111001011011001001111001010101111001010001010101100111110110100111101001110100101000011011111000011100011001110011000100010101110010011000001110010001110100100101110'

#key with 2 repetition size 15:
key15rep2 = '01110000011110011011000010110011101010010011100100101001101011110010101000101110111011000001110001001010010100111110111110111010010100110110100001110101101110000011000100101001110101000010011100011100000110011001100110010111000011111101100100110010001101011001011010000100010100100110110011011100010110111110001111000101011011100001100001000110010101100001001110001100111011000100100011100010000101000100000001110110101010000011110000111010011111110111100011110010000010110010110101100100010110110110100010111001111010101110101101101000011001010001001111000001100010100100010010111110000001110000110001001011111101110111111011100011111011011011001111100011110011111101110111110100000100101010111000101111011111010011101011110110000010100101011111110111111101111001110100101011010000010110010111101110100101101111111001101000000101100011110010111010111010000011101000010111010001001010000011000100011001011001101010100100101111011000010110000100000001011100011001001000000110101101101000000000100110011100101010110001101111101110001010111101001000101111110001111001000100110101101011001011000111001011101001100100100100101110110100000000011111111001000001011010111000100001010011001010001110011011010100110111010100010001100000110010110011011011011010101001101110111110001111101011100110111000110101011110001011101001010111000010000100010001100000101010011001111001001111100011101010010001000001001011101011001001000110111111011010010101001001101110000011101100110101000010000001001001111000001111110100101101110100001011000001110000010111111001001010010001001001101000011110101010111011010001100010010000100110111111001010101011000110111110100011011101101100000101001011001101100111110010011101001001100011101010011100101010101010100010111010010101110110001000001110011010100010111111101000010100111111000011001011011101000101110000110001011100010101010010110101011101001010111111011111111010111011000110000110010110001001001100101000010010101011110111001100001100101101100100110000010101010110100110001101000001101110000011000110101001000011001001'


def Error(error):
    error_dict = {

        5: {"flip": 0.05,
            "del": 0.05,
            "insert": 0.05,
            "samples_num_vec": range(100000, 1500000, 100000)
            },

        7: {"flip": 0.07,
            "del": 0.07,
            "insert": 0.07,
            "samples_num_vec": range(100000, 1500000, 100000)
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



def TryMkdir(path):
    try:
        os.mkdir(path)
    except:
        pass
    return path



def PrintToSummryFile(summryMy, key, key_length, candidate_key, samples_num, result_df, quantile, common_samples_df, stitch_shift_size, window_size):
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
    return dist


if __name__ == "__main__":

    SIMULATION = True

    DIR_RESULT_PATH = "./results"
    DIR_PATH_SIMULATION = "/simulation"

    TryMkdir(DIR_RESULT_PATH)
    TryMkdir(DIR_RESULT_PATH + DIR_PATH_SIMULATION)

    key_length_vec = [2048]
    sample_len_vec = [40]
    # megic_num_vec = [10, 30, 50]
    # samples_num_vec = [600000]
    stitch_vec = [1]
    window_size_vec = [12, 15, 18]  # each has its own graph
    stitch_shift_size = 1
    quantile_vec = [0.9]  # each has
    method_vec = ["notOpposite", "Opposite"]  # ["notOpposite","Opposite"]
    error_vec = [5, 7]

    tableResult = {}

    i = 0
    print "key2048 with no 11 bit repets"
    key = key11rep0
    for key_length in key_length_vec:
        KEY_LENGTH_PATH = "/key_length{0}_key11rep0".format(key_length)

        TryMkdir(DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH)
        tableResult["key_length{0}".format(key_length)] = {}

        for quantile in quantile_vec:
            QUANTILE_NUM_PATH = "/quantile{0}".format(quantile)
            TryMkdir(DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH)
            tableResult["key_length{0}".format(key_length)]["quantile{0}".format(quantile)] = {}
            for sample_len in sample_len_vec:
                SAMPLE_LEN_PATH = "/sample_len{0}".format(sample_len)

                TryMkdir(DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH)
                tableResult["key_length{0}".format(key_length)]["quantile{0}".format(quantile)][
                    "sample_len{0}".format(sample_len)] = {}




                for error in error_vec:
                    error_dict = Error(error)
                    ERROR_PATH = "/error{0}".format(error)

                    TryMkdir(DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH)
                    tableResult["key_length{0}".format(key_length)]["quantile{0}".format(quantile)][
                        "sample_len{0}".format(sample_len)]["error{0}".format(error)] = {}


                    workbook = xlsxwriter.Workbook(DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH + '/simulation_table{0}.xlsx'.format(key_length_vec[0]))
                    worksheet = workbook.add_worksheet()

                    row = -3
                    for window_size in window_size_vec:
                        row += 3
                        WINDOWS_SIZE_PATH = "/window_size{0}".format(window_size)
                        TryMkdir(DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH + WINDOWS_SIZE_PATH)
                        tableResult["key_length{0}".format(key_length)]["quantile{0}".format(quantile)]["sample_len{0}".format(sample_len)][
                            "error{0}".format(error)]["window_size{0}".format(window_size)] = {}

                        start_samp = 0
                        result_dict = {}
                        samples_num_vec = error_dict["samples_num_vec"]

                        col=0
                        for samples_num in samples_num_vec:
                            SAMPLE_NUM_PATH = "/samples_num{0}".format(samples_num)
                            TryMkdir(DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH + WINDOWS_SIZE_PATH + SAMPLE_NUM_PATH)
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
                                path = TryMkdir(DIR_RESULT_PATH + DIR_PATH_SIMULATION + KEY_LENGTH_PATH + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH + WINDOWS_SIZE_PATH + SAMPLE_NUM_PATH + METHOD_PATH)

                                if method == "notOpposite":
                                    retrieved_key = notOpposite(common_samples_df, stitch_shift_size,
                                                                window_size)
                                elif method == "Opposite":
                                    retrieved_key = opposite(common_samples_df, stitch_shift_size, window_size)

                                candidate_key = max(retrieved_key, key=len)

                                summryMy = open(path + "/summryMy.txt","w")

                                ## print results conclusion to file
                                dist = PrintToSummryFile(summryMy, key, key_length, candidate_key, samples_num,
                                                         result_df, quantile, common_samples_df, stitch_shift_size,
                                                         window_size)

                                tmpOk = False
                                if dist['DIST'] < 25:
                                    if dist['DIST'] - dist['I'] <= 10 and candidate_key[:5] == "00000":
                                        tmpOk = True
                                    elif dist['DIST'] <= 10:
                                        tmpOk = True

                                string = "\nDIST-INSERTION = " + str(dist['DIST'] - dist['I'])
                                summryMy.write(string)

                                dist['DIST - INSERTIONS'] = dist['DIST'] - dist['I']
                                worksheet.write(row, col, int(dist['DIST']))
                                worksheet.write(row+1, col, str(dist))
                                worksheet.write(row+2, col, str("GOOD") if tmpOk else str("BAD"))


                                tableResult["key_length{0}".format(key_length)]["quantile{0}".format(quantile)][
                                    "sample_len{0}".format(sample_len)]["error{0}".format(error)][
                                    "window_size{0}".format(window_size)]["samples_num{0}".format(samples_num)][
                                    "{0}".format(method)] = dist

                                tableFile = open(
                                    DIR_RESULT_PATH + DIR_PATH_SIMULATION + "/simulation_table{0}.txt".format(key_length),
                                    "w")
                                tableFile.write(str(tableResult))

                                summryMy.close()
                                tableFile.close()
                                col+=1
                    workbook.close()

















